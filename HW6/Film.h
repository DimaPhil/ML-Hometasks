#ifndef FILM_H
#define FILM_H

struct Film {
  long long userId;
  long long itemId;
  double rating;

  Film() {
  }
  
  Film(long long userId, long long itemId, double rating) : userId(userId), itemId(itemId), rating(rating) {
  }
};

#endif