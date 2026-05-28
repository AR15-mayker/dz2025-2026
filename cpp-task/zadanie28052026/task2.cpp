#include <iostream>

int factorial(int n) {
    if (n == 0 || n == 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

void countdown(int n) {
    if (n < 0) {
        return;
    }
    std::cout << n << " ";
    countdown(n - 1);
}

int main() {
    std::cout << "=== ПРИМЕРЫ РЕКУРСИИ ===" << std::endl;
    
    std::cout << "Факториал 5: " << factorial(5) << std::endl;
    std::cout << "Факториал 7: " << factorial(7) << std::endl;
    
    std::cout << "\nОбратный отсчет от 5: ";
    countdown(5);
    std::cout << std::endl;
    
    return 0;
}