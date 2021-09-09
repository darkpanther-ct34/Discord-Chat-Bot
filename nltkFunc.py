import nltk
import numpy as np

# nltk.download('punkt')
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()


def tokenize(sentance):
    return nltk.word_tokenize(sentance)


def stem(word):
    return stemmer.stem(word.lower())


def bagofwords(tokenizedsentance, allwords):
    tokenizedsentance = [stem(w) for w in tokenizedsentance]
    bag = np.zeros(len(allwords), dtype=np.float32)
    for idx, w in enumerate(allwords):
        if w in tokenizedsentance:
            bag[idx] = 1.0
    return bag
