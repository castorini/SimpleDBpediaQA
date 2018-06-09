import re
from fuzzywuzzy import fuzz
import json
import sys
sys.path.append('../script')
from utils import process_original_entity, repalce_punc, processed_text, process_entity
from nltk.tokenize.treebank import TreebankWordTokenizer
tokenizer = TreebankWordTokenizer()


def get_indices(src_list, pattern_list):
    indices = None
    for i in range(len(src_list)):
        match = 1
        for j in range(len(pattern_list)):
            if src_list[i+j] != pattern_list[j]:
                match = 0
                break
        if match:
            indices = range(i, i + len(pattern_list))
            break
    return indices

def get_ngram(tokens):
    ngram = []
    for i in range(1, len(tokens)+1):
        for s in range(len(tokens)-i+1):
            ngram.append((" ".join(tokens[s: s+i]), s, i+s))
    return ngram




def reverseLinking(sent, dbpedia_text, original):
    tokens = sent.split()
    label = ["O"] * len(tokens)
    exact_match = False

    pattern = r'(^|\s)(%s)($|\s)' % (re.escape(dbpedia_text))
    #print(pattern)
    entity_span = None
    if re.search(pattern, sent):
        entity_span = get_indices(tokens, dbpedia_text.split())
    pattern = r'(^|\s)(%s)($|\s)' % (re.escape(original))
    if re.search(pattern, sent):
        entity_span = get_indices(tokens, original.split())
    #print(sent, dbpedia_text, original)
    if entity_span != None:
        exact_match = True
        for i in entity_span:
            label[i] = "I"
    else:
        n_gram_candidate = get_ngram(tokens)
        n_gram_candidate = sorted(n_gram_candidate, key=lambda x: fuzz.token_sort_ratio(x[0], dbpedia_text), reverse=True)
        top = n_gram_candidate[0]
        for i in range(top[1], top[2]):
            label[i] = 'I'
    entity_text = []
    for l, t in zip(label, tokens):
        if l == 'I':
            entity_text.append(t)
    entity_text = " ".join(entity_text)
    label = " ".join(label)
    return entity_text, label, exact_match



if __name__=="__main__":
    # question = "what film did peter menzies jr. do cinematography for"
    # entity = "Peter_Menzies_Jr."
    # processed_query = processed_text(repalce_punc(question))
    # processed_candidate = process_entity(repalce_punc(entity))
    # processed_candidate_original = process_original_entity(repalce_punc(entity))
    # entity_text, label, exact_match = reverseLinking(processed_query, processed_candidate, processed_candidate_original)
    # print("{}\t{}\t{}\t{}\n".format(question, label, entity_text, str(exact_match)))
    # exit()
    folds = ["train", "valid", "test"]
    for fold in folds:
        exact_match_counter = 0
        total = 0
        fin = open("../V1/{}.json".format(fold))
        json_data = json.load(fin)
        fout = open("../V1/{}.txt".format(fold), "w")
        for instance in json_data["Questions"]:
            total += 1
            idx = instance["ID"]
            sub = instance["Subject"]
            pre = instance["PredicateList"][0]["Predicate"]
            direction = instance["PredicateList"][0]["Direction"]
            constraint = instance["PredicateList"][0]["Constraint"]
            free_pre = instance["FreebasePredicate"]
            question = instance["Query"]
            entity = sub.replace("http://dbpedia.org/resource/", "")
            processed_query = processed_text(repalce_punc(question))
            processed_candidate = process_entity(repalce_punc(entity))
            processed_candidate_original = process_original_entity(repalce_punc(entity))
            entity_text, label, exact_match = reverseLinking(processed_query, processed_candidate, processed_candidate_original)
            fout.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(idx, processed_query, sub, pre, direction, pre + "@" + direction + "@" + str(constraint), free_pre, label)) # entity_text, str(exact_match)
            if exact_match:
                exact_match_counter += 1
        print("{}\t{} / {} : {}".format(fold, exact_match_counter, total, exact_match_counter/total))
