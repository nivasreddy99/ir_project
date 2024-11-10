# stemmer.py
class NewString:
    def __init__(self):
        self.str = ""

class PorterStemmer:
    def __init__(self):
        pass

    def clean(self, word):
        import re
        return re.sub(r'[^a-zA-Z]', '', word)

    def has_suffix(self, word, suffix, stem):
        if len(word) <= len(suffix):
            return False
        if word.endswith(suffix):
            stem.str = word[:-len(suffix)]
            return True
        return False

    def vowel(self, ch, prev):
        vowels = 'aeiou'
        if ch in vowels:
            return True
        if ch == 'y':
            return prev not in vowels
        return False

    def measure(self, stem):
        count = 0
        prev_vowel = False
        for i in range(len(stem)):
            if self.vowel(stem[i], stem[i - 1] if i > 0 else ''):
                if not prev_vowel:
                    count += 0.5  # Counting vowel sequences
                prev_vowel = True
            else:
                prev_vowel = False
        return int(count)

    def contains_vowel(self, stem):
        for i in range(len(stem)):
            if self.vowel(stem[i], stem[i - 1] if i > 0 else ''):
                return True
        return False

    def cvc(self, word):
        if len(word) < 3:
            return False
        if (not self.vowel(word[-1], word[-2]) and
                self.vowel(word[-2], word[-3]) and
                not self.vowel(word[-3], word[-4] if len(word) > 3 else '')):
            if word[-1] not in 'wxy':
                return True
        return False

    def step1a(self, word):
        if word.endswith('sses'):
            return word[:-2]
        elif word.endswith('ies'):
            return word[:-2]
        elif word.endswith('ss'):
            return word
        elif word.endswith('s'):
            return word[:-1]
        else:
            return word

    def step1b(self, word):
        stem = NewString()
        if self.has_suffix(word, 'eed', stem):
            if self.measure(stem.str) > 0:
                return word[:-1]
            else:
                return word
        elif (self.has_suffix(word, 'ed', stem) or self.has_suffix(word, 'ing', stem)):
            if self.contains_vowel(stem.str):
                word = stem.str
                if word.endswith(('at', 'bl', 'iz')):
                    return word + 'e'
                elif (word[-1:] == word[-2:-1] and word[-1:] not in 'lsz'):
                    return word[:-1]
                elif self.measure(word) == 1 and self.cvc(word):
                    return word + 'e'
                else:
                    return word
            else:
                return word
        else:
            return word

    def step1c(self, word):
        stem = NewString()
        if self.has_suffix(word, 'y', stem):
            if self.contains_vowel(stem.str):
                return stem.str + 'i'
            else:
                return word
        else:
            return word

    def step2(self, word):
        suffixes = {
            'ational': 'ate',
            'tional': 'tion',
            'enci': 'ence',
            'anci': 'ance',
            'izer': 'ize',
            'bli': 'ble',
            'alli': 'al',
            'entli': 'ent',
            'eli': 'e',
            'ousli': 'ous',
            'ization': 'ize',
            'ation': 'ate',
            'ator': 'ate',
            'alism': 'al',
            'iveness': 'ive',
            'fulness': 'ful',
            'ousness': 'ous',
            'aliti': 'al',
            'iviti': 'ive',
            'biliti': 'ble',
            'logi': 'log'
        }
        for key in suffixes:
            stem = NewString()
            if self.has_suffix(word, key, stem):
                if self.measure(stem.str) > 0:
                    return stem.str + suffixes[key]
                else:
                    return word
        return word

    def step3(self, word):
        suffixes = {
            'icate': 'ic',
            'ative': '',
            'alize': 'al',
            'iciti': 'ic',
            'ical': 'ic',
            'ful': '',
            'ness': ''
        }
        for key in suffixes:
            stem = NewString()
            if self.has_suffix(word, key, stem):
                if self.measure(stem.str) > 0:
                    return stem.str + suffixes[key]
                else:
                    return word
        return word

    def step4(self, word):
        suffixes = ['al', 'ance', 'ence', 'er', 'ic', 'able', 'ible', 'ant',
                    'ement', 'ment', 'ent', 'sion', 'tion', 'ou', 'ism', 'ate',
                    'iti', 'ous', 'ive', 'ize']
        for suffix in suffixes:
            stem = NewString()
            if self.has_suffix(word, suffix, stem):
                if self.measure(stem.str) > 1:
                    return stem.str
                else:
                    return word
        return word

    def step5a(self, word):
        stem = NewString()
        if word.endswith('e'):
            stem.str = word[:-1]
            if self.measure(stem.str) > 1:
                return stem.str
            elif self.measure(stem.str) == 1 and not self.cvc(stem.str):
                return stem.str
            else:
                return word
        else:
            return word

    def step5b(self, word):
        if self.measure(word) > 1 and word.endswith('ll'):
            return word[:-1]
        else:
            return word

    def stem(self, word):
        word = word.lower()
        word = self.clean(word)
        if len(word) <= 2:
            return word
        word = self.step1a(word)
        word = self.step1b(word)
        word = self.step1c(word)
        word = self.step2(word)
        word = self.step3(word)
        word = self.step4(word)
        word = self.step5a(word)
        word = self.step5b(word)
        return word
