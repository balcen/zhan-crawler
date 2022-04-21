import json
import pathlib


def store(data, filename):
    path = pathlib.Path('storage') / filename

    with open(path, 'w') as fp:
        json.dump(data, fp)

def read(filename):
    path = pathlib.Path('storage') / filename

    with open(path, 'r') as fp:
        return json.load(fp)