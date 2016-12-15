#include "SVD.h"
#include "SVDParameters.h"
#include "Utils.h"

const int MAX_LENGTH = 50;

int main(int argc, char **argv) {
  SVD svd = SVD("data/train.csv");
  SVDParameters bestParameters = svd.learn();
  const char *submission = "ans-submission.csv";
  freopen(submission, "w", stdout);
  printf("Id,Prediction\n");
  freopen("data/test-ids.csv", "r", stdin);
  fprintf(stderr, "Reading test-ids.csv...");
  char s[MAX_LENGTH];
  scanf("%s", s);
  while (scanf("%s", s) >= 1) {
    std::vector<std::string> parts = split(s, ',');
    long long testId = std::stoll(strip(parts[0]));
    long long userId = std::stoll(strip(parts[1]));
    long long itemId = std::stoll(strip(parts[2]));
    printf("%lld,%d\n", testId, svd.predictRating(Film(userId, itemId, 0), bestParameters));
  }
  fprintf(stderr, "Finished, submission is ready");
  bool found = false;
  for (int i = 0; i < argc; i++) {
    if (!strcmp(argv[i], "--output-rmse")) {
      found = true;
    }
  }
  if (found) {
    double rmse = 0.0;
    freopen(submission, "r", stdin);
    fprintf(stderr, "Calculating RMSE of output...\n");
    scanf("%s", s);
    int size = 0;
    while (scanf("%s", s) >= 1) {
      size++;
      std::vector<std::string> parts = split(s, ',');
      long long userId = std::stoll(strip(parts[0]));
      long long itemId = std::stoll(strip(parts[1]));
      int rating = std::stoi(strip(parts[2]));
      Film film = Film(userId, itemId, rating);
      double error = svd.predictRating(film, bestParameters) - film.rating;
      rmse += error * error;
    }
    fclose(stdin);
    fprintf(stderr, "RMSE: %.5f\n", sqrt(rmse / size));
  }
}