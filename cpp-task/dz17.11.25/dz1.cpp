#include <iostream>
using namespace std;

int main() {
    int number, sum = 0;
    
    cout << "Вводите числа (0 для завершения):" << endl;
    
    do {
        cin >> number;
        sum += number;
    } while (number != 0);
    
    cout << "Сумма всех введенных чисел: " << sum << endl;
    
    return 0;
}