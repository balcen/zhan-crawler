from selenium import webdriver


class TpoListening:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Firefox()

    def get_tpo_list():
        driver = webdriver.Firefox()
        driver.get('https://top.zhan.com/ielts/listen/cambridge.html')

        ul_tag = driver.find_element_by_css_selector('ul.tpo_list.tpo_no_row')
        li_tags = ul_tag.find_elements_by_tag_name('li')

        result = list()
        for li_tag in li_tags:
            a_tag = li_tag.find_element_by_tag_name('a')
            result.append((a_tag.text, a_tag.get_attribute('href')))

        driver.close()

        return result
