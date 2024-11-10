# stopword_finder.py
class StopWordFinder:
    def __init__(self, stopword_file='../stopwords.txt'):
        self.stopwords = set()
        with open(stopword_file, 'r') as f:
            for line in f:
                self.stopwords.add(line.strip())

    def is_stopword(self, word):
        return word in self.stopwords
