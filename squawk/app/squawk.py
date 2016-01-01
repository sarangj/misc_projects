import re
from collections import defaultdict
import random

class Squawk(object):

    def __init__(self, speaker, words):
        self.speaker = speaker
        self.words = words

    def generate_vocab(self):

        doc = []
        regex = r"[\w']+|[\.\?]"
        all_words = re.findall(regex, self.words)
        doc.extend(all_words)

        return doc

    def generate_word_order(self, doc):

        trigrams = zip(doc, doc[1:], doc[2:])
        trigram_transitions = defaultdict(list)
        starts = []

        for prev, current, next in trigrams:
            if prev in ['.', '?']:
                starts.append(current)
            trigram_transitions[(prev, current)].append(next)

        return starts, trigram_transitions

    def _clean_output(self, sentence):

        contractions = [("dont", "don't"), ("wont", "won't"), ("theyre", "they're"),
                        ("theyll", "they'll"), ("Im", "I'm"), ("Id", "I'd"), ("Ive", "I've"),
                        ("Ill", "I'll"), ("lets", "let's"), ("isnt", "isn't"),
                        ("didnt", "didn't"), ("doesnt", "doesn't"), ("youre", "you're"),
                        ("youll", "you'll"), ("thats", "that's"), ("whats", "what's"),
                        ("theyve", "they've"), ("hes", "he's"), ("youve", "you've"),
                        ("weve", "we've")]
        for old, new in contractions:
            if old in sentence.split():
                sentence = sentence.replace(old, new)

        sentence = sentence[0:-2] + sentence[-1]  # remove space before punctuation mark
        sentence = '"' + sentence + '"'
        return sentence

    def generate_using_trigrams(self, starts, trigram_transitions):

        current = random.choice(starts)
        prev = '.'
        result = [current]
        while True:
            next_word_candidates = trigram_transitions[(prev, current)]
            next_word = random.choice(next_word_candidates)

            prev, current = current, next_word
            result.append(current)

            if current in ['.', '?']:
                try:
                    return self._clean_output(' '.join(result))
                except IndexError:
                    return 'Oops. Chief Squawk says try again.'
