import pickle
import string
from itertools import permutations
import collections

from bs4 import BeautifulSoup
import requests

def load_from_pkl_file(pkl_path):
    with open(pkl_path, 'rb') as file:
        data = pickle.load(file)

    return data

def generate_alphabet_elements():
    alphabet_elements = {}
    alphabet_elements['alphabet_list'] = list(string.ascii_lowercase)

    alphabet_elements['vowels'] = ['a','e','i','o','u']
    alphabet_elements['special_vowels'] = ['á','é','í','ó','ú','ü','ö']
    alphabet_elements['same_consecutive_vowels'] = ['aa','ee', 'ii', 'oo', 'uu']
    alphabet_elements['consecutive_vowels'] = [''.join(p) for p in permutations(alphabet_elements['vowels'],2)]

    alphabet_elements['consonants'] = [item for item in alphabet_elements['alphabet_list'] if item not in alphabet_elements['vowels']]
    alphabet_elements['consecutive_consonants'] = [''.join(p) for p in permutations(alphabet_elements['consonants'],2)]
    alphabet_elements['same_consecutive_consonants'] = [str(l) + str(l) for l in alphabet_elements['consonants']]

    return alphabet_elements

def create_features(dataframe, alph_elems):
    dataframe['word_count'] = dataframe['Sentences'].apply(lambda x : len(x.split()))
    dataframe['character_count'] = dataframe['Sentences'].apply(lambda x : len(x.replace(" ","")))
    dataframe['word_density'] = dataframe['word_count'] / (dataframe['character_count'] + 1)
    
    dataframe['num_double_consec_vowels'] = dataframe['Sentences'].apply(lambda x : sum([any(c_v in a for c_v in alph_elems['same_consecutive_vowels']) for a in x.split()]))
    dataframe['num_consec_vowels'] = dataframe['Sentences'].apply(lambda x : sum([any(c_v in a for c_v in alph_elems['consecutive_vowels']) for a in x.split()]))
    dataframe['num_vowels'] = dataframe['Sentences'].apply(lambda x : sum([any(v in a for v in alph_elems['vowels']) for a in x.split()]))
    dataframe['num_special_vowels'] = dataframe['Sentences'].apply(lambda x : sum([any(v in a for v in  alph_elems['special_vowels']) for a in x.split()]))

    dataframe['num_unique_words'] = dataframe['Sentences'].apply(lambda x: len(set(w for w in x.split())))
    dataframe['num_repeated_words'] = dataframe['Sentences'].apply(lambda x: len([w for w in collections.Counter(x.split()).values() if w > 1]))
    
    dataframe['num_any_special_character'] = dataframe['Sentences'].apply(lambda x : sum([any(not spc in sp for spc in  alph_elems['alphabet_list']) for sp in x.split()]))
    dataframe['num_consec_consonants'] = dataframe['Sentences'].apply(lambda x : sum([any(c_v in a for c_v in  alph_elems['consecutive_consonants']) for a in x.split()]))
    dataframe['num_double_consec_consonants'] = dataframe['Sentences'].apply(lambda x : sum([any(c_c in b for c_c in  alph_elems['same_consecutive_consonants']) for b in x.split()]))
    dataframe['num_consonants'] = dataframe['Sentences'].apply(lambda x : sum([any(c in aa for c in  alph_elems['consonants']) for aa in x.split()]))
    
    return dataframe

def load_url(url):

    req = requests.get(url)

    try:
        soup = BeautifulSoup(req.text, features="lxml")
    except Exception:
        soup = BeautifulSoup(req.text)

    html = soup.get_text()

    return html

def cleaning(html):

    filtered_text = html.replace("\t", "").replace("\r", "").replace("\n", "")

    return filtered_text

