#include <iostream>
#include <climits>
using namespace std;

int main() {
    cout << "Задача 6: Статистика чисел\n";
    int number, count = 0, total = 0, minNum = INT_MAX, maxNum = INT_MIN;
    
    cout << "Вводите числа (0 для завершения):\n";
    while (true) {
        cin >> number;
        if (number == 0) break;
        
        count++;
        total += number;
        if (number < minNum) minNum = number;
        if (number > maxNum) maxNum = number;
    }
    
    if (count > 0) {
        cout << "Количество: " << count << endl
             << "Сумма: " << total << endl
             << "Среднее: " << static_cast<double>(total) / count << endl
             << "Минимум: " << minNum << endl
             << "Максимум: " << maxNum << endl;
    }
    
    return 0;
}
