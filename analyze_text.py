from __future__ import division

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from string import punctuation
import csv
import re
import json
from collections import defaultdict

JSON_FILE = 'scrapespn/items.json'

white_presidents = set(['bush','clinton','reagan','carter','ford','nixon','kennedy',    
                        'eisenhower','truman','roosevelt','coolidge','taft'])
non_white_presidents = set(['obama'])

all_presidents = white_presidents.union(non_white_presidents)
president_firsts = set(['george','bill','ronald','jimmy','gerald','richard','john','dwight','harry','theodore','teddy',
                        'franklin','calvin','william','barack'])

# regex to find president names in text
rgx = re.compile(r"\b(" + "|".join([p for p in all_presidents]) + r")\b",re.I)

items = json.loads(open(JSON_FILE).read())

def presidents_and_bucket(text):
    """given some text, find which presidents it mentions and bucket it accordingly"""
    presidents = set([p.lower() for p in rgx.findall(text)])
    has_white_president = any([p in white_presidents for p in presidents])
    has_non_white_president = any([p in non_white_presidents for p in presidents])
    if has_white_president and has_non_white_president:
        bucket = 'both'
    elif has_white_president:
        bucket = 'white'
    elif has_non_white_president:
        bucket = 'non-white'
    else:
        bucket = 'none'
        
    return presidents, bucket

buckets = ['white','non-white','both','none']
words = defaultdict(dict)
num_sentences = defaultdict(int)
capitals = {}
    
for item in items:
    for sentence in sent_tokenize(item["text"]):
        presidents,bucket = presidents_and_bucket(sentence)
        num_sentences[bucket] += 1
        cased_words = word_tokenize(sentence)
        unique_words = set([w.lower() for w in cased_words])
        for word in unique_words:
            words[word][bucket] = words[word].get(bucket,0) + 1
        for cased_word in cased_words[1:]:
            word = cased_word.lower()
            c,l = capitals.get(word,(0,0))
            if cased_word[0] == cased_word[0].upper():
                c += 1
            else:
                l += 1
            capitals[word] = (c,l)

def is_proper(word):
    c,l = capitals.get(word,(0,1))
    return c > l

my_stopwords = set(stopwords.words('english'))
word_regex = re.compile("^[a-z]+$",re.I)

# don't want words that only occur in 'none' sentences, or proper nouns, or stopwords
either_words = [(w,d) 
                for w,d in words.iteritems()
                if any([d.get(x,0) > 0 for x in ['white','non-white','both']])
                and w not in my_stopwords
                and not is_proper(w)
                and w not in all_presidents
                and w not in president_firsts
                and word_regex.match(w)]

white_pct = {}
non_white_pct = {}

# a little bit of smoothing, so that a word that gets used only once won't be at the top
SMOOTHER = 0.5

for word, counts in either_words:
    white_freq = counts.get('white',0) + counts.get('both',0) + SMOOTHER
    non_white_freq = counts.get('non-white',0) + counts.get('both',0) + SMOOTHER
    white_frac = 1.0 * white_freq / (num_sentences['white'] + num_sentences['both'])
    non_white_frac = 1.0 * non_white_freq / (num_sentences['non-white'] + num_sentences['both'])
    sum_frac = white_frac + non_white_frac
    white_pct[word] = (white_frac / sum_frac,white_freq)
    non_white_pct[word] = (non_white_frac / sum_frac,non_white_freq)

print "most-white words:"
for w,pct in sorted(white_pct.iteritems(),key=lambda (w,pct): pct, reverse=True)[:25]:
    ratio = pct[0] / (1 - pct[0])
    d = words[w]
    white = d.get('white',0)
    non_white = d.get('non-white',0)
    both = d.get('both',0)
    print w,ratio,white,non_white,both

print "most-non-white words:"
for w,pct in sorted(non_white_pct.iteritems(),key=lambda (w,pct): pct, reverse=True)[:25]:
    ratio = pct[0] / (1 - pct[0])
    d = words[w]
    white = d.get('white',0)
    non_white = d.get('non-white',0)
    both = d.get('both',0)
    print w,ratio,non_white,white,both