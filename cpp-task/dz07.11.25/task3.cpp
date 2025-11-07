#include <iostream>
using namespace std;

int main() {
    cout << "Задача 3: Калькулятор\n";
    char choice;
    
    while (true) {
        double a, b;
        char op;
        cout << "Введите выражение (например 2 + 3): ";
        cin >> a >> op >> b;

        switch (op) {
            case '+': cout << "Результат: " << a + b << endl; break;
            case '-': cout << "Результат: " << a - b << endl; break;
            case '*': cout << "Результат: " << a * b << endl; break;
            case '/': 
                if (b != 0) cout << "Результат: " << a / b << endl;
                else cout << "Ошибка: деление на ноль!\n";
                break;
            default: cout << "Неизвестная операция!\n";
        }

        cout << "Продолжить? (y/n): ";
        cin >> choice;
        if (choice != 'y' && choice != 'Y') break;
    }
    
    return 0;
}