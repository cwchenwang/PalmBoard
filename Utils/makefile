all: test
bayes.o: bayes.cpp
	g++ -c bayes.cpp -std=c++11
main.o: main.cpp
	g++ -c main.cpp -std=c++11
utils.o: utils.cpp
	g++ -c utils.cpp -std=c++11
test: main.o bayes.o utils.o
	g++ -o main main.o bayes.o utils.o