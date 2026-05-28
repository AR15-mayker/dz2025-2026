#include <iostream>
#include <string>

class Animal {
protected:
    std::string name;
    
public:
    Animal(const std::string& n) : name(n) {}
    
    virtual void makeSound() const = 0;
    
    virtual void eat() const {
        std::cout << name << " кушает" << std::endl;
    }
    
    void sleep() const {
        std::cout << name << " спит" << std::endl;
    }
    
    virtual ~Animal() {}
};

class Dog : public Animal {
public:
    Dog(const std::string& n) : Animal(n) {}
    
    void makeSound() const override {
        std::cout << name << " говорит: Гав-гав!" << std::endl;
    }
    
    void eat() const override {
        std::cout << name << " с удовольствием ест кость" << std::endl;
    }
};

class Cat : public Animal {
public:
    Cat(const std::string& n) : Animal(n) {}
    
    void makeSound() const override {
        std::cout << name << " говорит: Мяу-мяу!" << std::endl;
    }
};

int main() {
    std::cout << "=== ДЕМОНСТРАЦИЯ ВИРТУАЛЬНОГО И АБСТРАКТНОГО КЛАССОВ ===" << std::endl;
    
    Dog dog("Шарик");
    Cat cat("Мурка");
    
    Animal* animals[] = {&dog, &cat};
    
    for (Animal* animal : animals) {
        animal->makeSound();
        animal->eat();
        animal->sleep();
        std::cout << "---" << std::endl;
    }
    
    std::cout << "\nВажность виртуального деструктора:" << std::endl;
    Animal* ptr = new Dog("Бобик");
    delete ptr;
    
    return 0;
}