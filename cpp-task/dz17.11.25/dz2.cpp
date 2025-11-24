#include <iostream>
#include <cstdlib> // Для rand() и srand()
#include <ctime> // Для time()

using namespace std;

int main() {
    // Инициализация генератора случайных чисел
    srand(time(0));
    
    // Генерация случайного числа от 1 до 100
    int randomNumber = 1 + rand() % 100;
    int userGuess, attempts = 0;
    
    cout << "Я загадал число от 1 до 100. Попробуйте угадать!" << endl;
    
    do {
        cout << "Ваша попытка: ";
        cin >> userGuess;
        attempts++;
        
        if (userGuess < randomNumber) {
            cout << "Больше!" << endl;
        } else if (userGuess > randomNumber) {
            cout << "Меньше!" << endl;
        }
    } while (userGuess != randomNumber);
    
    cout << "Поздравляем! Вы угадали число " << randomNumber << " за " << attempts << " попыток." << endl;
    
    return 0;
}