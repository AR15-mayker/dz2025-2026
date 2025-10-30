#include <iostream>
#include <iomanip>

using namespace std;

int main() {
    setlocale(LC_ALL, "ru");
    
    cout << "=== Мини округлятор ===" << endl;
    double num;
    int decimals;
    cout << "Введите число: ";
    cin >> num;
    cout << "Введите количество знаков после запятой: ";
    cin >> decimals;
    
    cout << "Округленное число: " << fixed << setprecision(decimals) << num << endl;
    
    return 0;
}
