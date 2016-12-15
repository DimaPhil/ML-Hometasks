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
  int number_of_films;
  std::map<long long, std::map<long long, int>> ratings;
  double error;

  SVDParameters() {
  }

  SVDParameters(double lambda, int number_of_films, double gamma, double mu) {
    this->lambda = lambda;
    this->number_of_films = number_of_films;
    this->gamma = gamma;
    this->mu = mu;
  }
};

#endif