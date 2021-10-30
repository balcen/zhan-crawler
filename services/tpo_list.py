from selenium import webdriver


URL = 'https://top.zhan.com/ielts/listen/cambridge.html'


class TpoList:
    def __init__(self, url=URL):
        self.url = url
        self.driver = webdriver.Firefox()

    def __del__(self):
        self.driver.close()

    def get(self):
        ul_tag = self.driver.find_element_by_css_selector('ul.tpo_list.tpo_no_row')
        li_tags = ul_tag.find_elements_by_tag_name('li')

        result = list()
        for li_tag in li_tags:
            a_tag = li_tag.find_element_by_tag_name('a')
            result.append((a_tag.text, a_tag.get_attribute('href')))

        return result
