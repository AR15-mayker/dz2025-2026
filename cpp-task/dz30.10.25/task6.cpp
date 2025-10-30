#include <iostream>
#include <iomanip>
#include <string>
#include <sstream>

using namespace std;

int main() {
    setlocale(LC_ALL, "ru");
    
    cout << "=== Где цифры? ===" << endl;
    double num;
    int digit;
    cout << "Введите число: ";
    cin >> num;
    cout << "Введите цифру для поиска (0-9): ";
    cin >> digit;
    
    if (digit < 0 || digit > 9) {
        cout << "Некорректная цифра!" << endl;
        return 1;
    }
    
    stringstream ss;
    ss << fixed << setprecision(15) << abs(num);
    string numStr = ss.str();
    
    char digitChar = '0' + digit;
    size_t pos = numStr.find(digitChar);
    
    if (pos != string::npos) {
        cout << "Цифра " << digit << " найдена на позиции " << pos;
        if (pos < numStr.find('.')) {
            cout << " (в целой части)" << endl;
        } else {
            cout << " (в дробной части)" << endl;
        }
    } else {
        cout << "Цифра " << digit << " не найдена в числе" << endl;
    }
    
    return 0;
}
