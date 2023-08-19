from lib.controller import Controller

# # Example to how to run the script without the GUI
# WORDS_TXT_FILE = ''

# def no_gui():
#     from lib.language_deck_creator import parse_words, Deck
#     path = WORDS_TXT_FILE
#     parse_words(path)
#     with open(path, 'r', encoding='utf8') as f:
#         data = f.read()
#         words = data.split('$')
#         Deck.generate_deck(words, 'german')

if __name__ == '__main__':
    controller = Controller()
    controller.run()
