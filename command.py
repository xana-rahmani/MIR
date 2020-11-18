import csv
import xml.etree.ElementTree as Et
from first_part import prepare_text
from second_part import Create_Inverted_Index, Create_Bigrame, FA_Tokens, FA_Token_Repetition, EN_Tokens, \
    EN_Token_Repetition, RemoveDoc, AddDoc, Last_Doc_ID, Load__Invert_Index_File, Load__bigrame_Index_File
from third_part import compress_file, decompress_file
from fourth_part import Spell_Checker, edit_distance, jaccard
from Fifth_part import relevent_docIDs_with_tf_idf
import json


def Read_And_AddDocsFile(path, lang="en"):
    if lang == "en":
        remvoed_Doc_IDs = []
        try:
            with open("data/EN_Removed_Docs.csv", encoding='utf-8') as csv_file:
                read_csv = csv.reader(csv_file)
                for row in read_csv:
                    remvoed_Doc_IDs.append(int(row[0]))
        except:
            pass
        with open(path, encoding='utf-8') as csv_file:
            read_csv = csv.reader(csv_file)
            fields = next(read_csv)
            title_index = fields.index("title")
            description_index = fields.index("description")
            doc_id = 1
            for row in read_csv:
                if doc_id in remvoed_Doc_IDs:
                    continue
                title_tokens = prepare_text(text=row[title_index], lang="en")
                description_tokens = prepare_text(text=row[description_index], lang="en")
                EN_Tokens[doc_id] = {
                    "title_token": title_tokens,
                    "description": description_tokens
                }
                for tok in title_tokens + description_tokens:
                    if tok not in EN_Token_Repetition.keys():
                        EN_Token_Repetition[tok] = 1
                    else:
                        EN_Token_Repetition[tok] += 1
                doc_id += 1
            Last_Doc_ID["EN"] = doc_id - 1
        with open('EN_Tokens.txt', 'w', encoding='utf-8') as f:
            f.write(json.dumps(EN_Tokens, ensure_ascii=False))
    if lang == "fa":
        remvoed_Doc_IDs = []
        try:
            with open("data/FA_Removed_Docs.csv", encoding='utf-8') as csv_file:
                read_csv = csv.reader(csv_file)
                for row in read_csv:
                    remvoed_Doc_IDs.append(int(row[0]))
        except:
            pass
        root = Et.parse(path).getroot()
        file_path = "{http://www.mediawiki.org/xml/export-0.10/}"
        i = 1
        for title_tag in root.iter(file_path + 'title'):
            if i in remvoed_Doc_IDs:
                continue
            title_tokens = prepare_text(text=title_tag.text, lang="fa")
            FA_Tokens[i] = {
                "title_token": title_tokens,
            }
            for tok in title_tokens:
                if tok not in FA_Token_Repetition.keys():
                    FA_Token_Repetition[tok] = 1
                else:
                    FA_Token_Repetition[tok] += 1
            i += 1
        i = 1
        for text_tag in root.iter(file_path + 'text'):
            if i in remvoed_Doc_IDs:
                continue
            description_tokens = prepare_text(text=text_tag.text, lang="fa")
            FA_Tokens[i]["description"] = description_tokens
            for tok in description_tokens:
                if tok not in FA_Token_Repetition.keys():
                    FA_Token_Repetition[tok] = 1
                else:
                    FA_Token_Repetition[tok] += 1
            i += 1
        Last_Doc_ID["FA"] = i - 1
        try:
            with open("data/Added_Doc.csv", encoding='utf-8') as csv_file:
                read_csv = csv.reader(csv_file)
                for row in read_csv:
                    if i in remvoed_Doc_IDs:
                        continue
                    title_tokens = prepare_text(text=row[0], lang="en")
                    description_tokens = prepare_text(text=row[1], lang="en")
                    EN_Tokens[i] = {
                        "title_token": title_tokens,
                        "description": description_tokens
                    }
                    for tok in title_tokens + description_tokens:
                        if tok not in FA_Token_Repetition.keys():
                            FA_Token_Repetition[tok] = 1
                        else:
                            FA_Token_Repetition[tok] += 1
                    i += 1
                Last_Doc_ID["FA"] = i - 1
        except Exception as e:
            pass
        with open('FA_Tokens.txt', 'w', encoding='utf-8') as f:
            f.write(json.dumps(FA_Tokens, ensure_ascii=False))


def Add_New_Doc_in_csv_file(title, description, lang="en",):
    if lang == "en":
        doc_info = ['' for i in range(18)]
        doc_info[14] = title
        doc_info[1] = description
        path = "data/ted_talks.csv"
        with open(path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(doc_info)
    if lang == "fa":
        doc_info = [title, description]
        path = "data/Added_Doc.csv"
        with open(path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(doc_info)


def Write__Removed_DOC_ID_in_csv(doc_id, lang="en"):
    path = "data/EN_Removed_Docs.csv"
    if lang == "fa":
        path = "data/FA_Removed_Docs.csv"
    with open(path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([doc_id])


def ShowRelevantDoc(relevantDocIDs, lang):
    doc_info = {}
    if lang == "en":
        with open('data/ted_talks.csv', encoding='utf-8') as csv_file:
            read_csv = csv.reader(csv_file)
            fields = next(read_csv)
            title_index = fields.index("title")
            description_index = fields.index("description")
            id = 1
            for row in read_csv:
                if id in relevantDocIDs:
                    doc_info[id] = {
                        "title": row[title_index],
                        "description": row[description_index]
                    }
                id += 1
    if lang == "fa":
        path = 'data/Persian.xml'
        root = Et.parse(path).getroot()
        file_path = "{http://www.mediawiki.org/xml/export-0.10/}"
        id = 1
        for title_tag in root.iter(file_path + 'title'):
            if id in relevantDocIDs:
                doc_info[id] = {
                    "title": title_tag.text,
                }
            id += 1
        id = 1
        for text_tag in root.iter(file_path + 'text'):
            if id in relevantDocIDs:
                doc_info[id] = {
                    "description": text_tag.text,
                }
            id += 1
        try:
            with open("data/Added_Doc.csv", encoding='utf-8') as csv_file:
                read_csv = csv.reader(csv_file)
                for row in read_csv:
                    if id in relevantDocIDs:
                        doc_info[id] = {
                            "title": row[0],
                            "description": row[1]
                        }
                    id += 1
        except:
            pass

    print("\n----------------------------------------------------------------------\n")
    for i in relevantDocIDs:
        print("# DOC ID: ", i)
        print("_Title")
        print("\t", doc_info.get(i).get("title"))
        print("_Description")
        print("\t", doc_info.get(i).get("description"))
        print("\n----------------------------------------------------------------------\n")


print("###################  Commands  ########################\n")
print("- for sample text preparation:")
print("\tprepare-text lang text")
print("- for loading doc's file:")
print("\tadd-docs-file  input-path  lang")
print("- for creating invert index:")
print("\tcreate-invert-index  lang  output-path")
print("- for creating bigrame:")
print("\tcreate-bigrame  lang  output-path")
print("- for showing token posting:")
print("\tshow-token-posting")
print("- for showing token positions :")
print("\tshow-token-positions")
print("- for showing bigrame tokens :")
print("\tshow-bigrame-tokens")
print("- for removing doc with id:")
print("\tremove-doc doc_id")
print("- for adding doc with id:")
print("\tadd-doc doc_id")
print("- for file compression:")
print("\tcompress file-path encoding")
print("- for file decompression:")
print("\tdecompress file-path encoding")
print("- for spell checking:")
print("\tspell-checker file-path words")
print("- for getting jaccard distance:")
print("\tjaccard-distance word1 word2")
print("- for getting edit distance:")
print("\tedit-distance word1 word2")
print("- for querying the system:")
print("\tquery")
print("\n#######################################################\n")
while True:
    try:
        print("$ ", end="")
        input_command = input()
        command = input_command.split()
        if command is None or len(command) == 0:
            continue
        if command[0] == "prepare-text":
            # prepare-text en "Hello Modern Information Retrieval"
            # prepare-text fa درس بازیابی اطلاعات
            lang = command[1]
            text = " ".join(command[2:])
            tokens = prepare_text(text, lang)
            print(tokens)
        elif command[0] == "add-docs-file":
            # add-docs-file data/ted_talks.csv en
            # add-docs-file data/Persian.xml fa
            path = command[1]
            lang = command[2]
            Read_And_AddDocsFile(path, lang)
        elif command[0] == "create-invert-index":
            # create-invert-index en en_inverted.txt
            # create-invert-index fa fa_inverted.txt
            lang = command[1]
            output_path = command[2]
            Create_Inverted_Index(lang, output_path)
        elif command[0] == "create-bigrame":
            # create-bigrame en en_bigrame.txt
            # create-bigrame fa fa_bigrame.txt
            lang = command[1]
            output_path = command[2]
            Create_Bigrame(lang, output_path)
        elif command[0] == "show-token-posting":
            # show-token-posting
            print("\t language\n\t := ", end="")
            lang = input()
            print("\t enter token\n\t := ", end="")
            token = input()
            if lang == "en":
                inverted_index = Load__Invert_Index_File("en_inverted.txt")
            if lang == "fa":
                inverted_index = Load__Invert_Index_File("fa_inverted.txt")
            print(inverted_index.get(token))
        elif command[0] == "show-token-positions":
            # show-token-positions
            print("\t language\n\t := ", end="")
            lang = input()
            print("\t enter token\n\t := ", end="")
            token = input()
            if lang == "en":
                inverted_index = Load__Invert_Index_File("en_inverted.txt")
            if lang == "fa":
                inverted_index = Load__Invert_Index_File("fa_inverted.txt")
            token_posting = inverted_index.get(token)
            for i in token_posting:
                print("\ntoken position in doc ", i.get("doc_ID"))
                if i.get("title_positions"):
                    print("\t#titile: ", end="")
                    for j in i.get("title_positions"):
                        print(j, "  ,  ", end="")
                    print()
                if i.get("description_positions"):
                    print("\t#description: ", end="")
                    for j in i.get("description_positions"):
                        print(j, "  ,  ", end="")
                    print()
        elif command[0] == "show-bigrame-tokens":
            # show-bigrame-tokens
            print("\t language\n\t := ", end="")
            lang = input()
            print("\t enter your bigrame case:\n\t := ", end="")
            token = input()
            if lang == "en":
                inverted_index = Load__bigrame_Index_File("en_bigrame.txt")
            if lang == "fa":
                inverted_index = Load__bigrame_Index_File("fa_bigrame.txt")
            temp = inverted_index.get(token, [])
            for i in temp:
                print(i)
        elif command[0] == "remove-doc":
            # remove-doc 1878 en
            # remove-doc 146 fa
            doc_id = command[1]
            lang = command[2]
            inverted_file_path = "en_inverted.txt"
            bigrame_file_path = "en_bigrame.txt"
            if lang == "fa":
                inverted_file_path = "fa_inverted.txt"
                bigrame_file_path = "fa_bigrame.txt"
            RemoveDoc(int(doc_id), lang, inverted_file_path, bigrame_file_path)
            Write__Removed_DOC_ID_in_csv(int(doc_id), lang)
        elif command[0] == "add-doc":
            print("\t enter doc language\n\t := ", end="")
            lang = input()
            print("\t enter doc title\n\t := ", end="")
            title = input()
            print("\t enter doc text\n\t := ", end="")
            text = input()
            AddDoc(lang=lang,  title=title, text=text)
            Add_New_Doc_in_csv_file(title, text, lang)
        elif command[0] == "compress":
            # compress en_inverted.txt gamma
            # compress en_inverted.txt variableByte
            # compress fa_inverted.txt gamma
            # compress fa_inverted.txt variableByte
            fileName = command[1]
            coding = command[2]
            compress_file(fileName, coding)
        elif command[0] == "decompress":
            # decompress en_inverted.txt gamma
            # decompress en_inverted.txt variableByte
            # decompress fa_inverted.txt gamma
            # decompress fa_inverted.txt variableByte
            fileName = command[1]
            coding = command[2]
            decompress_file(fileName, coding)
        elif command[0] == "spell-checker":
            # spell-checker en_bigrame.txt Spidir
            bigram_path = command[1]
            words_not_found = []
            for w in command[2:]:
                words_not_found.append(w)
            temp = Spell_Checker(words_not_found, bigram_path)
            print(temp)
        elif command[0] == "jaccard-distance":
            # jaccard-distance word1 word2
            word1, word2 = command[1], command[2]
            w1, w2, l = '$'+word1+'$', '$'+word2+'$', 0
            for i in range(len(w1)-1):
                if w1[i:i+2] in w2:
                    l += 1
            print(jaccard(word1, w2, l))
        elif command[0] == "edit-distance":
            # edit-distance word1 word2
            word1, word2 = command[1], command[2]
            print(edit_distance(word1, word2))
        elif command[0] == "query":
            print("\t language\n\t := ", end="")
            lang = input()
            print("\t enter query\n\t := ", end="")
            query = input()
            print("\t enter the part of document you would like your query to be searched in (title, description, both)"
                  "\n\t := ", end="")
            part = input()
            relevant_docIDs = relevent_docIDs_with_tf_idf(query=query, lang=lang, part=part)
            print(relevant_docIDs)
            ShowRelevantDoc(relevant_docIDs, lang)
    except Exception as e:
        print("#Error: ", e)