import json
import time
import urllib.error
from pathlib import Path
from urllib.request import urlretrieve
from urllib.error import ContentTooShortError
from services.login import login
from services.storage import Storage
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Test:
    def get_content(self, path):
        with open(path, 'r') as fp:
            tpo_url_content = json.load(fp)

        tpo = {
            'title': tpo_url_content['title'],
            'order': tpo_url_content['order'],
            'tests': list(),
        }

        caps = DesiredCapabilities().FIREFOX
        caps['pageLoadStrategy'] = 'eager'
        driver = webdriver.Firefox(desired_capabilities=caps)

        tests = tpo_url_content['tests']

        for test in tests:
            tmp_test = {
                'title': test['title'],
                'order': test['order'],
                'sections': list()
            }

            sections = test['sections']

            for section in sections:
                tmp_section = {'title': section['title']}
                driver.get(section['url'])

                if len(driver.find_elements(By.CSS_SELECTOR, 'div.regist_view_pop')) > 0:
                    login(driver)
                    driver.implicitly_wait(0)
                    WebDriverWait(driver, 10).until_not(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.regist_view_pop'))
                    )

                while 'sectiontest' not in driver.current_url:
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input.next_btn'))
                    )
                    next_btn = driver.find_element_by_css_selector('input.next_btn')
                    next_btn.click()

                WebDriverWait(driver, 999).until(
                    lambda d: d.find_element_by_id('jp_audio_0').get_attribute('src') != ''
                )

                time.sleep(3)

                audio_tag = driver.find_element_by_id('jp_audio_0')
                tmp_section['question_audio_url'] = audio_tag.get_attribute('src')

                tmp_test['sections'].append(tmp_section)

            tpo['tests'].append(tmp_test)

        driver.close()

        storage = Storage()
        storage.store(tpo, f"ielts/tpo{tpo['order']}_content.json")

    def get_all_section_audio(self, path):
        print(path)
        with open(path, 'r') as fp:
            tpo = json.load(fp)

        for test in tpo['tests']:
            section_order = 1
            for section in test['sections']:
                folder = Path('storage/ielts/audio')
                filename = f"ielts_{tpo['order']}_test{test['order']}_section{section_order}.mp3"
                self.recu_down(section['question_audio_url'], folder/filename)
                section_order += 1

    def recu_down(self, url, filename):
        try:
            urlretrieve(url, filename)
        except ContentTooShortError:
            self.recu_down(url, filename)
