#include "SVD.h"
#include "SVDParameters.h"
#include "Utils.h"

const int MAX_LENGTH = 1000;

int main() {
  SVD svd = SVD("data/train.csv");
  SVDParameters bestParameters = svd.learn();
  freopen("ans-submission.csv", "w", stdout);
  printf("Id,Prediction\n");
  freopen("data/test-ids.csv", "r", stdin);
  char s[MAX_LENGTH];
  scanf("%s", s);
  while (scanf("%s", s) >= 1) {
    std::vector<std::string> parts = split(s, ',');
    long long testId = std::stoll(strip(parts[0]));
    long long userId = std::stoll(strip(parts[1]));
    long long itemId = std::stoll(strip(parts[2]));
    printf("%lld,%d\n", testId, svd.getRate(Film(userId, itemId, 0), bestParameters));
  }
}