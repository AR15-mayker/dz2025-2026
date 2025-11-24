#include <iostream>
#include <cstdlib>
#include <ctime>
#include <cmath>

using namespace std;
 
    srand(time(0));
    const int SIZE = 12;
    int arr[SIZE];

    for (int i = 0; i < SIZE; i++) {
        arr[i] = rand() % 61 - 30; // от -30 до 30
    }

    cout << "Исходный массив: ";
    for (int i = 0; i < SIZE; i++) {
        cout << arr[i] << " ";
    }
    cout << endl;

    double sum = 0;
    for (int i = 0; i < SIZE; i++) {
        sum += arr[i];
    }
    cout << "Среднее арифметическое: " << sum / SIZE << endl;

    for (int i = 0; i < SIZE; i++) {
        if (arr[i] < 0) {
            arr[i] = abs(arr[i]);
        }
    }

    cout << "Массив после замены: ";
    for (int i = 0; i < SIZE; i++) {
        cout << arr[i] << " ";
    }
    cout << endl << endl;
