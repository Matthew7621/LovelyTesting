# Импорт модуля time для работы с временем (например, для паузы с помощью sleep)
import time
# Импорт модуля os для работы с файловой системой
import os
# Импорт базового класса BasePage из файла base_page.py в текущей директории
from .base_page import BasePage
# Импорт класса By для использования различных стратегий поиска элементов
from selenium.webdriver.common.by import By


class SbisPage(BasePage):
    # Определение локаторов элементов веб-страницы для взаимодействия с ними
    CONTACTS_LOCATOR = (By.XPATH, "//a[contains(@href, '/contacts')]")
    TENSOR_BANNER_LOCATOR = (By.XPATH, "//img[contains(@alt, 'Разработчик системы СБИС — компания «Тензор»')]")

    REGION_LABEL_LOCATOR = (By.CSS_SELECTOR, "span.sbis_ru-Region-Chooser__text.sbis_ru-link")
    PARTNERS_LIST_LOCATOR = (By.CSS_SELECTOR, '.sbisru-Contacts-List__name')

    LOCAL_VERSIONS_LINK_LOCATOR = (By.LINK_TEXT, "Скачать локальные версии")
    PLUGIN_LINK_LOCATOR = (By.XPATH, '//div[contains(@class, "controls-TabButton__caption") and contains(text(), "СБИС Плагин")]')
    PAGE_WINDOWS_LOCATOR = (By.CSS_SELECTOR, 'span.sbis_ru-DownloadNew-innerTabs__title--default')
    WEB_INSTALLER_LINK_LOCATOR = (By.XPATH, '//h3[contains(text(), "Веб-установщик")]/ancestor::div[contains(@class, "sbis_ru-DownloadNew-flex")]/descendant::a[contains(@class, "sbis_ru-DownloadNew-loadLink__link")]')
    PLUGIN_SIZE_LOCATOR = (By.XPATH, '//h3[contains(text(), "Веб-установщик")]/ancestor::div[contains(@class, "sbis_ru-DownloadNew-flex")]/descendant::a[contains(@class, "sbis_ru-DownloadNew-loadLink__link")]')

    def go_to_contacts(self) -> None:
        # Находит элемент ссылки "Контакты", ожидая, пока он станет видимым, и выполняет клик по нему
        self.find_element_visibility(self.CONTACTS_LOCATOR).click()

    def click_tensor_banner(self) -> None:
        # Находит баннер "Тензор", ожидая, пока он станет видимым, и выполняет клик по нему
        self.find_element_visibility(self.TENSOR_BANNER_LOCATOR).click()

    def get_region(self) -> str:
        # Находит элемент региона, ожидая, пока он станет видимым, и возвращает его текст
        region_element = self.find_element_visibility(self.REGION_LABEL_LOCATOR)
        return region_element.text

    def get_partners_list(self) -> list:
        # Находит все элементы списка партнеров, ожидая, пока они станут видимыми, и возвращает их текст в виде списка
        partners_elements = self.find_elements_visibility(self.PARTNERS_LIST_LOCATOR)
        # Извлекает текст каждого элемента и сохраняет в список
        partners_texts = [element.text for element in partners_elements]
        return partners_texts

    def change_region(self, region: str) -> None:
        # Находит элемент региона и кликает по нему для вызова панели выбора региона
        self.find_element(self.REGION_LABEL_LOCATOR).click()
        time.sleep(2)  # Ждет 2 секунды для загрузки панели
        # Определяет локатор нужного региона
        REGION_ITEM = (By.XPATH, f'//li[@class="sbis_ru-Region-Panel__item"]//span[text()="{region}"]')
        self.find_element_clickable(REGION_ITEM).click()  # Находит и кликает по нужному региону
        region_without_number = ' '.join(region.split(' ')[1:])  # Убирает номер региона из строки для точного сравнения
        # Ждет, пока текст текущего региона изменится на новый
        self.wait_for_change(self.REGION_LABEL_LOCATOR, region_without_number)

    def navigate_to_local_versions(self) -> None:
        # Находит ссылку на "Скачать локальные версии", ожидая, пока она станет кликабельной
        footer_link = self.find_element_clickable(self.LOCAL_VERSIONS_LINK_LOCATOR)
        # Скроллит страницу до этой ссылки
        self.driver.execute_script("arguments[0].scrollIntoView(true);", footer_link)
        footer_link.click()  # Собственно сам клик

    def download_plugin(self) -> None:
        # Находит ссылку на плагин, ожидая, пока она станет видимой, и кликает по ней
        plugin_link = self.find_element_visibility(self.PLUGIN_LINK_LOCATOR)
        plugin_link.click()
        # Находит элемент для выбора платформы Windows и кликает по нему
        self.find_element_clickable(self.PAGE_WINDOWS_LOCATOR).click()
        # Находит ссылку на веб-установщик и кликает по ней
        self.find_element_clickable(self.WEB_INSTALLER_LINK_LOCATOR).click()
        time.sleep(7)  # Для скачивания

    def get_plugin_size(self) -> float:
        # Находит элемент размера плагина, ожидая, пока он станет кликабельным, и получает его текст
        size_text = self.find_element_clickable(self.PLUGIN_SIZE_LOCATOR).text
        # Извлекает размер в МБ из текста и преобразует в тип float
        size_in_mb = size_text.split('(')[-1].split()[1].replace('МБ', '').replace(',', '.')
        return float(size_in_mb)

    def is_file_downloaded(self, filename: str) -> bool:
        # Получает путь к файлу в текущей директории и проверяет, существует ли файл
        file_path = os.path.join(os.getcwd(), filename)
        return os.path.isfile(file_path)

    def get_file_size_in_mb(self, filepath: str) -> float:
        # Получает размер файла в байтах и преобразует в МБ, округляя до 2 знаков после запятой
        size_in_bytes = os.path.getsize(filepath)
        size_in_mb = size_in_bytes / (1024 * 1024)
        return round(size_in_mb, 2)

