from main import *
english_tokens, english_repetions, persian_tokens, persian_repetitions = main()
def create_inverted_index(language = 'en'):

    tokens = 0
    output_path = ''
    index = {}
    tokens_of_dictionary = []
    if language == 'en':
        tokens = english_tokens
        output_path = 'english_index.txt'
    else:
        tokens = persian_tokens
        output_path = 'persian_index.txt'
    print(language)
    # print(len(tokens.keys()))
    for id in tokens.keys():
        # print(id)
        for token in set(tokens[id]['title_token'] + tokens[id]['description']):
            posting = {}
            posting['doc_ID'] = id
            posting['part'] = ''  # 't' means title 'd' means description 'b' means both
            if token in tokens[id]['title_token']:
                posting['part'] = 't'
                posting['title_positions'] = []
                posting['title_repetitions'] = 0
                for i in range(len(tokens[id]['title_token'])):
                    if tokens[id]['title_token'][i] == token:
                        posting['title_positions'].append(i)
                        posting['title_repetitions'] += 1
            if token in tokens[id]['description']:
                if posting['part'] == 't':
                    posting['part'] = 'b'
                else:
                    posting['part'] = 'd'
                posting['description_positions'] = []
                posting['description_repetitions'] = 0
                for i in range(len(tokens[id]['description'])):
                    if tokens[id]['description'][i] == token:
                        posting['description_positions'].append(i)
                        posting['description_repetitions'] += 1

            tokens_of_dictionary.append({'token': token, 'posting': posting,
                                                 'docid': id})  # the docid is also in the 'posting'. but i also added it here to use it in the next line for sorting
    tokens_of_dictionary = sorted(tokens_of_dictionary, key=lambda k: (k['token'], k['docid']))
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
# create_inverted_index('en')
# create_inverted_index('fa')


#bigram function
def create_bigrame(language = 'en'):
    tokens = 0
    output_path = ''
    index = {}
    tokens_of_dictionary = []
    if language == 'en':
        tokens = english_tokens
        output_path = 'english_bigram.txt'
    else:
        tokens = persian_tokens
        output_path = 'persian_bigram.txt'
    bigram_index ={}
    all_tokens = set()
    for id in tokens.keys():
        # print(id)
        for token in set(tokens[id]['title_token'] + tokens[id]['description']):
            all_tokens.add(token)
    all_tokens = list(all_tokens)
    all_tokens.sort()
    for token in all_tokens:
        text = "$" + token + "$"
        for i in range(0,len(text) - 1):
            bigrame = text[i:i+2]
            if bigrame in bigram_index.keys():
                bigram_index[bigrame].append(token)
            else:
                bigram_index[bigrame] = [token]
    import json
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(bigram_index))
create_bigrame('en')





