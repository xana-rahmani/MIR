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
            INVERTED_INDEX[tokens_of_dic[current_token]['token']].append(tokens_of_dic[i + 1]['posting'])
            i += 1
        i += 1
    Write_And_Clear__Invert_Index(output_path)


def Write_And_Clear__Invert_Index(output_path):
    new_inverted_index = {}
    for keys in INVERTED_INDEX.keys():
        posting_list = INVERTED_INDEX[keys]
        new_posting_list = []
        for doc in posting_list:
            new_doc = []
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
        new_inverted_index[keys] = new_posting_list
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(new_inverted_index, ensure_ascii=False))
    new_inverted_index.clear()
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
                loaded_docs = loaded_index[key]
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
        print("#Erorr in Load Invert Index File: ", e)
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


def RemoveDoc(doc_id, lang, inverted_file_path, bigrame_file_path):

    """ get doc tokens """
    Tokens = {}
    token_repetition = {}
    if lang == "en":
        Tokens = EN_Tokens
        token_repetition = EN_Token_Repetition
    elif lang == "fa":
        Tokens = FA_Tokens
        token_repetition = FA_Token_Repetition

    doc_tokens = Tokens.get(doc_id)
    title_token = doc_tokens.get("title_token", [])
    description_token = doc_tokens.get("description", [])

    """ Remove from invert index"""
    token_is_removed = []
    temp_invert_index = Load__Invert_Index_File(inverted_file_path)
    if temp_invert_index is not None and bool(temp_invert_index):
        for token in set(title_token):
            posting = temp_invert_index.get(token)
            new_posting = []
            for p in posting:
                if p.get("doc_ID") == doc_id:
                    token_repetition[token] = token_repetition.get(token) - p.get("title_repetitions")
                else:
                    new_posting.append(p)
            if len(new_posting) != 0:
                temp_invert_index[token] = new_posting
            else:
                token_is_removed.append(token)
                temp_invert_index.pop(token)
        for token in set(description_token):
            posting = temp_invert_index.get(token)
            new_posting = []
            for p in posting:
                if p.get("doc_ID") == doc_id:
                    token_repetition[token] = token_repetition.get(token) - p.get("description_repetitions")
                else:
                    new_posting.append(p)
            if len(new_posting) != 0:
                temp_invert_index[token] = new_posting
            else:
                token_is_removed.append(token)
                temp_invert_index.pop(token)
        Write_Update_Invert_Index(temp_invert_index, inverted_file_path)
        temp_invert_index.clear()

    """ Remove from bigrame index"""
    temp_bigram_index = Load__bigrame_Index_File(bigrame_file_path)
    if temp_bigram_index is not None and bool(temp_bigram_index):
        for token in token_is_removed:
            t = "$" + token + "$"
            for i in range(0, len(t) - 1):
                bigrame = t[i:i + 2]
                bigrame_list = temp_bigram_index.get(bigrame)
                new_bigrame_list = []
                for i in bigrame_list:
                    if i != token:
                        new_bigrame_list.append(i)
                if len(new_bigrame_list) != 0:
                    temp_bigram_index[bigrame] = new_bigrame_list
                else:
                    temp_bigram_index.pop(bigrame)
        Write_Update_Bigrame_Index(temp_bigram_index, bigrame_file_path)
        temp_bigram_index.clear()
    Tokens.pop(doc_id)


def Write_Update_Invert_Index(inverted_index, output_path):
    new_inverted_index = {}
    for keys in inverted_index.keys():
        posting_list = inverted_index[keys]
        new_posting_list = []
        for doc in posting_list:
            new_doc = []
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
        new_inverted_index[keys] = new_posting_list
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(new_inverted_index, ensure_ascii=False))
    new_inverted_index.clear()
    inverted_index.clear()


def Load__bigrame_Index_File(load_file_path):
    with open(load_file_path, 'r') as file:
        data = file.read()
        if len(data) == 0:
            return None
        loaded_index = json.loads(data)
        return loaded_index


def Write_Update_Bigrame_Index(bigram_index, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(bigram_index, ensure_ascii=False))