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
    // Задача 3: Подгруппы из 9 человек (не менее 2 человек)
    int groupSize = 9;
    long long ways = 0;
    
    // Суммируем сочетания для размеров подгрупп от 2 до 9
    for (int i = 2; i <= groupSize; ++i) {
        ways += combinations(groupSize, i);
    }
    
    std::cout << "Задача 3: " << ways << " способов" << std::endl;
    
    return 0;
}