#include <iostream>
using namespace std;

int main() {
    int number;
    
    cout << "Введите число для обратного отсчета: ";
    cin >> number;
    
    cout << "Обратный отсчет:" << endl;
    
    for (int i = number; i >= 0; i--) {
        cout << i << endl;
    }
    
    cout << "Пуск!" << endl;
    
    return 0;
}