#ifndef TRAIN_H
#define TRAIN_H

struct Train {
  int userId;
  int itemId;
  int rating;

  Train(int userId, int itemId, int rating) : userId(userId), itemId(itemId), rating(rating) {
  }
};

#endif