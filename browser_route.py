from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from webdriver_manager.chrome import ChromeDriverManager


from time import sleep

import os


class Browser:
    def __init__(self, url: str) -> None:

        self.url = url

    def create_driver(self):
        
        """Create ChromeDriver with applicable options"""

        user = os.getlogin()

        s = Service(ChromeDriverManager(log_level=1).install())

        chrome_options = Options()
        chrome_options.add_argument(
            fr"user-data-dir=C:\Users\{user}\AppData\Local\Google\Chrome\User Data" 
        ) #retrieves current users login info, so it points to their phone
        chrome_options.add_argument('--log-level=3') #hide verbose logs

        driver = webdriver.Chrome(service=s, options=chrome_options)

        return driver

    def open_browser(self, driver: webdriver.Chrome):
        
        """Open browser with specified URL"""

        driver.get(f"https://www.google.com/maps/dir/{self.url}")

    def send_to_phone(self, driver: webdriver.Chrome):
        
        """Sends google map route directly to phone. Should be switched to walk mode when received."""

        send_to_phone = driver.find_element_by_xpath(
            '//*[@id="pane"]/div/div[1]/div/div/div[3]/div[1]/div[2]/button'
        )

        driver.execute_script("arguments[0].click();", send_to_phone)

        driver.implicitly_wait(3)

        send_phone_direct = driver.find_element_by_class_name(
            "lRsTH-Tswv1b-JIbuQc-LgbsSe"
        )

        send_phone_direct.click()

    def quit_driver(self, driver: webdriver.Chrome):
        
        """Quit Chrome Browser"""

        sleep(3)
        driver.implicitly_wait(3)
        driver.quit()

    def main(self):
        driver = self.create_driver()
        self.open_browser(driver)
        self.send_to_phone(driver)
        self.quit_driver(driver)
