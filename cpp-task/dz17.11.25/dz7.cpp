#include <iostream>
#include <string>
using namespace std;

int main() {
    string secretWord = "программа";
    string userWord;
    int maxAttempts = 5;
    int attempts = 0;
    
    cout << "Добро пожаловать в игру 'Угадай слово'!" << endl;
    cout << "У вас есть " << maxAttempts << " попыток чтобы угадать слово." << endl;
    cout << "Подсказка: это связано с компьютерами" << endl;
    
    while (attempts < maxAttempts) {
        cout << "\nПопытка " << attempts + 1 << " из " << maxAttempts << ": ";
        cin >> userWord;
        
        if (userWord == secretWord) {
            cout << "Поздравляем! Вы угадали слово!" << endl;
            break;
        } else {
            cout << "Неверно! Попробуйте еще раз." << endl;
            attempts++;
        }
    }
    
    if (attempts == maxAttempts) {
        cout << "К сожалению, вы не угадали. Загаданное слово было: " << secretWord << endl;
    }
    
    return 0;
}