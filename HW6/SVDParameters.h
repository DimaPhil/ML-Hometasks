#ifndef SVDParameters_H
#define SVDParameters_H

#include <algorithm>
#include <vector>
#include <cstring>
#include <boost/unordered_map.hpp>

struct SVDParameters {
  double mu;
  boost::unordered_map<long long, double> bu;
  boost::unordered_map<long long, double> bi;
  double lambda;
  double gamma;
  boost::unordered_map<long long, std::vector<double>> pu;
  boost::unordered_map<long long, std::vector<double>> qi;
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
