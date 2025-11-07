#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;

int main() {
    srand(time(0));
    cout << "Задача 2: Угадай число\n";
    
    int randomNumber = 1 + rand() % 100;
    int guess, attempts = 0;
    
    while (true) {
        cout << "Ваша догадка: ";
        cin >> guess;
        attempts++;
        
        if (guess == randomNumber) {
            cout << "Поздравляем! Угадано за " << attempts << " попыток.\n";
            break;
        }
        cout << (guess < randomNumber ? "Больше\n" : "Меньше\n");
    }
    
    return 0;
}