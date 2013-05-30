# coding=UTF-8
from __future__ import division
import heapq
from goose import Goose
import sys

from nltk import word_tokenize, sent_tokenize


class Revolver():
    def __init__(self, url):
        self.url = url
        self.article = Goose({'browser_user_agent': 'Mozilla'}).extract(url=self.url)
        self.title = self.article.title
        self.content = self.article.cleaned_text

    def split_into_sentences(self, text):
        return sent_tokenize(text)

    def split_into_unique_words(self, text):
        return set(word_tokenize(text))

    def calculate_intersection(self, sentence1, sentence2):
        # Split sentences into words
        words1 = self.split_into_unique_words(sentence1)
        words2 = self.split_into_unique_words(sentence2)

        # Automatic 0 for sentences without length
        if (len(words1) + len(words2)) == 0:
            return 0
        # Normalize for sentence length - may need to tweak here
        intersection = len(words1.intersection(words2)) / ((len(words1) + len(words2)) / 2)

        return intersection


    def sentence_ranks(self, content):
        sentences = self.split_into_sentences(content)

        # Find intersection values for each sentence combination
        n = len(sentences)
        values = [[0 for x in xrange(n)] for x in xrange(n)]
        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = self.calculate_intersection(sentences[i], sentences[j])

        # Dict of sentence keys and summed score values
        sentences_dict = {}
        for i in range (0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score += values[i][j]
            sentences_dict[sentences[i]] = score
        return sentences_dict

    def get_best_sentences(self, sentences_dict):
        def dict_nlargest(d,n):
            return heapq.nlargest(n, d, key=lambda k: d[k])
        return dict_nlargest(sentences_dict, 5)

    @property
    def bullets(self):
        sentences_dict = self.sentence_ranks(self.content)
        bullets = self.get_best_sentences(sentences_dict)
        return bullets

def main():
    revolver = Revolver(sys.argv[1])
    print revolver.title
    for bullet in revolver.bullets:
        print "--> ", bullet

if __name__ == '__main__':
    main()

