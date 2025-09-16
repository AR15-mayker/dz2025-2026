"""
Тема: Реляционная модель данных. Основные понятия

1. Введение
Реляционная модель данных — это логическая модель, в которой все данные представлены в виде таблиц (отношений).

2. Основные понятия:
 - Отношение (Таблица)
 - Атрибут (Столбец)
 - Домен (Область допустимых значений)
 - Кортеж (Строка)
 - Ключи: первичный, внешний, потенциальный
"""

import sqlite3

# --- Шаг 1: Создание таблиц ---
conn = sqlite3.connect('university.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Groups (
	group_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL UNIQUE
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Students (
	student_id INTEGER PRIMARY KEY AUTOINCREMENT,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	group_id INTEGER,
	FOREIGN KEY (group_id) REFERENCES Groups (group_id)
);
''')

conn.commit()

# --- Шаг 2: Вставка данных ---
cursor.execute('DELETE FROM Students;')
cursor.execute('DELETE FROM Groups;')
conn.commit()

cursor.executemany('INSERT INTO Groups (name) VALUES (?)', [('P-101',), ('P-102',)])
conn.commit()

students_data = [
	('Иван', 'Иванов', 1),
	('Петр', 'Петров', 1),
	('Мария', 'Сидорова', 2)
]
cursor.executemany('INSERT INTO Students (first_name, last_name, group_id) VALUES (?,?,?)', students_data)
conn.commit()

# --- Шаг 3: Выборка и вывод ---
# Используем LEFT JOIN, чтобы показать всех студентов, даже если у них нет группы
cursor.execute('''
SELECT s.student_id, s.first_name, s.last_name, g.name as group_name
FROM Students s
LEFT JOIN Groups g ON s.group_id = g.group_id
''')

print("Студенты и их группы:")
rows = cursor.fetchall()
if not rows:
	print("Нет данных о студентах.")
else:
	for row in rows:
		group = row[3] if row[3] is not None else "(нет группы)"
		print(f"ID: {row[0]}, Имя: {row[1]}, Фамилия: {row[2]}, Группа: {group}")

conn.close()
