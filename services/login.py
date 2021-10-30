from selenium import webdriver

USERNAME = '17621187291'
PASSWORD = 'ivyway1600'


def login(driver: webdriver):
    login_btn = driver.find_element_by_css_selector('a.login_btn.md_passport')
    login_btn.click()

    username_password_label = driver.find_element_by_css_selector('label.tab_label.tab1')
    username_password_label.click()

    username_input = driver.find_element_by_id('userNamePop')
    username_input.send_keys(USERNAME)
    password_input = driver.find_element_by_id('loginPasswordPop')
    password_input.send_keys(PASSWORD)
