#include <iostream>
#include <string>
#include <vector>
#include <chrono>

void zadanie1_virtual_vs_abstract() {
    std::cout << "\n========== ЗАДАНИЕ 1 ==========" << std::endl;
    std::cout << "Разница между виртуальным и абстрактным классом\n" << std::endl;
    
    class Animal {
    protected:
        std::string name;
    public:
        Animal(const std::string& n) : name(n) {}
        virtual void makeSound() const = 0;
        virtual void eat() const { std::cout << name << " кушает" << std::endl; }
        void sleep() const { std::cout << name << " спит" << std::endl; }
        virtual ~Animal() {}
    };
    
    class Dog : public Animal {
    public:
        Dog(const std::string& n) : Animal(n) {}
        void makeSound() const override { std::cout << name << " говорит: Гав-гав!" << std::endl; }
        void eat() const override { std::cout << name << " с удовольствием ест кость" << std::endl; }
    };
    
    class Cat : public Animal {
    public:
        Cat(const std::string& n) : Animal(n) {}
        void makeSound() const override { std::cout << name << " говорит: Мяу-мяу!" << std::endl; }
    };
    
    Dog dog("Шарик");
    Cat cat("Мурка");
    
    Animal* animals[] = {&dog, &cat};
    
    for (Animal* animal : animals) {
        animal->makeSound();
        animal->eat();
        animal->sleep();
        std::cout << "---" << std::endl;
    }
}

void zadanie2_rekursiya() {
    std::cout << "\n========== ЗАДАНИЕ 2 ==========" << std::endl;
    std::cout << "Пример рекурсии\n" << std::endl;
    
    int factorial(int n) {
        if (n == 0 || n == 1) return 1;
        return n * factorial(n - 1);
    }
    
    void countdown(int n) {
        if (n < 0) return;
        std::cout << n << " ";
        countdown(n - 1);
    }
    
    std::cout << "Факториал 5: " << factorial(5) << std::endl;
    std::cout << "Факториал 7: " << factorial(7) << std::endl;
    std::cout << "Обратный отсчет от 5: ";
    countdown(5);
    std::cout << std::endl;
}

void zadanie3_fibonacci() {
    std::cout << "\n========== ЗАДАНИЕ 3 ==========" << std::endl;
    std::cout << "Рекурсивное нахождение числа Фибоначчи\n" << std::endl;
    
    unsigned long long fib(int n) {
        if (n == 0) return 0;
        if (n == 1) return 1;
        return fib(n - 1) + fib(n - 2);
    }
    
    std::cout << "Числа Фибоначчи от 0 до 10:" << std::endl;
    for (int i = 0; i <= 10; i++) {
        std::cout << "F(" << i << ") = " << fib(i) << std::endl;
    }
    
    std::cout << "\nF(15) = " << fib(15) << std::endl;
}

int main() {
    zadanie1_virtual_vs_abstract();
    zadanie2_rekursiya();
    zadanie3_fibonacci();
    
    return 0;
}