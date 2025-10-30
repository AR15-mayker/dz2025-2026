#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;

int main() {
    setlocale(LC_ALL, "ru");
    
    cout << "=== Вещественные числа -- 2 ===" << endl;
    double a, b;
    cout << "Введите два вещественных числа: ";
    cin >> a >> b;
    
    cout << fixed << setprecision(6);
    cout << "a + b = " << a + b << endl;
    cout << "a - b = " << a - b << endl;
    cout << "a * b = " << a * b << endl;
    cout << "a / b = " << a / b << endl;
    cout << "a^b = " << pow(a, b) << endl;
    
    return 0;
}
