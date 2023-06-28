import spacy

nlp = spacy.load("en_core_web_sm")


def extract_number(query):
    doc = nlp(query)
    for ent in doc.ents:
        if ent.label_ in ["CARDINAL", "PERCENT"]:
            try:
                number = int(ent.text)
                return number
            except ValueError:
                # The entity text couldn't be converted to an integer
                return None
    return None
