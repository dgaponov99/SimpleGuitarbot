import requests
from bs4 import BeautifulSoup


class _Chord:
    def __init__(self, chord):
        """Представление аккорда по частям"""

        self.chord = chord.lower()
        self.head_part = ''
        self.optional_part = ''
        self.bass_part = ''

        self._division()

    def _division(self):
        """Разделение аккорда на части"""

        try:
            # Выделение главной части
            if self.chord[1] == '#' or self.chord[1] == 'b':
                self.head_part = self.chord[:2]
            else:
                self.head_part = self.chord[0]

            # Выделение основной и басовой частей
            bass = self.chord.rfind('/')
            if bass >= 0:
                if self.chord[bass + 1].isalpha() and len(self.chord[bass + 1:]) < 3:
                    self.optional_part = self.chord[:bass]
                    self.bass_part = self.chord
                else:
                    self.optional_part = self.chord
            else:
                self.optional_part = self.chord
        except IndexError:
            self.head_part = self.chord
            self.optional_part = self.chord


class Images_chord:
    def __init__(self, chord):
        self.chord = _Chord(chord)
        self.website = 'http://www.gitaristu.ru'

    def getUrl(self):
        """Возвращает список url изображений аккорда"""

        image_list = []

        head_url = ''
        optional_url = ''
        bass_url = ''

        caption = ''

        flag = False

        page = requests.get('http://www.gitaristu.ru/generator_akkordov/chords')
        soup = BeautifulSoup(page.text, 'html.parser')
        list_head_chords = soup.find(id='chordslist').find_all('a')
        for a in list_head_chords:
            head = a.text.split(' ')[-1]
            if head.lower() == self.chord.head_part:
                head_url = a.get('href')
                flag = True
                break

        if flag:
            flag = False
            page = requests.get(self.website + head_url)
            soup = BeautifulSoup(page.text, 'html.parser')
            list_optional_chord = soup.find(id='chordslist').find_all('a')
            for a in list_optional_chord:
                if a.text.lower() == self.chord.optional_part:
                    optional_url = a.get('href')
                    flag = True
                    break

        if flag:
            flag = False
            page = requests.get(self.website + optional_url)
            soup = BeautifulSoup(page.text, 'html.parser')

            if self.chord.bass_part == '':
                fancybox = soup.find_all('a', {'class': 'fancybox'})
                caption = fancybox[0].get('alt')
                for a in fancybox:
                    image_list.append(self.website + a.get('href'))
            else:
                list_bass_chord = soup.find(id='chordslist').find_all('a')
                for a in list_bass_chord:
                    bass = a.text.split(' ')[-1]
                    if bass.lower() == self.chord.bass_part:
                        bass_url = a.get('href')
                        flag = True
                        break
                if flag:
                    page = requests.get(self.website + bass_url)
                    soup = BeautifulSoup(page.text, 'html.parser')
                    fancybox = soup.find_all('a', {'class': 'fancybox'})
                    caption = fancybox[0].get('alt')
                    for a in fancybox:
                        image_list.append(self.website + a.get('href'))

        return caption, image_list
