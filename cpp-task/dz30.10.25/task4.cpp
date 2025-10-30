#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;

int main() {
    setlocale(LC_ALL, "ru");
    
    cout << "=== Объем колобка ===" << endl;
    double radius;
    cout << "Введите радиус колобка: ";
    cin >> radius;
    
    double volume = (4.0 / 3.0) * M_PI * pow(radius, 3);
    cout << fixed << setprecision(6);
    cout << "Объем колобка с радиусом " << radius << " = " << volume << endl;
    
    return 0;
}
