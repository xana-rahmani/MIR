import os
import math
import vbcode
import json
import functools as ft


def gamma_encoding(postings):
    gapList = get_gaps_list(postings)
    gapList[0] += 2  # to adapt 0,1 in gamma encoding
    res = ''.join([get_length(get_offset(gap))+get_offset(gap) for gap in gapList])
    return int(res, 2)


def gamma_decoding(gamma):
    gamma = bin(gamma)[2:]
    _, length, offset, aux, res = 0, "", "", 0,[]
    while gamma != "":
        aux = gamma.find('0')
        length = gamma[:aux]
        if length == "": res.append(1); gamma = gamma[1:]
        else:
            offset = "1"+gamma[aux+1:aux+1+int(unary_decodification(length))]
            res.append(int(offset, 2))
            gamma = gamma[aux+1+int(unary_decodification(length)):]
    res[0] -= 2  # to revert the adaptaion of 0,1
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


def compress_file(fileName, coding, show_print=True):
    # determine mode function
    if coding == 'gamma':
        mode = gamma_encoding
    elif coding == 'variableByte':
        mode = variable_encoding
    else:
        return
    # read uncompressed data from file
    with open(fileName, 'r', encoding='utf-8') as f:
        data = json.loads(f.read()) # data is now a dict
    # compression
    for word, postingList in data.items():
        for i in range(len(postingList)):
            if postingList[i][1] == 1:
                data[word][i][2] = mode(postingList[i][2])
            elif postingList[i][1] == 0:
                data[word][i][2] = mode(postingList[i][2])
            elif postingList[i][1] == 2:
                data[word][i][4] = mode(postingList[i][4])
                data[word][i][2] = mode(postingList[i][2])
    # write to file
    compressedFileName = fileName[:-4] + '_' + coding + 'Compressed.txt'
    with open(compressedFileName, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data))
    # get the uncompressed file size in KB
    unComp = math.ceil(os.stat(fileName).st_size/1024)
    comp = math.ceil(os.stat(compressedFileName).st_size/1024)
    if show_print:
        print(fileName + ' size before ' + coding + ' compression:', unComp ,'KB')
        print(fileName + ' size after  ' + coding + ' compression:', comp ,'KB')


def decompress_file(fileName, coding):
    # determine mode function
    if coding == 'gamma':
        mode = gamma_decoding
    elif coding == 'variableByte':
        mode = variable_decoding
    else:
        return
    # read compressed data from file
    compressedFileName = fileName[:-4] + '_' + coding + 'Compressed.txt'
    with open(compressedFileName, 'r', encoding='utf-8') as f:
        data = json.loads(f.read()) # data is now a dict
    # decompression
    for word, postingList in data.items():
        for i in range(len(postingList)):
            if postingList[i][1] == 1:
                data[word][i][2] = mode(postingList[i][2])
            elif postingList[i][1] == 0:
                data[word][i][2] = mode(postingList[i][2])
            elif postingList[i][1] == 2:
                data[word][i][4] = mode(postingList[i][4])
                data[word][i][2] = mode(postingList[i][2])
    # write to file
    lang = fileName[0:2]
    decompressedFileName = lang + '_' + 'decompressed.txt'
    with open(decompressedFileName, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data))
