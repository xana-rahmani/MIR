import csv
import string
import nltk
import xml.etree.ElementTree as ET
from hazm import *

English_stop_words_level1 = ['an', 'and', 'for', 'that', 'the', 'with', 'he', 'in', 'can', 'from', 'a', 'to', 'of',
                             'it', 'talk', 'how', 'you', 'thi', 'about', 'we', 'what', 'on', 'as', 'hi', 'is', 'us',
                             'our', 'at']
English_stop_words_level2 = ['do', 'her', 'be', 'but', 'by', 'she', 'are']

Persian_stop_words_level1 = ['را', 'با', 'به', 'و', 'آن', 'که', 'از', 'این', 'بر', 'در', 'یا', 'تا']
Persian_stop_words_level2 = ['اس', 'کرد', 'ایر', 'دو',  'یک', 'سال', 'نیز', 'بود', 'شد', 'خود', 'برا','دارد'  ,'']


def prepare_text(text, lang="en"):
    tokens = []
    if lang == "en":
        stemmer = nltk.stem.porter.PorterStemmer()
        tokens = nltk.word_tokenize(text)
        tokens = [stemmer.stem(t) for t in tokens]
        tokens = [tok for tok in tokens if tok not in string.punctuation]  # removing punctuations
        tokens = [t.lower() for t in tokens if t.isalpha()]  # removing punctuations
        tokens = [tok for tok in tokens if tok not in English_stop_words_level1 + English_stop_words_level2]
    elif lang == "fa":
        normalizer = Normalizer()
        punctuations = [']]', '[[', '[', ']', '؟', '!', '.', ',', '،', '?', ')', '(', ')', '(', '\n', '=','==', '===', '«',
                        '»',
                        '//www', 'http', '</ref>', '||', '<ref', '<ref>', 'name=', '|-', 'of', '–','|','-','\'','"']
        for punc in punctuations:
            text = text.replace(punc,' ')
        text = normalizer.normalize(text)
        tokens = word_tokenize(text)

        tokens = [tok.replace('\u200c', '').replace(' ', '') for tok in tokens if
                  tok not in punctuations and tok not in string.punctuation]
        tokens = [Stemmer().stem(t) for t in tokens]
        tokens = [tok for tok in tokens if tok not in Persian_stop_words_level1 + Persian_stop_words_level2]

    return tokens


def read_file_and_create_token(lang="en"):
    if lang == "en":
        english_tokens = {}
        with open('data/ted_talks.csv', encoding='utf-8') as csv_file:
            read_csv = csv.reader(csv_file)
            fields = next(read_csv)
            title_index = fields.index("title")
            description_index = fields.index("description")
            doc_id = 1
            english_token_repetition = {}
            number_of_tokens = 0
            for row in read_csv:
                title_tokens = prepare_text(text=row[title_index], lang="en")
                description_tokens = prepare_text(text=row[description_index], lang="en")
                english_tokens[doc_id] = {
                    "title_token": title_tokens,
                    "description": description_tokens
                }
                number_of_tokens += len(title_tokens) + len(description_tokens)
                for tok in title_tokens + description_tokens:
                    if tok not in english_token_repetition.keys():
                        english_token_repetition[tok] = 1
                    else:
                        english_token_repetition[tok] += 1
                doc_id += 1
        return english_tokens, english_token_repetition

    if lang == "fa":
        persian_tokens = {}
        persian_token_repetition = {}
        number_of_persian_tokens = 0
        root = ET.parse('data/Persian.xml').getroot()
        file_path = "{http://www.mediawiki.org/xml/export-0.10/}"
        persian_ids = [id_tag.text for id_tag in root.iter(file_path + 'id')]
        i = 1
        for title_tag in root.iter(file_path + 'title'):
            title_tokens = prepare_text(text=title_tag.text, lang="fa")
            number_of_persian_tokens += len(title_tokens)
            persian_tokens[i] = {
                "title_token": title_tokens,
            }
            for tok in title_tokens:
                if tok not in persian_token_repetition.keys():
                    persian_token_repetition[tok] = 1
                else:
                    persian_token_repetition[tok] += 1
            i += 1

        i = 1
        for text_tag in root.iter(file_path + 'text'):
            description_tokens = prepare_text(text=text_tag.text, lang="fa")
            number_of_persian_tokens += len(description_tokens)
            persian_tokens[i]["description"] = description_tokens
            for tok in description_tokens:
                if tok not in persian_token_repetition.keys():
                    persian_token_repetition[tok] = 1
                else:
                    persian_token_repetition[tok] += 1
            i += 1

        return persian_tokens, persian_token_repetition
