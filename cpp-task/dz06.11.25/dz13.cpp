#include <iostream>
#include <cmath>
#include <iomanip>
using namespace std;

int main() {
    double a, b;
    cin >> a >> b;
    double c = sqrt(a*a + b*b);
    double P = a + b + c;
    double p = P / 2;
    double S = sqrt(p * (p-a) * (p-b) * (p-c));
    
    cout << fixed << setprecision(6) << c << " " << P << " " << S << endl;
    return 0;
}