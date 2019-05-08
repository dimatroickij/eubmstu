import os
import platform
from telnetlib import EC

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from eubmstu.settings import BASE_DIR


class getDataEU:
    # Инициализация класса
    def __init__(self, username, password, teacher, vpn):
        self.options = webdriver.ChromeOptions()
        if platform.system() == 'Linux':
            display = Display(visible=0, size=(1920, 1080))
            display.start()
            self.driver = webdriver.Chrome(os.path.join(BASE_DIR, 'chromedriver'), 0, self.options)
        elif platform.system() == 'Windows':
            self.driver = webdriver.Chrome(os.path.join(BASE_DIR, 'chromedriver.exe'), 0, self.options)
        self.username = username
        self.password = password
        self.teacher = teacher
        self.vpn = vpn
        if vpn:
            self.linkProgress = 'https://webvpn.bmstu.ru/+CSCO+1h75676763663A2F2F72682E6F7A6667682E6568++/modules/progress3/'
            self.linkSession = 'https://webvpn.bmstu.ru/+CSCO+1h75676763663A2F2F72682E6F7A6667682E6568++/modules/session/'
        else:
            self.linkProgress = 'https://eu.bmstu.ru/modules/progress3/'
            self.linkSession = 'https://eu.bmstu.ru/modules/session/'
        self.isLogin = False

    # Авторизация на сайте
    def login(self):
        if self.vpn:
            self.driver.get("https://webvpn.bmstu.ru/+CSCOE+/logon.html")
            self.driver.find_element(By.NAME, 'username').send_keys(self.username)
            self.driver.find_element(By.NAME, 'password').send_keys(self.password)
            self.driver.find_element(By.NAME, 'Login').click()
            element = WebDriverWait(self.driver, 30).until(
                EC.title_is("BMSTU Remote Access"))
            self.driver.execute_script(
                "parent.doURL('75676763663A2F2F72682E6F7A6667682E6568',[{ 'l' : '4829322D03D1606FB09AE9AF59A271D3', 'n' : 1}],'get',false,'no', false)")
        else:
            self.driver.get("http://eu.bmstu.ru")
        if self.teacher:
            self.driver.find_element(By.NAME, 'login').send_keys(self.username)
            self.driver.find_element(By.NAME, 'password').send_keys(self.password)
            self.driver.find_element(By.NAME, 'send').click()
        else:
            element = WebDriverWait(self.driver, 30).until(
                EC.title_is('НОЦ "ЭУ" Авторизация'))
            self.driver.get(
                self.driver.find_element(By.XPATH, "//div[@class='auth-ais-container']//dl//dt/a").get_attribute(
                    'href'))
            self.driver.find_element(By.NAME, 'username').send_keys(self.username)
            self.driver.find_element(By.NAME, 'password').send_keys(self.password)
            self.driver.find_element(By.NAME, 'submit').click()
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.ID, 'workarea')))
        self.isLogin = True
        # except Exception as e:
        #     print(str(e))
        # self.driver.quit()
