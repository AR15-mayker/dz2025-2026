#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <algorithm>
#include <limits>

// ---------------------------
// Задание 1
// ---------------------------
void task1() {
    auto sum = [](int a, int b) { return a + b; };

    int result = sum(20, 22);
    std::cout << "Задание 1: сумма 20 и 22 = " << result << "\n\n";
}

// ---------------------------
// Задание 2
// ---------------------------
class PhoneBook {
private:
    std::map<std::string, std::string> contacts; // имя -> номер

public:
    void add(const std::string& name, const std::string& number) {
        contacts[name] = number;
    }

    bool remove(const std::string& name) {
        return contacts.erase(name) > 0;
    }

    std::string findNumberByName(const std::string& name) const {
        auto it = contacts.find(name);
        if (it != contacts.end()) {
            return it->second;
        }
        return "Не найдено";
    }

    void printAll() const {
        std::cout << "Телефонная книга:\n";
        for (const auto& [name, number] : contacts) {
            std::cout << "  " << name << " -> " << number << '\n';
        }
        std::cout << '\n';
    }
};

void task2() {
    PhoneBook pb;
    pb.add("Иван", "+7-900-111-22-33");
    pb.add("Мария", "+7-901-123-45-67");
    pb.add("Олег", "+7-902-222-33-44");

    pb.printAll();

    std::cout << "Номер Мария: " << pb.findNumberByName("Мария") << '\n';

    if (pb.remove("Олег")) {
        std::cout << "Контакт Олег удалён.\n";
    }

    std::cout << "После удаления:\n";
    pb.printAll();
}

// ---------------------------
// Задание 3
// ---------------------------
class vozrast {
private:
    int age;

public:
    vozrast() : age(0) {}
    explicit vozrast(int a) : age(a) {}

    int getAge() const {
        return age;
    }

    void setAge(int a) {
        age = a;
    }
};

class stud {
private:
    struct Student {
        std::string surname;
        std::string university;
        std::string group;
        vozrast age;
    };

    std::vector<Student> students;

public:
    // Ввод ВСЕХ данных о студентах
    void enter() {
        int n;
        std::cout << "Сколько студентов ввести? ";
        std::cin >> n;
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

        students.clear();
        students.reserve(n);

        for (int i = 0; i < n; ++i) {
            Student s;
            int age;

            std::cout << "\nСтудент " << (i + 1) << ":\n";
            std::cout << "Фамилия: ";
            std::getline(std::cin, s.surname);

            std::cout << "Вуз: ";
            std::getline(std::cin, s.university);

            std::cout << "Группа: ";
            std::getline(std::cin, s.group);

            std::cout << "Возраст: ";
            std::cin >> age;
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

            s.age.setAge(age);
            students.push_back(s);
        }
    }

    // Вывод студентов младше 18 лет
    void show() const {
        std::cout << "\nСтуденты младше 18 лет:\n";
        bool found = false;

        for (const auto& s : students) {
            if (s.age.getAge() < 18) {
                found = true;
                std::cout << "  Фамилия: " << s.surname
                          << ", Вуз: " << s.university
                          << ", Группа: " << s.group
                          << ", Возраст: " << s.age.getAge() << '\n';
            }
        }

        if (!found) {
            std::cout << "  Нет студентов младше 18 лет.\n";
        }
    }
};

void task3() {
    stud st;
    st.enter();
    st.show();
}

int main() {
    task1();
    task2();
    task3();

    return 0;
}