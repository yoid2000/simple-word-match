import json
import random
import os

class WordManager:
    def __init__(self, num_words=10):
        self.delay = 5   # don't show frequent word again for this many rounds
        self.purge = 3   # remove from frequent words if correct this many times
        self.max_frequent = 3   # maximum number of frequent words to show
        self.num_words = num_words
        self.file_path = os.path.join(os.path.dirname(__file__), 'translations.json')
        self.frequent_words_path = os.path.join(os.path.dirname(__file__), 'frequent_words.json')
        self.frequent_words = []
        self.english_words = []   # words displayed in English
        self.german_words = []    # words displayed in German
        self.english_order = []   # order of English words to display
        self.german_order = []    # order of German words to display
        self.working_set = []     # dictionary indices of words currently on display
        self._load_words()
        self._load_frequent_words()
        self._make_new_display_words()
    def _load_frequent_words(self):
        if os.path.exists(self.frequent_words_path):
            with open(self.frequent_words_path, 'r', encoding='utf-8') as file:
                self.frequent_words = json.load(file)
        else:
            self.frequent_words = []

    def _save_frequent_words(self):
        with open(self.frequent_words_path, 'w', encoding='utf-8') as file:
            json.dump(self.frequent_words, file, ensure_ascii=False, indent=4)

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

    def _bump_correct_count(self, translations_index):
        entry_index = self._get_entry_from_frequent_words(translations_index)
        if entry_index is not None:
            self.frequent_words[entry_index]['correct_count'] += 1
            if self.frequent_words[entry_index]['correct_count'] > self.purge:
                self.frequent_words.pop(entry_index)
            self._save_frequent_words()

    def _put_into_frequent_words(self, translations_index):
        entry = {'translations_index': translations_index,
                 'display_count_down': self.delay,
                 'correct_count': 0}
        entry_index = self._get_entry_from_frequent_words(translations_index)
        if entry_index is not None:
            self.frequent_words[entry_index] = entry
        else:
            self.frequent_words.append(entry)
        self._save_frequent_words()

    def _load_words(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            self.words = json.load(file)
        # Add English words if missing
        for i, entry in enumerate(self.words):
            if 'english' not in entry:
                entry['english'] = f'Word {i+1}'

    def get_words(self, english_index=None, german_index=None, click_type='single'):
        if english_index is None or german_index is None:
            return self.english_words, self.german_words
        if not self.working_set or not self.english_order or not self.german_order:
            return self.english_words, self.german_words
        if self.english_order[english_index] == self.german_order[german_index]:
            # Correct match
            if click_type == 'single':
                color = 'lightgrey'
                self._bump_correct_count(self.working_set[self.english_order[english_index]])
            else:
                color = 'lightblue'
                self._put_into_frequent_words(self.working_set[self.english_order[english_index]])
            # Always set both to correct color, even if previously red
            self.english_words[english_index]['color'] = color
            self.german_words[german_index]['color'] = color
            if self._all_grey():
                self._make_new_display_words()
        else:
            # Incorrect match
            self.english_words[english_index]['color'] = 'red'
            self.german_words[german_index]['color'] = 'red'
        # After a correct match, ensure all pairs that are correct are grey/blue, not red
        for i, word in enumerate(self.english_words):
            if self.english_order[i] == self.german_order[i]:
                if word['color'] == 'red':
                    word['color'] = 'lightgrey'
        for i, word in enumerate(self.german_words):
            if self.german_order[i] == self.english_order[i]:
                if word['color'] == 'red':
                    word['color'] = 'lightgrey'
        return self.english_words, self.german_words

    def _all_grey(self):
        for word in self.english_words:
            if word['color'] != 'lightgrey' and word['color'] != 'lightblue':
                return False
        return True

    def _make_new_display_words(self):
        self.working_set = self._assign_initial_words() or []
        # Insert frequent words
        frequent_words = self._get_frequent_words_to_show()
        if self.working_set:
            for i, freq_word in enumerate(frequent_words):
                if i < len(self.working_set):
                    self.working_set[i] = freq_word
        self.english_order = [i for i in range(self.num_words)]
        random.shuffle(self.english_order)
        self.german_order = [i for i in range(self.num_words)]
        random.shuffle(self.german_order)
        self.english_words = []
        for i in self.english_order:
            if self.working_set and i < len(self.working_set):
                self.english_words.append({'color': 'black', 'word': self.words[self.working_set[i]].get('english', f'Word {i+1}')})
            else:
                self.english_words.append({'color': 'black', 'word': f'Word {i+1}'})
        self.german_words = []
        for i in self.german_order:
            if self.working_set and i < len(self.working_set):
                self.german_words.append({'color': 'black', 'word': self.words[self.working_set[i]]['german']})
            else:
                self.german_words.append({'color': 'black', 'word': f'German {i+1}'})

    def _assign_initial_words(self):
        initial_words = []
        if not hasattr(self, 'words') or not self.words:
            return []
        candidates = random.sample(range(len(self.words)), min(self.num_words + 10, len(self.words)))
        for translations_index in candidates:
            initial_words.append(translations_index)
            if len(initial_words) >= self.num_words:
                return initial_words
        return initial_words
