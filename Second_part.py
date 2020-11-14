import json
EN_Tokens = {}
FA_Tokens = {}
EN_Token_Repetition = {}
FA_Token_Repetition = {}

INVERTED_INDEX = {}
Bigram_Index = {}


def Create_Inverted_Index(lang='en', output_path='out.txt'):
    tokens_of_dictionary = []
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

            tokens_of_dictionary.append({'token': token, 'posting': posting, 'doc_id': doc_id})
            # the doc id is also in the 'posting'. but i also added it here to use it in the next line for sorting
    tokens_of_dictionary = sorted(tokens_of_dictionary, key=lambda k: (k['token'], k['doc_id']))

    Merge_Index_Posting(tokens_of_dictionary, load_file_path=output_path)
    Write_And_Clear__Invert_Index(output_path)


def Merge_Index_Posting(dic, load_file_path):
    load_dic = Load__Invert_Index_File(load_file_path)
    if load_dic is None:
        i = 0
        while i < len(dic):
            INVERTED_INDEX[dic[i]['token']] = [dic[i]['posting']]
            current_token = i
            while i + 1 < len(dic) and dic[i + 1]['token'] == dic[current_token]['token']:
                INVERTED_INDEX[dic[current_token]['token']].append([dic[i + 1]['posting']])
                i += 1
            i += 1
    else:
        print("To DO")  # TODO


def Write_And_Clear__Invert_Index(output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(INVERTED_INDEX, ensure_ascii=False))
    INVERTED_INDEX.clear()


def Load__Invert_Index_File(load_file_path):
    try:
        with open(load_file_path, 'r') as file:
            data = file.read()
            if len(data) == 0:
                return None
            index = json.loads(data)
            return index
    except Exception as e:
        print(10)
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
