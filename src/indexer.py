# indexer.py
from collections import defaultdict

class Indexer:
    def __init__(self):
        self.forward_index = {}
        self.inverted_index = defaultdict(dict)  # {word_id: {doc_id: freq}}

    def add_to_forward_index(self, doc_id, token_ids):
        token_freq = {}
        for token_id in token_ids:
            token_freq[token_id] = token_freq.get(token_id, 0) + 1
        self.forward_index[doc_id] = token_freq

    def build_inverted_index(self):
        for doc_id, tokens in self.forward_index.items():
            for token_id, freq in tokens.items():
                self.inverted_index[token_id][doc_id] = freq
