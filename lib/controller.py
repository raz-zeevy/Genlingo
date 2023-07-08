from lib.gui import GUI
from lib.modules import get_lang_list, open_decks_folder, \
    generate_deck_in_bg, delete_folders
import lib.const as const
from threading import Timer

TIMER_INTERVAL = 7

e_BUTTON_CLICK = '<Button-1>'
e_BUTTON_PRESS = '<ButtonPress-1>'

class Controller():
    def __init__(self):
        self.gui = GUI()
        self.gui.parse_btn.bind(e_BUTTON_PRESS, lambda e: self.parse_words())
        self.gui.creat_btn.bind(e_BUTTON_PRESS, lambda e: self.create_deck())
        self.gui.open_search_folder.bind(e_BUTTON_PRESS, lambda e:
        open_decks_folder())
        self.set_lang_picker()
        self.words = []
        self.run()

    def set_lang_picker(self):
        values = get_lang_list()
        self.gui.set_lang_picker(value='German', values = values)

    def parse_words(self):
        input_words = self.gui.click_parse()
        if not input_words.rstrip():
            self.update_words([])
            return
        words = []
        for row in input_words.split('\n'):
            # remove "-"'s
            # row = row.split('-')[0]
            for char in ['[','?','!','(','.','+']:
                if char in row:
                    row = row.split(char)[0]
            word = row.rstrip()
            if word:
                words.append(row.rstrip())
        self.update_words(words)
        self.gui.creat_btn.state(["!disabled"])

    def create_deck(self):
        def check_deck_created():
            nonlocal timer
            if self.current_t.is_alive():
                self.gui.update_meter(used=timer)
                Timer(TIMER_INTERVAL, check_deck_created).start()
                if timer < len(self.words)-1: timer += 1
            else:
                try:
                    words, name = self.current_t.join()
                    self.gui.update_meter(used=len(self.words))
                    self.gui.show_msg(const.DeckCreationSuccess, words=words,
                                      name=name)
                except Exception as e:
                    self.gui.show_msg(e)
                finally:
                    delete_folders()
                    self.update_words(None)

        if not self.words: return
        self.gui.creat_btn.state(["disabled"])
        timer = 0
        lang = self.gui.lang_picker.get()
        name = self.gui.deck_name_entry.get()
        try:
            self.current_t = generate_deck_in_bg(self.words, lang, name)
        except Exception as e:
            self.gui.show_msg(e)
        self.gui.update_meter(used = timer, strip=5)
        self.current_t.start()
        check_deck_created()

    def update_words(self,words):
        self.words = words
        if not words:
            self.gui.reset_inputs()
        else:
            self.gui.change_entry_text('\n'.join(words))
            self.gui.set_meter(len(words))

    def run(self):
        self.gui.run()

if __name__ == '__main__':
    controller = Controller()
