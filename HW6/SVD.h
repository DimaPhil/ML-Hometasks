#ifndef SVD_H
#define SVD_H

#include <cstdio>
#include <iostream>
#include <algorithm>
#include <cassert>
#include <vector>
#include <cstring>

#include "SVDParameters.h"
#include "Utils.h"
#include "Film.h"
#include "Train.h"

struct SVD {
  const char* filename;
  const char* validation;
  bool isValidationEnabled;
  const int MAX_LENGTH = 50;

  const double MU = 3.6033;
  const int MAX_ITERATIONS = 20;
  const int EPS = 1e-4;

  const double MIN_LAMBDA = 0.002;
  const double MAX_LAMBDA = 0.008;
  const double STEP_LAMBDA = 0.001;

  const int MIN_F = 10;
  const int MAX_F = 15;
  const int STEP_F = 5;

  const double MIN_GAMMA = 0.005;
  std::vector<Train> trains;

  bool getLine(char *s) {
    char c;
    int n = 0;
    bool first = true;
    while (true) {
      c = getchar();
      if (c == EOF) {
        if (first) {
          return false;
        } else {
          break;
        }
      }
      if (c == '\n') {
        break;
      }
      s[n++] = c;
      first = false;
    }
    s[n] = '\0';
    return true;
  }

  SVD(const char* filename) : filename(filename), isValidationEnabled(false) {
      freopen(filename, "r", stdin);
      char s[MAX_LENGTH];
      getLine(s);
      freopen(filename, "r", stdin);
      getLine(s);
      int counter = 0;
      int sumRate = 0;
      while (getLine(s)) {
        std::vector<std::string> parts = split(s, ',');
        if (++counter % 1000000 == 0) {
          std::cerr << counter << " lines read\n";
        }

        long long userId = std::stoll(strip(parts[0]));
        long long itemId = std::stoll(strip(parts[1]));
        int rate = std::stoi(strip(parts[2]));
        sumRate += rate;

        trains.emplace_back(userId, itemId, rate);
      }
      std::cerr << "Average rating: " << (double)sumRate / static_cast<int>(trains.size()) << '\n';
  }

  void setValidation(const char* validation) {
    this->validation = validation;
    this->isValidationEnabled = false;
  }

  std::vector<double> generateRandomArray(int n) {
    std::vector<double> as(n);
    double min = 0.0;
    double max = 1.0 / n;

    for (int i = 0; i < n; i++) {
      as[i] = min + (max - min) * ((double) rand() / RAND_MAX);
    }
    return std::move(as);
  }

  double scal(const std::vector<double> &qi, const std::vector<double> &pu) {
    double answer = 0;
    assert(qi.size() == pu.size());
    for (size_t i = 0; i < qi.size(); i++) {
      answer += qi[i] * pu[i];
    }
    return answer;
  }

  double normalizedSquare(const std::vector<double> as) {
    double answer = 0;
    for (size_t i = 0; i < as.size(); i++) {
      answer += as[i] * as[i];
    }
    return answer;
  }

  int getRate(const Film &film, SVDParameters &parameters) {
    double result = parameters.mu + parameters.bu[film.userId] + 
                    parameters.bi[film.itemId] + scal(parameters.pu[film.userId], parameters.qi[film.itemId]);
    int rate = (int)result;
    rate = std::min(5, std::max(1, rate));
    return rate;
  }

  double countError(SVDParameters &parameters) {
    double error = 0.0;
    for (auto userId : parameters.ratings) {
      for (auto itemId : parameters.ratings[userId.first]) {
        Film film = Film(userId.first, itemId.first, parameters.ratings[userId.first][itemId.first]);
        double predictedRate = getRate(film, parameters);
        double difference = film.rate - predictedRate;
        error += difference * difference;
        error += parameters.lambda * (normalizedSquare(parameters.pu[userId.first]) + normalizedSquare(parameters.qi[itemId.first]) + 
                                      parameters.bu[userId.first] * parameters.bu[userId.first] +
                                      parameters.bi[itemId.first] * parameters.bi[itemId.first]);
      }
    }
    return error;
  }

  SVDParameters solve(const SVDParameters &parameters) {
    fprintf(stderr, "Using parameters: lambda=%.6f, f=%d, gamma=%.6f, mu = %.6f\n", parameters.lambda, parameters.f,
                                                                                    parameters.gamma, parameters.mu);
    double error = 0.0;
    double previousError = 1.0;

    SVDParameters newParameters = SVDParameters(parameters.lambda, parameters.f, parameters.gamma, parameters.mu);

    int i = 0;
    while (i < MAX_ITERATIONS && std::abs(error - previousError) > EPS) {
      int size = 0;
      for (const Train &train : trains) {
        int userId = train.userId;
        int itemId = train.itemId;
        int rate = train.rate;

        if (i == 0) {
          newParameters.pu[userId] = generateRandomArray(newParameters.f);
          newParameters.qi[itemId] = generateRandomArray(newParameters.f);
          newParameters.bu[userId] = 0.0;
          newParameters.bi[itemId] = 0.0;
          newParameters.ratings[userId][itemId] = rate;
        }

        size++;

        double cbu = newParameters.bu[userId];
        double cbi = newParameters.bi[itemId];
        std::vector<double> cqi = newParameters.qi[itemId];
        std::vector<double> cpu = newParameters.pu[userId];

        double predictedRate = newParameters.mu + cbi + cbu + scal(cqi, cpu);
        double e = rate - predictedRate;

        newParameters.bu[userId] = cbu + newParameters.gamma * (e - newParameters.lambda * cbu);
        newParameters.bi[itemId] = cbi + newParameters.gamma * (e - newParameters.lambda * cbi);

        for (int k = 0; k < newParameters.f; k++) {
          double qi = cqi[k];
          double pu = cpu[k];
          cqi[k] = qi + newParameters.gamma * (e * pu - newParameters.lambda * qi);
          cpu[k] = pu + newParameters.gamma * (e * qi - newParameters.lambda * pu);
        }
      }
      newParameters.gamma *= 0.9;
      previousError = error;
      error = countError(newParameters);
      i++;
      fclose(stdin);

      fprintf(stderr, "Finished %d/%d iterations, error = %.10f\n", i, MAX_ITERATIONS, error);
    }
    newParameters.error = error;
    return newParameters;
  }

  double calcRMSE(SVDParameters &parameters) {
    SVDParameters newParameters = solve(parameters);
    /*char s[MAX_LENGTH];
    if (isValidationEnabled) {
      double rmse = 0.0;
      int size = 0;
      freopen(validation, "r", stdin);
      scanf("%s", s);
      while (scanf("%s", s) >= 1) {
        std::vector<std::string> parts = split(s, ',');
        long long userId = std::stoll(strip(parts[0]));
        long long itemId = std::stoll(strip(parts[1]));
        int rate = std::stoi(strip(parts[2]));
        size++;
        Film film = Film(userId, itemId, rate);
        double e = getRate(film, parameters) - film.rate;
        rmse += e * e;
      }
      fclose(stdin);
      return sqrt(rmse / size);
    }*/
    return newParameters.error;
  }

  SVDParameters learn() {
    SVDParameters parameters = SVDParameters();
    parameters.error = 1e18;
    parameters.mu = MU;

    for (double lambda = MIN_LAMBDA; lambda <= MAX_LAMBDA; lambda += STEP_LAMBDA) {
      for (int f = MIN_F; f <= MAX_F; f += STEP_F) {
        SVDParameters tmpParameters = SVDParameters(lambda, f, MIN_GAMMA, MU);
        double error = calcRMSE(tmpParameters);
        if (parameters.error > error) {
          parameters = SVDParameters(lambda, f, MIN_GAMMA, MU);
          parameters.error = error;
        }
      }
    }

    return solve(parameters);
  }
};

#endif