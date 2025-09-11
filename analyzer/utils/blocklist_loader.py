import json
import os

def get_blocklist():
    try:
        path = os.path.join('analyzer', 'utils', 'blocklist.json')
        with open(path, 'r') as file:
            data = json.load(file)
            return data
    except Exception as error:
        print(f'An Error occured during the parsing process: {error}')