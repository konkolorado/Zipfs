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
    en = wikipedia_language(5, "https://en.wikipedia.org/wiki/Bogosort", False)
    es = wikipedia_language(84, "https://es.wikipedia.org/wiki/Bogosort", False)
    fr = wikipedia_language(497, "https://fr.wikipedia.org/wiki/Tri_stupide", False)
    de = wikipedia_language(490, "https://de.wikipedia.org/wiki/Bogosort", False)
    rand = random_language(1000000)

    loglangs([en, es, fr, de, rand])

def wikipedia_language(num_pages, start_url, wrangle, graph=False):
    wrangler = WordWrangler(num_pages, start_url)
    if wrangle:
        wrangler.begin_wrangling()
        wrangler.save_progress()
    sorted_words = sort_by_frequency(wrangler.words)
    words, frequencies = split_sorted(sorted_words)
    if graph:
        graph_it(10, words, frequencies)
    return words, frequencies

def random_language(num_words, graph=False):
    random_words = make_random(num_words, "abcdefghijklmnopqrstuvwxyz")
    rand_sorted_words = sort_by_frequency(random_words)
    rand_w, rand_f = split_sorted(rand_sorted_words)
    if graph:
        graph_it(10, rand_w, rand_f)
    return rand_w, rand_f

def sort_by_frequency(d):
    """
    given a dictionary containing word:freq info, sort on freq value
    """
    return sorted(d.items(), key=operator.itemgetter(1), reverse=True)

def split_sorted(ls):
    """
    given a list of tuples, returns 2 lists containing the tuple
    info in a 1-to-1 correspondence
    """
    return zip(*ls)

def graph_it(num_items, x_items, y_items):
    fig, ax = plt.subplots()
    index = np.arange(num_items)
    bar_width = 0.5
    opacity = 0.4

    rects1 = plt.bar(index + bar_width / 2, y_items[:num_items], bar_width,
                     alpha=opacity, color='b', label='words')

    plt.xlabel('rank')
    plt.ylabel('frequency')
    plt.title('distribution of words on wikipedia')
    plt.xticks(index + bar_width, x_items[:num_items])
    plt.show()

def loglog(num_items, x_items, y_items):
    fig, ax = plt.subplots()
    bar_width = 0.5
    opacity = 0.4

    plt.xlabel('log(rank)')
    plt.ylabel('log(frequency)')
    plt.title('distribution of words on wikipedia')
    xs = range(1, len(x_items)+1)
    plt.scatter(np.log2(xs), np.log2(y_items), s=100, c='b', alpha=0.5)
    plt.show()

def plotlogs(x_items, y_items, color):
    xs = range(1, len(x_items)+1)
    plt.scatter(np.log10(xs), np.log10(y_items), s=10, c=color, alpha=0.5)

def loglangs(langs_list):
    """
    parameters: a list of language tuples: [ (words, frequencies), ...]
    plots language statistics
    """
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    if len(colors) < len(langs_list):
        print "not enough colors for each lang, reduce langs"
        return

    plt.xlabel("log(rank)")
    plt.ylabel("log(frequency)")
    plt.title("distribution of words in various languages on wikipedia")

    for lang in langs_list:
        words, freqs = lang
        plotlogs(words, freqs, colors.pop())
    plt.show()

def make_random(v_size, alphabet):
    """
    given a string of alphabet characters, produce a random vocabulary
    of words of size v_size. a white space char indicates the end of
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
        if let == " " and len(word) > 0:
            return word
        if let == " ":
            continue
        else:
            word += let

if __name__ == '__main__':
    main()
