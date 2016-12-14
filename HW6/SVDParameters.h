#ifndef SVDParameters_H
#define SVDParameters_H

#include <map>
#include <algorithm>
#include <vector>
#include <cstring>

struct SVDParameters {
  double mu;
  std::map<long long, double> bu;
  std::map<long long, double> bi;
  double lambda;
  double gamma;
  std::map<long long, std::vector<double>> pu;
  std::map<long long, std::vector<double>> qi;
  int f;
  std::map<long long, std::map<long long, int>> ratings;
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