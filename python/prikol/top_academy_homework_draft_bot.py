#!/usr/bin/env python3
"""Помощник для заполнения домашек Top Academy.

Скрипт автоматизирует рутину:
- авторизация;
- переход по страницам домашних заданий;
- заполнение полей (ссылка GitHub, оценка, время, комментарий);
- отправка только после ручного подтверждения.

Важно: используйте скрипт только по правилам вашей платформы обучения.
"""

from __future__ import annotations

import argparse
import getpass
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://journal.top-academy.ru/ru/main/homework/page/index"
DEFAULT_CREDS_FILE = Path(__file__).with_name(".top_academy_credentials.env")

# Наборы селекторов на случай, если верстка немного меняется.
LOGIN_SELECTORS = [
    "input[name='LoginForm[username]']",
    "input[name='username']",
    "input[type='text']",
]
PASSWORD_SELECTORS = [
    "input[name='LoginForm[password]']",
    "input[name='password']",
    "input[type='password']",
]
LOGIN_BUTTON_SELECTORS = [
    "button[type='submit']",
    "input[type='submit']",
]
HOMEWORK_LINK_SELECTORS = [
    "a[href*='/main/homework/']",
    "a[href*='homework/view']",
]
GITHUB_FIELD_SELECTORS = [
    "input[name*='github']",
    "input[placeholder*='GitHub']",
    "input[type='url']",
]
TIME_FIELD_SELECTORS = [
    "input[name*='time']",
    "input[name*='duration']",
    "input[type='time']",
]
COMMENT_FIELD_SELECTORS = [
    "textarea[name*='comment']",
    "textarea[name*='text']",
    "textarea",
]
SUBMIT_BUTTON_SELECTORS = [
    "button[type='submit']",
    "input[type='submit']",
]


@dataclass
class HomeworkPayload:
    github_url: str
    duration_text: str
    comment: str
    stars: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Черновое автозаполнение домашек Top Academy")
    parser.add_argument("--username", default=os.getenv("TOP_ACADEMY_USERNAME"), help="Логин")
    parser.add_argument("--password", default=os.getenv("TOP_ACADEMY_PASSWORD"), help="Пароль")
    parser.add_argument(
        "--creds-file",
        default=str(DEFAULT_CREDS_FILE),
        help="Файл с сохраненными данными входа (формат .env)",
    )
    parser.add_argument(
        "--save-creds",
        action="store_true",
        help="Сохранить введенные логин/пароль в --creds-file",
    )
    parser.add_argument(
        "--no-prompt",
        action="store_true",
        help="Не спрашивать логин/пароль в интерактивном режиме",
    )
    parser.add_argument("--github-url", required=True, help="Ссылка на GitHub")
    parser.add_argument("--hours", type=int, default=1, help="Часы, потраченные на выполнение")
    parser.add_argument("--minutes", type=int, default=13, help="Минуты, потраченные на выполнение")
    parser.add_argument("--stars", type=int, default=5, help="Количество звёзд (1-5)")
    parser.add_argument("--comment", default="Круто", help="Комментарий")
    parser.add_argument("--headless", action="store_true", help="Запустить браузер без UI")
    parser.add_argument(
        "--max-homeworks",
        type=int,
        default=0,
        help="Ограничить количество домашних заданий (0 = без ограничений)",
    )
    parser.add_argument(
        "--auto-submit",
        action="store_true",
        help="Отправлять автоматически без подтверждения (не рекомендуется)",
    )
    return parser.parse_args()


def load_creds_from_env_file(file_path: Path) -> tuple[str | None, str | None]:
    if not file_path.exists():
        return None, None
    username: str | None = None
    password: str | None = None
    for raw_line in file_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key == "TOP_ACADEMY_USERNAME":
            username = value
        elif key == "TOP_ACADEMY_PASSWORD":
            password = value
    return username, password


def save_creds_to_env_file(file_path: Path, username: str, password: str) -> None:
    file_path.write_text(
        "\n".join(
            [
                "# Автогенерация top_academy_homework_draft_bot.py",
                f"TOP_ACADEMY_USERNAME={username}",
                f"TOP_ACADEMY_PASSWORD={password}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def resolve_credentials(args: argparse.Namespace) -> tuple[str, str]:
    file_username, file_password = load_creds_from_env_file(Path(args.creds_file))
    username = args.username or file_username
    password = args.password or file_password

    if not username and not args.no_prompt:
        username = input("Логин Top Academy: ").strip()
    if not password and not args.no_prompt:
        password = getpass.getpass("Пароль Top Academy: ")

    if not username or not password:
        raise ValueError(
            "Не удалось получить логин/пароль. Передайте --username/--password "
            "или создайте файл --creds-file."
        )

    if args.save_creds:
        save_creds_to_env_file(Path(args.creds_file), username, password)
        print(f"✅ Учетные данные сохранены в {args.creds_file}")

    return username, password


def first_existing(driver: WebDriver, selectors: Sequence[str], timeout: int = 8):
    last_exc: Exception | None = None
    for selector in selectors:
        try:
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
        except Exception as exc:  # noqa: BLE001 - соберем последнюю ошибку
            last_exc = exc
    raise TimeoutException(f"Элемент не найден. Селекторы: {selectors}") from last_exc


def find_all_links(driver: WebDriver, selectors: Iterable[str]) -> list[str]:
    links: set[str] = set()
    for selector in selectors:
        for elem in driver.find_elements(By.CSS_SELECTOR, selector):
            href = elem.get_attribute("href")
            if href and "homework" in href:
                links.add(href)
    return sorted(links)


def set_value_by_selectors(driver: WebDriver, selectors: Sequence[str], value: str) -> bool:
    for selector in selectors:
        try:
            elem = driver.find_element(By.CSS_SELECTOR, selector)
            elem.clear()
            elem.send_keys(value)
            return True
        except NoSuchElementException:
            continue
    return False


def set_stars(driver: WebDriver, stars: int) -> bool:
    stars = max(1, min(stars, 5))
    candidate_selectors = [
        f"input[type='radio'][value='{stars}']",
        f"input[name*='star'][value='{stars}']",
        f"input[name*='rating'][value='{stars}']",
        f".star:nth-child({stars}) input",
    ]
    for selector in candidate_selectors:
        try:
            elem = driver.find_element(By.CSS_SELECTOR, selector)
            driver.execute_script("arguments[0].click();", elem)
            return True
        except NoSuchElementException:
            continue
    return False


def login(driver: WebDriver, username: str, password: str) -> None:
    driver.get(BASE_URL)
    user_input = first_existing(driver, LOGIN_SELECTORS)
    pass_input = first_existing(driver, PASSWORD_SELECTORS)
    user_input.clear()
    user_input.send_keys(username)
    pass_input.clear()
    pass_input.send_keys(password)
    login_btn = first_existing(driver, LOGIN_BUTTON_SELECTORS)
    login_btn.click()
    WebDriverWait(driver, 12).until(EC.url_contains("/main/homework"))


def submit_homework(driver: WebDriver, url: str, payload: HomeworkPayload, auto_submit: bool) -> None:
    print(f"\n➡ Обрабатываю: {url}")
    driver.get(url)
    time.sleep(1)

    github_ok = set_value_by_selectors(driver, GITHUB_FIELD_SELECTORS, payload.github_url)
    stars_ok = set_stars(driver, payload.stars)
    time_ok = set_value_by_selectors(driver, TIME_FIELD_SELECTORS, payload.duration_text)
    comment_ok = set_value_by_selectors(driver, COMMENT_FIELD_SELECTORS, payload.comment)

    print(
        "   Заполнено:"
        f" github={'OK' if github_ok else 'нет'},"
        f" stars={'OK' if stars_ok else 'нет'},"
        f" time={'OK' if time_ok else 'нет'},"
        f" comment={'OK' if comment_ok else 'нет'}"
    )

    if not auto_submit:
        answer = input("   Отправить это задание? [y/N]: ").strip().lower()
        if answer != "y":
            print("   Пропускаю отправку.")
            return

    submit_btn = first_existing(driver, SUBMIT_BUTTON_SELECTORS)
    driver.execute_script("arguments[0].click();", submit_btn)
    print("   ✅ Отправлено")
    time.sleep(1)


def main() -> int:
    args = parse_args()
    try:
        username, password = resolve_credentials(args)
    except ValueError as exc:
        print(f"Ошибка: {exc}")
        return 2

    payload = HomeworkPayload(
        github_url=args.github_url,
        duration_text=f"{args.hours:02d}:{args.minutes:02d}",
        comment=args.comment,
        stars=args.stars,
    )

    options = ChromeOptions()
    if args.headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1400,1000")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2)

    try:
        login(driver, username, password)
        print("✅ Вход выполнен")

        homework_links = find_all_links(driver, HOMEWORK_LINK_SELECTORS)
        if not homework_links:
            print("Не найдены ссылки на домашние задания. Проверьте селекторы.")
            return 1

        if args.max_homeworks > 0:
            homework_links = homework_links[: args.max_homeworks]

        print(f"Найдено домашних заданий: {len(homework_links)}")

        for link in homework_links:
            submit_homework(driver, link, payload, auto_submit=args.auto_submit)

        print("\nГотово.")
        return 0
    finally:
        driver.quit()


if __name__ == "__main__":
    raise SystemExit(main())
