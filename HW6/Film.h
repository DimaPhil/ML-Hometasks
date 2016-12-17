#ifndef FILM_H
#define FILM_H

struct Film {
  int userId;
  int itemId;
  double rating;

  Film() {
  }
  
  Film(int userId, int itemId, double rating) : userId(userId), itemId(itemId), rating(rating) {
  }
};

#endif