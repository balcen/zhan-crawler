import threading
import json
from ielts.tpo import Tpo
from ielts.test import Test
from pathlib import Path


class IeltsListeningService:
    @staticmethod
    def get_tpo_list():
        tpo = Tpo()
        return tpo.get_tpo_urls()

    @staticmethod
    def get_all_section_url(tpo_urls: list):
        threads = list()
        tpo = Tpo()

        for tpo_url in tpo_urls:
            t = threading.Thread(target=tpo.get_test_urls, args=(tpo_url,))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    @staticmethod
    def get_all_section_content():
        paths = Path('storage/ielts').glob('*section_urls.json')
        threads = list()
        test = Test()
        for path in paths:
            t = threading.Thread(target=test.get_content, args=(path,))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    @staticmethod
    def download_all_section_audio():
        paths = Path('storage/ielts').glob('*content.json')
        test = Test()
        for path in paths:
            test.get_all_section_audio(path)
