#include <iostream>
using namespace std;

int main() {
    double a, b, c;
    cout << "Введите три стороны треугольника: ";
    cin >> a >> b >> c;
    
    // Проверка на существование треугольника
    if (a + b > c && a + c > b && b + c > a) {
        if (a == b && b == c) {
            cout << "Равносторонний треугольник" << endl;
        } else if (a == b || a == c || b == c) {
            cout << "Равнобедренный треугольник" << endl;
        } else {
            cout << "Разносторонний треугольник" << endl;
        }
    } else {
        cout << "Не треугольник" << endl;
    }
    
    return 0;
}