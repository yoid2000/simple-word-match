import re
import json

def convert_unicode_to_characters(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Example usage
# file_path = 'c:/paul/GitHub/simple-word-match/translations.json'
# convert_unicode_to_characters(file_path)

def parse_anki_file(path_to_file):
    all_translations = []

    with open(path_to_file, 'r', encoding='utf-8') as file:
        content = file.read()

    records = content.split('\n"\n')
    for record in records:
        parts = record.split('\n"\t"\n')
        if len(parts) != 2:
            continue
        second_part = parts[1]
        english_line_match = re.search(r'<ol class=""eng"">(.*?)<font color=""grey""></font></ol>', second_part, re.DOTALL)
        german_line_match = re.search(r'<span class=""word"">(.*?)</span>', second_part, re.DOTALL)
        
        if not english_line_match or not german_line_match:
            print('Skipping record without english or german line')
            continue
        
        english_word_html = english_line_match.group(1)
        german_word_html = german_line_match.group(1)
        
        # Handle multiple <li> elements in the English word
        english_word_html = re.sub(r'<li>(.*?)</li>', r'\1', english_word_html, count=1)
        english_word_html = re.sub(r'<li>.*?</li>', '', english_word_html)
        
        english_word = re.sub(r'<.*?>', '', english_word_html).strip()
        german_word = re.sub(r'<.*?>', '', german_word_html).strip()
        

        if second_part.index(english_line_match.group(0)) < second_part.index(german_line_match.group(0)):
            all_translations.append({"english": english_word, "german": german_word})

    return all_translations

path_to_file = 'All Decks.txt'
translations = parse_anki_file(path_to_file)
# write the translations to a json file
import json
with open('translations.json', 'w') as f:
    json.dump(translations, f, indent=4)