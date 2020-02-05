from nltk.cluster.util import cosine_distance
from nltk import sent_tokenize, word_tokenize
from operator import itemgetter
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import numpy as np
import nltk
import math
nltk.download('punkt')

def textrank(sentences, top_n, stopwords=None):

    S = build_similarity_matrix(sentences, stopwords)
    sentence_ranking = pagerank(S)

    # mengurutkan ranking kalimat
    ranked_sentence_indexes = [item[0] for item in sorted(enumerate(sentence_ranking), key=lambda item: -item[1])]
    # print("\nRANKED SENTENCE INDEXES")
    # print(ranked_sentence_indexes)

    selected_sentences = sorted(ranked_sentence_indexes[:top_n])
    # print("\nSELECTED SENTENCES")
    # print(selected_sentences)

    return selected_sentences


def pagerank(matrix, eps=0.0001, d=0.85):
    P = np.ones(len(matrix)) / len(matrix)
    while True:
        new_P = np.ones(len(matrix)) * (1 - d) / len(matrix) + d * matrix.T.dot(P)
        delta = abs(new_P - P).sum()
        if delta <= eps:
            return new_P
        P = new_P

def sentence_similarity(sent1, sent2, stopwords=None):

    if stopwords is None:
        stopwords = []

    all_words = list(set(sent1 + sent2))
    #print("\nALL WORDS")
    #print(all_words)

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    # membuat vector untuk kalimat pertama
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
    
    # membuat vector untuk kalimat kedua
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1

    #print("\nVECTOR1")
    #print(vector1)
    #print("\nVECTOR2")
    #print(vector2)
    
    # menghitung cosine similarity
    return 1 - cosine_distance(vector1, vector2) 
    

def build_similarity_matrix(sentences, stopwords=None):
    # membuat similarity matrix kosong
    S = np.zeros((len(sentences), len(sentences)))
    #print("\nMEMBUAT MATRIX SIMILARITY KOSONG")
    #print(S)

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i == j:
                continue

            S[i][j] = sentence_similarity(sentences[i], sentences[j], stopwords)
    
    #print("\nMATRIX SIMILARITY TERISI")
    #print(S)

    # normalisasi matrix
    for i in range(len(S)):
        S[i] /= S[i].sum()
    
    #print("\nNORMALISASI MATRIX")
    #print(S)

    return S

def process(req):  

    stemmer_factory = StemmerFactory()
    stemmer = stemmer_factory.create_stemmer()

    sw_factory = StopWordRemoverFactory()
    stopwords = sw_factory.get_stop_words()

    # sentence splitting
    st = sent_tokenize(req)
    # print("\nSENTENCE SPLITTING")
    # print(st)

    arr = [word_tokenize(stemmer.stem(sent)) for sent in st]
    #print("\nARRAY - TOKENIZING WORD SENTENCE")
    #print(arr)

    n = math.floor(len(st) / 4) # jumlah kalimat yang akan dihasilkan

    final_summ = []

    summary = itemgetter(*textrank(arr, n, stopwords))(st)
    for sentence in summary:
        final_summ.append(sentence)

    return (' '.join(final_summ))