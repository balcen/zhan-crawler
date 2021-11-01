from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


USERNAME = '17621187291'
PASSWORD = 'ivyway1600'


def login(driver: webdriver):
    wait = WebDriverWait(driver, 999)
    wait.until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )
    # time.sleep(4)
    username_password_label = driver.find_element_by_css_selector('label.tab_label.tab1')
    username_password_label.click()

    wait.until(
        EC.element_to_be_clickable((By.ID, 'userNamePop'))
    )
    username_input = driver.find_element_by_id('userNamePop')
    username_input.click()
    username_input.send_keys(USERNAME)

    password_input = driver.find_element_by_id('loginPasswordPop')
    password_input.click()
    password_input.send_keys(PASSWORD)

    login_btn = driver.find_element_by_id('loginBtnPop')
    login_btn.click()
