import genanki
import random
import lib.dtw_lib.language_card_templates_c as templates
from lib.language_notes_creator import get_notes
import os
import datetime
import lib.const as const

def get_id():
    id = random.randrange(1 << 30, 1 << 31)
    return id

class Deck:
    def __init__(self, deck_name, data, language):
        self.lang = language
        self.name = deck_name
        self.data = data
        self.deck = genanki.Deck(
            get_id(),
            deck_name)
        self.model = genanki.Model(
            314159262,
            f'{language.capitalize()} German Words',
            css= templates.get_style(),
            fields=[
                {'name': 'Frequency Rank'},
                {'name': language.capitalize()},
                {'name': "Tips"},
                {'name': 'English (Simplified Translation)'},
                {'name': 'Example Sentences (Translation)'},
                {'name': 'Example Sentences'},
                {'name': 'English (Detailed Translation)'},
                {'name': 'Audio'},
                {'name': 'Picture'},
            ],
            templates=[
                {
                    'name': f'English -> {language.capitalize()}',
                    'qfmt': templates.get_front(),
                    'afmt': templates.get_back(self.lang)
                },
            ]
        )
        self.gen_notes()

    def gen_notes(self):
        for i, note in enumerate(self.data):
            image_path = f'<img src={os.path.basename(note.img_path)}>' \
                if note.img_path else ''
            if note.reverse:
                new_note = genanki.Note(
                    tags=['added'],
                    model=self.model,
                    fields=[str(i) +'_reverse',
                            note.trans, note.tips, note.word,note.sentences,
                            '', '',
                            f'[sound:{os.path.basename(note.audio_path)}]',
                            image_path])
            else:
                new_note = genanki.Note(
                    tags=['added'],
                    model=self.model,
                    fields=[str(i),
                            note.word, note.tips, note.trans, note.sentences,
                            '','',
                            f'[sound:{os.path.basename(note.audio_path)}]',
                            image_path])
            self.deck.add_note(new_note)

    def export(self):
        new_package = genanki.Package(self.deck)
        media_files = []
        for note in self.data:
            media_files.append(note.audio_path)
            if note.img_path:
                media_files.append(note.img_path)
        new_package.media_files = media_files
        if const.p_OUTPUT_FOLDER and not os.path.isdir(const.p_OUTPUT_FOLDER):
            os.mkdir(const.p_OUTPUT_FOLDER)
        output_path = os.path.join(const.p_OUTPUT_FOLDER,f"{self.name}.apkg")
        new_package.write_to_file(output_path)
        print(f'"{self.name}.apkg" created with {len(self.data)} notes')

    @classmethod
    def generate_deck(cls, words, language):
        date = datetime.datetime.now().strftime('%m %d')
        deck_name = f'{language.capitalize()} Essential Words {date}'
        notes = get_notes(language, words)['notes']
        lang_deck = cls(deck_name,data=notes,language=language)
        lang_deck.export()
        return (notes, deck_name)

def parse_words(path='words.txt'):
    rows = []
    with open(path, 'r',encoding="utf8") as f:
        for row in f.readlines():
            row = row.split('-')[0]
            for char in ['[','?','!','(','.','+']:
                if char in row:
                    row = row.split(char)[0]
            rows.append(row.rstrip())
    with open(path, 'w',encoding="utf8") as f:
        f.write('$'.join(rows))

if __name__ == '__main__':
    path = '../words.txt'
    # parse_words(path)
    with open(path, 'r', encoding='utf8') as f:
        data = f.read()
        words = data.split('$')
        Deck.generate_deck(words, 'german')