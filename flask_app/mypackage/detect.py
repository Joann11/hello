
import re
import keywords
import spacy 
from spacy.symbols import ORTH
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher

nlp = spacy.load('en_core_web_sm')

degreeAdverbs = ['quite','very', 'extremely', 'intensely']
neutraldic = keywords.neutraldic
negativedic = keywords.negativedic
positivedic = keywords.positivedic




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

#this function detects the pronouns in a text in response to a keyword
def detectpersonalpronoun(text):
     
     
     temp = 0
     text_doc = text
     sub = ""
    
     subject = None
     for token in text_doc:
        if token.dep_ == 'nsubj':
            subject = (token.text).lower()
            break
       
     if subject:
            if subject == "she" or subject == "he" or subject == "her" or subject == "him" or subject == "they" or subject == "them":
                sub = "thirdperson"
                
            elif subject == "you":
                sub = "secondperson"

            elif  subject == "i" or subject == "me" or subject == "myself" :
                 sub = "firstperson"
            
            elif subject == "we" or subject == "us":
                sub = "firstpersonplural"
            

            print("The subject of the sentence is " + subject)
     else:
            print("Could not identify the subject of the sentence")
        

     for sent in text_doc.sents:
                
                for ent in sent.ents:
                    for token in sent:
                    
                        for child in token.children:
                    
                            if child.pos_ == 'PRON' and child.dep_ == 'nsubj' and child.text == subject:
                                    print(token.text, 'is attached to the subject:', subject)
                            else:
                                    print(child.pos_)
   
    
     return sub
            

def detect_negation(token, ent, detectedwords, scoring, severetotal, positivetotal):
   
   
            detectedwords[token.text] =  token.dep_
            print("Token dep" + token.dep_)
            
            action = token.head.text
            print("NOT WRONG")
            print(token.head.text, token, ent.text)
                   
            #if it is a keyword then the idea is inverted like 'not depressed'
            if ent.text == action and ent.label_ == "Negative":
                negationcomment, severetotal = handle_negative(ent.text, negationcomment, severetotal, scoring)
            
            #if is not happy inverted positive to negative    
            elif ent.text == action and ent.label_ == "Positive":
                negationcomment, severetotal, positivetotal = handle_positive(ent.text, negationcomment, severetotal, positivetotal)
            
            else:  
                negationcomment, severetotal, positivetotal = detect_sub_negation(token, ent, scoring, severetotal, positivetotal)
                                          
            return negationcomment, severetotal, positivetotal


def handle_negative(text, comment, total, scoring):
    total = total - scoring
    comment += f"Total Negative Score decreased by {scoring} because {text.lower()} was negated."
    return comment, total


def handle_positive(text, comment, negative_total, positive_total):
    negative_total = negative_total + positivedic.get(text.lower())
    positive_total = positive_total - positivedic.get(text.lower())
    comment += f"Total Negative Score increased by {positivedic.get(text.lower())} because {text.lower()} was negated."
    return comment, negative_total, positive_total



def detect_sub_negation(token, ent, scoring, severetotal, positivetotal):
     # Check if there is a sub-tree to the right of the head
                negationcomment = ""  # initialize negationcomment
                substuff = list(token.head.rights)
           
                #exp:She is not going to be sad 
                if len(substuff) > 0 and (substuff[0].pos_ == 'AUX'):
                    t = substuff[0]
                    substuff = list(t.rights)
                
                #loop through the sub-tree of the token
                for k in substuff:   
                    if ent.text == k.text: 
                       
                        if ent.label_ == "Positive":
                            negationcomment, severetotal, positivetotal = handle_positive(ent.text, negationcomment, severetotal, positivetotal)
                            
                        elif ent.label_ == "Negative":
                            negationcomment, severetotal = handle_negative(ent.text, negationcomment, severetotal, scoring)
                        


    
                        
                return negationcomment, severetotal, positivetotal


                            #    
    


 #detect personal pronounce
    #  for token in text_doc:

    #             if token.text.lower() == "i" or token.text.lower() == "me" or token.text.lower() == "myself":
    #                 print(token.text.lower())
    #                 temp = 1
    #                 return temp

                