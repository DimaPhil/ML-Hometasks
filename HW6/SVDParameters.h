#ifndef SVDParameters_H
#define SVDParameters_H

#include <algorithm>
#include <vector>
#include <cstring>
#include <boost/unordered_map.hpp>

struct SVDParameters {
  double mu;
  boost::unordered_map<int, double> bu;
  boost::unordered_map<int, double> bi;
  double lambda;
  double gamma;
  boost::unordered_map<int, std::vector<double>> pu;
  boost::unordered_map<int, std::vector<double>> qi;
  int f;
  boost::unordered_map<long long, boost::unordered_map<long long, int>> ratings;
  double error;

  SVDParameters() {
  }

  SVDParameters(double lambda, int f, double gamma, double mu) {
    this->lambda = lambda;
    this->f = f;
    this->gamma = gamma;
    this->mu = mu;
  }
};

#endif
