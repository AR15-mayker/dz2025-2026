#include <iostream>
#include <string>
using namespace std;

int main() {
    cout << "Задача 5: Проверка пароля\n";
    const string correctPassword = "password123";
    string inputPassword;
    int tries = 3;
    
    while (tries > 0) {
        cout << "Введите пароль (осталось попыток: " << tries << "): ";
        cin >> inputPassword;
        
        if (inputPassword == correctPassword) {
            cout << "Доступ разрешен!\n";
            break;
        }
        tries--;
    }
    
    if (tries == 0) cout << "Доступ запрещен!\n";
    return 0;
}