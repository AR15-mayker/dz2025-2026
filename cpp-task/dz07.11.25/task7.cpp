#include <iostream>
#include <string>
using namespace std;

int main() {
    cout << "Задача 7: Угадай слово\n";
    string secretWord = "apple";
    string displayWord(secretWord.length(), '_');
    int attemptsWord = 0;
    const int maxAttempts = 6;

    while (attemptsWord < maxAttempts && displayWord != secretWord) {
        cout << "Текущее состояние: " << displayWord << endl;
        cout << "Введите букву: ";
        char letter;
        cin >> letter;

        bool found = false;
        for (int i = 0; i < secretWord.length(); i++) {
            if (secretWord[i] == letter) {
                displayWord[i] = letter;
                found = true;
            }
        }

        if (!found) {
            attemptsWord++;
            cout << "Не угадали! Ошибок: " << attemptsWord << "/" << maxAttempts << endl;
        }
    }

    if (displayWord == secretWord) 
        cout << "Поздравляем! Вы угадали слово: " << secretWord << endl;
    else 
        cout << "Вы проиграли! Загаданное слово: " << secretWord << endl;
    
    return 0;
}