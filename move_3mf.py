import os
import shutil
from pathlib import Path

# Папка, где лежат твои файлы (можешь поменять путь)
BASE_DIR = Path(r"C:\Users\Пользователь\dz2025-2026-11")

# Имя папки, куда будем складывать все .3mf
TARGET_DIR = BASE_DIR / "3mf_files"

def move_3mf_files():
    # создаем папку, если её нет
    TARGET_DIR.mkdir(exist_ok=True)

    # перебираем все файлы в BASE_DIR (без подпапок; если нужны подпапки, скажу ниже)
    for file in BASE_DIR.iterdir():
        # проверяем, что это файл и у него расширение .3mf
        if file.is_file() and file.suffix.lower() == ".3mf":
            # формируем путь назначения
            dest = TARGET_DIR / file.name
            # переносим файл
            shutil.move(str(file), str(dest))
            print(f"Перемещен: {file} -> {dest}")

if __name__ == "__main__":
    move_3mf_files()
    print("Готово!")
