from ielts.tpo import get_tpo_urls
from selenium import webdriver
from services.storage import Storage
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def main():
    caps = DesiredCapabilities().FIREFOX

    caps['pageLoadStrategy'] = 'eager'

    driver = webdriver.Firefox(desired_capabilities=caps)

    result = get_tpo_urls(driver, 'http://top.zhan.com/ielts/speak/cambridge.html')

    print(result)

if __name__ == '__main__':
    main()
