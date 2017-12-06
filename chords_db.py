from pymongo import MongoClient

import config

LINK = config.LINK
db = MongoClient(LINK).SimpleGuitarbot  # Подключение к БД
collection = db.chords  # Подключение к коллекции chords


def get_files_id(chord):
    """
    Возвращает подпись (название) аккорда и список file_id его позиций.
    Если аккорда в базе нет, возвращает None None.
    """
    global collection
    try:
        ch = collection.find_one({'chord': chord})
        return ch['caption'], ch['files_id']
    except TypeError:
        return None, None


def set_files_id(chord, files_id, caption):
    """Добавляет аккорд в БД (его название, список file_id позиций, подпись)"""
    global collection
    collection.insert_one({'chord': chord, 'files_id': files_id, 'caption': caption})
