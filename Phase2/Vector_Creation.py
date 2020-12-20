from Phase1.first_part import *
import csv
import numpy as np
import math


def train_documents_to_vectors(path):
    tokens = {}  # doc id to tokens
    results = []
    INVERTED_INDEX = {}
    with open(path, encoding='utf-8') as csv_file:
        read_csv = csv.reader(csv_file)
        fields = next(read_csv)
        title_index = fields.index("title")
        description_index = fields.index("description")
        views = fields.index("views")
        doc_id = 1
        for row in read_csv:
            title_tokens = prepare_text(text=row[title_index], lang="en")
            description_tokens = prepare_text(text=row[description_index], lang="en")
            tokens[doc_id] = {
                "title_token": title_tokens,
                "description": description_tokens
            }
            doc_id += 1
            results.append(int(row[views]))
    tokens_of_dic = []
    for doc_id in tokens.keys():
        for token in set(tokens[doc_id]['title_token'] + tokens[doc_id]['description']):
            posting = {
                'doc_ID': doc_id,
                'repetition': 0
            }
            if token in tokens[doc_id]['title_token']:  # 't' means title 'd' means description 'b' means both
                for i in range(len(tokens[doc_id]['title_token'])):
                    if tokens[doc_id]['title_token'][i] == token:
                        posting['repetition'] += 1
            if token in tokens[doc_id]['description']:
                for i in range(len(tokens[doc_id]['description'])):
                    if tokens[doc_id]['description'][i] == token:
                        posting['repetition'] += 1

            tokens_of_dic.append({'token': token, 'posting': posting, 'doc_id': doc_id})
            # the doc id is also in the 'posting'. but i also added it here to use it in the next line for sorting
    tokens_of_dic = sorted(tokens_of_dic, key=lambda k: (k['token'], k['doc_id']))
    i = 0
    while i < len(tokens_of_dic):
        INVERTED_INDEX[tokens_of_dic[i]['token']] = [tokens_of_dic[i]['posting']]
        current_token = i
        while i + 1 < len(tokens_of_dic) and tokens_of_dic[i + 1]['token'] == tokens_of_dic[current_token]['token']:
            INVERTED_INDEX[tokens_of_dic[current_token]['token']].append(tokens_of_dic[i + 1]['posting'])
            i += 1
        i += 1
    N = len(tokens)
    idf = {}  # token to idf
    # computing idf of all tokens
    for tok in INVERTED_INDEX.keys():
        idf[tok] = math.log(N/len(INVERTED_INDEX[tok]))
    X = np.zeros([N, len(INVERTED_INDEX)])  # a set of vectors each representing a training feature
    y = np.zeros(N, dtype=int)
    all_tokens = list(INVERTED_INDEX.keys())
    i = 0
    for doc_id in tokens.keys():
        for token_in_this_doc in tokens[doc_id]["title_token"] + tokens[doc_id]["description"]:
            tf = 0
            for posting in INVERTED_INDEX[token_in_this_doc]:
                if posting['doc_ID'] == doc_id:
                    tf = posting['repetition']
                    break
            X[i][all_tokens.index(token_in_this_doc)] = tf * idf[token_in_this_doc]
            y[i] = results[i]
        i += 1
    return X.tolist(), y.tolist(), idf, all_tokens


def other_documents_to_vectors(path, idf, all_tokens, is_test=True):
    tokens = {}  # doc id to tokens
    results = []
    vectors = []
    N = len(all_tokens)
    with open(path, encoding='utf-8') as csv_file:
        read_csv = csv.reader(csv_file)
        fields = next(read_csv)
        title_index = fields.index("title")
        description_index = fields.index("description")
        for row in read_csv:
            title_tokens = prepare_text(text=row[title_index], lang="en")
            description_tokens = prepare_text(text=row[description_index], lang="en")
            tokens_in_this_document = {}  #tokens to number of repitions
            vector = [0.0 for i in range(N)]
            for token in title_tokens + description_tokens:
                if token in all_tokens:
                    if token not in tokens_in_this_document.keys():
                        tokens_in_this_document[token] = 1
                    else:
                        tokens_in_this_document[token] += 1
            for token in tokens_in_this_document.keys():
                vector[all_tokens.index(token)] = tokens_in_this_document[token] * idf[token]
            vectors.append(vector)
            if is_test:
                views = fields.index("views")
                results.append(int(row[views]))
    return vectors, results
