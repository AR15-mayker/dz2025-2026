#include <iostream>
using namespace std;

int main() {
    cout << "Бонус: Банкомат\n";
    double balance = 1000.0;
    int option;
    
    while (true) {
        cout << "\n1. Проверить баланс\n2. Снять наличные\n3. Выйти\nВыберите операцию: ";
        cin >> option;

        if (option == 1) {
            cout << "Ваш баланс: $" << balance << endl;
        }
        else if (option == 2) {
            double amount;
            cout << "Введите сумму: ";
            cin >> amount;
            if (amount <= balance && amount > 0) {
                balance -= amount;
                cout << "Операция выполнена. Новый баланс: $" << balance << endl;
            }
            else {
                cout << "Недостаточно средств или неверная сумма!\n";
            }
        }
        else if (option == 3) {
            cout << "До свидания!\n";
            break;
        }
        else {
            cout << "Неверная операция!\n";
        }
    }
    
    return 0;
}