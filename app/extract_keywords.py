from nltk.cluster.util import cosine_distance
from nltk import sent_tokenize, word_tokenize
from operator import itemgetter
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import numpy as np
import nltk
import math
nltk.download('punkt')

def extract_keywords(req):

    stemmer_factory = StemmerFactory()
    stemmer = stemmer_factory.create_stemmer()

    sw_factory = StopWordRemoverFactory()
    stopwords = sw_factory.get_stop_words()

    # sentence splitting
    arr = word_tokenize(req)

    

    print(arr)

    return "wow"