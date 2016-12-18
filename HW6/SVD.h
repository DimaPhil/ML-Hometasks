#ifndef SVD_H
#define SVD_H

#include <cstdio>
#include <iostream>
#include <algorithm>
#include <cassert>
#include <vector>
#include <cstring>
#include <chrono>
#include <random>

#include "SVDParameters.h"
#include "Utils.h"
#include "Film.h"
#include "Train.h"

struct SVD {
  const char* filename;
  const int MAX_LENGTH = 50;

  const double MU = 3.6033; //average rating
  const int MAX_ITERATIONS = 30;
  const int EPS = 1e-7;

  const double MIN_LAMBDA = 0.001;
  const double MAX_LAMBDA = 0.010;
  const double DELTA_LAMBDA = 0.001;

  const int MIN_F = 5;
  const int MAX_F = 15;
  const int DELTA_F = 5;

  const double OPTIMAL_GAMMA = 0.005;
  const double DELTA_GAMMA = 0.95;
  std::vector<Film> trains;

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
      char s[MAX_LENGTH];
      freopen(filename, "r", stdin);
      getLine(s);
      int counter = 0;
      int sumRate = 0;
      int minUserId = INT_MAX;
      int maxUserId = 0;
      int minItemId = INT_MAX;
      int maxItemId = 0;
      fprintf(stderr, "Started reading...\n");
      while (getLine(s)) {
        std::vector<std::string> parts = split(s, ',');
        if (++counter % 1000000 == 0) {
          fprintf(stderr, "%d lines read\n", counter);
        }

        int userId = std::stoi(strip(parts[0]));
        int itemId = std::stoi(strip(parts[1]));
        int rating = std::stoi(strip(parts[2]));
        sumRate += rating;

        minUserId = std::min(minUserId, userId);
        maxUserId = std::max(maxUserId, userId);
        minItemId = std::min(minItemId, itemId);
        maxItemId = std::max(maxItemId, itemId);
        trains.emplace_back(userId, itemId, rating * 1.0);
      }
      fclose(stdin);
      fprintf(stderr, "userId: [%d, %d]\n", minUserId, maxUserId);
      fprintf(stderr, "itemId: [%d, %d]\n", minItemId, maxItemId);
      fprintf(stderr, "Average rating: %.5f\n", (double)sumRate / static_cast<int>(trains.size()));
  }

  std::vector<double> generateRandomValues(int n) {
    srand(time(nullptr));
    std::vector<double> as(n);
    for (int i = 0; i < n; i++) {
      as[i] = (1.0 / n) * (rand() * 1.0 / RAND_MAX);
    }
    return std::move(as);
  }

  inline double scal(const std::vector<double> &pu, const std::vector<double> &qi) {
    double answer = 0;	    
    for (size_t i = 0; i < qi.size(); i++) {
      answer += pu[i] * qi[i];
    }
    return answer;
  }

  inline double squareOfNorm(const std::vector<double> &as) {
    double answer = 0;
    for (size_t i = 0; i < as.size(); i++) {
      answer += as[i] * as[i];
    }
    return answer;
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
    fprintf(stderr, "Using parameters: lambda=%.6f, best_films_count=%d, gamma=%.6f, mu = %.6f\n", parameters.lambda, parameters.f,
                                                                                    parameters.gamma, parameters.mu);
    double error = 0.0;
    double lastError = 1.0;

    SVDParameters answer = SVDParameters(parameters.lambda, parameters.f, parameters.gamma, parameters.mu);
    for (int i = 0; i < MAX_ITERATIONS && std::abs(error - lastError) > EPS; i++) {
      int counter = 0;
      for (const Film &train : trains) {
        int userId = train.userId;
        int itemId = train.itemId;
        int rating = train.rating;

        if (i == 0) {
          answer.pu[userId] = generateRandomValues(answer.f);
          answer.qi[itemId] = generateRandomValues(answer.f);
          answer.bu[userId] = 0;
          answer.bi[itemId] = 0;
          answer.ratings[userId][itemId] = rating;
        }

        double nbu = answer.bu[userId];
        double nbi = answer.bi[itemId];
        std::vector<double> &npu = answer.pu[userId];
        std::vector<double> &nqi = answer.qi[itemId];
        
        double predictedRating = answer.mu + nbu + nbi + scal(npu, nqi);
        double errorPredicted = rating - predictedRating;
        
        answer.bu[userId] = nbu + answer.gamma * (errorPredicted - answer.lambda * nbu);
        answer.bi[itemId] = nbi + answer.gamma * (errorPredicted - answer.lambda * nbi);

        for (int j = 0; j < answer.f; j++) {
          double pu = npu[j];
          double qi = nqi[j];
          npu[j] = pu + answer.gamma * (errorPredicted * qi - answer.lambda * pu);
          nqi[j] = qi + answer.gamma * (errorPredicted * pu - answer.lambda * qi);
        }
        if (++counter % 10000000 == 0) {
            fprintf(stderr, "Finished analyzing train #%d\n", counter);
        }
      }
      answer.gamma *= DELTA_GAMMA;
      lastError = error;
      fprintf(stderr, "Started re-calculating error\n");
      error = calculateParametersError(answer);
      fprintf(stderr, "Finished %d/%d iterations, error = %.10f\n", i + 1, MAX_ITERATIONS, error);
    }
    fprintf(stderr, "Started calculating error\n");
    answer.error = calculateParametersError(answer);
    fprintf(stderr, "Finished solve()\n");
    return answer;
  }

  SVDParameters learn() {
    SVDParameters parameters = SVDParameters();
    parameters.error = 1e18;
    parameters.mu = MU;

    for (double lambda = MIN_LAMBDA; lambda <= MAX_LAMBDA; lambda += DELTA_LAMBDA) {
      for (int f = MIN_F; f <= MAX_F; f += DELTA_F) {
        SVDParameters tmpParameters = SVDParameters(lambda, f, OPTIMAL_GAMMA, MU);
        SVDParameters answer = solve(tmpParameters);
	      if (parameters.error > answer.error) {
	        parameters = SVDParameters(lambda, f, OPTIMAL_GAMMA, MU);
        }
      }
    }
    return solve(parameters);
  }
};

#endif
