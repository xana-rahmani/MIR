import sys
import vbcode
import json
import functools as ft
import objsize

def gamma_encoding(postings): 
    res =  ''.join([get_length(get_offset(gap))+get_offset(gap) for gap in get_gaps_list(postings)])
    return int(res, 2)

def gamma_decoding(gamma):
    gamma = bin(gamma)[2:]
    _,length,offset,aux,res = 0,"","",0,[]
    while gamma != "":
        aux = gamma.find('0')
        length = gamma[:aux]
        if length=="":res.append(1); gamma = gamma[1:]
        else:
            offset = "1"+gamma[aux+1:aux+1+int(unary_decodification(length))]
            res.append(int(offset,2))
            gamma  = gamma[aux+1+int(unary_decodification(length)):]
    for i in range(1, len(res)):
        res[i] += res[i-1]
    return res

def variable_encoding(postings): return int.from_bytes(vbcode.encode(get_gaps_list(postings)), byteorder='big')

def variable_decoding(vbc):
    res = vbcode.decode(vbc.to_bytes((vbc.bit_length()//8)+1, byteorder='big'))
    for i in range(1, len(res)):
        res[i] += res[i-1]
    return res

def get_offset(gap): return bin(gap)[3:]

def get_length(offset): return unary_codification(len(offset))+"0"

def unary_codification(gap):  return "".join(["1" for _ in range(gap)])

def unary_decodification(gap): return ft.reduce(lambda x,y : int(x)+int(y),list(gap))

def get_gaps_list(posting_lists): return [posting_lists[0]]+[posting_lists[i]-posting_lists[i-1] for i in range(1,len(posting_lists))]

def compress_file(fileName, mode):
    # read uncompressed data from file
    with open(fileName + '.txt', 'r', encoding='utf-8') as f:
        data = json.loads(f.read()) # data is now a dict
    # compression
    for word, postingList in data.items():
        for i in range(len(postingList)):
            if postingList[i]['part'] == 'd':
                data[word][i]['description_positions'] = mode(postingList[i]['description_positions'])
            elif postingList[i]['part'] == 't':
                data[word][i]['title_positions'] = mode(postingList[i]['title_positions'])
            elif postingList[i]['part'] == 'b':
                data[word][i]['description_positions'] = mode(postingList[i]['description_positions'])
                data[word][i]['title_positions'] = mode(postingList[i]['title_positions'])
    # write to file
    if mode == gamma_encoding:
        coding = 'gamma'
    else:
        coding = 'variableByte'
    with open(fileName + '_' + coding + 'Compressed.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data))

def decompress_file(fileName, mode):
    # read compressed data from file
    if mode == gamma_decoding:
        coding = 'gamma'
    else:
        coding = 'variableByte'
    with open(fileName + '_' + coding + 'Compressed.txt', 'r', encoding='utf-8') as f:
        data = json.loads(f.read()) # data is now a dict
    # decompression
    for word, postingList in data.items():
        for i in range(len(postingList)):
            if postingList[i]['part'] == 'd':
                data[word][i]['description_positions'] = mode(postingList[i]['description_positions'])
            elif postingList[i]['part'] == 't':
                data[word][i]['title_positions'] = mode(postingList[i]['title_positions'])
            elif postingList[i]['part'] == 'b':
                data[word][i]['description_positions'] = mode(postingList[i]['description_positions'])
                data[word][i]['title_positions'] = mode(postingList[i]['title_positions'])
    return data

lang = 'en'
# lang = 'fa'
if lang == 'en':
    fileName = 'english_index'
elif lang == 'fa':
    fileName = 'persian_index'
# read uncompressed data from file
with open(fileName + '.txt', 'r', encoding='utf-8') as f:
    data = json.loads(f.read()) # data is now a dict
print('data size before compression:', type(data), objsize.get_deep_size(data))
# compression using gamma encoding
compress_file(fileName, gamma_encoding)
print('data size after gamma encoding compression:', type(data), objsize.get_deep_size(data))
# compression using variable byte encoding
compress_file(fileName, variable_encoding)
print('data size after variable byte encoding compression:', type(data), objsize.get_deep_size(data))
# decompression using gamma encoding
data_gamma = decompress_file(fileName, gamma_decoding)
print('data size after gamma encoding decompression:', type(data_gamma), objsize.get_deep_size(data_gamma))
# decompression using variable byte encoding
data_variableByte = decompress_file(fileName, variable_decoding)
print('data size after variable byte encoding decompression:', type(data_variableByte), objsize.get_deep_size(data_variableByte))
