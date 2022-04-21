import web
import ielts.tpo
import storage
import pdb
import re


def load_tpo_urls(type):
    url = f"http://top.zhan.com/ielts/{type}/cambridge.html"

    file_path = f"ielts/tpo_{type}_urls.json"

    driver = web.get_driver()

    result = ielts.tpo.get_tpo_urls(driver, url)

    storage.store(result, file_path)

def load_section_urls(type):
    driver = web.get_driver()

    url_data = storage.read(f"ielts/tpo_{type}_urls.json")

    results = []
    for url_datum in url_data:
        result = ielts.tpo.get_section_urls(driver, url_datum['url'])

        results.append({
            'title': url_datum['title'],
            'sections': result,
        })

    storage.store(results, f"ielts/section_{type}_urls.json")

def load_speak_questions():
    driver = web.get_driver()

    url_data = storage.read('ielts/section_speak_urls.json')

    results = []

    for url_datum in url_data:
        tests = []

        for test in url_datum['sections']:
            sections = []

            for section in test['sections']:
                questions = ielts.tpo.get_speak_question(driver, section['url'])

                sections.append({
                    'part': section['section_part'],
                    'title': section['title'],
                    'questions': questions
                })

            tests.append({
                'title': test['title'],
                'sections': sections,
            })

        results.append({
            'title': url_datum['title'],
            'tests': tests,
        })

    driver.close()

    storage.store(results, 'ielts/speak_questions.json')

def load_write_questions():
    driver = web.get_driver()

    url_data = storage.read('ielts/section_write_urls.json')

    results = []

    for url_datum in url_data:
        tests = []

        tpo_order = re.search(r"\d+", url_datum['title']).group(0)

        for test in url_datum['sections']:
            sections = []

            test_order = re.search(r"\d+$", test['title']).group(0)

            for section in test['sections']:
                task_order = re.search(r"\d+", section['section_part']).group(0)

                pending_title = f"tpo{tpo_order}_test{test_order}_task{task_order}"

                questions = ielts.tpo.get_write_question(driver, section['url'], pending_title)

                sections.append({
                    'part': section['section_part'],
                    'title': section['title'],
                    'questions': questions
                })

            tests.append({
                'title': test['title'],
                'sections': sections,
            })

        results.append({
            'title': url_datum['title'],
            'tests': tests,
        })

    driver.close()

    storage.store(results, 'ielts/write_questions.json')

if __name__ == '__main__':
    load_write_questions()
