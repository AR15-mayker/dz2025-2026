#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace std;

    srand(time(0));
    const int ROWS = 4, COLS = 4;
    int matrix[ROWS][COLS];

    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            matrix[i][j] = rand() % 41 + 10; // от 10 до 50
        }
    }

    cout << "Исходная матрица:" << endl;
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            cout << matrix[i][j] << "\t";
        }
        cout << endl;
    }

    cout << "Максимальные элементы в строках:" << endl;
    for (int i = 0; i < ROWS; i++) {
        int maxVal = matrix[i][0];
        for (int j = 1; j < COLS; j++) {
            if (matrix[i][j] > maxVal) {
                maxVal = matrix[i][j];
            }
        }
        cout << "Строка " << i + 1 << ": " << maxVal << endl;
    }
    cout << endl;
