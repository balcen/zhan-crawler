from google_trans_new import google_translator
import json
import pdb

def translate_speak_title():
    with open('storage/ielts/speak_questions.json', 'r') as handler:
        speak_data = json.load(handler)

    t = google_translator(timeout=5)

    for tpo_data in speak_data:
        for test in tpo_data['tests']:
            for section in test['sections']:
                section['title_en'] = t.translate(section['title'], 'en')
                section['title_tw'] = t.translate(section['title'], 'zh-tw')

    with open('storage/ielts/speak_questions.json', 'w') as handler:
        json.dump(speak_data, handler)

def translate_write_title():
    with open('storage/ielts/write_questions.json', 'r') as handler:
        speak_data = json.load(handler)

    t = google_translator(timeout=5)

    for tpo_data in speak_data:
        for test in tpo_data['tests']:
            for section in test['sections']:
                section['part_en'] = t.translate(section['part'], 'en')
                section['part_tw'] = t.translate(section['part'], 'zh-tw')
                section['title_en'] = t.translate(section['title'], 'en')
                section['title_tw'] = t.translate(section['title'], 'zh-tw')
                section['tpo'] = tpo_data['title']
                section['test'] = test['title']

    with open('storage/ielts/write_questions.json', 'w') as handler:
        json.dump(speak_data, handler)

if __name__ == '__main__':
    translate_write_title()
