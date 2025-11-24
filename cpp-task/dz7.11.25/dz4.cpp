#include <iostream>

// Функция для вычисления факториала
long long factorial(int n) {
    long long result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}

// Функция для вычисления числа сочетаний C(n, k)
long long combinations(int n, int k) {
    if (k < 0 || k > n) return 0;
    return factorial(n) / (factorial(k) * factorial(n - k));
}

int main() {
    // Задача 4: Выбрать 5 мальчиков из 10, 2 определенных уже в команде
    int totalBoys = 10, teamSize = 5;
    int fixedBoys = 2;
    
    // Выбираем оставшихся 3 мальчиков из 8
    long long ways = combinations(totalBoys - fixedBoys, teamSize - fixedBoys);
    
    std::cout << "Задача 4: " << ways << " способов" << std::endl;
    
    return 0;
}