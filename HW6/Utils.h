#ifndef UTILS_H
#define UTILS_H

#include <cstring>
#include <cstdlib>

bool isWhitespace(char c) {
  return c == ' ' || c == '\t' || c == '\n';
}

std::vector<std::string> split(char *s, char delimeter) {
  size_t length = strlen(s);
  std::vector<std::string> parts;
  std::string current;
  for (size_t i = 0; i < length; i++) {
    if (s[i] == delimeter) {
      parts.push_back(current);
      current = "";
    } else {
      current += s[i];
    }
  }
  if (current.size() > 0) {
    parts.push_back(current);
  }
  return std::move(parts);
}

std::string strip(const std::string &s) {
  size_t l = 0;
  size_t r = s.size() - 1;
  while (isWhitespace(s[l])) {
    l++;
  }
  while (isWhitespace(s[r])) {
    r--;
  }
  return s.substr(l, r - l + 1);
}

#endif