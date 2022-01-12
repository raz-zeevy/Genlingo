p_OUTPUT_FOLDER = 'decks'
p_IMAGES = 'images'
p_AUDIO = 'audio'
DeckCreationSuccess = 'deck_creation_success'

import json
with open('settings.json', 'r') as f:
    y = json.loads(f.read())
    print(y['deck_name'])