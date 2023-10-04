import json
import random
import time
from os import listdir

import httpx
from selenium import common, webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions

from constants import BING_LOGIN_URL, GECKODRIVER, MSEDGEDRIVER, RANDOM_WORDS_URL
from get_webdriver import save_webdriver


def wait_for(sec=2):
    time.sleep(sec)


def get_driver_firefox(mobile=False):
    profile = webdriver.FirefoxProfile()
    options = FirefoxOptions()
    options.headless = False
    options.add_argument("--disable-notifications")
    if mobile:
        profile.set_preference("general.useragent.override",
                                "Mozilla/5.0 (Android 8.0.0; Mobile; rv:63.0) Gecko/63.0 Firefox/63.0")

    try:
        return webdriver.Firefox(firefox_profile=profile, options=options,
                                 service=FirefoxService(f"{GECKODRIVER}/{listdir(GECKODRIVER)[0]}"))
    except FileNotFoundError:
        save_webdriver(GECKODRIVER)
        return get_driver_firefox(mobile=mobile)


def get_driver_edge(mobile=False, service=False):
    options = EdgeOptions()
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    options.add_argument("--disable-notifications")
    options.add_argument('--disable-gpu')
    if mobile:
        mobile_emulation = {"deviceName": "iPhone X"}
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        options.add_argument('--headless')
    try:
        return webdriver.Edge(options=options,
                              service=EdgeService(f"{MSEDGEDRIVER}/{listdir(MSEDGEDRIVER)[0]}") if service else None)
    except (FileNotFoundError, WebDriverException):
        save_webdriver(MSEDGEDRIVER)
        return get_driver_edge(mobile=mobile, service=True)


def get_word_list(search_count):
    response = httpx.get(RANDOM_WORDS_URL, follow_redirects=True)
    words_list = random.sample(json.loads(response.text)['data'], search_count)
    print(f'{len(words_list)} words selected')
    return words_list


def login(driver, email, password):
    try:
        print('Logging with microsoft credentials\n')
        driver.get(BING_LOGIN_URL)
        wait_for(5)
        mail_element = driver.find_element('name', 'loginfmt')
        mail_element.clear()
        mail_element.send_keys(email)
        mail_element.send_keys(Keys.RETURN)
        wait_for(5)
        password_element = driver.find_element('name', 'passwd')
        password_element.clear()
        password_element.send_keys(password)
        password_element.send_keys(Keys.ENTER)
        if driver.name == 'firefox':
            try:
                wait_for(5)
                checkbox_element = driver.find_element('name', 'DontShowAgain')
                checkbox_element.click()
                checkbox_element.submit()
            except common.exceptions.NoSuchElementException:
                pass

    except Exception as e:
        driver.close()
        raise SystemExit(e)

    wait_for(5)
