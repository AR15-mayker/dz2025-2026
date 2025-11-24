#include <iostream>

// Функция для вычисления факториала
long long factorial(int n) {
    long long result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}

int main() {
    // Задача 2: Рассадить 4 человек в 9 вагонах
    int wagons = 9, people = 4;
    
    // Количество способов = размещения из 9 по 4
    long long ways = factorial(wagons) / factorial(wagons - people);
    
    std::cout << "Задача 2: " << ways << " способов" << std::endl;
    
    return 0;
}