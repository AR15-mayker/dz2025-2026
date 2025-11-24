#include <iostream>
using namespace std;

int main() {
    int score;
    cout << "Введите оценку (0-100): ";
    cin >> score;
    
    if (score < 0 || score > 100) {
        cout << "Ошибка: оценка должна быть от 0 до 100" << endl;
    } else if (score >= 90) {
        cout << "A" << endl;
    } else if (score >= 80) {
        cout << "B" << endl;
    } else if (score >= 70) {
        cout << "C" << endl;
    } else if (score >= 60) {
        cout << "D" << endl;
    } else {
        cout << "F" << endl;
    }
    
    return 0;
}