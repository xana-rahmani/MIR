import csv
import string
import nltk
import xml.etree.ElementTree as ET
from hazm import *
# nltk.download()
english_stop_words = ['an', 'and', 'for', 'that', 'the', 'with', 'he', 'in', 'can', 'from', 'a', 'to', 'of', 'it', 'talk', 'how', 'you', 'thi', 'about', 'we', 'what', 'on', 'as', 'hi', 'is', 'us', 'our','at']
english_stop_words_level2 = ['do', 'her', 'be', 'but', 'by', 'she', 'are']
def prepare_text(text, lang="en"):

    if lang == "en":
        stemmer = nltk.stem.porter.PorterStemmer()
        #removing punctuations
        tokens = nltk.word_tokenize(text)
        tokens = [tok for tok in tokens if tok not in string.punctuation]
        tokens = [stemmer.stem(t) for t in tokens]
        tokens = [t.lower() for t in tokens if t.isalpha()]
        tokens = [tok for tok in tokens if tok not in english_stop_words + english_stop_words_level2]


    elif lang == "fa":
        normalizer = Normalizer()
        text = normalizer.normalize(text)
        tokens = word_tokenize(text)
        punctuations = [ '؟', '!', '.', ',', '،', '?', ')', '(', ')', '(', '\n']
        tokens = [tok for tok in tokens if tok not in punctuations and tok not in string.punctuation]
        tokens = [Stemmer().stem(t) for t in tokens]




    return tokens


def main():
    english_tokens = {}
    persian_tokens = {}
    with open('data/ted_talks.csv',encoding= 'utf-8') as csv_file:
        read_csv = csv.reader(csv_file)
        fields = next(read_csv)
        title_index = fields.index("title")
        description_index = fields.index("description")
        doc_id = 1
        token_repition = {}
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
                if tok not in token_repition.keys():
                    token_repition[tok] = 1
                else:
                    token_repition[tok] += 1
            doc_id += 1
        # Test
        print(english_tokens.get(1))
        print(english_tokens.get(2))
        print(english_tokens.get(3))
        print(english_tokens.get(4))
    ###persian
    persian_tokens = {}
    persian_token_repitition = {}
    number_of_persian_tokens = 0
    root = ET.parse('data/Persian.xml').getroot()
    persian_titles = [title_tag.text for title_tag in root.iter('{http://www.mediawiki.org/xml/export-0.10/}title')]
    persian_descriptions = [text_tag.text for text_tag in root.iter('{http://www.mediawiki.org/xml/export-0.10/}text')]
    persian_ids = [id_tag.text for id_tag in root.iter('{http://www.mediawiki.org/xml/export-0.10/}id')]
    for i in range(len(persian_titles)):
        title_tokens = prepare_text(text=persian_titles[i], lang="fa")
        description_tokens = prepare_text(text=persian_descriptions[i], lang="fa")
        persian_tokens[persian_ids[2 * i]] = {
            "title_token": title_tokens,
            "description": description_tokens
        }
        number_of_persian_tokens += len(title_tokens) + len(description_tokens)
        for tok in title_tokens + description_tokens:
            if tok not in persian_token_repitition.keys():
                persian_token_repitition[tok] = 1
            else:
                persian_token_repitition[tok] += 1

    print(persian_tokens['3014'])
    print(persian_tokens['107456'])

    print([t for t in persian_token_repitition.keys() if persian_token_repitition[t] > 0.0045 * number_of_tokens])



main()
