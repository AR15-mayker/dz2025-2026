# Полезные инструменты Python

## requests
**Описание:** Это самая популярная и простая в использовании HTTP-библиотека для Python. Позволяет легко отправлять HTTP/1.1-запросы (GET, POST, PUT, DELETE и др.), автоматически кодирует параметры, обрабатывает cookies, сессии, SSL-соединения и многое другое.

## pytest
**Описание:** Мощный и гибкий фреймворк для написания тестов на Python. Позволяет писать простые модульные тесты и сложные функциональные тесты. Ключевые особенности: простота синтаксиса (`assert`), автоматическое обнаружение тестов, фикстуры (fixtures), богатый набор плагинов.

## black
**Описание:** "Неумолимый" форматтер кода на Python. Black автоматически форматирует ваш код согласно единому стилю, делает код более читаемым и уменьшает количество "мусорных" правок в pull request'ах.

---

# Задание 1: Создание структуры проекта

**Шаги:**
1. Открыть терминал и перейти в рабочую директорию:
   ```bash
   cd ~/my_work_directory
   ```
2. Создать папку для проекта:
   ```bash
   mkdir my_awesome_project
   cd my_awesome_project
   ```
3. Создать виртуальное окружение:
   ```bash
   python -m venv .venv
   ```
4. Активировать виртуальное окружение:
   - **Linux/macOS:**
     ```bash
     source .venv/bin/activate
     ```
   - **Windows (Cmd.exe):**
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - **Windows (PowerShell):**
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
5. Проверить, что Python запускается из виртуального окружения:
   - Linux/macOS: `which python`
   - Windows: `where python`
6. Установить библиотеку requests:
   ```bash
   pip install requests
   ```
7. Узнать версию requests и создать структуру папок:
   ```bash
   pip show requests  # Смотрим версию (например, 2.31.0)
   mkdir src tests data
   ```
8. Создать requirements.txt с нужной версией:
   ```bash
   echo "requests==2.31.0" > requirements.txt  # Подставьте свою версию
   ```

---

# Задание 2: Рекурсивный поиск и перенаправление вывода

**Шаги:**
1. Перейти в папку с проектом:
   ```bash
   cd ~/path/to/your/python_project
   ```
2. Рекурсивно найти все `.py` файлы и записать их в файл:
   ```bash
   find . -name "*.py" > python_files.txt
   ```
3. Вывести содержимое файла:
   ```bash
   cat python_files.txt
   ```
4. Найти все строки с `import os` в этих файлах и записать результат:
   ```bash
   grep -r "import os" --include="*.py" . > os_imports.txt
   ```
5. Подсчитать количество строк в файле:
   - Linux/macOS/Bash: `wc -l os_imports.txt`
   - PowerShell: `(Get-Content .\os_imports.txt).Count`
6. Найти все файлы, в названии которых есть "test":
   ```bash
   find . -name "*test*"
   ```
7. Найти файлы, изменённые за последние 24 часа:
   ```bash
   find . -mtime -1
   ```
8. Найти все тестовые файлы, изменённые за последние 24 часа:
   ```bash
   find . -name "*test*" -mtime -1
   ```

---

# Задание 3: Массовое переименование файлов

**Шаги:**
1. Создать папку и перейти в неё:
   ```bash
   mkdir temp_photos && cd temp_photos
   ```
2. Создать 5 пустых `.jpg` файлов:
   ```bash
   touch photo{1..5}.jpg
   ```
3. Создать ещё 3 файла:
   ```bash
   touch document{1..2}.txt image.png
   ```
4. Вывести список `.jpg` файлов:
   ```bash
   ls *.jpg
   ```
5. Скопировать все `.jpg` файлы с новым префиксом:
   - Bash:
     ```bash
     for file in *.jpg; do cp "$file" "vacation_$file"; done
     ```
   - PowerShell:
     ```powershell
     foreach ($file in (Get-ChildItem *.jpg)) { Copy-Item $file.Name ("vacation_" + $file.Name) }
     ```
6. Удалить все оригинальные `.jpg` файлы:
   - Bash: `rm photo*.jpg`
   - PowerShell: `Remove-Item photo*.jpg`
7. Переименовать файл:
   - Bash: `mv image.png picture.png`
   - PowerShell: `Rename-Item image.png picture.png`
8. Создать папку docs и перенести в неё `.txt` файлы:
   ```bash
   mkdir docs && mv *.txt docs/
   ```
9. Удалить папку temp_photos со всем содержимым:
   - Bash: `cd .. && rm -rf temp_photos`
   - PowerShell: `cd .. ; Remove-Item -Recurse -Force temp_photos`

---

# Задание 4: Анализ лог-файла

**Пример содержимого файла app.log:**
```
[INFO] User logged in
[ERROR] Connection timeout
[DEBUG] Starting calculation
[WARNING] Disk space low
[INFO] Data saved successfully
[ERROR] File not found
[DEBUG] Operation completed in 5ms
[WARNING] API response slow
[INFO] User logged out
[ERROR] Permission denied
```

**Шаги:**
1. Создать файл app.log и записать в него данные (см. выше).
2. Вывести все строки лога на экран:
   ```bash
   cat app.log
   ```
3. Вывести только строки с "ERROR":
   - Bash: `grep "ERROR" app.log`
   - PowerShell: `Select-String -Pattern "ERROR" app.log`
4. Вывести строки с "timeout", игнорируя регистр:
   - Bash: `grep -i "timeout" app.log`
   - PowerShell: `Select-String -Pattern "timeout" app.log`
5. Посчитать общее количество строк:
   - Bash: `wc -l app.log`
   - PowerShell: `(Get-Content app.log).Count`
6. Посчитать количество строк с "WARNING":
   - Bash: `grep -c "WARNING" app.log`
   - PowerShell: `(Select-String -Pattern "WARNING" app.log).Count`
7. Добавить новую строку с ERROR в конец файла:
   ```bash
   echo "[ERROR] New critical error" >> app.log
   ```
8. Вывести последние 3 строки файла:
   - Bash: `tail -3 app.log`
   - PowerShell: `Get-Content app.log -Tail 3`
9. Заменить "logged" на "connected" и сохранить в новый файл (Bash):
   ```bash
   sed 's/logged/connected/g' app.log > app_fixed.log
   ```

---

# Задание 5: Написание простого скрипта

## Для Bash (deploy.sh):
```bash
#!/bin/bash

echo "Starting deployment..."

# Создаем папку backup
mkdir -p backup

# Копируем все .py файлы в backup. Проверяем, успешно ли выполнилось копирование.
if cp *.py backup/; then
    echo "Files copied successfully."
else
    echo "Backup failed!"
    exit 1
fi

# Проверяем стиль кода с помощью black (если установлен)
echo "Running code style check..."
black --check *.py

echo "Deployment finished!"
```

**Команды для выполнения скрипта в Bash:**
1. Создать файл, сделать исполняемым:
   ```bash
   touch deploy.sh && chmod +x deploy.sh
   ```
2. Вставить код выше с помощью редактора (nano, vim, code).
3. Запустить скрипт:
   ```bash
   ./deploy.sh
   ```
4. Проверить папку backup:
   ```bash
   ls -la backup/
   ```

## Для PowerShell (deploy.ps1):
```powershell
Write-Host "Starting deployment..."

# Создаем папку backup
New-Item -ItemType Directory -Name "backup" -Force | Out-Null

# Пытаемся скопировать файлы
$pyFiles = Get-ChildItem -Path . -Filter *.py
if ($pyFiles) {
    try {
        Copy-Item -Path $pyFiles -Destination ./backup/ -ErrorAction Stop
        Write-Host "Files copied successfully."
    }
    catch {
        Write-Host "Backup failed!"
        exit 1
    }
} else {
    Write-Host "No .py files found to backup."
}

# Проверяем стиль кода (предполагается, что black установлен и доступен)
Write-Host "Running code style check..."
black --check *.py

Write-Host "Deployment finished!"
```

**Команды для выполнения скрипта в PowerShell:**
1. Создать файл:
   ```powershell
   New-Item deploy.ps1
   ```
2. Вставить код выше с помощью редактора (notepad, VSCode).
3. Разрешить выполнение для текущей сессии:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
   ```
4. Запустить скрипт:
   ```powershell
   .\deploy.ps1
   ```
5. Проверить папку backup:
   ```powershell
   Get-ChildItem -Path ./backup
   ```