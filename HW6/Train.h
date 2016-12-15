#ifndef TRAIN_H
#define TRAIN_H

struct Train {
  long long userId;
  long long itemId;
  int rating;

  Train(long long userId, long long itemId, int rating) : userId(userId), itemId(itemId), rating(rating) {
  }
};

#endif