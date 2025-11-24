#include <iostream>
using namespace std;

int main() {
    int hour;
    cout << "Введите текущий час (0-23): ";
    cin >> hour;
    
    if (hour < 0 || hour > 23) {
        cout << "Ошибка: час должен быть от 0 до 23" << endl;
    } else if (hour >= 0 && hour <= 5) {
        cout << "Ночь" << endl;
    } else if (hour >= 6 && hour <= 11) {
        cout << "Утро" << endl;
    } else if (hour >= 12 && hour <= 17) {
        cout << "День" << endl;
    } else {
        cout << "Вечер" << endl;
    }
    
    return 0;
}