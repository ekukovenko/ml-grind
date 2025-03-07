from typing import List, Union
from time import sleep, time
from abc import ABC, abstractmethod

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from item import Item


class Parser(ABC):
    @abstractmethod
    def get_product_list(self) -> List[Item]:
        pass

    @staticmethod
    def get_page_content(url: str,
                         scroll: bool = False,
                         scroll_timeout: Union[int, float] = 0.3,
                         scroll_duration: int = 500) -> list[str]:
        options = Options()
        options.add_argument("window-size=1920,1080")
        service = Service(ChromeDriverManager().install())

        all_content = []

        with (webdriver.Chrome(service=service, options=options) as driver):
            driver.get(url)

            if scroll:
                end_time = time() + scroll_duration
                while time() < end_time:
                    driver.execute_script("window.scrollBy(0, 1000);")
                    sleep(scroll_timeout)

            all_content.append(driver.page_source)

        return all_content
