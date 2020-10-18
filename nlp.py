import spacy

nlp = spacy.load("en_core_web_sm")


def find_entities(sentence):
    subject = nlp(sentence)
    result = []

    for entity in subject.ents:
        result.append(entity.text)

    return result
