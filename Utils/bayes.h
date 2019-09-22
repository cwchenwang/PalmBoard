#ifndef BAYES_H
#define BAYES_H

#include <cmath>
#include <vector>
#include <string>
#include <unordered_map>
#include <fstream>
#include <sstream>
#include <iostream>
#include <limits>

using namespace std;

struct Centroid {
    double ux, uy, sx, sy;
};

class Bayes
{
    const double PI = 3.1415926;
    const int MAX_WORD_LEN = 20;
    static constexpr double DOUBLE_MIN = std::numeric_limits<double>::lowest();

    vector<unordered_map<string, double>> words; //words and their frequency
    unordered_map<char, Centroid> centroids; //the centroids of every character
    vector<unordered_map<char, double>> lookup_table;
    int word_len = 0;
public:
    double calPsi(char c, double x, double y);
    void newContact(double x, double y);
    vector<string> getCandidate();
    void newWord();
    Bayes();
};

#endif // BAYES_H
