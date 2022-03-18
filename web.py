from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def get_eager_driver():
    caps = DesiredCapabilities().FIREFOX

    caps['pageLoadStrategy'] = 'eager'

    return webdriver.Firefox(desired_capabilities=caps)

def get_driver():
    return webdriver.Firefox()