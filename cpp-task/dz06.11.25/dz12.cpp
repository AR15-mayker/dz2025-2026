#include <iostream>
#include <cmath>
using namespace std;

int main() {
    double marks[5];
    for (int i = 0; i < 5; i++) {
        cin >> marks[i];
        cout << round(marks[i]) << endl;
    }
    return 0;
}