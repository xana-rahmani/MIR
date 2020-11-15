import json
EN_Tokens = {}
FA_Tokens = {}
EN_Token_Repetition = {}
FA_Token_Repetition = {}

INVERTED_INDEX = {}
Bigram_Index = {}


def Create_Inverted_Index(lang='en', output_path='out.txt'):
    tokens_of_dic = []
    if lang == 'en':
        tokens = EN_Tokens
    else:
        tokens = FA_Tokens
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

            tokens_of_dic.append({'token': token, 'posting': posting, 'doc_id': doc_id})
            # the doc id is also in the 'posting'. but i also added it here to use it in the next line for sorting
    tokens_of_dic = sorted(tokens_of_dic, key=lambda k: (k['token'], k['doc_id']))
    i = 0
    while i < len(tokens_of_dic):
        INVERTED_INDEX[tokens_of_dic[i]['token']] = [tokens_of_dic[i]['posting']]
        current_token = i
        while i + 1 < len(tokens_of_dic) and tokens_of_dic[i + 1]['token'] == tokens_of_dic[current_token]['token']:
            INVERTED_INDEX[tokens_of_dic[current_token]['token']].append([tokens_of_dic[i + 1]['posting']])
            i += 1
        i += 1
    Write_And_Clear__Invert_Index(output_path)


def Write_And_Clear__Invert_Index(output_path):
    i = 0
    new_inverted_index = {}
    for keys in INVERTED_INDEX.keys():
        posting_list = INVERTED_INDEX[keys]
        new_posting_list = []
        for doc in posting_list:
            new_doc = []
            print(i, doc)
            new_doc.append(doc['doc_ID'])
            part = doc['part']
            if part == 't':
                new_doc.append(0)
                new_doc.append(doc['title_positions'])
                new_doc.append(doc['title_repetitions'])
            elif part == 'd':
                new_doc.append(1)
                new_doc.append(doc['description_positions'])
                new_doc.append(doc['description_repetitions'])
            else:
                new_doc.append(2)
                new_doc.append(doc['title_positions'])
                new_doc.append(doc['title_repetitions'])
                new_doc.append(doc['description_positions'])
                new_doc.append(doc['description_repetitions'])
            new_posting_list.append(new_doc)
            i += 1
        new_inverted_index[keys] = new_posting_list
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(INVERTED_INDEX, ensure_ascii=False))
    INVERTED_INDEX.clear()


def Load__Invert_Index_File(load_file_path):
    try:
        with open(load_file_path, 'r') as file:
            data = file.read()
            if len(data) == 0:
                return None
            loaded_index = json.loads(data)
            index = {}  # we want to return the index with postings that are dictionaries
            for key in loaded_index.keys():
                loaded_docs = index[key]
                new_docs = []
                for doc in loaded_docs:
                    new_posting = {
                        'doc_ID': doc[0],
                    }
                    if doc[1] == 0:
                        new_posting['part'] = 't'
                        new_posting['title_positions'] = doc[2]
                        new_posting['title_repetitions'] = doc[3]
                    elif doc[1] == 1:
                        new_posting['part'] = 'd'
                        new_posting['description_positions'] = doc[2]
                        new_posting['description_repetitions'] = doc[3]
                    elif doc[1] == 2:
                        new_posting['part'] = 'b'
                        new_posting['title_positions'] = doc[2]
                        new_posting['title_repetitions'] = doc[3]
                        new_posting['description_positions'] = doc[4]
                        new_posting['description_repetitions'] = doc[5]
                    new_docs.append(new_posting)
                index[key] = new_docs
            return index
    except Exception as e:
        print("#Erorr in Load Invert Index File", e)
        return None


def Create_Bigrame(lang='en', output_path='out.txt'):
    if lang == 'en':
        tokens = EN_Tokens
    else:
        tokens = FA_Tokens
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
            if bigrame in Bigram_Index.keys():
                Bigram_Index[bigrame].append(token)
            else:
                Bigram_Index[bigrame] = [token]

    Write_And_Clear__Bigram_Index(output_path)


def Write_And_Clear__Bigram_Index(output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(Bigram_Index, ensure_ascii=False))
    Bigram_Index.clear()


def AddDoc():
    pass


def RemoveDoc():
    pass
