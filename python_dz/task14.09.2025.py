import sqlite3


def get_connection():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn


def add_user(username, email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            (username, email)
        )
        conn.commit()
        print(f"Пользователь {username} успешно добавлен!")
    except sqlite3.IntegrityError:
        print("Ошибка: такое имя пользователя или email уже существует")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")
    finally:
        conn.close()


def create_post(title, content, user_id, category_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO posts (title, content, user_id, category_id)
               VALUES (?, ?, ?, ?)""",
            (title, content, user_id, category_id)
        )
        conn.commit()
        print(f"Пост '{title}' успешно создан!")
    except sqlite3.Error as e:
        print(f"Ошибка при создании поста: {e}")
    finally:
        conn.close()


def get_all_posts():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT 
                posts.id, 
                posts.title, 
                posts.content, 
                users.username as author,
                categories.name as category,
                posts.created_at
def show_all_posts():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT posts.id, posts.title, posts.content, users.username, categories.name, posts.created_at
            FROM posts
            JOIN users ON posts.user_id = users.id
            JOIN categories ON posts.category_id = categories.id
            ORDER BY posts.created_at DESC
        """)
        posts = cursor.fetchall()
        print("Все посты:")
        for post in posts:
            print(f"ID: {post[0]}, Заголовок: {post[1]}, Автор: {post[3]}, Категория: {post[4]}, Дата: {post[5]}")
            print(f"Содержание: {post[2]}")
            print("-"*40)
    except sqlite3.Error as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()
