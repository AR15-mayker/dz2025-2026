#include <iostream>
using namespace std;

int main() {
    cout << "Задача 4: Обратный отсчет\n";
    int countdown;
    
    cout << "Введите число: ";
    cin >> countdown;
    
    while (countdown >= 0) {
        cout << countdown << " ";
        countdown--;
    }
    cout << endl;
    
    return 0;
}