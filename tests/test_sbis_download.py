from pages.sbis_page import SbisPage  # Импорт класса SbisPage для взаимодействия с элементами страницы СБИС
from conftest import log_assert_result  # Импорт функции логирования результатов assert из файла conftest


# Тест для проверки скачивания плагина СБИС
def test_download_plugin(browser):
    plugin_filename = "sbisplugin-setup-web.exe"  # Имя файла, который ожидается после загрузки

    # Открывает главную страницу сайта СБИС
    browser.get("https://sbis.ru/")
    sbis_page = SbisPage(browser)  # Инициализирует объект страницы СБИС с использованием фикстуры browser

    # Находит в футере и переходит в раздел "Скачать локальные версии"
    sbis_page.navigate_to_local_versions()

    # Выполняет скачивание СБИС Плагина для Windows
    sbis_page.download_plugin()

    # Проверяет, что файл плагина был успешно скачан
    result_file_download = sbis_page.is_file_downloaded(plugin_filename)
    log_assert_result(result_file_download,
                      f"Файл {plugin_filename} скачался",  # Успех
                      f"Файл {plugin_filename} не скачался")  # Провал
    assert result_file_download, "Файл не скачался"  # Проверка, если файл не был найден — тест падает

    # Получает размер скачанного файла в мегабайтах
    downloaded_file_size = sbis_page.get_file_size_in_mb(plugin_filename)
    # Получает ожидаемый размер плагина с сайта
    expected_size = sbis_page.get_plugin_size()

    # Сравнивает размер скачанного файла с размером, указанным на сайте
    log_assert_result(downloaded_file_size == expected_size,
                      f"Размер скачанного файла ({downloaded_file_size} MB) совпадает с указанным на сайте ({expected_size} MB)",
                      f"Размер скачанного файла ({downloaded_file_size} MB) не совпадает с указанным на сайте ({expected_size} MB)")
    assert downloaded_file_size == expected_size, f"Размер скачанного файла ({downloaded_file_size} MB) не совпадает с указанным на сайте ({expected_size} MB)"