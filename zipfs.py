"""
Using a wikipedia crawler, examines words frequencies to see
if they follow a Zipfian relationship
"""
from wordwrangler import WordWrangler

import matplotlib.pyplot as plt

import operator
import numpy as np
import random

def main():
    wikipedia_language(5, "https://en.wikipedia.org/wiki/Bogosort", False)
    wikipedia_language(84, "https://es.wikipedia.org/wiki/Bogosort", False)
    wikipedia_language(497, "https://fr.wikipedia.org/wiki/Tri_stupide", False)
    wikipedia_language(490, "https://de.wikipedia.org/wiki/Bogosort", False)

    # TODO
    # find other ways to display data
    # figure out if randomlang follows Zipfian Distribution

def wikipedia_language(num_pages, start_url, wrangle):
    wrangler = WordWrangler(num_pages, start_url)
    if wrangle:
        wrangler.begin_wrangling()
        wrangler.save_progress()
    sorted_words = sort_by_frequency(wrangler.words)
    words, frequencies = split_sorted(sorted_words)
    graph_it(10, words, frequencies)

def random_language():
    random_words = make_random(500000, "abcdefghijklmnopqrstuvwxyz")
    rand_sorted_words = sort_by_frequency(random_words)
    rand_w, rand_f = split_sorted(rand_sorted_words)
    graph_it(10, rand_w, rand_f)

def sort_by_frequency(d):
    """
    Given a dictionary containing word:freq info, sort on freq value
    """
    return sorted(d.items(), key=operator.itemgetter(1), reverse=True)

def split_sorted(ls):
    """
    Given a list of tuples, returns 2 lists containing the tuple
    info in a 1-to-1 correspondence
    """
    return zip(*ls)

def graph_it(num_items, x_items, y_items):
    fig, ax = plt.subplots()
    index = np.arange(num_items)
    bar_width = 0.5
    opacity = 0.4

    rects1 = plt.bar(index + bar_width / 2, y_items[:num_items], bar_width,
                     alpha=opacity, color='b', label='Words')

    plt.xlabel('Words')
    plt.ylabel('Frequencies')
    plt.title('Distribution of words on wikipedia')
    plt.xticks(index + bar_width, x_items[:num_items])
    plt.show()

def loglog(num_items, x_items, y_items):
    fig, ax = plt.subplots()
    index = np.arange(num_items)
    bar_width = 0.5
    opacity = 0.4

    plt.xlabel('Word rank (log)')
    plt.ylabel('Frequency (log)')
    plt.title('Distribution of words on wikipedia')
    xs = range(len(x_items))
    plt.scatter(np.log10(xs), np.log10(y_items), s=100, c='b', alpha=0.5)
    plt.show()

def make_random(v_size, alphabet):
    """
    Given a string of alphabet characters, produce a random vocabulary
    of words of size v_size. A white space char indicates the end of
    a word
    """
    random_words = {}
    for i in range(v_size):
        word = make_word(alphabet)
        random_words[word] = random_words.get(word, 0) + 1
    return random_words

def make_word(alphabet):
    alphabet += " "
    word = ""
    while True:
        let = random.choice(alphabet)
        if let == " " and word != "":
            return word
        if let == " ":
            continue
        else:
            word += let

if __name__ == '__main__':
    main()
