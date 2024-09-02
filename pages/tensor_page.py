from .base_page import BasePage  # Импорт базового класса BasePage, содержащего общие методы для работы с веб-страницами
from selenium.webdriver.common.by import By  # Импорт класса By, используемого для локаторов элементов
from typing import List, Tuple  # Импорт типов данных для аннотаций (список и кортеж)
import time  # Импорт модуля time для использования функции задержки


class TensorPage(BasePage):
    # Определение локаторов элементов на странице
    FORCE_IN_PEOPLE_LOCATOR = (By.XPATH, "//p[contains(text(), 'Сила в людях')]")
    DETAILS_LOCATOR = (By.XPATH, "//div[contains(@class, 'tensor_ru-Index__block4-content')]//a[text()='Подробнее']")
    WORK_SECTION_LOCATOR = (By.XPATH, "//div[contains(@class, 'tensor_ru-container tensor_ru-section tensor_ru-About__block3')]//h2[text()='Работаем']/ancestor::div[contains(@class, 'tensor_ru-container tensor_ru-section tensor_ru-About__block3')]")
    PHOTO_LOCATOR = "img.tensor_ru-About__block3-image"

    def is_power_in_people_block_present(self) -> bool:
        # Прокрутка к элементу "Сила в людях"
        self.scroll_to_element(self.FORCE_IN_PEOPLE_LOCATOR)
        # Проверка, отображается ли элемент на странице
        return self.find_element(self.FORCE_IN_PEOPLE_LOCATOR).is_displayed()

    def click_more_details(self) -> None:
        time.sleep(3)  # Задержка в 3 секунды, чтобы дождаться загрузки элемента
        self.find_element(self.DETAILS_LOCATOR).click()  # Поиск элемента и клик по ссылке "Подробнее"

    def get_timeline_image_sizes(self) -> List[Tuple[str, str]]:
        self.scroll_to_element(self.WORK_SECTION_LOCATOR)  # Прокрутка к секции "Работаем"
        work_section = self.find_element(self.WORK_SECTION_LOCATOR)  # Поиск элемента секции "Работаем"
        images = work_section.find_elements(By.CSS_SELECTOR, self.PHOTO_LOCATOR)  # Поиск всех изображений внутри секции
        # Возвращает список размеров изображений (ширина, высота)
        return [(img.get_attribute("width"), img.get_attribute("height")) for img in images]

    def scroll_to_element(self, locator: Tuple[str, str]) -> None:
        element = self.find_element(locator)  # Поиск элемента по переданному локатору
        self.driver.execute_script("arguments[0].scrollIntoView();", element)  # Выполнение JavaScript для прокрутки к элементу
