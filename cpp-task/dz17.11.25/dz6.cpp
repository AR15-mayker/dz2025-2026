#include <iostream>
#include <climits>
using namespace std;

int main() {
    int number, count = 0, sum = 0;
    int minNum = INT_MAX, maxNum = INT_MIN;
    char continueInput;
    
    cout << "Вводите числа для статистики:" << endl;
    
    do {
        cout << "Введите число: ";
        cin >> number;
        
        count++;
        sum += number;
        
        if (number < minNum) minNum = number;
        if (number > maxNum) maxNum = number;
        
        cout << "Продолжить ввод? (y/n): ";
        cin >> continueInput;
        
    } while (continueInput == 'y' || continueInput == 'Y');
    
    if (count > 0) {
        double average = static_cast<double>(sum) / count;
        
        cout << "\nСтатистика:" << endl;
        cout << "Количество чисел: " << count << endl;
        cout << "Сумма: " << sum << endl;
        cout << "Среднее арифметическое: " << average << endl;
        cout << "Минимальное значение: " << minNum << endl;
        cout << "Максимальное значение: " << maxNum << endl;
    } else {
        cout << "Числа не были введены." << endl;
    }
    
    return 0;
}