#ifndef TRAIN_H
#define TRAIN_H

struct Train {
  long long userId;
  long long itemId;
  int rate;

  Train(long long userId, long long itemId, int rate) : userId(userId), itemId(itemId), rate(rate) {
  }
};

#endif