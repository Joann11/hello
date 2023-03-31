negdicfile = "negdicfile.txt"
posdicfile = "posdicfile.txt"
neudicfile = "neudicfile.txt"
filename = "example.txt" 

import re
import spacy
import plotGraph
import json

import keywords
import matplotlib.pyplot as plt
import detect
from spacy.symbols import ORTH
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from spacy.pipeline import EntityRuler
from spacy.tokens import Token #import Token class from spacy
from jinja2 import Template
from flask import render_template
#from spacy import displacy

nlp = spacy.load('en_core_web_sm', disable=['ner']) 


matcher = PhraseMatcher(nlp.vocab)
neutraldic = keywords.addnewKeyWordNeu_function(neudicfile)
negativedic = keywords.addnewKeyWordNegative_function(negdicfile)
positivedic = keywords.addnewKeyWordPositive_function(posdicfile)
detectedwords = {}                       
Token.set_extension('score', default=False, force=True)


def getText():
    text = open(filename, "r").read()
    text_doc = nlp(text)
    return text_doc


def set_score(doc):
    for token in doc:
        token._.set("score", 0.0)

def  nlpSetRule():  
       
    
        pattern = re.compile(r'"(.*?)"\s+=\s+"(.*?)"')
                    #Create the Ruler and Add it

        ruler = nlp.add_pipe("entity_ruler", config={"phrase_matcher_attr": "LEMMA"})
        #nlp.add_pipe(set_score, name='set_score', last=True)
      
        for p in negativedic:
                 ruler.add_patterns([{"label": "Negative", "pattern": p}])
                 
        for x in neutraldic:
                 ruler.add_patterns([{"label": "Neutral", "pattern": x}])
        
        for z in positivedic:
                 ruler.add_patterns([{"label": "Positive", "pattern": z}])




        ruler.to_disk("patterns.jsonl")  # saves patterns only
        ruler.to_disk("entity_ruler")    # saves patterns and config    
                            


# def wh_handling(text):

#      for token in text:
#          if token.dep_ == "relcl":
#            subject = None
#             for child in token.children:
#                 if child.dep_ == "nsubj":
#                     subject = child
#             if subject is None:
#                 continue
#             new_sentence = f"{subject} {token.head.text}"
#             for child in token.children:
#                 if child.dep_ != "nsubj":
#                     new_sentence += f" {child}"
#             return new_sentence.strip(), text.replace(new_sentence, "").strip()
#     return None, None

# def conjunction_handling(text):
#     for token in text:
#         if token.text == "and":
#             subject = None
#             for child in token.children:
#                 if child.dep_ == "conj":
#                     subject = child
#             if subject is None:
#                 continue
#             if subject.dep_ == "ccomp":
#                 subject = None
#                 for child in token.children:
#                     if child.dep_ == "nsubj":
#                         subject = child
#                 if subject is None:
#                     continue
#             new_sentence = f"{subject.text} {token.head.text}"
#             for child in token.children:
#                 if child.dep_ != "conj":
#                     new_sentence += f" {child}"
#             return new_sentence.strip(), text.replace(new_sentence, "").strip()
#     return None, None

# def insertion_handling(text):
    
#     for token in text:
#         if token.dep_ in ["amod", "appos", "acl", "advcl", "advmod", "relcl"]:
#             clause_root = None
#             for child in token.children:
#                 if child.dep_ == "mark":
#                     clause_root = child.head
#                 elif child.dep_ == "relcl":
#                     clause_root = child
#             if clause_root is None:
#                 continue
#             clause = clause_root.subtree
#             subject = None
#             for child in clause_root.children:
#                 if child.dep_ == "nsubj":
#                     subject = child
#             if subject is None:
#                 continue
#             new_sentence = f"{subject} {clause_root.text}"
#             for child in clause:
#                 if child is not clause_root:
#                     new_sentence += f" {child}"
#             return new_sentence.strip(), text.replace(new_sentence, "").strip()
#     return None, None

# def split_complex_sentenceX(sentence):
#     new_sentences = []
#     while sentence:
#         new_sentence, sentence = wh_handling(sentence)
#         if new_sentence:
#             new_sentences.append(new_sentence)
#             continue
#         new_sentence, sentence = conjunction_handling(sentence)
#         if new_sentence:
#             new_sentences.append(new_sentence)
#             continue
#         new_sentence, sentence = insertion_handling(sentence)
#         if new_sentence:
#             new_sentences.append(new_sentence)
#             continue
#         new_sentences.append(sentence.strip())
#         break
#     return new_sentences

# doccc = getText()
# split_complex_sentenceX(doccc)


# #spliting sentence
# def split_complex_sentence(sentence):
#     doc = nlp(sentence)
    
#     # Handling Relational Arguments (R-ARGs)
#     for token in doc:
#         if token.dep_ == 'relcl':
#             r_arg = token.head
#             s_arg = [t for t in r_arg.lefts if t.dep_ == 'nsubj'][0]
#             new_sentence = s_arg.text + ' ' + sentence[s_arg.end:r_arg.start].strip() + ' ' + r_arg.text + ' ' + sentence[r_arg.end:].strip()
#             return split_complex_sentence(new_sentence)
    
#     # Handling Conjunctions with Argument (ARG) following 'and'
#     for token in doc:
#         if token.text == 'and' and token.nbor(1).dep_ in ['dobj', 'pobj', 'nsubj', 'attr']:
#             arg = token.nbor(1)
#             new_sentence = sentence[:arg.idx] + sentence[arg.end:].lstrip()
#             return [sentence[:token.idx].strip(), new_sentence.strip()]
        
#         # Handling Conjunctions with verb following 'and'
#         elif token.text == 'and' and token.nbor(1).pos_ == 'VERB':
#             s_arg = [t for t in token.lefts if t.dep_ == 'nsubj'][0]
#             new_sentence = s_arg.text + ' ' + sentence[s_arg.end:token.idx].strip() + ' ' + token.nbor(1).text + ' ' + sentence[token.nbor(1).end:].strip()
#             return [new_sentence.strip()]
    
#     # Handling Insertions
#     for token in doc:
#         if token.dep_ in ['amod', 'advmod', 'prep', 'appos', 'relcl']:
#             new_sentence = sentence[token.left_edge.idx:token.right_edge.idx].strip()
#             new_sentence = sentence[:token.head.idx].strip() + ' ' + new_sentence + ' ' + sentence[token.right_edge.idx:].strip()
#             return [new_sentence.strip(), sentence[:token.left_edge.idx].strip()]
        
#     return [sentence.strip()]

# #print(split_complex_sentence("I think she thinks I am rubbish and I am sad"))



def setNegativeTotal(severetotal):
      

       return severetotal

def setPositiveTotal(positivetotal):
     

     return positivetotal


##https://research.reading.ac.uk/research-blog/people-with-depression-use-language-differently-heres-how-to-spot-it/#:~:text=Those%20with%20symptoms%20of%20depression%20use%20significantly%20more%20first%20person,them%E2%80%9D%20or%20%E2%80%9Cshe%E2%80%9D.

def totalScore(text, severetotal, positivetotal):

     detectedadverbLists = detect.detect_adverb(text) 
     adscore = 0
     totalscore = 0
     if detectedadverbLists :
                     for adverb in detectedadverbLists:
                            adscore += adverb[2]


     totalscore = positivetotal - severetotal
     #if result is positive plus, else minus
     if totalscore > 0 :
        totalscore += adscore
     else : 
        totalscore -= adscore 
      
     return float(totalscore)


    #ddoc :https://subscription.packtpub.com/book/data/9781838987312/2/ch02lvl1sec13/splitting-sentences-into-clauses





def totalScoreComment(totalscore, positivetotal, severetotal, neu):
    
            
            #total analysis 

         

            if(totalscore == 0):
                        comment = "<br> This sentences is Neutral</br>"
            elif(totalscore > 0):
                        comment = "<br> This sentences is quite positive </br>"
            else: 
                        comment = "<br> This sentence is quite negative </br>"
            

           # html = Template( """<html> <body> <p> {{comment}}</p> </body></html>""")

           # return html.render(comment = comment)
                          
            comment = "Positive Score : "+"<b>" +str(positivetotal)+ "</b><br>" +" Negative Score : "+ "<b>"+str(severetotal)+ "</b><br>"+" Neutral Detected : "+ "<b>"+str(neu)+ "</b><br>"+ "Total Score: "+"<b> " + str(totalscore) +"</b>" + comment 
            comment += str(positivetotal) +" - " + str(severetotal) + " = " + str(totalscore)
            return  comment     # data = {"score" : 1}

            # return render_template("main.html", data=data)


def PronounComment(severetotal, positivetotal):

            sub = detect.detectpersonalpronoun(getText())
            comment = ""
            temp = 0
            extraScore = 0
            totalscore =  positivetotal - severetotal
            #total analysis with personal pronounce analysed
            #get the score of the personal pronoun
            
            if sub is not "":
                   
                        if sub == "firstperson":
                            extraScore = 2
                        
                        elif sub == "thirdperson":
                            extraScore = 1.5
                        
                        temp = totalscore * extraScore
                        comment = "Pronoun detected: <b>"+ sub + "</b><br> "     
                        comment +=  str(totalscore) + " * " + str(extraScore) + " = <b> " + str(temp) + "</b>"

                        comment +=  "Total Score : " + "<b>"+ str(temp) 

            else:

                comment = "No first person personal pronounce detected"
        
            
            result = "<p>" +comment +"</p>"

            return result 
       

                
  

nlpSetRule()


def createWordTable():
    strW = "" 
    text_doc = getText()

    scoring = 0
    strW += "<table>"
    strW += "<tr>"
    for sent in text_doc.sents:
     for token in sent:


            strW += "<th>"
            
            
         
            if token.text.lower() in detectedwords.keys():
                print(token.text.lower() +"TEST")
                # one-liner
                # 
               # keyList = list(detectedwords.keys())
                sentiment = detectedwords.get(token.text.lower())
               # val_list = list(detectedwords.values())
               # position = keyList.index(token.text)
               # print( val_list[position])
                
                if sentiment == "Negative":
                        strW += " <mark class = \"negativeWord\">"  + token.text + "</mark> "
                        scoring = negativedic.get(token.text.lower())

                elif sentiment == "Positive":
                        scoring = positivedic.get(token.text.lower())
                        strW += " <mark class = \"positiveWord\">" + token.text + "</mark> "

                elif sentiment == "neg":
                        
                        foundN = "<mark class = \"negation\">" + token.text +"</mark> "
                        #Negation found :"
                        strW += foundN
                        strW += "</th>"

                elif sentiment == 'PRON':
                     
                    if token.text.lower() == 'i' or token.text.lower() == 'myself' or token.text.lower() == 'me':
                        foundP = "<mark class = \"firstpronoun\">" + token.text +"</mark>"

                    else:
                        foundP = "<mark class = \"pronoun\">" + token.text +"</mark> " 
                        print(token.text +"pron")
                        
                        
                    strW += foundP
                    strW += "</th>"


            else:
                strW += token.text 
                strW += "</th>"
    
    strW += "<th>TOTAL</th>"
    strW += "</tr>"
    strW += "<tr>"
    for sent in text_doc.sents:
        for token in sent:
          strW += "<td>"
          if token.text.lower() in detectedwords.keys():
            sentiment = detectedwords.get(token.text.lower())

           
            if sentiment == "Negative":
                  
                    scoring = negativedic.get(token.text.lower())
                    strW +=  "-" + str(scoring)

            elif sentiment == "Positive":
                    scoring = positivedic.get(token.text.lower())
                    strW +=  str(scoring) 

            elif sentiment == "neg":
                    strW += foundN
            
            elif sentiment == "PRON":
                    strW += foundP

          else:
            strW += " "
          strW += "</td>"


    strW += "<td>"+calculatescore_function()+"</td> </tr> </table>"
    



   # strW += token.text

    return strW
def printSA():
    strW = "" 
    text_doc = getText()
    scoring = 0

   # for token in text_doc:
        
    # for ent in text_doc.ents:
    #         if ent.label_ == "Negative":
    #                 scoring = negativedic.get(ent.text.lower())
                   
    #         elif  ent.label_ == "Positive":
    #                 scoring = positivedic.get(ent.text.lower())                    
                    
    #         strW += "<" + ent.text +":"+ str(scoring) + ent.label_+ ">"
    
    for token in text_doc:
        if token.text in detectedwords.values():
            # one-liner
            # 
            keyList = list(detectedwords.keys())
            val_list = list(detectedwords.values())
            position = val_list.index(token.text)
            print(position)

            if keyList[position] == "Negative":
                    
                    scoring = negativedic.get(token.text.lower())
                    strW += "[" + keyList[position] + " : "+ "-" + str(scoring) + "] "
                    strW += " <mark class = \"negativeWord\">" +token.text + "</mark> "

            elif keyList[position] == "Positive":
                    scoring = positivedic.get(token.text.lower())
                    strW += "[" + keyList[position] + " : "+ str(scoring)  + "]"
                    strW += " <mark class = \"positiveWord\">" + token.text + "</mark> "

            elif keyList[position] == "neg":
                    print("got it")
                    foundN = "<mark class = \"negation\">" + token.text +"</mark> "
                     #Negation found :"
                    strW += foundN

           
            

        else:
            strW += token.text + " "
   # strW += token.text

    return strW









def calculatescore_function():
        #findkeywords
        
       
            severetotal = 0
            positivetotal = 0
            text_doc = getText()
            
            #sentences = [sent.text for sent in text_doc.sents]

            print(text_doc)
            negationcomment = ""
            comment = ""
            neu = 0
            commentP = ""
            result = ""
            scores = []
            # Process each sentence separately

            # for sent in text_doc.sents:
            
            #     for ent in sent.ents:

            lemma = [token.lemma_ for token in text_doc]
            text_doc = ' '.join(lemma)
            text_doc = nlp(text_doc)
            print(text_doc)
            key = ""
            for ent in text_doc.ents :
                        
                                    print("OK")
                                    print(ent, ent.label_)
                                    scoring = 0
                                    
                                    detectedwords[ent.text.lower()] = ent.label_
                                    print(detectedwords)
                                    
                                    word = nlp(ent.text)[0]
                                    key = word.lemma_

                                    if ent.label_ == "Negative":
                                        print(ent.text, key)
                                        scoring = negativedic.get(key)
                                        severetotal = severetotal + scoring

                                    elif  ent.label_ == "Positive":
                                        scoring = positivedic.get(ent.text.lower())
                                        positivetotal = positivetotal + scoring

                                    elif  ent.label_ == "Neutral":
                                        neu = neu + 1
                                    

                                    for token in text_doc:
                                            if token.pos_ == 'PRON':
                                                            detectedwords[token.text.lower()] =  token.pos_

                                            if token.dep_ == 'neg':

                                                # Apply negation detection to this entity
                                                    negationcomment, severetotal, positivetotal = detect.detect_negation(token, ent, detectedwords, scoring, severetotal, positivetotal)
                                                
                                           #total analysis 
                                            
                                       
                            
                                    totalscore = totalScore(text_doc, severetotal, positivetotal)
                                    comment = totalScoreComment(totalscore,positivetotal, severetotal, neu)
                                    commentP =  str(PronounComment(severetotal, positivetotal))

                                        
            #count = str(plotGraph.sentenceAnalysis(text_doc))
                    
            #p,n,c = sentenceAnalysis()
            #  plotGraph(p,n,c)

            if not detectedwords:
                            result = "no word detected" 
            else:    
                            result = comment + negationcomment + commentP 

            return result

            
print(str(calculatescore_function()))






# def calculatescore_function_OLD():
#         #findkeywords
        
       
#         severetotal = 0
#         positivetotal = 0
#         text_doc = getText()
        
#         #sentences = [sent.text for sent in text_doc.sents]

#         print(text_doc)
#         negationcomment = ""
#         comment = ""
#         neu = 0
#         commentP = ""
#         result = ""
#         scores = []
#         # Process each sentence separately

#         # for sent in text_doc.sents:
        
#         #     for ent in sent.ents:

#         lemma = [token.lemma_ for token in text_doc]
#         text_doc = ' '.join(lemma)
#         text_doc = nlp(text_doc)
#         print(text_doc)
#         key = ""
#         for ent in text_doc.ents :
                    




#                     for token in text_doc:
#                     #if there is a negation such as 'not' in the text phrase
#                         if token.dep_ == 'neg':
#                             detectedwords[token.text] =  token.dep_
#                             print ("Token dep" +token.dep_)

                        
#                             action = token.head.text
#                             #find the dependecy of this negation. 
#                             print("NOT WRONG")
#                             print(token.head.text, token, ent.text)
                                
#                             #if it is a keyword then the idea is inverted like 'not depressed'
#                             if ent.text == action and ent.label_ == "Negative":
#                                     print("Found negation to keyword Negative " + token.text)
#                                     print(token.head.text, token)
#                                     #negativedic.get(ent.text.lower())
#                                 #severe of depression deducted but positive will not be changed. Take it as neutral. 
#                                     #severetotal = severetotal - negativedic.get(ent.text.lower())
#                                     severetotal = severetotal - scoring
#                                     print(severetotal)
#                                     negationcomment += "Total Negative Score decreased by" + str(positivedic.get(ent.text.lower())) +"because"
                                    
                                                    
#                             #if is not happy inverted positive to negative
#                             elif ent.text == action and ent.label_ == "Positive":
#                                     positivetotal = positivetotal - positivedic.get(ent.text.lower())
#                                     severetotal = severetotal + positivedic.get(ent.text.lower())
#                                     print(severetotal)
                                
#                                 #severe of negative increased and positive deducted.
                                    
#                                     print("Found negation to keyword Positive hi " + token.text)
#                                     print(token.head.text, token)
#                                     negationcomment += "Total Negative Score increased by" + str(positivedic.get(ent.text.lower())) +"because"

                                                
#                             #         #if the negation is not dependent on the keywords such as 'want' or 'hope', search for keyword within the subtree
                            
#                             else:
#                                     substuff = list(token.head.rights)
                                    
#                                     #FIND AUX IN THE SUB TREE SUCH AS BE, HAS DONE, WILL DO, SHOULD DO
#                                     if(len(substuff) > 0 and substuff[0].pos_ == 'AUX' ):
#                                         print("FOUND AUX")
#                                         t = substuff[0] 
#                                         substuff = list(t.rights)
#                                         print(str(substuff))
                                    
#                                     for k in substuff:
#                                         if ent.text == k.text :
                                            
#                                                 if(ent.label_ == "Positive"):
                                                

#                                                     negationcomment += "Total Negative Score increased by" + str(positivedic.get(ent.text.lower())) +"because"

#                                                     severetotal = severetotal + positivedic.get(ent.text.lower())
#                                                     positivetotal = positivetotal - positivedic.get(ent.text.lower())
#                                                 print("Found negation " + token.text+ ent.text)
#                                                 if(ent.label_ == "Negative"):
                
#                                                     negationcomment += "Total Ngative Score decreased by" + str(negativedic.get(ent.text.lower())) +"because"
#                                                     severetotal = severetotal - negativedic.get(ent.text.lower())
                                            
#                                                 print("Found negation " + token.text+ ent.text)
#                             negationcomment += "Found negation: " + token.text +" to keyword "+ ent.label_ + " :"+ ent.text
                            
                    
#                     scores.append(positivetotal - severetotal)
#                     positivetotal = 0
#                     severetotal = 0

        
                            
                        
                        
                   
#                     #print("score" + str(plotEachSentence(ent)))
#                     #total analysis 
#                     totalscore = totalScore(text_doc, severetotal, positivetotal)
#                     comment = totalScoreComment(totalscore,positivetotal, severetotal, neu)
#                     commentP =  str(totalScorePersonalPronoun(totalscore))

                
#         count = str(plotGraph.sentenceAnalysis(text_doc))
                
#         #p,n,c = sentenceAnalysis()
#         #  plotGraph(p,n,c)

#         if not detectedwords:
#                 result = "no word detected" + count 
#         else:    
#                 result = comment + negationcomment+ commentP + count 

#         return result

            

# print(str(calculatescore_function_OLD()))





                        #if the negation is not dependent on the keywords such as 'want' or 'hope', search for keyword within the subtree
                        
        #                 else:
        #                         substuff = list(token.head.rights)
        #                         for k in substuff:
                                    
        #                             if ent.text == k.text :
                                        
        #                                     if(ent.label_ == "Positive"):

        #                                         scoring = negativedic.get(action) * -1
        #                                         for k in substuff:
        #                                             score.append(scoring)
                                                
                                                
        #                                         negationcomment += "Total Negative Score increased by" + str(positivedic.get(ent.text.lower())) +"because"

        #                                         severetotal = severetotal + positivedic.get(ent.text.lower())
        #                                         #positivetotal = positivetotal - positivedic.get(ent.text.lower())
        #                                     print("Found negation " + token.text+ ent.text)
        #                                     if(ent.label_ == "Negative"):
        #                                         negationcomment += "Total Ngative Score decreased by" + str(negativedic.get(ent.text.lower())) +"because"
        #                                         severetotal = severetotal - negativedic.get(ent.text.lower())
                                        
        #                                     print("Found negation " + token.text+ ent.text)
        #                 negationcomment += "Found negation: " + token.text +" to keyword "+ ent.label_ + " :"+ ent.text
    
                        
                    
                    
                    

                
        #         #total analysis 
        #         comment = totalScoreComment(severetotal, positivetotal)
        #         commentP =  totalscorePronounce(severetotal, positivetotal)

        # count = str(sentenceAnalysis())
        
        # # p,n,c = sentenceAnalysis()
        # # plotGraph(p,n,c)

        # if not detectedwords:
        #     result = "no word detected" + count 
        # else:    
        #     result = comment + negationcomment+ commentP + count 

        # return result
           
    
   # string_id = nlp.vocab.strings[match_id]
   # span = text_doc[start:end]  
   # if string_id == "Negative Dictionary":
    #    severetotal = severetotal + negativedic.get(span.text)
   # elif string_id == "Positive Dictionary":
    #    positivetotal = positivetotal + positivedic.get(span.text)
    





#for match_id, start, end in matches:
 #       string_id = nlp.vocab.strings[match_id]  # Get string representation
  #      span = text_doc[start:end]  # The matched span
   #     #total number of detected words from depression 
    #    if string_id == "Depression":
     #       severetotal = severetotal + 1
      ##  if string_id == 'Happy':
        #    positivetotal = positivetotal + 1 
        #
            
        #stringid is the key 
        #print("Matched keyword from " + span.text, string_id)
        #for token in text_doc:
                #if there is a negation such as 'not' in the text phrase
        #    if token.dep_ == 'neg':
        #     #find the dependecy of this negation. 
        #          action = token.head.text
        #          print(token.head.text, token, span.text)
                  
        #          #if it is a keyword then the idea is inverted like 'not depressed'
        #          if span.text == action and string_id == "Depression":
        #             print("Found negation to keyword Depression " + token.text)
        #             print(token.head.text, token)
        #             #severe of depression deducted but positive will not be changed. Take it as neutral. 
        #             severetotal = severetotal - 1
                    
        #         #if is not happy inverted positive to negative
        #          elif span.text == action and string_id == "Happy":
        #             print("Found negation to keyword Happy hi " + token.text)
        #             print(token.head.text, token)
        #             #severe of depression increased and positive deducted.
        #             positivetotal = positivetotal - 1
        #             severetotal = severetotal + 1
                   
        #         #if the negation is not dependent on the keywords such as 'want' or 'hope', search for keyword within the subtree
        #          else:
        #              substuff = list(token.head.rights)
        #              for k in substuff:
        #                 if span.text == k.text :
        #                       if(severetotal > 0):
        #                         if(string_id == "Happy"):
        #                          severetotal = severetotal + 1
        #                          positivetotal = positivetotal - 1
                                
               
                                # print("Found negation " + token.text)
                                # if(string_id == "Depression"):
                                #  severetotal = severetotal - 1
                                # print("Found negation " + token.text)
                                
                                # print(k)



                   


#print ([token.text for token in text_doc])

# about_doc = nlp(text)
# sentences = list(about_doc.sents)
# normalized_text = [token for token in text_doc if not token.is_stop]
# #print (normalized_text)
#clean _text = [token for token in normalized_text if not token.is_punct]
# #print (clean_text)  
# #get token by index
# token = text_doc[2]
# #print(token)
# for token in clean_text:
#    # print (token, token.lemma_)
#     print(token.text, token.dep_, token.head.text, token.head.pos_,
#       token.pos_,[child for child in token.children])


#     #word frequency count 
#     from collections import Counter 
# words = [token.text for token in clean_text if not token.is_stop and not token.is_punct]
# word_freq = Counter(words)
# # 10 commonly occurring words with their frequencies
# common_words = word_freq.most_common(10)
# #print (common_words)


   








#https://www.merriam-webster.com/thesaurus/depression
#https://towardsdatascience.com/journey-to-the-center-of-multi-label-classification-384c40229bff
#https://medium.com/neuronio/from-sentiment-analysis-to-emotion-recognition-a-nlp-story-bcc9d6ff61ae
#https://monkeylearn.com/sentiment-analysis/
#https://www.nature.com/articles/s41746-022-00589-7
#https://www.researchgate.net/publication/343915061_Detecting_Depression_from_Human_Conversations
#https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3107011/
