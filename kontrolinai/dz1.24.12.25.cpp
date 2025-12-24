#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

// ============================
// Класс Date (упрощенный)
// ============================
class Date {
private:
    int d, m, y;
public:
    Date(int day = 1, int month = 1, int year = 2000) : d(day), m(month), y(year) {}
    
    void print() const { 
        printf("%02d.%02d.%04d", d, m, y); 
    }
    
    bool operator<(const Date& other) const {
        if (y != other.y) return y < other.y;
        if (m != other.m) return m < other.m;
        return d < other.d;
    }
    
    friend ostream& operator<<(ostream& os, const Date& dt);
};

ostream& operator<<(ostream& os, const Date& dt) {
    os << dt.d << "." << dt.m << "." << dt.y;
    return os;
}

// ============================
// Класс Book
// ============================
class Book {
private:
    string isbn, title, author;
    bool available;
public:
    Book(string i = "", string t = "", string a = "") 
        : isbn(i), title(t), author(a), available(true) {}
    
    string getISBN() const { return isbn; }
    string getTitle() const { return title; }
    string getAuthor() const { return author; }
    bool isAvail() const { return available; }
    
    void setAvail(bool a) { available = a; }
    
    void display() const {
        cout << isbn << " | " << title << " | " << author 
             << " | " << (available ? "Доступна" : "Выдана");
    }
    
    bool operator==(const Book& other) const {
        return isbn == other.isbn;
    }
};

// ============================
// Базовый класс LibraryMember
// ============================
class LibraryMember {
protected:
    string id, name;
    vector<string> borrowedBooks;
    int maxBooks;
    
public:
    LibraryMember(string i = "", string n = "", int max = 5) 
        : id(i), name(n), maxBooks(max) {}
    
    virtual ~LibraryMember() {}
    
    string getID() const { return id; }
    string getName() const { return name; }
    
    bool borrowBook(const string& isbn) {
        if (borrowedBooks.size() >= maxBooks) {
            cout << "Лимит книг (" << maxBooks << ") превышен!\n";
            return false;
        }
        borrowedBooks.push_back(isbn);
        return true;
    }
    
    bool returnBook(const string& isbn) {
        auto it = find(borrowedBooks.begin(), borrowedBooks.end(), isbn);
        if (it != borrowedBooks.end()) {
            borrowedBooks.erase(it);
            return true;
        }
        return false;
    }
    
    bool hasBook(const string& isbn) const {
        return find(borrowedBooks.begin(), borrowedBooks.end(), isbn) != borrowedBooks.end();
    }
    
    virtual void display() const {
        cout << id << " | " << name << " | Книг: " << borrowedBooks.size();
    }
    
    virtual string getType() const { return "Обычный"; }
};

// ============================
// Класс StudentMember
// ============================
class StudentMember : public LibraryMember {
private:
    string major;
public:
    StudentMember(string i = "", string n = "", string m = "") 
        : LibraryMember(i, n, 7), major(m) {}
    
    void display() const override {
        LibraryMember::display();
        cout << " | " << major << " | Студент";
    }
    
    string getType() const override { return "Студент"; }
};

// ============================
// Класс FacultyMember
// ============================
class FacultyMember : public LibraryMember {
private:
    string department;
public:
    FacultyMember(string i = "", string n = "", string d = "") 
        : LibraryMember(i, n, 10), department(d) {}
    
    void display() const override {
        LibraryMember::display();
        cout << " | " << department << " | Преподаватель";
    }
    
    string getType() const override { return "Преподаватель"; }
};

// ============================
// Класс Library
// ============================
class Library {
private:
    vector<Book> books;
    vector<LibraryMember*> members;
    
    Book* findBook(const string& isbn) {
        for (auto& b : books)
            if (b.getISBN() == isbn) return &b;
        return nullptr;
    }
    
    LibraryMember* findMember(const string& id) {
        for (auto m : members)
            if (m->getID() == id) return m;
        return nullptr;
    }
    
public:
    ~Library() {
        for (auto m : members) delete m;
    }
    
    void addBook(const Book& b) { books.push_back(b); }
    
    void addMember(LibraryMember* m) { members.push_back(m); }
    
    bool borrowBook(const string& mid, const string& isbn) {
        auto member = findMember(mid);
        auto book = findBook(isbn);
        
        if (!member || !book) {
            cout << "Не найдено!\n";
            return false;
        }
        
        if (!book->isAvail()) {
            cout << "Книга уже выдана!\n";
            return false;
        }
        
        if (member->borrowBook(isbn)) {
            book->setAvail(false);
            cout << "Книга выдана " << member->getName() << endl;
            return true;
        }
        return false;
    }
    
    bool returnBook(const string& mid, const string& isbn) {
        auto member = findMember(mid);
        auto book = findBook(isbn);
        
        if (!member || !book) return false;
        
        if (member->returnBook(isbn)) {
            book->setAvail(true);
            cout << "Книга возвращена\n";
            return true;
        }
        return false;
    }
    
    void showBooks() const {
        cout << "\n=== КНИГИ (" << books.size() << ") ===\n";
        for (const auto& b : books) {
            b.display();
            cout << endl;
        }
    }
    
    void showMembers() const {
        cout << "\n=== ЧЛЕНЫ (" << members.size() << ") ===\n";
        for (const auto& m : members) {
            m->display();
            cout << endl;
        }
    }
    
    void searchByTitle(const string& title) const {
        cout << "\n=== Поиск: " << title << " ===\n";
        for (const auto& b : books)
            if (b.getTitle().find(title) != string::npos) {
                b.display();
                cout << endl;
            }
    }
};

// ============================
// Главная программа
// ============================
int main() {
    Library lib;
    
    // Тестовые данные
    lib.addBook(Book("123-4567890123", "Война и мир", "Лев Толстой"));
    lib.addBook(Book("123-4567890124", "Преступление и наказание", "Фёдор Достоевский"));
    lib.addBook(Book("123-4567890125", "Мастер и Маргарита", "Михаил Булгаков"));
    
    lib.addMember(new StudentMember("S001", "Иван Иванов", "Информатика"));
    lib.addMember(new FacultyMember("F001", "Петр Петров", "Математика"));
    lib.addMember(new LibraryMember("R001", "Сергей Сергеев"));
    
    // Демонстрация
    lib.showBooks();
    lib.showMembers();
    
    cout << "\n=== Тест выдачи книги ===\n";
    lib.borrowBook("S001", "123-4567890123");
    lib.showBooks();
    
    cout << "\n=== Тест возврата книги ===\n";
    lib.returnBook("S001", "123-4567890123");
    lib.showBooks();
    
    cout << "\n=== Поиск ===\n";
    lib.searchByTitle("мир");
    
    return 0;
}