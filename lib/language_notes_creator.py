import os, random, time
from googletrans import Translator
import unidecode
from pyppeteer import launch
import bs4
import pandas as pd
from gtts import gTTS
import asyncio
import pycountry
import shutil
from icrawler.builtin import GoogleImageCrawler
import lib.const as const

p_JPG_NAME_CONV = '000001.jpg'
p_PNG_NAME_CONV = '000001.png'

class Note():
    def __init__(self, lang, word, no_audio=False, no_image=False):
        self.lang = pycountry.languages.get(name=lang)
        self.lang_pre = self.lang.alpha_2
        if not self.lang: raise Exception("LanguageDoesntExist")
        self.reverse = False
        self.word = self.word_clean(word)
        self.en_trans = ''
        self.trans = self.get_trans()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.sentences = loop.run_until_complete(self.fetch_sentences())
        # self.sentences = asyncio.get_event_loop(). \
        #     run_until_complete(self.fetch_sentences())
        if not no_audio:
            self.audio_path = self.text_to_speech()
        if not no_image:
            try:
                self.img_path = self.text_to_image()
            except TypeError:
                self.img_path = ''

    def __repr__(self):
        return f'"{self.word}","{self.trans}","{self.sentences}","added"'

    def word_clean(self, input_word):
        word = input_word.replace("\n", '')
        if word.startswith(const.REV_TOKEN):
            self.reverse = True
            word = word.lstrip(const.REV_TOKEN)
        while word[-1] == ' ': word = word[:-1]
        return word

    def safe_word_name(self):
        safe_name = unidecode.unidecode(self.word.replace(" ", '_')).lower()
        for char in ["/",":","?","*","\\",'"',"<",">","|"]:
            safe_name = unidecode.unidecode(safe_name.replace(char, ''))
        return safe_name

    def text_to_speech(self):
        '''
        Could raise problems with the token, might need occasional
        upgrade
        :return:
        '''
        myText = self.word
        language = self.lang_pre
        a = random.randint(100, 1000)
        folder_path = const.p_AUDIO
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        path = os.path.join(folder_path, self.safe_word_name() + ".mp3")
        output = gTTS(text=myText, lang=language, slow=False)
        output.save(path)
        return path

    def text_to_image(self):
        path = os.path.join(const.p_IMAGES, self.safe_word_name())
        google_crawler = GoogleImageCrawler(storage={'root_dir': path})
        # Can be added if wanted
        filters = dict()
        google_crawler.crawl(keyword=self.en_trans, filters=filters,
                             max_num=1)
        # Move img to outer folder, try jpg or png
        try:
            img_path = os.path.join(const.p_IMAGES,
                                    self.word.replace(' ', '_') + '.jpg')
            shutil.move(os.path.join(path, p_JPG_NAME_CONV),
                        img_path)
        except:
            try:
                img_path = os.path.join(const.p_IMAGES,
                                        self.word.replace(' ', '_') + '.png')
                shutil.move(os.path.join(path, p_PNG_NAME_CONV),
                            img_path)
            except: return False
            # Remove auto-created folder
            os.rmdir(path)
            # Lower Resolution
            from PIL import Image
            # Open the image by specifying the image path.
            image_file = Image.open(img_path)
            image_file.thumbnail((450, 450))
            image_file.save(img_path)
        return img_path

    def get_trans(self):
        '''
        Could raise problems with the lib version, might need occasional
        upgrade. try unisntall and then pip install googletrans==4.0.0rc1
        :return:
        '''
        word = self.word
        translator = Translator()
        try:
            ret1 = translator.translate(text=word, dest='he',
                                        src=self.lang_pre)
            ret = translator.translate(text=word, dest='en',
                                       src=self.lang_pre)
            self.en_trans = ret.text
            return ret1.text + " " + ret.text
        except Exception as e:
            raise e
            print(word, "->", e)
            return word

    async def fetch_sentences(self):
        # parsed_word = textParse(self.word)
        parsed_word = self.word
        lang_lower = self.lang.name.lower()
        url = f'https://context.reverso.net/translation/hebrew-{lang_lower}/'
        browser = await launch(
            handleSIGINT=False,
            handleSIGTERM=False,
            handleSIGHUP=False
        )
        page = await browser.newPage()
        page.setDefaultNavigationTimeout(50000)
        try:
            await page.goto(url + parsed_word)
            content = await page.content()
            soup = bs4.BeautifulSoup(content, features='html.parser')
            examples = soup.find_all('div', {'class': 'example blocked'})
        except:
            examples = []
        word_sentences = ''
        if len(examples) == 0:
            print('No found sentences for -')
            return word_sentences
        for i, example in enumerate(examples):
            text = example.find_all('span', {'class': 'text'})
            text = [line.get_text()[11:] for line in text]
            word_sentences += '<b>' + text[0] + '</b>'',' + text[1] + '<br>'
            if i == 2: break
        await browser.close()
        return word_sentences


def get_notes(lang, words, no_audio=False, check_dups_in=None):
    exist_words = []
    deck_words = []
    if check_dups_in:
        deck_words = \
            pd.read_csv(check_dups_in, encoding='utf-8', names=[1, 2, 3, 4, 5, 6,
                                                                7, 8])[2]
        deck_words = deck_words.tolist()
    notes = []
    for word in list(set(words)):
        if word in deck_words:
            exist_words.append(word)
            continue
        try:
            new_note = Note(lang, word, no_audio=no_audio)
            notes.append(new_note)
            word_type = 'regular' if not new_note.reverse else 'reverse'
            print(f'created {word_type} note for "{new_note.word}"')
        except Exception as e:
            # raise e
            print(f'couldn\'t create note for {word} because: "{e}"')
            quit()
    return {'notes': notes, 'added': len(notes), 'existing': len(exist_words)}


def check_dups(data):
    words = data.split('$')
    exist_words = []
    deck_words = pd.read_csv('modules/russian_deck.csv', encoding='utf-8',
                             names=[1, 2, 3, 4, 5, 6, 7, 8])[2]
    for word in list(set(words)):
        if word[0] in ['^', '*']: word = word[1:]
        if word in deck_words.tolist(): exist_words.append(word)
    return exist_words


if __name__ == '__main__':
    start_time = time.time()
    get_notes(words=['лошадям'])
    print('-------------')
    print(f'run time: {time.time() - start_time}')
