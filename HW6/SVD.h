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
  const int MAX_LENGTH = 50;

  const double MU = 3.6033; //average rating
  const int MAX_ITERATIONS = 10;
  const int EPS = 1e-6;

  const double MIN_LAMBDA = 0.003;
  const double MAX_LAMBDA = 0.007;
  const double DELTA_LAMBDA = 0.001;
  const double OPTIMAL_LAMBDA = 0.005;

  const int MIN_NUMBER_OF_BEST = 5;
  const int MAX_NUMBER_OF_BEST = 5;
  const int DELTA_NUMBER_OF_BEST = 5;

  const double OPTIMAL_GAMMA = 0.005;
  const double DELTA_GAMMA = 0.9;
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

  SVD(const char* filename) : filename(filename) {
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
        int rating = std::stoi(strip(parts[2]));
        sumRate += rating;

        trains.emplace_back(userId, itemId, rating);
      }
      std::cerr << "Average rating: " << (double)sumRate / static_cast<int>(trains.size()) << '\n';
  }

  std::vector<double> generateRandomValues(int n) {
    std::vector<double> as(n);
    double min = 0.0;
    double max = 1.0 / n;

    for (int i = 0; i < n; i++) {
      as[i] = min + (max - min) * ((double) rand() / RAND_MAX);
    }
    return std::move(as);
  }

  double scal(const std::vector<double> &pu, const std::vector<double> &qi) {
    double answer = 0;
    assert(pu.size() == qi.size());
    for (size_t i = 0; i < pu.size(); i++) {
      answer += pu[i] * qi[i];
    }
    return answer;
  }

  double squareOfNorm(const std::vector<double> &as) {
    return scal(as, as);
  }

  int predictRating(const Film &film, SVDParameters &parameters) {
    double result = parameters.mu + 
                    parameters.bu[film.userId] + 
                    parameters.bi[film.itemId] +
                    scal(parameters.pu[film.userId], parameters.qi[film.itemId]);
    int rating = static_cast<int>(result);
    rating = std::min(5, std::max(1, rating));
    return rating;
  }

  template<class T>
  T sqr(T x) {
    return x * x;
  }

  double calculateParametersError(SVDParameters &parameters) {
    double error = 0.0;
    for (auto userId : parameters.ratings) {
      for (auto itemId : parameters.ratings[userId.first]) {
        Film film = Film(userId.first, itemId.first, parameters.ratings[userId.first][itemId.first]);
        error += sqr(film.rating - predictRating(film, parameters)) +
                 parameters.lambda * (squareOfNorm(parameters.pu[userId.first]) + 
                                      squareOfNorm(parameters.qi[itemId.first]) + 
                                      sqr(parameters.bu[userId.first]) +
                                      sqr(parameters.bi[itemId.first]));
      }
    }
    return error;
  }

  SVDParameters solve(const SVDParameters &parameters) {
    fprintf(stderr, "Using parameters: lambda=%.6f, best_films_count=%d, gamma=%.6f, mu = %.6f\n", parameters.lambda, parameters.best_films_count,
                                                                                    parameters.gamma, parameters.mu);
    double error = 0.0;
    double lastError = 1.0;

    SVDParameters answer = SVDParameters(parameters.lambda, parameters.best_films_count, parameters.gamma, parameters.mu);
    for (int i = 0; i < MAX_ITERATIONS && std::abs(error - lastError) > EPS; i++) {
      for (const Train &train : trains) {
        int userId = train.userId;
        int itemId = train.itemId;
        int rating = train.rating;

        if (i == 0) {
          answer.pu[userId] = generateRandomValues(answer.best_films_count);
          answer.qi[itemId] = generateRandomValues(answer.best_films_count);
          answer.ratings[userId][itemId] = rating;
        }

        double nbu = answer.bu[userId];
        double nbi = answer.bi[itemId];
        std::vector<double> &nqi = answer.qi[itemId];
        std::vector<double> &npu = answer.pu[userId];

        double predictedRating = parameters.mu + nbu + nbi + scal(npu, nqi);
        double error = rating - predictedRating;

        answer.bu[userId] = nbu + answer.gamma * (error - answer.lambda * nbu);
        answer.bi[itemId] = nbi + answer.gamma * (error - answer.lambda * nbi);

        for (int j = 0; j < answer.best_films_count; j++) {
          double qi = nqi[j];
          double pu = npu[j];
          nqi[j] = qi + answer.gamma * (error * pu - answer.lambda * qi);
          npu[j] = pu + answer.gamma * (error * qi - answer.lambda * pu);
        }
      }
      answer.gamma *= DELTA_GAMMA;
      lastError = error;
      error = calculateParametersError(answer);
      fclose(stdin);
      fprintf(stderr, "Finished %d/%d iterations, error = %.10f\n", i + 1, MAX_ITERATIONS, error);
    }
    answer.error = error;
    return answer;
  }

  SVDParameters learn() {
    SVDParameters parameters = SVDParameters();
    parameters.error = 1e18;
    parameters.mu = MU;

    //for (double lambda = MIN_LAMBDA; lambda <= MAX_LAMBDA; lambda += DELTA_LAMBDA) {
    for (double lambda = OPTIMAL_LAMBDA; lambda <= OPTIMAL_LAMBDA; lambda += DELTA_LAMBDA) {
      for (int best_films_count = MIN_NUMBER_OF_BEST; best_films_count <= MAX_NUMBER_OF_BEST; best_films_count += DELTA_NUMBER_OF_BEST) {
        SVDParameters tmpParameters = SVDParameters(lambda, best_films_count, OPTIMAL_GAMMA, MU);
        double error = solve(tmpParameters).error;
        if (parameters.error > error) {
          parameters = SVDParameters(lambda, best_films_count, OPTIMAL_GAMMA, MU);
          parameters.error = error;
        }
      }
    }

    return solve(parameters);
  }
};

#endif