# Импорт класса SbisPage для взаимодействия со страницей СБИС
from pages.sbis_page import SbisPage
# Импорт функции логирования результатов assert из файла conftest
from conftest import log_assert_result


def test_change_region_and_verify(browser):
    # Тест для проверки изменения региона и верификации списка партнеров
    browser.get("https://sbis.ru/")  # Открывает главную страницу сайта СБИС

    # Инициализация страницы СБИС с использованием фикстуры browser
    sbis_page = SbisPage(browser)
    sbis_page.go_to_contacts()  # Выполняет переход в раздел "Контакты" на сайте СБИС

    # Получает текущий регион и список партнеров
    current_region = sbis_page.get_region()  # Получает текст текущего региона
    partners_list_before = sbis_page.get_partners_list()  # Получает список партнеров в текущем регионе

    # Проверяет, что текущий регион "Ярославская обл."
    log_assert_result("Ярославская обл." in current_region,
                      f"Регион '{current_region}' совпал с 'Ярославская обл.'",  # Успех
                      f"Регион '{current_region}' не совпал с 'Ярославская обл.'")  # Провал
    assert "Ярославская обл." in current_region  # Проверка, если регион не совпадает — тест падает

    # Проверяет, что список партнеров не пуст
    log_assert_result(len(partners_list_before) > 0,
                      f"Получен список партнеров - ({len(partners_list_before)}) {partners_list_before}!",  # Успех
                      f"Cписок партнеров не получен, либо пустой!")  # Провал
    assert len(partners_list_before) > 0  # Проверка, если список пуст — тест падает

    # Изменяет регион на "Камчатский край"
    sbis_page.change_region("41 Камчатский край")

    # Получает новый регион и обновленный список партнеров
    current_region = sbis_page.get_region()  # Получает текст нового региона после изменения
    partners_list_after = sbis_page.get_partners_list()  # Получает новый список партнеров в измененном регионе

    # Проверяет, что регион изменился на "Камчатский край"
    log_assert_result("Камчатский край" in current_region,
                      f"Регион изменен на '{current_region}' и совпадает с 'Камчатский край'!",  # Успех
                      f"Регион изменен на '{current_region}' и не совпадает с 'Камчатский край'!")  # Провал
    assert "Камчатский край" in current_region  # Проверка, если регион не совпадает — тест падает

    # Проверяет, что список партнеров изменился после смены региона
    log_assert_result(partners_list_before != partners_list_after,
                      f"Лист партнеров изменен на '{partners_list_after}'!",  # Успех
                      f"Лист партнеров не изменился - '{partners_list_after}'")  # Провал
    assert partners_list_before != partners_list_after  # Проверка, если списки совпадают — тест падает

    # Проверяет, что URL страницы содержит '41-kamchatskij-kraj', соответствующий новому региону
    log_assert_result("41-kamchatskij-kraj" in browser.current_url,
                      f"Ссылка изменена и содержит '41-kamchatskij-kraj' - {browser.current_url}!",  # Успех
                      f"Ссылка не корректно изменена и не содержит '41-kamchatskij-kraj' - {browser.current_url}!")  # Провал
    assert "41-kamchatskij-kraj" in browser.current_url  # Проверка, если URL не содержит ожидание — тест падает

    # Проверяет, что заголовок страницы (title) содержит текст "Камчатский край"
    log_assert_result("Камчатский край" in browser.title,
                      f"Регион 'Камчатский край' отобразился в titel - {browser.title}",  # Успех
                      f"Регион 'Камчатский край' не отобразился в titel - {browser.title}")  # Провал
    assert "Камчатский край" in browser.title  # Проверка, если заголовок не содержит регион — тест падает

