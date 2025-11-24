#include <iostream>
#include <string>
using namespace std;

int main() {
    const string correctPassword = "password123";
    string userPassword;
    int attempts = 0;
    const int maxAttempts = 3;
    
    while (attempts < maxAttempts) {
        cout << "Введите пароль (попытка " << attempts + 1 << " из " << maxAttempts << "): ";
        cin >> userPassword;
        
        if (userPassword == correctPassword) {
            cout << "Доступ разрешен!" << endl;
            break;
        } else {
            cout << "Неверный пароль!" << endl;
            attempts++;
        }
    }
    
    if (attempts == maxAttempts) {
        cout << "Превышено количество попыток. Доступ заблокирован!" << endl;
    }
    
    return 0;
}