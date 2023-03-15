
import re
import spacy
from spacy.symbols import ORTH
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher


degreeAdverbs = ['quite','very', 'extremely', 'intensely']

#return the type of adverb meaning 
def detect_adverb(text):

   
    score = 0
    detectedadverbLists = []
    for sent in text.sents:
     for ent in sent.ents:
        for token in sent:
              for child in token.children:
                if child.dep_ == 'advmod':
                    adv_function = ''
                    if child.text.lower() in degreeAdverbs:
                        if child.text == 'quite':
                              score = 0.25
                        elif child.text == 'very':
                              score = 0.5
                        elif child.text == 'extremely':
                              score = 0.75
                        elif child.text == 'intensely':
                              score = 1
                        adv_function = 'degree'
                    else:
                        for prep_child in child.children:
                            if prep_child.dep_ == 'prep':
                                if prep_child.pos_ == 'NOUN':
                                    if prep_child.text == 'time':
                                        adv_function = 'time'
                                    else:
                                        adv_function = 'place or direction'
                                elif prep_child.pos_ == 'ADJ':
                                    adv_function = 'manner'
                    if adv_function : 
                              listadverb = [token.text, adv_function, score]
                              print("ADVERB" + adv_function, score)
                              detectedadverbLists.append(listadverb)
                              return adv_function, score

    return detectedadverbLists

def detectpersonalpronounce(text):
     temp = 0
     text_doc = text
    #detect personal pronounce
     for token in text_doc:

                if token.text.lower() == "i" or token.text.lower() == "me" or token.text.lower() == "myself":
                    print(token.text.lower())
                    temp = 1
                    return temp
    
     return temp
            
