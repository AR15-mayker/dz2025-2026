#include <iostream>
using namespace std;

int main() {
    double a, b;
    cout << "Enter a and b: ";
    cin >> a >> b;

    if (a != 0) {
        double x = b / a;
        cout << "x = " << x << endl;
    } else {
        if (b == 0) {
            cout << "any" << endl;
        } else {
            cout << "No" << endl;
        }
    }

    return 0;
}