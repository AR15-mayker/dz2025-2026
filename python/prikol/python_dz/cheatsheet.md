### Шпаргалка по Python для начинающих

#### 1. Переменные и типы данных

```python
name = "Анна"  # str
age = 20        # int
height = 1.75   # float
is_student = True # bool
```

#### 2. Базовые операции

```python
# Арифметика
a = 10 + 5
b = 10 * 2

# Строки
greeting = "Привет, " + name
# f-строки
msg = f"Привет, {name}! Тебе {age} лет."
```

#### 3. Работа с файлами

```python
# Запись
with open("test.txt", "w", encoding="utf-8") as f:
    f.write("Первая строка\nВторая строка")

# Чтение
with open("test.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
```

#### 4. JSON

```python
import json
data = {"name": "Иван", "age": 20}
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
    print(loaded)
```

#### 5. Строковые методы

```python
text = "Python и разработка"
print(text.upper())
print(text.lower())
print(text.replace("разработка", "dev"))
print(text.split())
```

---

См. также модули `os` и `pathlib` для работы с файлами и путями.
