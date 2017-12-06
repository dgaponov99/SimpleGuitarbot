from pymongo import MongoClient

import config

LINK = config.LINK
db = MongoClient(LINK).SimpleGuitarbot
collection = db.chords
collection.insert_one({'chord': 'dd'})


def get_files_id(chord):
    global collection
    try:
        # print(collection.find_one({'chord': chord}))
        return collection.find_one({'chord': chord})['files_id']
    except TypeError:
        return None


def set_files_id(chord, files_id):
    global collection
    collection.insert_one({'chord': chord, 'files_id': files_id})
