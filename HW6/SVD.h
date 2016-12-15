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

  const int MIN_NUMBER_OF_BEST = 10;
  const int MAX_NUMBER_OF_BEST = 10;
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
      fclose(stdin);
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

  inline double scal(const std::vector<double> &pu, const std::vector<double> &qi) {
    double answer = 0;
    assert(pu.size() == qi.size());
    for (size_t i = 0; i < pu.size(); i++) {
      answer += pu[i] * qi[i];
    }
    return answer;
  }

  inline double squareOfNorm(const std::vector<double> &as) {
    return scal(as, as);
  }

  inline int predictRating(const Film &film, SVDParameters &parameters) {
    double result = parameters.mu + 
                    parameters.bu[film.userId] + 
                    parameters.bi[film.itemId] +
                    scal(parameters.pu[film.userId], parameters.qi[film.itemId]);
    int rating = static_cast<int>(result);
    rating = std::min(5, std::max(1, rating));
    return rating;
  }

  template<class T>
  inline T sqr(T x) {
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
    //double error = 0.0;
    //double lastError = 1.0;

    SVDParameters answer = SVDParameters(parameters.lambda, parameters.best_films_count, parameters.gamma, parameters.mu);
    //for (int i = 0; i < MAX_ITERATIONS && std::abs(error - lastError) > EPS; i++) {
    for (int i = 0; i < MAX_ITERATIONS; i++) {
      int counter = 0;
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
        double errorPredicted = rating - predictedRating;

        answer.bu[userId] = nbu + answer.gamma * (errorPredicted - answer.lambda * nbu);
        answer.bi[itemId] = nbi + answer.gamma * (errorPredicted - answer.lambda * nbi);

        for (int j = 0; j < answer.best_films_count; j++) {
          double qi = nqi[j];
          double pu = npu[j];
          nqi[j] = qi + answer.gamma * (errorPredicted * pu - answer.lambda * qi);
          npu[j] = pu + answer.gamma * (errorPredicted * qi - answer.lambda * pu);
        }
        if (++counter % 10000000 == 0) {
            fprintf(stderr, "Finished analyzing train #%d\n", counter);
        }
      }
      answer.gamma *= DELTA_GAMMA;
      //lastError = error;
      //fprintf(stderr, "Started re-calculating error\n");
      //error = calculateParametersError(answer);
      //fprintf(stderr, "Finished %d/%d iterations, error = %.10f\n", i + 1, MAX_ITERATIONS, error);
      fprintf(stderr, "Finished %d/%d iterations\n", i + 1, MAX_ITERATIONS);
    }
    //answer.error = error;
    //fprintf(stderr, "Started calculating error\n");
    //answer.error = calculateParametersError(answer);
    answer.error = 0;
    fprintf(stderr, "Finished solve()\n");
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
        SVDParameters answer = solve(tmpParameters);
	fprintf(stderr, "Returned back to learn()\n");
        if (parameters.error > answer.error) {
          parameters = SVDParameters(lambda, best_films_count, OPTIMAL_GAMMA, MU);
          parameters.error = answer.error;
        }
	fprintf(stderr, "Updated error, lambda = %.5f, best = %d\n", lambda, best_films_count);
      }
      fprintf(stderr, "Exit best loop\n");
    }
    fprintf(stderr, "Before return\n");
    return parameters;
  }
};

#endif
