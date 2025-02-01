import json
import random

class WordManager:
    def __init__(self, num_words=10):
        self.num_words = num_words
        self.file_path = 'translations.json'
        self.words = self._load_words()
        self.english_words = []
        self.german_words = []
        self._initialize()

    def get_words(self, english_index=None, german_index=None):
        if english_index is None:
            self._initialize()
        elif self.english_order[english_index] == self.german_order[german_index]:
            # Correct guess, so make the words grey
            self.english_words[english_index]['color'] = 'lightgrey'
            self.german_words[german_index]['color'] = 'lightgrey'
            if self._all_grey() or english_index is None:
                self._initialize()
        else:
            # Incorrect guess, so color the words red
            self.english_words[english_index]['color'] = 'red'
            self.german_words[german_index]['color'] = 'red'
        return self.english_words, self.german_words

    def _all_grey(self):
        for word in self.english_words:
            if word['color'] != 'lightgrey':
                return False
        return True

    def _initialize(self):
        # working_set is the set of indices of words currently on display
        self.working_set = self._assign_initial_words()
        # english_order and german_order are indices into working_set and
        # are in the order in which the words will be displayed
        self.english_order = [i for i in range(self.num_words)]
        random.shuffle(self.english_order)
        self.german_order = [i for i in range(self.num_words)]
        random.shuffle(self.german_order)
        self.english_words = []
        for i in self.english_order:
            self.english_words.append({'color': 'black',
                                  'word': self.words[self.working_set[i]]['english']})
        self.german_words = []
        for i in self.german_order:
            self.german_words.append({'color': 'black',
                                  'word': self.words[self.working_set[i]]['german']})

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
