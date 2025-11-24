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
    // Задача 1: У мамы 2 яблока и 3 груши
    int apples = 2, pears = 3;
    int totalFruits = apples + pears;
    
    // Количество способов = перестановки с повторениями
    long long ways = factorial(totalFruits) / (factorial(apples) * factorial(pears));
    
    std::cout << "Задача 1: " << ways << " способов" << std::endl;
    
    return 0;
}