from Phase1.first_part import prepare_text
from Phase1.fourth_part import Spell_Checker
import operator
from Phase1.third_part import *
def intersect(postingList1,postingList2):
    answers = []#list of documents mutual in both posting lists
    p1 = 0
    p2 = 0
    while p1 != len(postingList1) and p2 != len(postingList2):
        if postingList1[p1] == postingList2[p2]:
            answers.append(postingList1[p1])
            p1 += 1
            p2 += 1
        elif postingList1[p1] < postingList2[p2]:
            p1 += 1
        else:
            p2 += 1
    return answers


def build_document_vector_from_document_tokens(doc_id,query_tokens,document_tokens,part,inverted_index):
    #building vector for a document based on inc
    #the final vector only comprises of the tokens in the query
    N = len(inverted_index)
    idf = {}
    tf = {}
    all_tokens_in_document = []

    if part == 'title':
        all_tokens_in_document = document_tokens[str(doc_id)]['title_token']
    elif part == 'description':
        all_tokens_in_document = document_tokens[str(doc_id)]['description']
    else:
        all_tokens_in_document = document_tokens[str(doc_id)]['title_token'] + document_tokens[str(doc_id)]['description']

    for token in all_tokens_in_document:
        if token in tf.keys():
            tf[token] += 1
        else:
            tf[token] = 1

    for token in set(all_tokens_in_document):
        idf[token] = math.log(N/len(inverted_index[token]))
    normalization_coefficient = 0
    query_tokens = set(query_tokens)

    for key in tf.keys():
        normalization_coefficient += ((math.log(tf[key]) + 1) * idf[key]) ** 2
    normalization_coefficient = normalization_coefficient ** 0.5
    vector = []
    for token in query_tokens:
        t = math.log(tf[token]) + 1
        vector.append((t * idf[token])/normalization_coefficient)
    return vector


def normalize(vector):
    weight_sum = 0
    for v in vector:
        weight_sum += v ** 2
    weight_sum = weight_sum ** 0.5
    return [v/weight_sum for v in vector]


def dot_product(v1,v2):
    result = 0
    for i in range(len(v1)):
        result += v1[i] * v2[i]
    return result


## main function
def relevent_docIDs_with_tf_idf(query, lang="en", part="both"):
    query_tokens = prepare_text(query, lang=lang)
    inverted_index = {}
    bigram_path = ''
    document_tokens = {}
    if lang == "en":
        with open('en_decompressed.txt', 'r', encoding='utf-8') as f:
            inverted_index = json.loads(f.read())
        bigram_path ="en_bigrame.txt"
        with open('EN_Tokens.txt', 'r', encoding='utf-8') as f:
            document_tokens = json.loads(f.read())

        #open en_tokens
    else:
        with open('fa_decompressed.txt', 'r', encoding='utf-8') as f:
            inverted_index = json.loads(f.read())
        bigram_path = 'fa_bigrame.txt'
        with open('FA_Tokens.txt', 'r', encoding='utf-8') as f:
            document_tokens = json.loads(f.read())
    postings = []#consists only of doc_ids
    words_not_found =[]
    idf_token = {}# the dft of the tokens in the query
    N = len(document_tokens)  # number of documents
    for token in query_tokens:
        if token in inverted_index.keys():
            idf_token[token] = math.log(N/len(inverted_index[token]))
            doc_ids = []
            for element in inverted_index[token]:
                if part == "both":
                    doc_ids.append(element[0])
                elif part == "title":
                    if element[1] == 0 or element[1] == 2:
                        doc_ids.append(element[0])
                elif part == "description":
                    if element[1] == 1 or element[1] == 2:
                        doc_ids.append(element[0])
            postings.append(doc_ids)
        else:
            words_not_found.append(token)
    corrected_tokens = Spell_Checker(words_not_found,bigram_path)
    corrected_query_tokens = []
    k = 0
    for token in query_tokens:
        if token in inverted_index.keys():
            corrected_query_tokens.append(token)
        else:
            corrected_query_tokens.append(corrected_tokens[k])
            k += 1
    query_tokens = corrected_query_tokens
    for token in corrected_tokens:
        idf_token[token] = math.log(N/len(inverted_index[token]))
        doc_ids = []
        for element in inverted_index[token]:
            if part == "both":
                doc_ids.append(element[0])
            elif part == "title":
                if element[1] == 0 or element[1] == 2:
                    doc_ids.append(element[0])
            elif part == "description":
                if element[1] == 1 or element[1] == 2:
                    doc_ids.append(element[0])
        postings.append(doc_ids)
    postings.sort(key=len)  # sorting the postings based on their lengths.it's a good practice for finding the intersections
    i = 1
    relevant_documents = postings[0]
    while i < len(postings):
        relevant_documents = intersect(relevant_documents,postings[i])
        i += 1
    # sorting answer based on tf_idf
    # creating vector for each of the relevant documents:
    document_vectors = {}
    for doc_id in relevant_documents:
        document_vectors[doc_id] = build_document_vector_from_document_tokens(doc_id=doc_id,query_tokens = query_tokens
                                                                     ,document_tokens = document_tokens,part= part,inverted_index = inverted_index)

    query_vector = []
    query_tf = {}
    for token in query_tokens:
        if token in query_tf.keys():
            query_tf[token] += 1
        else:
            query_tf[token] = 1

    for token in set(query_tokens):
        I = 1 + math.log(query_tf[token])
        query_vector.append(I)
    query_vector = normalize(query_vector)
    tf_idf = {}
    for key in document_vectors.keys():
        tf_idf[key] = dot_product(document_vectors[key],query_vector)
    result = sorted(tf_idf.items(), key=operator.itemgetter(1))
    if len(result) > 10:
        return [tuple[0] for tuple in result[-10:]][::-1]
    else:
        return [tuple[0] for tuple in result][::-1]


# with open('EN_Tokens.txt', 'r', encoding='utf-8') as f:
#     document_tokens = json.loads(f.read())
# rel = relevent_docIDs_with_tf_idf('spidir','en','both')
# print(rel)
# for re in rel:
#     print(document_tokens[str(re)])
#     print("********")

# with open('FA_Tokens.txt', 'r', encoding='utf-8') as f:
#     document_tokens = json.loads(f.read())
# rel = relevent_docIDs_with_tf_idf('تهران','fa','description')
# print(rel)





