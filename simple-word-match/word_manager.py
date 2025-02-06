import json
import random
import os

class WordManager:
    def __init__(self, num_words=10):
        self.delay = 5   # don't show frequent word again for this many rounds
        self.purge = 3   # remove from frequent words if correct this many times
        self.max_frequent = 3   # maximum number of frequent words to show
        self.num_words = num_words
        self.port = None
        self.file_path = 'translations.json'
        self.frequent_words_path = None
        self.frequent_words = []
        self.display_path = None
        self._load_words()
        # The following is all needed to keep track of the display state
        self.english_words = []   # words displayed in English
        self.german_words = []    # words displayed in German
        self.english_order = []   # order of English words to display
        self.german_order = []    # order of German words to display
        self.working_set = []     # dictionary indices of words currently on display

    def set_port(self, port):
        self.port = port
        self.frequent_words_path = f'frequent_words_{port}.json'
        self._load_frequent_words()
        self.display_path = f'display_{port}.json'
        self._initialize()

    def _load_frequent_words(self):
        # check if self.frequent_works_path exists
        if self.frequent_words_path is not None and os.path.exists(self.frequent_words_path):
            with open(self.frequent_words_path, 'r', encoding='utf-8') as file:
                self.frequent_words = json.load(file)
        else:
            self.frequent_words = []

    def get_words(self, english_index=None, german_index=None, click_type='single'):
        # We always start from the stored set
        self._initialize()
        if english_index is None:
            # Do nothing. We'll just return the last stored display
            pass
        elif self.english_order[english_index] == self.german_order[german_index]:
            # Correct guess on single click, so make the words grey
            if click_type == 'single':
                color = 'lightgrey'
                self._bump_correct_count(self.working_set[self.english_order[english_index]])
            else:
                color = 'lightblue'
                self._put_into_frequent_words(self.working_set[self.english_order[english_index]])
            self.english_words[english_index]['color'] = color
            self.german_words[german_index]['color'] = color
            if self._all_grey() or english_index is None:
                self._make_new_display_words()
        else:
            # Incorrect guess, so color the words red
            self.english_words[english_index]['color'] = 'red'
            self.german_words[german_index]['color'] = 'red'
        self._save_display()
        return self.english_words, self.german_words

    def _all_grey(self):
        for word in self.english_words:
            if word['color'] != 'lightgrey' and word['color'] != 'lightblue':
                return False
        return True

    def _get_entry_from_frequent_words(self, translations_index):
        for i, entry in enumerate(self.frequent_words):
            if entry['translations_index'] == translations_index:
                return i
        return None

    def _get_frequent_words_to_show(self):
        # first, count down all of the display counters
        for entry in self.frequent_words:
            entry['display_count_down'] -= 1
        # Next, order the frequent words by display_count_down low to high
        self.frequent_words.sort(key=lambda x: x['display_count_down'])
        frequent_words_to_show = []
        for freq_word in self.frequent_words:
            if freq_word['display_count_down'] <= 0:
                freq_word['display_count_down'] = self.delay
                frequent_words_to_show.append(freq_word['translations_index'])
            if len(frequent_words_to_show) >= self.max_frequent:
                break
        self._save_frequent_words()
        return frequent_words_to_show

    def _save_frequent_words(self):
        with open(self.frequent_words_path, 'w', encoding='utf-8') as file:
            json.dump(self.frequent_words, file, ensure_ascii=False, indent=4)

    def _bump_correct_count(self, translations_index):
        print(f"bump correct count for {translations_index}")
        entry_index = self._get_entry_from_frequent_words(translations_index)
        if entry_index is not None:
            print(f"bump correct count for {translations_index} at index {entry_index}")
            self.frequent_words[entry_index]['correct_count'] += 1
            if self.frequent_words[entry_index]['correct_count'] > self.purge:
                self.frequent_words.pop(entry_index)
            self._save_frequent_words()

    def _put_into_frequent_words(self, translations_index):
        ''' This adds the word if it isn't in frequent_words, and
            updates the counters if it is.
        '''
        entry = {'translations_index': translations_index,
                 'display_count_down': self.delay,
                 'correct_count': 0}
        entry_index = self._get_entry_from_frequent_words(translations_index)
        if entry_index is not None:
            self.frequent_words[entry_index] = entry
        else:
            self.frequent_words.append(entry)
        self._save_frequent_words()

    def _initialize(self):
        if os.path.exists(self.display_path):
            with open(self.display_path, 'r', encoding='utf-8') as file:
                display = json.load(file)
                self.english_order = display['english_order']
                self.german_order = display['german_order']
                self.working_set = display['working_set']
                self.english_words = display['english_words']
                self.german_words = display['german_words']
        else:
            self._make_new_display_words()

    def _save_display(self):
        display = {'english_order': self.english_order,
                   'german_order': self.german_order,
                   'working_set': self.working_set,
                   'english_words': self.english_words,
                   'german_words': self.german_words}
        with open(self.display_path, 'w', encoding='utf-8') as file:
            json.dump(display, file, ensure_ascii=False, indent=4)

    def _make_new_display_words(self):
        # working_set is the set of indices of words currently on display
        self.working_set = self._assign_initial_words()
        # english_order and german_order are indices into working_set and
        # are in the order in which the words will be displayed
        frequent_words = self._get_frequent_words_to_show()
        print(f"freq words: {frequent_words}")
        # This substitutes some regular words for frequent words
        for i, freq_word in enumerate(frequent_words):
            print(f"Add frequent word: {freq_word} at index {i}")
            self.working_set[i] = freq_word
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
        self._save_display()

    def _load_words(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            self.words = json.load(file)

    def _assign_initial_words(self):
        # Get a random set of indexes to select words from
        initial_words = []
        candidates = random.sample(range(len(self.words)), self.num_words + len(self.frequent_words) + 10)
        for translations_index in candidates:
            if self._get_entry_from_frequent_words(translations_index) is None:
                initial_words.append(translations_index)
            if len(initial_words) >= self.num_words:
                return initial_words
