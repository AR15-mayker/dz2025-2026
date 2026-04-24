#!/usr/bin/env python3
"""Playwright-скрипт для работы с домашками Top Academy.

Скрипт:
- авторизуется;
- открывает список ДЗ;
- заполняет поля (GitHub, звезды, время, комментарий);
- по умолчанию спрашивает подтверждение перед отправкой.
"""

from __future__ import annotations

import argparse
import getpass
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from playwright.sync_api import BrowserContext, Page, TimeoutError, sync_playwright

BASE_URL = "https://journal.top-academy.ru/ru/main/homework/page/index"
DEFAULT_CREDS_FILE = Path(__file__).with_name(".top_academy_credentials.env")

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
    parser = argparse.ArgumentParser(description="Playwright-автозаполнение домашек Top Academy")
    parser.add_argument("--username", default=os.getenv("TOP_ACADEMY_USERNAME"), help="Логин")
    parser.add_argument("--password", default=os.getenv("TOP_ACADEMY_PASSWORD"), help="Пароль")
    parser.add_argument(
        "--creds-file",
        default=str(DEFAULT_CREDS_FILE),
        help="Файл с сохраненными данными входа (формат .env)",
    )
    parser.add_argument("--save-creds", action="store_true", help="Сохранить логин/пароль в --creds-file")
    parser.add_argument("--no-prompt", action="store_true", help="Не спрашивать логин/пароль в интерактивном режиме")

    parser.add_argument("--github-url", required=True, help="Ссылка на GitHub")
    parser.add_argument("--hours", type=int, default=1, help="Часы")
    parser.add_argument("--minutes", type=int, default=13, help="Минуты")
    parser.add_argument("--stars", type=int, default=5, help="Звезды (1-5)")
    parser.add_argument("--comment", default="Круто", help="Комментарий")

    parser.add_argument("--headless", action="store_true", help="Режим без UI")
    parser.add_argument("--max-homeworks", type=int, default=0, help="Ограничить число ДЗ (0 = без лимита)")
    parser.add_argument("--auto-submit", action="store_true", help="Отправлять без ручного подтверждения")
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
            "Не удалось получить логин/пароль. Передайте --username/--password или создайте файл --creds-file."
        )

    if args.save_creds:
        save_creds_to_env_file(Path(args.creds_file), username, password)
        print(f"✅ Учетные данные сохранены в {args.creds_file}")

    return username, password


def wait_first_selector(page: Page, selectors: Sequence[str], timeout_ms: int = 8000) -> str:
    for selector in selectors:
        try:
            page.wait_for_selector(selector, timeout=timeout_ms)
            return selector
        except TimeoutError:
            continue
    raise TimeoutError(f"Элемент не найден. Селекторы: {selectors}")


def set_value_by_selectors(page: Page, selectors: Sequence[str], value: str) -> bool:
    for selector in selectors:
        loc = page.locator(selector).first
        if loc.count() > 0:
            loc.fill(value)
            return True
    return False


def click_first(page: Page, selectors: Sequence[str]) -> bool:
    for selector in selectors:
        loc = page.locator(selector).first
        if loc.count() > 0:
            loc.click()
            return True
    return False


def set_stars(page: Page, stars: int) -> bool:
    stars = max(1, min(stars, 5))
    candidate_selectors = [
        f"input[type='radio'][value='{stars}']",
        f"input[name*='star'][value='{stars}']",
        f"input[name*='rating'][value='{stars}']",
        f".star:nth-child({stars}) input",
    ]
    return click_first(page, candidate_selectors)


def find_all_links(page: Page, selectors: Iterable[str]) -> list[str]:
    links: set[str] = set()
    for selector in selectors:
        for element in page.locator(selector).all():
            href = element.get_attribute("href")
            if href and "homework" in href:
                if href.startswith("http"):
                    links.add(href)
                else:
                    links.add(f"https://journal.top-academy.ru{href}")
    return sorted(links)


def login(page: Page, username: str, password: str) -> None:
    page.goto(BASE_URL, wait_until="domcontentloaded")

    if "/main/homework" in page.url and page.locator("input[type='password']").count() == 0:
        print("ℹ️ Уже авторизован, продолжаю.")
        return

    user_selector = wait_first_selector(page, LOGIN_SELECTORS)
    pass_selector = wait_first_selector(page, PASSWORD_SELECTORS)

    page.locator(user_selector).first.fill(username)
    page.locator(pass_selector).first.fill(password)

    if not click_first(page, LOGIN_BUTTON_SELECTORS):
        raise RuntimeError("Не найдена кнопка входа")

    page.wait_for_url("**/main/homework/**", timeout=15000)


def submit_homework(page: Page, url: str, payload: HomeworkPayload, auto_submit: bool) -> None:
    print(f"\n➡ Обрабатываю: {url}")
    page.goto(url, wait_until="domcontentloaded")

    github_ok = set_value_by_selectors(page, GITHUB_FIELD_SELECTORS, payload.github_url)
    stars_ok = set_stars(page, payload.stars)
    time_ok = set_value_by_selectors(page, TIME_FIELD_SELECTORS, payload.duration_text)
    comment_ok = set_value_by_selectors(page, COMMENT_FIELD_SELECTORS, payload.comment)

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

    if not click_first(page, SUBMIT_BUTTON_SELECTORS):
        raise RuntimeError("Кнопка отправки не найдена")
    print("   ✅ Отправлено")


def run(context: BrowserContext, args: argparse.Namespace, payload: HomeworkPayload, username: str, password: str) -> int:
    page = context.new_page()
    login(page, username, password)
    print("✅ Вход выполнен")

    page.goto(BASE_URL, wait_until="domcontentloaded")
    homework_links = find_all_links(page, HOMEWORK_LINK_SELECTORS)
    if not homework_links:
        print("Не найдены ссылки на домашние задания. Проверьте селекторы.")
        return 1

    if args.max_homeworks > 0:
        homework_links = homework_links[: args.max_homeworks]

    print(f"Найдено домашних заданий: {len(homework_links)}")
    for link in homework_links:
        submit_homework(page, link, payload, auto_submit=args.auto_submit)

    print("\nГотово.")
    return 0


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

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=args.headless)
        context = browser.new_context()
        try:
            return run(context, args, payload, username, password)
        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    raise SystemExit(main())
