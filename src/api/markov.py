import os
import random

from .const import MAX_LENGTH
from .graph import WordGraph

def create_training_set(dir):
    training_set = ''
    for filename in os.listdir(dir):
        file = os.path.join(dir, filename)

        assert os.path.isfile(file)
        assert filename[-4:] == '.txt'

        with open(file, 'r') as f:
            line = f.read()
            training_set += line.lower()

    # clean data
    training_set = training_set.replace('\n',' ')
    training_set = training_set.replace('\t',' ')
    training_set = training_set.replace('“', ' ')
    training_set = training_set.replace('”', ' ')
    training_set = training_set.replace('(', ' ')
    training_set = training_set.replace(')', ' ')

    for spaced in ['.', '-', ',', '!', '?', '(', '—', ')']:
        training_set = training_set.replace(spaced, f' {spaced} ')

    training_set = training_set.split(' ')

    return training_set

def build_word_graph(training_set):
    size = len(training_set)
    word_graph = WordGraph.get_instance()

    i = 0
    while i < size - 1:
        word = training_set[i]
        next_word = training_set[i + 1]
        word_graph.add(word, next_word)
        i += 1
    word_graph.save()
    return word_graph

def build_two_word_graph(training_set):
    size = len(training_set)
    word_graph = WordGraph.get_instance()

    i = 0
    prev_word = None
    while i < size - 1:
        word = training_set[i]
        next_word = training_set[i + 1]

        if prev_word is None: word_graph.add(word, next_word)
        else: word_graph.add(f'{prev_word} {word}', next_word)

        prev_word = word
        i += 1
    word_graph.save()
    return word_graph

def generate_tweet(word_graph, prompt):
    tweet = [prompt]

    while prompt != '.' or len(tweet) < MAX_LENGTH:
        options = word_graph.get(prompt)
        words, weights = options.get_dist()

        if len(words) > 0:
            prompt = random.choices(words, weights=weights, k=1)[0]

            if len(tweet) > 20:
                last_two_words = ' '.join(tweet[-2:])
                print(last_two_words)
                two_word_options = word_graph.get(last_two_words, silent_fail=False)
                strong_words, strong_weights = two_word_options.get_dist()

                if prompt not in words:
                    prompt = random.choices(words, weights=weights, k=1)[0]
            tweet.append(prompt)
        else: break

    tweet = ' '.join(tweet)
    return tweet

def load_stored_response(tweet_text):
    """Building custom responses based on stored content."""

    word_graph = WordGraph.load()

    response = generate_tweet(word_graph, prompt='somebody')
    return response
