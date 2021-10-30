import json
import pathlib


class Storage:
    def __init__(self):
        self.path = pathlib.Path('storage')

    def store(self, data, filename):
        path = self.path / filename
        with open(path, 'w') as fp:
            json.dump(data, fp)
