from pymongo import MongoClient

import config

LINK = config.LINK
client = MongoClient(LINK)

db = client.test
collection = db['chords']


async def get_files_id(chord):
    global collection
    return await collection.find_one({'chord': chord})['files_id']


def set_files_id(chord, files_id):
    global collection
    collection.insert_one({'chord': chord, 'files_id': files_id})
