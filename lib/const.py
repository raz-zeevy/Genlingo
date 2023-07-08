p_OUTPUT_FOLDER = 'decks'
p_IMAGES = r'temp\images'
p_AUDIO = r'temp\audio'
DeckCreationSuccess = 'deck_creation_success'

# Shared Variables
REV_TOKEN = '^REV^'
REV_WORDS = 'rev_words'
REG_WORDS = 'reg_words'

import json
with open('settings.json', 'r') as f:
    y = json.loads(f.read())
    print(y['deck_name'])