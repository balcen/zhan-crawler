from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import login
import time
import pdb


def get_tpo_urls(driver, url):
    driver.get(url)

    tpo_li_tags = driver.find_elements(By.XPATH, '//ul[contains(@class, "tpo_no_row")]/li')

    result = []

    for tpo_li_tag in tpo_li_tags:
        a_tag = tpo_li_tag.find_element(By.XPATH, 'a')
        result.append({
            'title': a_tag.text,
            'url': a_tag.get_attribute('href'),
        })

    return result

def get_section_urls(driver, url):
    driver.get(url)

    tpo_desc_item_list = driver.find_element(By.XPATH, '//div[contains(@class, "tpo_desc_item_list")]')

    title_div_tags = tpo_desc_item_list.find_elements(By.XPATH, 'div[contains(@class, "title")]')

    test_div_tags = tpo_desc_item_list.find_elements(By.XPATH, 'div[contains(@class, "tpo_desc_list")]')

    results = []

    if len(title_div_tags) == len(test_div_tags):
        for index, title_div_tag in enumerate(title_div_tags):
            test_div_tag = test_div_tags[index]

            sections = []

            for section_div_tag in test_div_tag.find_elements(By.XPATH, 'div[contains(@class, "tpo_talking_item")]'):
                sections.append({
                    'section_part': section_div_tag.find_element(By.XPATH, 'div[contains(@class, "text")]').text,
                    'title': section_div_tag.find_element(By.XPATH, 'div[contains(@class, "text_line")]/span').text,
                    'url': section_div_tag.find_element(By.XPATH, 'a[2]').get_attribute('href'),
                })

            results.append({
                'title': title_div_tag.text,
                'sections': sections
            })

    return results

def get_speak_question(driver, url):
    driver.get(url)

    try:
        element = WebDriverWait(driver, 5).until(
            lambda d: d.find_element(By.XPATH, '//a[contains(@class, "login_btn")]')
        )

        element.click()

        login.login(driver)
    except TimeoutException:
        WebDriverWait(driver, 5).until(
            lambda d: d.find_element(By.XPATH, '//div[contains(@class, "avatar")]')
        )

    # pdb.set_trace()

    # driver.refresh()

    order = 1

    talk_title_element = driver.find_element(By.XPATH, '//div[@class="talk_title"]')

    try:
        talk_title = talk_title_element.find_element(By.XPATH, 'div').text
    except NoSuchElementException:
        talk_title = talk_title_element.find_element(By.XPATH, 'p').get_attribute('innerHTML')

    result = {
        'order': order,
        'talk_title': talk_title,
        'exp': driver.find_element(By.XPATH, '//div[@class="pigai_text"]/div[2]/p').get_attribute('innerHTML'),
    }

    try:
         result['question'] = driver.find_element(By.XPATH, '//div[@class="talk_test_text"]/p').text

         results = [result]

         order += 1

         question_page_li_tags = driver.find_elements(By.XPATH, '//div[@class="pages_content"]/ul/a')

         links_hrefs = [link.get_attribute('href') for link in question_page_li_tags[1:]]

         for href in links_hrefs:
             driver.get(href)

             talk_title_element = driver.find_element(By.XPATH, '//div[@class="talk_title"]')

             try:
                 talk_title = talk_title_element.find_element(By.XPATH, 'div').text
             except NoSuchElementException:
                 talk_title = talk_title_element.find_element(By.XPATH, 'p').get_attribute('innerHTML')

             talk_test_text_element = WebDriverWait(driver, 30).until(
                 EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "talk_test_text")]/p'))
             )

             exp_element = WebDriverWait(driver, 30).until(
                 EC.presence_of_element_located((By.XPATH, '//div[@class="pigai_text"]/div[2]/p'))
             )

             results.append({
                 'order': order,
                 'talk_title': talk_title,
                 'question': talk_test_text_element.text,
                 'exp': exp_element.get_attribute('innerHTML')
             })

             order += 1

    except NoSuchElementException:
        result['question'] = driver.find_element(By.XPATH, '//div[@class="nano-content_in"]/div').get_attribute('innerHTML')

        results = [result]

    return results
