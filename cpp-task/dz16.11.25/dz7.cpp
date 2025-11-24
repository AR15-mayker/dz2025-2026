#include <iostream>
using namespace std;

int main() {
    double purchaseAmount, discount = 0, finalAmount;
    
    cout << "Введите сумму покупки: ";
    cin >> purchaseAmount;
    
    if (purchaseAmount > 10000) {
        discount = 15;
    } else if (purchaseAmount >= 5000) {
        discount = 10;
    } else if (purchaseAmount >= 1000) {
        discount = 5;
    }
    
    finalAmount = purchaseAmount * (1 - discount / 100);
    
    cout << "Сумма покупки: " << purchaseAmount << " руб." << endl;
    cout << "Скидка: " << discount << "%" << endl;
    cout << "Итоговая сумма: " << finalAmount << " руб." << endl;
    
    return 0;
}