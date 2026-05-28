#include <iostream>
#include <vector>
#include <chrono>

unsigned long long fibonacciRecursive(int n) {
    if (n == 0) return 0;
    if (n == 1) return 1;
    return fibonacciRecursive(n - 1) + fibonacciRecursive(n - 2);
}

unsigned long long fibonacciMemoization(int n, std::vector<unsigned long long>& memo) {
    if (n == 0) return 0;
    if (n == 1) return 1;
    
    if (memo[n] != 0) return memo[n];
    
    memo[n] = fibonacciMemoization(n - 1, memo) + fibonacciMemoization(n - 2, memo);
    return memo[n];
}

unsigned long long fibonacciMemoization(int n) {
    std::vector<unsigned long long> memo(n + 1, 0);
    return fibonacciMemoization(n, memo);
}

unsigned long long fibonacciTailRecursion(int n, unsigned long long a = 0, unsigned long long b = 1) {
    if (n == 0) return a;
    if (n == 1) return b;
    return fibonacciTailRecursion(n - 1, b, a + b);
}

int main() {
    std::cout << "=== НАХОЖДЕНИЕ ЧИСЕЛ ФИБОНАЧЧИ РЕКУРСИЕЙ ===" << std::endl;
    
    std::cout << "Числа Фибоначчи от 0 до 10:" << std::endl;
    for (int i = 0; i <= 10; i++) {
        std::cout << "F(" << i << ") = " << fibonacciTailRecursion(i) << std::endl;
    }
    
    std::cout << "\nF(10) через классическую рекурсию: " << fibonacciRecursive(10) << std::endl;
    std::cout << "F(30) через мемоизацию: " << fibonacciMemoization(30) << std::endl;
    std::cout << "F(30) через хвостовую рекурсию: " << fibonacciTailRecursion(30) << std::endl;
    
    auto start = std::chrono::high_resolution_clock::now();
    auto result = fibonacciTailRecursion(40);
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "\nF(40) через хвостовую рекурсию: " << result << std::endl;
    std::cout << "Время выполнения: " << duration.count() << " мкс" << std::endl;
    
    return 0;
}