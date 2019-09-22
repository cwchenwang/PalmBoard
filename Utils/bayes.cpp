#include "bayes.h"
#include "utils.h"

Bayes::Bayes()
{ 
    ifstream file("words.csv");
    vector<string> rowInfo;
    string row;
    for(int i = 0; i < MAX_WORD_LEN; i++) {
        unordered_map<string, double> map;
        words.push_back(map);

        unordered_map<char, double> map1;
        lookup_table.push_back(map1);
    }
    while(getline(file, row)) {
        split(row, ",", rowInfo);
        stringstream ss;
        ss << rowInfo[1];
        double freq;
        ss >> freq;
        int len = rowInfo[0].length();
        words[len-1][rowInfo[0]] = log( freq );
    }

    ifstream cfile("center.csv");

    vector<string> info;
    while(getline(cfile, row)) {
        split(row, ",", info);
        stringstream ss;
        // cout << info[0] << endl;
        ss << info[0];
        char c;
        ss >> c;
        double ux, uy, sx, sy;
        stringstream ss1;
        ss1 << info[1];
        ss1 >> ux;
        stringstream ss2;
        ss2 << info[2];
        ss2 >> uy;
        stringstream ss3;
        ss3 << info[3];
        ss3 >> sx;
        stringstream ss4;
        ss4 << info[4];
        ss4 >> sy;
        centroids[c] = Centroid{ux, uy, sx, sy};
    }

    // for(unordered_map<char, Centroid>::iterator i=centroids.begin(); i != centroids.end(); i++) {
    //     cout << i->first << " " << i->second.ux << endl;
    // }

    // for(unordered_map<string, double> t : words) {
    //     for(unordered_map<string, double>::iterator i = t.begin(); i != t.end(); i++) {
    //         cout << i->first << " " << i->second << endl;
    //     }
    // }
}

void Bayes::newWord() {
    for(int i = 0; i < MAX_WORD_LEN; i++) {
        lookup_table[i].clear();
    }
    word_len = 0;
}

void Bayes::newContact(double x, double y) {
    for(int c = 97; c < 123; c++) {
        lookup_table[word_len][char(c)] = calPsi(c, x, y);
    }
    lookup_table[word_len]['0'] = calPsi('0', x, y);
    word_len = word_len + 1;
}

vector<string> Bayes::getCandidate() {
    double max_prob = DOUBLE_MIN;
    string max_word;
    vector<string> ans;
    // cout << "hello " << endl;
    cout << word_len << endl;
    for(unordered_map<string, double>::iterator i = words[word_len-1].begin(); i != words[word_len-1].end(); i++) {
        string word = i->first;
        double prob = i->second;
        for(int i = 0; i < word.length(); i++) {
            char c = word[i];
            prob += lookup_table[i][c];
        }
        // cout << prob << endl;
        if(prob > max_prob) {
            max_prob = prob;
            max_word = word;
            // cout << word << endl;
        }
    }
    ans.push_back(max_word);
    return ans;
}

double Bayes::calPsi(char c, double x, double y) {
    double z = pow(x-centroids[c].ux,2)/pow(centroids[c].sx,2) + pow(y-centroids[c].uy, 2)/pow(centroids[c].sy, 2);
    return log( 1/(2*PI*centroids[c].sx*centroids[c].sy)*exp(-0.5*z) );
}