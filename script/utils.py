from nltk.tokenize.treebank import TreebankWordTokenizer
tokenizer = TreebankWordTokenizer()

def process_original_entity(text):
    entity = " ".join(filter(lambda x: len(x)>0, text.lower().split("_")))
    entity = tokenizer.tokenize(entity)
    return " ".join(entity)

def repalce_punc(text):
    return text.replace(":", " ").replace("-", " ").replace("!", " ").replace("?", " ").replace(";", " ").replace(".", " ")

def processed_text(text):
    text = text.replace('\\\\','').replace(",", "")
    #stripped = strip_accents(text.lower())
    stripped = text.lower()
    toks = tokenizer.tokenize(stripped)
    return " ".join(toks) + " "

def process_entity(text):
    if "(" in text and ")" in text:
        left = text.index("(")
        right = text.index(")")
        entity = text[0: left] + text[right+1:]
    else:
        entity = text

    if ",_" in entity:
        right = text.index(",_")
        entity = entity[:right]

    entity = entity.replace(",", " ")

    entity = " ".join(filter(lambda x: len(x)>0, entity.lower().split("_")))
    entity = tokenizer.tokenize(entity)
    return " ".join(entity)
