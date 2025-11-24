#include <iostream>
using namespace std;

int main() {
    double num1, num2;
    char operation;
    char continueCalc;
    
    do {
        cout << "Введите первое число: ";
        cin >> num1;
        cout << "Введите второе число: ";
        cin >> num2;
        cout << "Введите оператор (+, -, *, /): ";
        cin >> operation;
        
        switch (operation) {
            case '+':
                cout << "Результат: " << num1 + num2 << endl;
                break;
            case '-':
                cout << "Результат: " << num1 - num2 << endl;
                break;
            case '*':
                cout << "Результат: " << num1 * num2 << endl;
                break;
            case '/':
                if (num2 != 0) {
                    cout << "Результат: " << num1 / num2 << endl;
                } else {
                    cout << "Ошибка: деление на ноль!" << endl;
                }
                break;
            default:
                cout << "Ошибка: неверный оператор!" << endl;
        }
        
        cout << "Хотите продолжить? (y/n): ";
        cin >> continueCalc;
        
    } while (continueCalc == 'y' || continueCalc == 'Y');
    
    cout << "Калькулятор завершил работу." << endl;
    
    return 0;
}