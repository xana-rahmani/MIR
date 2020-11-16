import csv
import xml.etree.ElementTree as Et
from First_part import prepare_text
from Second_part import Create_Inverted_Index, Create_Bigrame, FA_Tokens, FA_Token_Repetition, EN_Tokens, \
    EN_Token_Repetition, RemoveDoc
from Forth_part import Spell_Checker


def Read_And_AddDocsFile(path, lang="en"):
    if lang == "en":
        with open(path, encoding='utf-8') as csv_file:
            read_csv = csv.reader(csv_file)
            fields = next(read_csv)
            title_index = fields.index("title")
            description_index = fields.index("description")
            doc_id = 1
            for row in read_csv:
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
    if lang == "fa":
        root = Et.parse(path).getroot()
        file_path = "{http://www.mediawiki.org/xml/export-0.10/}"
        i = 1
        for title_tag in root.iter(file_path + 'title'):
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
            description_tokens = prepare_text(text=text_tag.text, lang="fa")
            FA_Tokens[i]["description"] = description_tokens
            for tok in description_tokens:
                if tok not in FA_Token_Repetition.keys():
                    FA_Token_Repetition[tok] = 1
                else:
                    FA_Token_Repetition[tok] += 1
            i += 1


print("###################  Commands  ########################\n")
print("- for load doc's file:")
print("\tadd-docs-file  input-path  lang")
print("- for create invert index:")
print("\tcreate-invert-index  lang  output-path")
print("- for remove doc with id:")
print("\tremove-doc doc_id  inverted_file_path  bigrame_file_path")
print("\n#######################################################\n")
while True:
    try:
        print("$ ", end="")
        command = input().split()
        if command is None:
            continue
        if command[0] == "prepare-text":
            # prepare-text en "Hello Modern Information Retrieval"
            # prepare-text fa "سلام درس بازیابی"
            lang = command[1]
            text = " ".join(command[2:])
            tokens = prepare_text(text, lang)
            print(tokens)
        if command[0] == "add-docs-file":
            # add-docs-file data/ted_talks.csv en
            # add-docs-file data/Persian.xml fa
            path = command[1]
            lang = command[2]
            Read_And_AddDocsFile(path, lang)
        if command[0] == "create-invert-index":
            # create-invert-index en en_inverted.txt
            # create-invert-index fa fa.txt
            lang = command[1]
            output_path = command[2]
            Create_Inverted_Index(lang, output_path)
        if command[0] == "create-bigrame":
            # create-bigrame en en_bigrame.txt
            # create-bigrame fa fa_bigrame.txt
            lang = command[1]
            output_path = command[2]
            Create_Bigrame(lang, output_path)
        if command[0] == "spell_checker":
            # spell_checker en_bigrame.txt Spidir
            bigram_path = command[1]
            words_not_found = []
            for w in command[2:]:
                words_not_found.append(w)
            temp = Spell_Checker(words_not_found, bigram_path)
            print(temp)
        if command[0] == "remove-doc":
            # remove-doc 1878 en_inverted.txt en_bigrame.txt
            doc_id = command[1]
            inverted_file_path = command[2]
            bigrame_file_path = command[3]
            RemoveDoc(int(doc_id), inverted_file_path, bigrame_file_path)
    except Exception as e:
        print("#Error: ", e)
