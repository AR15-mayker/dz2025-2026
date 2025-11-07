#include <iostream>
using namespace std;

int main() {
    cout << "Задача 1: Сумма чисел до нуля\n";
    int sum = 0, num;
    
    while (true) {
        cout << "Введите число: ";
        cin >> num;
        if (num == 0) break;
        sum += num;
    }
    
    cout << "Сумма: " << sum << endl;
    return 0;
}