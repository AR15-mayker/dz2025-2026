#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <algorithm>

using namespace std;

    srand(time(0));
    vector<int> vec;

    for (int i = 0; i < 15; i++) {
        vec.push_back(rand() % 21 + 5); // от 5 до 25
    }

    cout << "Исходный вектор: ";
    for (int num : vec) {
        cout << num << " ";
    }
    cout << endl;

    vector<int> uniqueVec;
    for (int num : vec) {
        // Проверяем, есть ли элемент уже в uniqueVec
        if (find(uniqueVec.begin(), uniqueVec.end(), num) == uniqueVec.end()) {
            uniqueVec.push_back(num);
        }
    }

    cout << "Вектор без повторений: ";
    for (int num : uniqueVec) {
        cout << num << " ";
    }
    cout << endl << endl;
