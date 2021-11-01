import re
from selenium import webdriver
from services.storage import Storage
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


INDEX_URL = 'https://top.zhan.com/ielts/listen/cambridge.html'


class Tpo:
    @staticmethod
    def get_tpo_urls(url=INDEX_URL):
        storage = Storage()

        try:
            result = storage.read('ielts/tpo_urls.json')
        except FileNotFoundError:
            caps = DesiredCapabilities().FIREFOX
            caps['pageLoadStrategy'] = 'eager'

            driver = webdriver.Firefox(desired_capabilities=caps)
            driver.get(url)

            ul_tag = driver.find_element_by_css_selector('ul.tpo_list.tpo_no_row')
            li_tags = ul_tag.find_elements_by_tag_name('li')

            result = list()
            for li_tag in li_tags:
                a_tag = li_tag.find_element_by_tag_name('a')
                result.append({
                    'title': a_tag.text,
                    'tpo_url': a_tag.get_attribute('href'),
                    'order': int(re.search(r"[0-9]+", a_tag.text).group())
                })

            storage.store(data=result, filename='ielts/tpo_urls.json')

            driver.close()

        return result

    def get_test_urls(self, tpo):
        caps = DesiredCapabilities().FIREFOX
        caps['pageLoadStrategy'] = 'eager'
        driver = webdriver.Firefox(desired_capabilities=caps)

        filename = f"ielts/tpo{tpo['order']}_section_urls.json"

        try:
            storage = Storage()
            tpo_content = storage.read(filename)
        except FileNotFoundError:
            driver.get(tpo['tpo_url'])
            test_list_tag = driver.find_element_by_css_selector('div.tpo_desc_item_list')
            test_tags = test_list_tag.find_elements_by_tag_name('div')

            tpo_content = {'title': tpo['title'], 'order': tpo['order'], 'tests': list()}
            tmp_test = dict()
            for test_tag in test_tags:
                class_name = test_tag.get_attribute('class')
                if class_name == 'clear':
                    if tmp_test:
                        tpo_content['tests'].append(tmp_test)
                        tmp_test = dict()
                elif class_name == 'title':
                    tmp_test['title'] = test_tag.text
                    tmp_test['order'] = int(re.search(r"(?<=Test)[0-9]+", test_tag.text).group())
                elif class_name == 'tpo_desc_list':
                    tmp_test['sections'] = self._get_section_urls(test_tag)

            storage = Storage()
            storage.store(data=tpo_content, filename=filename)

        driver.close()

        return tpo_content

    @classmethod
    def _get_section_urls(cls, tpo_desc_list_tag):
        # 在 tpo_desc_list 裡面有多個 tpo_desc_item 代表不同的 section
        tpo_desc_item_tags = tpo_desc_list_tag.find_elements_by_css_selector('div.tpo_desc_item')

        section_contents = list()
        for tpo_desc_item_tag in tpo_desc_item_tags:
            tmp_section = dict()
            # 每個 tpo_desc_item 裡面有一個 item_content
            content_tag = tpo_desc_item_tag.find_element_by_css_selector('div.item_content')

            # item_content 裏面有 item_img 和 item_text
            # item_img 放圖片上的資料
            item_img_tag = content_tag.find_element_by_css_selector('div.item_img')

            item_img_tip_tags = item_img_tag.find_element_by_css_selector('div.item_img_tips')
            title_span = item_img_tip_tags.find_element_by_css_selector('span.left')
            tmp_section['title'] = title_span.text

            cover_img_tag = item_img_tag.find_element_by_css_selector('img.cover_img')
            tmp_section['cover'] = cover_img_tag.get_attribute('src')

            section_answer_tag = item_img_tag.find_element_by_tag_name('a')
            tmp_section['url'] = section_answer_tag.get_attribute('href')

            section_contents.append(tmp_section)

        return section_contents
