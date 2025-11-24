#include <iostream>
using namespace std;

int main() {
    int number;
    cout << "Введите целое число: ";
    cin >> number;
    
    if (number % 2 == 0) {
        cout << "Чётное" << endl;
    } else {
        cout << "Нечётное" << endl;
    }
    
    return 0;
}