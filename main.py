import csv
import string
import nltk
# nltk.download()


def prepare_text(text, lang="en"):
    stemmer = nltk.stem.porter.PorterStemmer()
    if lang == "en":
        tokens = nltk.word_tokenize(text)
        tokens = [t.lower() for t in tokens if t.isalpha()]
        tokens = [stemmer.stem(t) for t in tokens]
    return tokens


def main():
    with open('data/ted_talks.csv') as csv_file:
        read_csv = csv.reader(csv_file)
        fields = next(read_csv)
        title_index = fields.index("title")
        description_index = fields.index("description")
        doc_id = 1
        token = {}
        for row in read_csv:
            token[doc_id] = {
                "title_token": prepare_text(text=row[title_index], lang="en"),
                "description":  prepare_text(text=row[description_index], lang="en")
            }
            doc_id += 1
        # Test
        print(token.get(1))
        print(token.get(2))
        print(token.get(3))
        print(token.get(4))


main()
