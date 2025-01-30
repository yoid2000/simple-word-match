import json
import random

class WordManager:
    def __init__(self, num_words=10):
        self.num_words = num_words
        self.file_path = 'translations.json'
        self.words = self._load_words()
        # working_set is the set of indices of words currently on display
        self.working_set = self._assign_initial_words()
        # english_order and german_order are indices into working_set and
        # are in the order in which the words will be displayed
        self.english_order = [i for i in range(self.num_words)]
        random.shuffle(self.english_order)
        self.german_order = [i for i in range(self.num_words)]
        random.shuffle(self.german_order)

    def get_words(self, english_index=None, german_index=None):
        ''' Returns the lists of English and German words, in the order of display.
            If the english_index and german_index are not None and match, the words are removed
            and new words put in their place, colored black.
            If the don't match, then the same list if returned, but with the two
            words colored red.
        '''
        # First populate the default list of words, and default color black
        english_words = []
        for i in self.english_order:
            english_words.append({'color': 'black',
                                  'word': self.words[self.working_set[i]]['english']})
        german_words = []
        for i in self.german_order:
            german_words.append({'color': 'black',
                                  'word': self.words[self.working_set[i]]['german']})
        if english_index is not None:
            # Player made a guess, so let's see if it is correct
            if self.english_order[english_index] == self.german_order[german_index]:
                # Correct guess, so replace the words
                new_word_index = self._get_random_word()
                self.working_set[self.english_order[english_index]] = new_word_index
                english_words[english_index]['word'] = self.words[new_word_index]['english']
                german_words[german_index]['word'] = self.words[new_word_index]['german']
            else:
                # Incorrect guess, so color the words red
                english_words[english_index]['color'] = 'red'
                german_words[german_index]['color'] = 'red'
        return english_words, german_words

    def _get_random_word(self):
        ''' Gets a random index from the list of words as long as it is not already
            in the working set
        '''
        candidates = random.sample(range(len(self.words)), self.num_words)
        for candidate in candidates:
            if candidate not in self.working_set:
                return candidate

    def _load_words(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def _assign_initial_words(self):
        # Get a random set of indexes to select words from
        return random.sample(range(len(self.words)), self.num_words)

if __name__ == '__main__':
    wm = WordManager()
    english_words, german_words = wm.get_words()
    next_english_index = 0
    prompt = ''
    while(True):
        for i in range(len(english_words)):
            print(f"{i}:")
            print(english_words[i])
            print(german_words[i])
        # get input from command line
        index = input(f"{prompt} {next_english_index} -> ")
        if index == 'q':
            break
        # split indices on ',' and convert to integers
        index = int(index)
        english_words, german_words = wm.get_words(english_index=next_english_index, german_index=index)
        prompt = "Good!\n"
        for word in english_words:
            if word['color'] == 'red':
                prompt = "Boo boo\n"
        if prompt == "Good!\n":
            next_english_index += 1
            if next_english_index == len(english_words):
                next_english_index = 0