import logging  # Модуль для логирования
import os  # Для работы с файловой системой
import pytest  # Модуль для написания тестов
from selenium import webdriver  # Импорт библиотеки Selenium для управления браузерами
from selenium.webdriver.chrome.service import Service  # Импорт класса Service для управления службой ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager  # Импорт менеджера для автоматической установки ChromeDriver


# Настройка логирования в файл 'test_results.log'
logging.basicConfig(filename='logs/test_results.log',  # Имя файла для сохранения логов
                    level=logging.INFO,  # Уровень логирования (информационные сообщения и ошибки)
                    format='%(asctime)s - %(levelname)s - %(message)s')  # Формат лог-сообщений
logging.info('\n\n---------------------------------------------\n')  # Начальная строка в лог-файл для разделения запусков


# Декоратор pytest для определения фикстуры с областью видимости на каждый тест (function)
@pytest.fixture(scope="function")
def browser():
    options = webdriver.ChromeOptions()  # Создание объекта с настройками Chrome
    options.add_argument('--no-sandbox')  # Отключение sandbox для Chrome
    options.add_argument('--disable-dev-shm-usage')  # Отключение использования /dev/shm в Chrome (увеличивает доступную память)
    options.add_experimental_option('prefs', {
        # Опции для управления настройками загрузок и безопасностью в Chrome
        "download.default_directory": os.getcwd(),  # Установка текущего рабочего каталога как директории для загрузок
        "download.prompt_for_download": False,  # Отключение запросов перед загрузкой
        "safebrowsing.enabled": True,  # Включение безопасного просмотра (по умолчанию True)
        "safebrowsing.disable_download_protection": True  # Отключение защиты от вредоносных загрузок (может быть небезопасно)
    })
    # Создание объекта службы для ChromeDriver с помощью ChromeDriverManager для автоматической установки драйвера
    service = Service(ChromeDriverManager().install())
    # Инициализация WebDriver Chrome с заданными опциями и службой
    driver = webdriver.Chrome(options=options, service=service)
    driver.implicitly_wait(10)  # Установка неявного ожидания (10 секунд) для поиска элементов
    yield driver  # Возвращает объект драйвера для использования в тестах
    driver.quit()  # Закрывает браузер после завершения теста


def log_assert_result(result: bool, message_done: str, message_failed: str) -> None:
    # Если результат assert положительный, записывает сообщение об успехе в лог
    if result:
        logging.info(f"Успех! {message_done}")
    else:
        logging.error(message_failed)