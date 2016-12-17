#ifndef SVDParameters_H
#define SVDParameters_H

#include <algorithm>
#include <vector>
#include <cstring>

struct SVDParameters {
  const int MAX_USER_ID = 480200;
  const int MAX_ITEM_ID = 18000;

  double mu;
  double bu[MAX_USER_ID];
  double bi[MAX_ITEM_ID];
  double lambda;
  double gamma;
  std::vector<double> pu[MAX_USER_ID];
  std::vector<double> qi[MAX_ITEM_ID];
  int best_films_count;
  //boost::unordered_map<long long, boost::unordered_map<long long, int>> ratings;
  double error;

  SVDParameters() {
  }

  SVDParameters(double lambda, int best_films_count, double gamma, double mu) {
    this->lambda = lambda;
    this->best_films_count = best_films_count;
    this->gamma = gamma;
    this->mu = mu;
  }
};

#endif
