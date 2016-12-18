#include "SVD.h"
#include "SVDParameters.h"
#include "Utils.h"

const int MAX_STR_LENGTH = 50;

int main(int argc, char **argv) {
  SVD svd = SVD("data/train.csv");
  SVDParameters bestParameters = svd.learn();
  fprintf(stderr, "Finished learning\n");
  fprintf(stderr, "Best parameters: lambda = %.5f, f = %d\n", bestParameters.lambda, bestParameters.f);
  const char *submission = "submission-new.csv";
  freopen(submission, "w", stdout);
  printf("Id,Prediction\n");
  freopen("data/test-ids.csv", "r", stdin);
  fprintf(stderr, "Reading test-ids.csv...\n");
  char s[MAX_STR_LENGTH];
  scanf("%s", s);
  while (scanf("%s", s) >= 1) {
    std::vector<std::string> parts = split(s, ',');
    int testId = std::stoi(strip(parts[0]));
    int userId = std::stoi(strip(parts[1]));
    int itemId = std::stoi(strip(parts[2]));
    printf("%d,%.6f\n", testId, svd.predictRating(Film(userId, itemId, 0), bestParameters));
  }
  fclose(stdin);
  fclose(stdout);
  fprintf(stderr, "Finished, submission is ready\n");
  return 0;
}