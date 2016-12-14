#ifndef FILM_H
#define FILM_H

struct Film {
  long long userId;
  long long itemId;
  double rate;

  Film() {
  }
  
  Film(long long userId, long long itemId, double rate) : userId(userId), itemId(itemId), rate(rate) {
  }
};

#endif