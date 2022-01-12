import pycountry
import lib.const as const
import os
from threading import Thread
from lib.language_deck_creator import Deck
import shutil

supported_languages = ['deu','heb','spa','rus','ara', 'eng', 'fra']
# http://www.loc.gov/standards/iso639-2/php/English_list.php

def get_lang_list():
    langs = pycountry.languages
    return [lang.name for lang in langs if lang.alpha_3 in supported_languages]

def delete_folders():
    shutil.rmtree(const.p_IMAGES)
    shutil.rmtree(const.p_AUDIO)

def open_decks_folder():
    if not os.path.isdir(const.p_OUTPUT_FOLDER):
        os.makedirs(const.p_OUTPUT_FOLDER)
    os.system(f"start {const.p_OUTPUT_FOLDER}")

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def generate_deck_in_bg(words, lang):
        global current_t
        current_t = ThreadWithReturnValue(target=Deck.generate_deck, args=(words,
                                                                     lang,))
        return current_t