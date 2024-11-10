# tokenizer.py
import re
from stemmer import PorterStemmer
from stopword_finder import StopWordFinder

class Tokenizer:
    def __init__(self, stopword_file=r'C:\Users\src\Downloads\ir_project\stopwords.txt'):
        self.stemmer = PorterStemmer()
        self.stopword_finder = StopWordFinder(stopword_file)
        self.word_dictionary = {}
        self.word_id_counter = 1
        self.file_dictionary = {}
        self.file_id_counter = 1

    def tokenize(self, text):
        # Remove numbers and words containing numbers
        tokens = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        processed_tokens = []
        for token in tokens:
            if not self.stopword_finder.is_stopword(token):
                stemmed_token = self.stemmer.stem(token)
                processed_tokens.append(stemmed_token)
        return processed_tokens

    def add_to_word_dictionary(self, tokens):
        for token in tokens:
            if token not in self.word_dictionary:
                self.word_dictionary[token] = self.word_id_counter
                self.word_id_counter += 1

    def add_to_file_dictionary(self, doc_name):
        if doc_name not in self.file_dictionary:
            self.file_dictionary[doc_name] = self.file_id_counter
            self.file_id_counter += 1
