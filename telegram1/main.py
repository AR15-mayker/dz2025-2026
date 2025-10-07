from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime
import os
import requests
from loguru import logger
from dotenv import load_dotenv, find_dotenv
import time
from pathlib import Path

# Загружаем переменные окружения
load_dotenv(find_dotenv())

def download_cat_meme():
    """Скачивает мем по указанной ссылке с улучшенной обработкой ошибок"""
    meme_url = "https://smart-lab.ru/uploads/2021/images/04/27/97/2021/12/23/bfd4bb.jpg"
    local_path = "cat_meme.jpg"
    
    if os.path.exists(local_path):
        file_size = os.path.getsize(local_path)
        logger.info(f"✅ Файл мема уже существует: {local_path} ({file_size} байт)")
        return local_path
    
    try:
        logger.info("📥 Скачиваю мем с котиком...")
        response = requests.get(meme_url, timeout=30)
        response.raise_for_status()
        
        with open(local_path, 'wb') as f:
            f.write(response.content)
        
        file_size = len(response.content)
        logger.success(f"✅ Мем скачан: {local_path} ({file_size} байт)")
        return local_path
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Ошибка сети при скачивании мема: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ Неожиданная ошибка при скачивании мема: {e}")
        return None

# Конфигурация
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
HOMEWORK_FILE = download_cat_meme()
REPO_LINK = os.getenv('REPO_LINK', 'https://github.com/your_username/your_repo').strip()

class HomeworkAutomation:
    def __init__(self, page):
        self.page = page
        self.it_keywords = [
            "информацион", "IT", "программирован", "компьютер", 
            "технолог", "информатик", "ИТ", "разработк", "software",
            "coding", "python", "javascript", "web", "сайт"
        ]

    def login_to_site(self):
        """Вход на сайт с улучшенной обработкой ошибок"""
        logger.info("🔐 Начинаю вход в систему...")
        
        try:
            # Загружаем страницу
            self.page.goto("https://journal.top-academy.ru", wait_until="networkidle", timeout=60000)
            logger.info("✅ Главная страница загружена")
            
            # Ждем форму входа
            logger.info("⏳ Ожидаю форму входа...")
            self.page.wait_for_selector('input[name="username"]', timeout=15000)
            
            # Заполняем логин и пароль
            self.page.fill('input[name="username"]', LOGIN)
            logger.info("✅ Логин введен")
            self.page.wait_for_timeout(1000)
            
            self.page.fill('input[name="password"]', PASSWORD)
            logger.info("✅ Пароль введен")
            self.page.wait_for_timeout(1000)
            
            # Кликаем кнопку входа
            self.page.click('button[type="submit"]')
            logger.info("✅ Форма отправлена")
            
            # Ждем загрузки после входа
            self.page.wait_for_timeout(5000)
            
            # Проверяем успешность входа
            current_url = self.page.url
            if any(path in current_url for path in ["/main/", "/dashboard", "/home"]):
                logger.success("✅ Вход успешен")
                return True
            elif self.page.query_selector('input[name="password"]'):
                logger.error("❌ Вход не удался - форма пароля все еще видна")
                return False
            else:
                logger.warning("⚠️ Не удалось точно определить успешность входа, продолжаю...")
                return True
                
        except PlaywrightTimeoutError:
            logger.error("❌ Таймаут при загрузке страницы входа")
            return False
        except Exception as e:
            logger.error(f"❌ Ошибка при входе: {e}")
            return False

    def find_homework_items(self):
        """Поиск домашних заданий с улучшенной логикой"""
        logger.info("📚 Ищу домашние задания...")
        
        try:
            # Ждем загрузки заданий
            self.page.wait_for_selector('.homework-item, [class*="homework"], [class*="assignment"]', timeout=15000)
            
            # Пробуем разные селекторы для заданий
            selectors = [
                '.homework-item',
                '[class*="homework"]',
                '[class*="assignment"]',
                '.task-item',
                '.lesson-item'
            ]
            
            for selector in selectors:
                items = self.page.query_selector_all(selector)
                if items:
                    logger.info(f"✅ Найдено {len(items)} заданий с селектором: {selector}")
                    return items
            
            logger.warning("⚠️ Не найдено заданий с стандартными селекторами")
            return []
            
        except PlaywrightTimeoutError:
            logger.error("❌ Таймаут при загрузке заданий")
            return []
        except Exception as e:
            logger.error(f"❌ Ошибка при поиске заданий: {e}")
            return []

    def is_it_homework(self, item_text):
        """Проверяет, является ли задание ИТ-тематики"""
        item_text_lower = item_text.lower()
        return any(keyword in item_text_lower for keyword in self.it_keywords)

    def wait_for_modal_and_interact(self, homework_item, subject_name):
        """Ожидание модального окна и взаимодействие с ним"""
        try:
            logger.info(f"🔧 Начинаю обработку: {subject_name}")
            
            # Прокручиваем к элементу
            homework_item.scroll_into_view_if_needed()
            self.page.wait_for_timeout(2000)
            
            # Ищем кнопку загрузки с разными селекторами
            upload_selectors = [
                '.upload-file',
                'button:has-text("Загрузить")',
                'button:has-text("Сдать")',
                'button:has-text("Добавить")',
                '[class*="upload"]',
                '[class*="submit"]',
                'a:has-text("Загрузить")'
            ]
            
            upload_button = None
            for selector in upload_selectors:
                upload_button = homework_item.query_selector(selector)
                if upload_button and upload_button.is_visible():
                    break
                self.page.wait_for_timeout(500)
            
            if not upload_button:
                logger.warning(f"⚠️ Кнопка загрузки не найдена для: {subject_name}")
                # Пробуем кликнуть по самой карточке
                try:
                    homework_item.click()
                    logger.info("📤 Кликнул на карточку задания")
                except:
                    return False
            
            else:
                # Кликаем на кнопку
                upload_button.click()
                logger.info("📤 Кликнул на кнопку загрузки")
            
            # Ждем появления модального окна
            self.page.wait_for_timeout(3000)
            
            # Проверяем, открылось ли модальное окно
            modal_indicators = [
                'input[type="file"]',
                'textarea',
                'button[type="submit"]',
                '.modal',
                '[role="dialog"]',
                '.popup',
                '.dialog'
            ]
            
            modal_visible = False
            for indicator in modal_indicators:
                if self.page.query_selector(indicator):
                    modal_visible = True
                    break
            
            if not modal_visible:
                logger.warning("⚠️ Модальное окно не открылось, пробую продолжить...")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка при открытии формы: {e}")
            return False

    def fill_homework_form(self):
        """Заполнение формы домашнего задания с улучшенной логикой"""
        try:
            # 1. Загрузка файла
            file_input = self.page.query_selector('input[type="file"]')
            if file_input and HOMEWORK_FILE and os.path.exists(HOMEWORK_FILE):
                file_input.set_input_files(HOMEWORK_FILE)
                logger.info("🐱 Файл с мемом загружен")
                self.page.wait_for_timeout(2000)
            else:
                logger.warning("⚠️ Поле загрузки файла не найдено или файл отсутствует")

            # 2. Вставка ссылки на репозиторий
            logger.info("🔗 Вставляю ссылку на GitHub...")
            
            # Ищем текстовые поля с разными селекторами
            text_selectors = [
                'textarea',
                'input[type="text"]',
                'input[type="url"]',
                '[placeholder*="ссылка"]',
                '[placeholder*="link"]',
                '[placeholder*="репозиторий"]',
                '[placeholder*="repository"]'
            ]
            
            link_added = False
            for selector in text_selectors:
                fields = self.page.query_selector_all(selector)
                for field in fields:
                    if field.is_visible() and field.is_enabled():
                        try:
                            field.click()
                            field.fill("")  # Очищаем поле
                            field.fill(REPO_LINK)
                            logger.info("✅ Ссылка вставлена")
                            link_added = True
                            break
                        except:
                            continue
                if link_added:
                    break
            
            if not link_added:
                logger.warning("⚠️ Не удалось вставить ссылку")

            # 3. Установка времени
            logger.info("⏰ Устанавливаю время выполнения...")
            current_time = datetime.now()
            hours = current_time.strftime("%H")
            minutes = current_time.strftime("%M")
            
            # Ищем поля для времени по плейсхолдерам
            time_selectors = [
                '[placeholder*="чч"]',
                '[placeholder*="hh"]',
                '[placeholder*="час"]',
                '[placeholder*="hour"]',
                '[placeholder*="мм"]',
                '[placeholder*="mm"]',
                '[placeholder*="мин"]',
                '[placeholder*="min"]'
            ]
            
            time_set = False
            for selector in time_selectors:
                time_fields = self.page.query_selector_all(selector)
                for field in time_fields:
                    placeholder = field.get_attribute('placeholder', '').lower()
                    if any(word in placeholder for word in ['чч', 'hh', 'час', 'hour']):
                        field.fill(hours)
                        logger.info(f"✅ Часы установлены: {hours}")
                        time_set = True
                    elif any(word in placeholder for word in ['мм', 'mm', 'мин', 'min']):
                        field.fill(minutes)
                        logger.info(f"✅ Минуты установлены: {minutes}")
                        time_set = True
            
            if not time_set:
                logger.info("⏰ Поля времени не найдены по плейсхолдерам, пропускаю...")

            # 4. Установка 5 звезд
            logger.info("⭐ Устанавливаю 5 звезд...")
            
            # Пробуем разные способы установки рейтинга
            stars_set = self._set_rating()
            
            if not stars_set:
                logger.info("⭐ Не удалось установить звезды, пропускаю...")

            # 5. Отправка формы
            return self._submit_form()

        except Exception as e:
            logger.error(f"❌ Ошибка при заполнении формы: {e}")
            return False

    def _set_rating(self):
        """Внутренний метод для установки рейтинга"""
        # Способ 1: Радио-кнопки (5 из 5)
        radio_buttons = self.page.query_selector_all('input[type="radio"]')
        if len(radio_buttons) >= 5:
            try:
                radio_buttons[4].click()
                logger.info("✅ 5 звезд установлено (радио-кнопки)")
                return True
            except:
                pass
        
        # Способ 2: Элементы звезд
        star_selectors = ['.star', '[class*="star"]', '[class*="rating"]', '[data-rating]']
        for selector in star_selectors:
            stars = self.page.query_selector_all(selector)
            if len(stars) >= 5:
                try:
                    stars[4].click()
                    logger.info("✅ 5 звезд установлено (элементы звезд)")
                    return True
                except:
                    continue
        
        # Способ 3: Текст "5"
        five_selectors = ['text="5"', 'button:has-text("5")', 'div:has-text("5")']
        for selector in five_selectors:
            five_element = self.page.query_selector(selector)
            if five_element:
                try:
                    five_element.click()
                    logger.info("✅ 5 звезд установлено (текст)")
                    return True
                except:
                    continue
        
        return False

    def _submit_form(self):
        """Внутренний метод для отправки формы"""
        logger.info("📨 Отправляю задание...")
        
        # Прокручиваем вниз для поиска кнопки
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(1000)
        
        # Ищем кнопку отправки
        submit_selectors = [
            'button[type="submit"]',
            'button:has-text("Отправить")',
            'button:has-text("Сдать")',
            'button:has-text("Сохранить")',
            'button:has-text("Загрузить")',
            '.btn-primary',
            '.btn-success',
            '.submit-btn',
            '.save-btn'
        ]
        
        for selector in submit_selectors:
            submit_btn = self.page.query_selector(selector)
            if submit_btn and submit_btn.is_visible() and submit_btn.is_enabled():
                try:
                    submit_btn.click()
                    logger.success("✅ Задание отправлено!")
                    self.page.wait_for_timeout(3000)
                    return True
                except Exception as e:
                    logger.warning(f"⚠️ Не удалось кликнуть на кнопку {selector}: {e}")
                    # Пробуем через JavaScript
                    try:
                        self.page.evaluate("arguments[0].click()", submit_btn)
                        logger.success("✅ Задание отправлено (через JS)!")
                        self.page.wait_for_timeout(3000)
                        return True
                    except:
                        continue
        
        logger.error("❌ Не удалось отправить задание")
        return False

    def process_homework(self, homework_item, subject_name):
        """Обработка одного домашнего задания"""
        try:
            # Открываем модальное окно
            if not self.wait_for_modal_and_interact(homework_item, subject_name):
                return False
            
            # Заполняем форму
            if not self.fill_homework_form():
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка при обработке задания {subject_name}: {e}")
            return False

    def process_all_it_homeworks(self):
        """Обработка всех ИТ-заданий"""
        homework_items = self.find_homework_items()
        processed_count = 0

        for i, homework_item in enumerate(homework_items, 1):
            try:
                # Проверяем, является ли задание ИТ-тематики
                item_text = homework_item.inner_text()
                if not self.is_it_homework(item_text):
                    continue

                # Получаем название предмета
                subject_element = homework_item.query_selector('.name-spec, .subject, .title, h3, h4')
                subject_name = subject_element.inner_text().strip() if subject_element else f"ИТ задание #{i}"
                
                logger.info(f"🎯 Найдено ИТ-задание: {subject_name}")

                # Обрабатываем задание
                if self.process_homework(homework_item, subject_name):
                    processed_count += 1
                    logger.info(f"📊 Успешно обработано заданий: {processed_count}")
                
                # Пауза между заданиями
                self.page.wait_for_timeout(3000)

            except Exception as e:
                logger.error(f"❌ Ошибка при обработке задания {i}: {e}")
                continue

        return processed_count

def submit_it_homework():
    """Основная функция для отправки домашних заданий"""
    if not all([LOGIN, PASSWORD]):
        logger.error("❌ Не указаны LOGIN или PASSWORD в файле .env")
        return False

    if not HOMEWORK_FILE or not os.path.exists(HOMEWORK_FILE):
        logger.error("❌ Не удалось скачать файл с мемом")
        return False

    try:
        with sync_playwright() as p:
            # Запускаем браузер
            browser = p.chromium.launch(
                headless=False,
                args=['--start-maximized']
            )
            context = browser.new_context(viewport=None)  # Полноэкранный режим
            page = context.new_page()
            
            # Устанавливаем таймауты
            page.set_default_timeout(30000)

            # Инициализируем автомат
            automation = HomeworkAutomation(page)

            # 1. Вход на сайт
            if not automation.login_to_site():
                logger.error("❌ Не удалось войти на сайт")
                browser.close()
                return False

            # 2. Переход к домашним заданиям
            logger.info("📚 Перехожу к домашним заданиям...")
            try:
                page.goto("https://journal.top-academy.ru/main/homework/page/index", wait_until="networkidle", timeout=30000)
                logger.info("✅ Страница заданий загружена")
            except Exception as e:
                logger.error(f"❌ Ошибка загрузки страницы заданий: {e}")
                browser.close()
                return False

            # 3. Поиск и обработка ИТ-заданий
            processed_count = automation.process_all_it_homeworks()

            logger.info(f"🎉 Работа завершена! Всего обработано: {processed_count} заданий")
            
            if processed_count == 0:
                logger.info("💡 Совет: Проверьте селекторы и ключевые слова для поиска ИТ-заданий")
            
            # Закрытие браузера
            input("Нажмите Enter для закрытия браузера...")
            browser.close()
            return processed_count > 0

    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        return False

if __name__ == "__main__":
    # Настройка логирования
    logger.add(
        "homework_uploader.log",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        rotation="10 MB",
        retention="3 days",
        backtrace=True,
        diagnose=True
    )
    
    logger.info("🚀 Запускаю программу...")
    success = submit_it_homework()
    
    if success:
        logger.success("✅ Программа завершила работу успешно!")
    else:
        logger.error("❌ Программа завершила работу с ошибками!")