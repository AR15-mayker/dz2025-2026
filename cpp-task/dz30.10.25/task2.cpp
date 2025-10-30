#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;

int main() {
    setlocale(LC_ALL, "ru");
    
    cout << "=== Швабра (округление) ===" << endl;
    double num;
    cout << "Введите число для округления: ";
    cin >> num;
    
    cout << "Исходное число: " << num << endl;
    cout << "floor (вниз): " << floor(num) << endl;
    cout << "ceil (вверх): " << ceil(num) << endl;
    cout << "round (математическое): " << round(num) << endl;
    cout << "trunc (отбрасывание): " << trunc(num) << endl;
    
    return 0;
}
