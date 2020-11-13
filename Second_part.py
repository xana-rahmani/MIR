from main import read_file_and_create_token as rf_ct


def create_inverted_index(lang='en'):
    """########################################

                    Inverted Index

    ########################################"""
    index = {}
    tokens_of_dictionary = []
    if lang == 'en':
        tokens, _ = rf_ct(lang=lang)
        output_path = 'english_index.txt'
    else:
        tokens, _ = rf_ct(lang=lang)
        output_path = 'persian_index.txt'
    for doc_id in tokens.keys():
        for token in set(tokens[doc_id]['title_token'] + tokens[doc_id]['description']):
            posting = {
                'doc_ID': doc_id,
                'part': ''
            }
            if token in tokens[doc_id]['title_token']:  # 't' means title 'd' means description 'b' means both
                posting['part'] = 't'
                posting['title_positions'] = []
                posting['title_repetitions'] = 0
                for i in range(len(tokens[doc_id]['title_token'])):
                    if tokens[doc_id]['title_token'][i] == token:
                        posting['title_positions'].append(i)
                        posting['title_repetitions'] += 1
            if token in tokens[doc_id]['description']:
                if posting['part'] == 't':
                    posting['part'] = 'b'
                else:
                    posting['part'] = 'd'
                posting['description_positions'] = []
                posting['description_repetitions'] = 0
                for i in range(len(tokens[doc_id]['description'])):
                    if tokens[doc_id]['description'][i] == token:
                        posting['description_positions'].append(i)
                        posting['description_repetitions'] += 1

            tokens_of_dictionary.append({'token': token, 'posting': posting, 'doc_id': doc_id})
            # the doc id is also in the 'posting'. but i also added it here to use it in the next line for sorting
    tokens_of_dictionary = sorted(tokens_of_dictionary, key=lambda k: (k['token'], k['doc_id']))
    # merging the tokens to create an index
    i = 0
    while i < len(tokens_of_dictionary):
        index[tokens_of_dictionary[i]['token']] = [tokens_of_dictionary[i]['posting']]
        current_token = i
        while i + 1 < len(tokens_of_dictionary) and tokens_of_dictionary[i + 1]['token'] == \
                tokens_of_dictionary[current_token]['token']:
            index[tokens_of_dictionary[current_token]['token']].append(
                [tokens_of_dictionary[i + 1]['posting']])
            i += 1
        i += 1
    import json

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(index))


def create_bigrame(lang='en'):
    """########################################

                      Bigram

    ########################################"""
    if lang == 'en':
        tokens, _ = rf_ct(lang=lang)
        output_path = 'english_bigram.txt'
    else:
        tokens, _ = rf_ct(lang=lang)
        output_path = 'persian_bigram.txt'
    bigram_index = {}
    all_tokens = set()
    for key in tokens.keys():
        for token in set(tokens[key]['title_token'] + tokens[key]['description']):
            all_tokens.add(token)
    all_tokens = list(all_tokens)
    all_tokens.sort()
    for token in all_tokens:
        t = "$" + token + "$"
        for i in range(0, len(t) - 1):
            bigrame = t[i:i+2]
            if bigrame in bigram_index.keys():
                bigram_index[bigrame].append(token)
            else:
                bigram_index[bigrame] = [token]
    import json
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(bigram_index))


create_inverted_index("fa")
# create_bigrame('en')