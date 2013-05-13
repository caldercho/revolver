#Splits your article into 6 important bullets

# coding=UTF-8
from __future__ import division
import re
import sys
from goose import Goose
import heapq

# This is a naive text summarization algorithm
# Created by Shlomi Babluki
# April, 2013


class SummaryTool(object):

    # Naive method for splitting a text into sentences
    def split_content_to_sentences(self, content):
        content = content.replace("\n", ". ")
        return content.split(". ")

    # Naive method for splitting a text into paragraphs
    def split_content_to_paragraphs(self, content):
        return content.split("\n\n")

    # Caculate the intersection between 2 sentences
    def sentences_intersection(self, sent1, sent2):

        # split the sentence into words/tokens
        s1 = set(sent1.split(" "))
        s2 = set(sent2.split(" "))

        # If there is not intersection, just return 0
        if (len(s1) + len(s2)) == 0:
            return 0

        # We normalize the result by the average number of words
        return len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)

    # Format a sentence - remove all non-alphbetic chars from the sentence
    # We'll use the formatted sentence as a key in our sentences dictionary
    def format_sentence(self, sentence):
        sentence = re.sub(r'\W+', ' ', sentence)
        return sentence

    # Convert the content into a dictionary <K, V>
    # k = The formatted sentence
    # V = The rank of the sentence
    def get_sentences_ranks(self, content):

        # Split the content into sentences
        sentences = self.split_content_to_sentences(content)

        print "this many sentenes ", len(sentences)

        # Calculate the intersection of every two sentences
        n = len(sentences)
        values = [[0 for x in xrange(n)] for x in xrange(n)]
        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = self.sentences_intersection(sentences[i], sentences[j])

        # Build the sentences dictionary
        # The score of a sentences is the sum of all its intersection
        sentences_dic = {}
        for i in range(0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score += values[i][j]
            sentences_dic[sentences[i]] = score
        return sentences_dic

    # Return the best sentence in a paragraph
    def get_best_sentences(self, sentences_dic):
        def dict_nlargest(d,n):
            return heapq.nlargest(n ,d, key = lambda k: d[k])
        top_sentences = dict_nlargest(sentences_dic, 6)

        for x in sentences_dic:
            print sentences_dic[x]


        return top_sentences



# Main method, just run "python summary_tool.py"
def main():

    
    url = sys.argv[1]
    article = Goose({'browser_user_agent': 'Mozilla'}).extract(url=url)
    title = article.title
    content = article.cleaned_text



    # Create a SummaryTool object
    st = SummaryTool()

    # Build the sentences dictionary
    sentences_dic = st.get_sentences_ranks(content)

    # Build the summary with the sentences dictionary
    summary = st.get_best_sentences(sentences_dic)

    # Print the summary
    for x in summary:
        print x



if __name__ == '__main__':
    main()
