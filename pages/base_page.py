# Импорт класса WebDriverWait из модуля selenium для ожидания
from selenium.webdriver.support.ui import WebDriverWait
# Импорт модуля expected_conditions с условными выражениями для ожиданий
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        # Конструктор класса, принимающий веб-драйвер в качестве аргумента и сохраняющий его в экземпляре класса
        self.driver = driver

    def find_element(self, locator, time=10):
        # Ожидание появления элемента в DOM
        # Возвращает найденный элемент
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator))

    def find_element_visibility(self, locator, time=10):
        # Ожидание того, что элемент станет видимым
        # Возвращает видимый элемент
        return WebDriverWait(self.driver, time).until(EC.visibility_of_element_located(locator))

    def find_element_clickable(self, locator, time=10):
        # Ожидание того, что элемент станет кликабельным
        # Возвращает кликабельный элемент
        return WebDriverWait(self.driver, time).until(EC.element_to_be_clickable(locator))

    def find_elements(self, locator, time=10):
        # Ожидание появления всех элементов по заданному локатору
        # Возвращает список найденных элементов
        return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator))

    def find_elements_visibility(self, locator, time=10):
        # Ожидание того, что все элементы по заданному локатору станут видимыми
        # Возвращает список видимых элементов
        return WebDriverWait(self.driver, time).until(EC.visibility_of_all_elements_located(locator))

    def wait_for_change(self, locator, expected_region, time=10):
        # Ожидание того, что текст в элементе по локатору станет равным ожидаемому значению
        WebDriverWait(self.driver, time).until(EC.text_to_be_present_in_element(locator, expected_region))
        return  # Возврат из функции (здесь он фактически ничего не возвращает)
