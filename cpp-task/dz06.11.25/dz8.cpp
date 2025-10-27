#include <iostream>
#include <cmath>
#include <iomanip>
using namespace std;

int main() {
    int x;
    cin >> x;
    double result = 3 * sqrt(x);
    cout << fixed << setprecision(4) << result << endl;
    return 0;
}