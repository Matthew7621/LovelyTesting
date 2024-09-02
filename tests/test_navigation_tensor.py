from pages.sbis_page import SbisPage  # Импорт класса SbisPage для взаимодействия со страницей СБИС
from pages.tensor_page import TensorPage  # Импорт класса TensorPage для взаимодействия со страницей Тензор
from conftest import log_assert_result  # Импорт функции логирования результатов assert из файла conftest
import time  # Импорт модуля time для работы с временными задержками


def test_tensor_navigation(browser):
    # Тест для проверки навигации и элементов на странице Тензор
    browser.get("https://sbis.ru/")  # Открывает главную страницу сайта СБИС

    # Инициализация страницы СБИС с использованием фикстуры browser
    sbis_page = SbisPage(browser)
    sbis_page.go_to_contacts()  # Выполняет переход в раздел "Контакты" на сайте СБИС

    # Кликает на баннер "Тензор" на странице "Контакты"
    sbis_page.click_tensor_banner()

    # Переключается на новую вкладку браузера, открывшуюся после клика
    browser.switch_to.window(browser.window_handles[1])

    # Инициализация страницы Тензор с использованием браузера
    tensor_page = TensorPage(browser)
    time.sleep(3)  # Ожидание 3 секунды для загрузки содержимого страницы

    # Проверяет наличие блока "Сила в людях" на странице Тензор
    result_block_power_in_people = tensor_page.is_power_in_people_block_present()
    log_assert_result(result_block_power_in_people,
                      f"Блок 'Сила в людях' найден!",  # Успех
                      f"Блок 'Сила в людях' не найден!")  # Провал
    # Проверка условия, если не найден — тест падает
    assert result_block_power_in_people, "Блок 'Сила в людях' не найден"

    # Кликает по кнопке "Подробнее" в блоке "Сила в людях"
    tensor_page.click_more_details()

    # Проверяет, что текущий URL совпадает с ожидаемым URL "https://tensor.ru/about"
    log_assert_result(browser.current_url == "https://tensor.ru/about",
                      f"URL совпал: '{browser.current_url}' == 'https://tensor.ru/about'",  # Успех
                      f"URL не соответствует ожиданиям {browser.current_url} != 'https://tensor.ru/about'")  # Провал
    # Проверка, если URL не совпадает — тест падает
    assert browser.current_url == "https://tensor.ru/about", "URL не соответствует ожиданиям"

    # Получает размеры всех изображений хронологии на странице
    image_sizes = tensor_page.get_timeline_image_sizes()

    # Проверяет, что все изображения хронологии имеют одинаковые размеры
    result_image_sizes = all(size == image_sizes[0] for size in image_sizes)  # Проверяет, что все размеры равны первому элементу
    log_assert_result(result_image_sizes,
                      f"Все изображения имеют одинаковые размеры: {image_sizes}!!",  # Успех
                      f"Не все изображения имеют одинаковые размеры: {image_sizes}!")  # Провал
    # Проверка, если размеры не совпадают — тест падает
    assert result_image_sizes, "Не все изображения имеют одинаковые размеры"
