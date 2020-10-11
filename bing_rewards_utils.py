import json
import random
import time
from os import listdir

import requests
from selenium import common, webdriver
from selenium.webdriver.common.keys import Keys

from geckodriver import save_geckodriver

RANDOM_WORDS_URL = 'https://www.randomlists.com/data/words.json'
BING_LOGIN_URL = 'https://login.live.com/'


def wait_for(sec=2):
    time.sleep(sec)


def get_driver_firefox(mobile=False):
    profile = webdriver.FirefoxProfile()
    if mobile:
        profile.set_preference("general.useragent.override",
                               "Mozilla/5.0 (Android 8.0.0; Mobile; rv:63.0) Gecko/63.0 Firefox/63.0")
    try:
        driver = webdriver.Firefox(firefox_profile=profile, executable_path=f"geckodriver/{listdir('geckodriver')[0]}")
        return driver
    except FileNotFoundError:
        save_geckodriver()
        return get_driver_firefox(mobile)


def get_word_list(search_count):
    response = requests.get(RANDOM_WORDS_URL)
    words_list = random.sample(json.loads(response.text)['data'], search_count)
    print(f'{len(words_list)} words selected')
    return words_list


def login(driver, email, password):
    try:
        driver.get(BING_LOGIN_URL)
        wait_for(5)
        mail_element = driver.find_element_by_name('loginfmt')
        mail_element.clear()
        mail_element.send_keys(email)
        mail_element.send_keys(Keys.RETURN)
        wait_for(5)
        password_element = driver.find_element_by_name('passwd')
        password_element.clear()
        password_element.send_keys(password)
        password_element.send_keys(Keys.ENTER)
        wait_for(5)
        try:
            checkbox_element = driver.find_element_by_name('DontShowAgain')
            checkbox_element.click()
            checkbox_element.submit()
        except common.exceptions.NoSuchElementException:
            pass

    except Exception as e:
        driver.close()
        raise SystemExit(e)

    wait_for(5)
