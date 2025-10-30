#include <iostream>
#include <cmath>
#include <iomanip>
#include <string>
#include <sstream>

using namespace std;

int main() {
    setlocale(LC_ALL, "ru");
    
    cout << "=== Что после точки? ===" << endl;
    double num;
    cout << "Введите число: ";
    cin >> num;
    
    double fractional = num - trunc(num);
    cout << "Дробная часть: " << fractional << endl;
    
    // Вывод с высокой точностью чтобы увидеть все цифры
    cout << "Все цифры после точки: ";
    stringstream ss;
    ss << fixed << setprecision(15) << abs(fractional);
    string fracStr = ss.str();
    
    if (fracStr.find('.') != string::npos) {
        cout << fracStr.substr(fracStr.find('.') + 1) << endl;
    }
    
    return 0;
}
