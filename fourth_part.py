import operator
import json
import numpy as np


def edit_distance(word1, word2):
    len_1 = len(word1)
    len_2 = len(word2)
    dp = np.zeros([len_1+1, len_2+1], dtype=int)
    for i in range(len_1+1):
        for j in range(len_2+1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1])
    return dp[len_1, len_2]


def closest_word_edit_distance(word, candidates):
    if len(candidates) == 0:
        return None
    edit_distances = [edit_distance(word, c) for c in candidates]
    index = edit_distances.index(min(edit_distances))
    return candidates[index]


def jaccard(word1, word2, length_of_intersection):
    word2 = "$" + word2 + "$"
    return length_of_intersection / (len(word1) - 1 + len(word2) - 1 - length_of_intersection)
def closest_words_with_jaccard(word, bigram_index):
    tokens_with_bigram_common_with_word = {}
    word = "$" + word + "$"
    for i in range(0, len(word) - 1):
        bigrame = word[i:i+2]
        if bigrame in bigram_index.keys():
            posting = bigram_index.get(bigrame)
            for token in posting:
                if token in tokens_with_bigram_common_with_word.keys():
                    tokens_with_bigram_common_with_word[token] += 1
                else:
                    tokens_with_bigram_common_with_word[token] = 1
    jaccard_coefficient = {}
    for token in tokens_with_bigram_common_with_word.keys():
        jaccard_coefficient[token] = jaccard(word, token, tokens_with_bigram_common_with_word[token])
    sorted_jaccards = sorted(jaccard_coefficient.items(), key=operator.itemgetter(1))
    if len(sorted_jaccards) > 10:
        return [tuple[0] for tuple in sorted_jaccards[-10:]]
    else:
        return [tuple[0] for tuple in sorted_jaccards]


def Spell_Checker(words_not_found, bigram_path):
    if len(words_not_found) == 0:
        return []
    with open(bigram_path, 'r', encoding='utf-8') as f:
        bigram_index = json.loads(f.read())
    result = []
    for word in words_not_found:
        result.append(closest_word_edit_distance(word, closest_words_with_jaccard(word, bigram_index)))
    return result
