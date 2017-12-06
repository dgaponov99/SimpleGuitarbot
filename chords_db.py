from pymongo import MongoClient

import config

LINK = config.LINK
client = MongoClient(LINK)

db = client.local
collection = db['chords']


def get_files_id(chord):
    global collection
    try:
        print(collection.find_one({'chord': chord}))
        return collection.find_one({'chord': chord})['files_id']
    except TypeError:
        return None


def set_files_id(chord, files_id):
    global collection
    collection.insert_one({'chord': chord, 'files_id': files_id})
