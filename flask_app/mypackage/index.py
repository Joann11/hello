negdicfile = "negdicfile.txt"
posdicfile = "posdicfile.txt"
neudicfile = "neudicfile.txt"
filename = "example.txt" 

import re
import spacy
import keywords
import matplotlib.pyplot as plt

from spacy.symbols import ORTH
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from spacy.pipeline import EntityRuler
from jinja2 import Template
from flask import render_template
from faker import Faker
import random

from random import randint


#from spacy import displacy

nlp = spacy.load('en_core_web_sm', disable=['ner']) 
matcher = PhraseMatcher(nlp.vocab)
neutraldic = keywords.addnewKeyWordNeu_function(neudicfile)
negativedic = keywords.addnewKeyWordNegative_function(negdicfile)
positivedic = keywords.addnewKeyWordPositive_function(posdicfile)
                        



def  nlpSetRule():  
       
    
        pattern = re.compile(r'"(.*?)"\s+=\s+"(.*?)"')
                    #Create the Ruler and Add it

        ruler = nlp.add_pipe("entity_ruler", config={"phrase_matcher_attr": "LOWER"})

        for p in negativedic:
                ruler.add_patterns([{"label": "Negative", "pattern": p}])
      
        for x in neutraldic:
                 ruler.add_patterns([{"label": "Neutral", "pattern": x}])
        for z in positivedic:
                 ruler.add_patterns([{"label": "Positive", "pattern": z}])



        ruler.to_disk("patterns.jsonl")  # saves patterns only
        ruler.to_disk("entity_ruler")    # saves patterns and config    
                         
                   

def getText():
    text = open(filename, "r").read()
    text_doc = nlp(text)
    return text_doc
    
def generaterandomSentTest():
      # Declaring names, verbs and nouns
        names=["You","I","They","He","She","Robert","Steve"]
        verbs=["was", "is", "are", "were"]
        nouns=["playing cricket.", "watching television.", "singing.", "fighting.", "cycling."]
        negsent = negativedic
        sent = ""
        t = random.randint(0,10)
        for x in range(t):
            
        
            a=(random.choice(names))
            b=(random.choice(verbs))
            c=(random.choice(list(negsent.keys())))
            sent += a+" "+b+" "+c +"."

            print(sent)
            
        # f = open("example.txt", "w")
        # f.write(str(sent))
        # f.close()

        return str(sent)
generaterandomSentTest()

# #create the list of words to match



       


# def addnewKeyWordNegative_function():

#         with open(negdicfile, 'r') as f:
#             for line in f:
              
#                         (key, val) = line.split() 
#                         if(negativedic.get(key) is None):
#                          negativedic[key] = int(val)
            
            
#             for p in negativedic:
#                 ruler.add_patterns([{"label": "Negative", "pattern": p}])

       
#             print (negativedic)
#             return negativedic

# def addnewKeyWordNeu_function():
#             with open(neudicfile, 'r') as f:
#                 for line in f:
#                             (key, val) = line.split()
#                             if(neutraldic.get(key) is None):

#                                 neutraldic[key] = int(val)
#                 for p in neutraldic:
#                     ruler.add_patterns([{"label": "Neutral", "pattern": p}])

#             print (neutraldic)
#             return neutraldic

# def addnewKeyWordPositive_function():
#         with open(posdicfile, 'r') as f:
#             for line in f:
#                         (key, val) = line.split()
#                         if(positivedic.get(key) is None):

#                             positivedic[key] = int(val)
                        
#             for p in positivedic:
#               ruler.add_patterns([{"label": "Positive", "pattern": p}])

#         print(positivedic)
#         return positivedic





# depressedKeyWords = ['die', 'anxiety','insomnia','dysfunction','fatigue','nervous', 'unhappy', 'no focus', 'disturbed', 'isolation', 'lack of interest', 'low interaction', 'sleep problems', 'loss meaning in life', 'stressed', 'uneasiness', 'instability', 'moody', 'emotional', 'low self-esteem', 'have no emotional support', 'depressed', 'depression', 'suicide', 'broken', 'killme', 'worthless', 'selfharm', 'pain', 'sad', 'numb']
# happyKeyWords = ['happy','grateful',]
#obtain doc object for each word in the list and store it in a list
#patterns = [nlp(keyword) for keyword in depressedKeyWords]
# #happypatterns = [nlp(keyword) for keyword in happyKeyWords]
# patternsNg = [nlp(keyword) for keyword in negativedic]
# patternsNu = [nlp(keyword) for keyword in neutraldic]
# patternsPs = [nlp(keyword) for keyword in positivedic]


#add the pattern to the matcher
##matcher.add("Negative Dictionary", patternsNg)
#matcher.add("Positive Dictionary", patternsPs)
#matcher.add("Neutral Dictionary", patternsNu)

#process some text


def setNegativeTotal(severetotal):
      

       return severetotal

def setPositiveTotal(positivetotal):
     

     return positivetotal


##https://research.reading.ac.uk/research-blog/people-with-depression-use-language-differently-heres-how-to-spot-it/#:~:text=Those%20with%20symptoms%20of%20depression%20use%20significantly%20more%20first%20person,them%E2%80%9D%20or%20%E2%80%9Cshe%E2%80%9D.

def detectpersonalpronounce():
     temp = 0
     text_doc = getText()
    #detect personal pronounce
     for token in text_doc:

                if token.text.lower() == "i" or token.text.lower() == "me" or token.text.lower() == "myself":
                    print(token.text.lower())
                    temp = 1
                    return temp
    
     return temp
            


def totalScoreComment(severetotal, positivetotal, neu):
    
            
            #total analysis 

            totalscore =  positivetotal - severetotal 
            if(totalscore == 0):
                        comment = "<br> This sentences is Neutral</br>"
            elif(totalscore > 0):
                        comment = "<br> This sentences is quite positive </br>"
            else: 
                        comment = "<br> This sentence is quite negative </br>"
            

           # html = Template( """<html> <body> <p> {{comment}}</p> </body></html>""")

           # return html.render(comment = comment)
                          
            comment = "Positive Score : "+"<b>" +str(positivetotal)+ "</b>" +" Negative Score : "+ "<b>"+str(severetotal)+ "</b>"+" Neutral Detected : "+ "<b>"+str(neu)+ "</b>"+ "Total Score: "+"<b> " + str(totalscore) +"</b>" + comment 
            comment += str(positivetotal) +" - " + str(severetotal) + " = " + str(totalscore)
            return  comment     # data = {"score" : 1}

            # return render_template("main.html", data=data)



def totalscorePronounce(severetotal, positivetotal):
            comment = ""
            #total analysis with personal pronounce analysed
            temp = detectpersonalpronounce()
            if( temp > 0):
            
                    totalscore =  positivetotal - severetotal - temp
                    if(totalscore == 0):
                        status ="this sentences is Neutral"
                    elif(totalscore > 0):
                        status = "this sentences is quite positive"
                    else:
                        status = "this sentence is quite negative"
                    comment = "Personal Pronounce detected Consider <br>"
                    comment +=  " Total Score : " + "<b>"+ str(totalscore) +  "</b>"+" Positive Score :" + "<b>"+ str(positivetotal) +  "</b>"+" Negative Score : "+ "<b>" + str(severetotal+temp) +  "</b>" + "<br>"+ status
                    comment += str(positivetotal) +" - " + str(severetotal) +"- <b>" +str(temp) +"<b>" +" = " + str(totalscore)

            else:

                comment = "No first person personal pronounce detected"
        
            
            result = "<p> Consider First Personal Pronounce (I, MYSELF, ME): "+ "<br>" +comment +"</p>"

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
         
            if token.text in detectedwords.keys():
                print(token.text +"TEST")
                # one-liner
                # 
               # keyList = list(detectedwords.keys())
                sentiment = detectedwords.get(token.text)
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
                        print("got it")
                        foundN = "<mark class = \"negation\">" + token.text +"</mark> "
                        #Negation found :"
                        strW += foundN
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
          if token.text in detectedwords.keys():
            sentiment = detectedwords.get(token.text)

            # keyList = list(detectedwords.keys())
            # val_list = list(detectedwords.values())
            # position = keyList.index(token.text)
            # print(position)

            if sentiment == "Negative":
                  
                    scoring = negativedic.get(token.text.lower())
                    strW +=  "-" + str(scoring)

            elif sentiment == "Positive":
                    scoring = positivedic.get(token.text.lower())
                    strW +=  str(scoring) 

            elif sentiment == "neg":
                     #Negation found :"
                    strW += foundN

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



detectedwords = {}



def getWordCount(sent):
    # Count words without counting punctuation 
        temp = 0
        clean_text = [token for token in sent if not token.is_punct]

        temp = temp + 1
        wordcount = len(clean_text)
    
        return wordcount

def sentenceAnalysis():
    totaleachSent = []
   
    averageN = []
    averageP = []
    averageC = []


    for sent in getText().sents:
        countK = 0
        countPositive = 0 
        countNegative = 0
        for ent in sent.ents:
                    
            countK = countK + 1

            if ent.label_ == "Negative":
                    countNegative = countNegative + 1
                    
            elif  ent.label_ == "Positive":
                    countPositive = countPositive + 1

        averageP.append(countPositive / getWordCount(sent))
        averageN.append(countNegative / getWordCount(sent))
        averageC.append(countK / getWordCount(sent))        
    
  
    return averageP, averageN, averageC



def plotGraph(averageP, averageN, averageC):
    y1 = averageP
    y2 = averageN
    y3 = averageC
    x = []
    
    for i in range(len(averageC)):
        x.append(i+1)
        print(i)
    
    plt.plot(x, y1, label= "Positive")
    plt.plot(x, y2, label = "Negative")
    plt.plot(x, y3, label = "Total")

    plt.xlabel('Sentences')
    plt.ylabel('Average of keywords')
    plt.xticks(x)
    plt.title('Average of keywords/Total Words Per Sentence')
    plt.legend()
    plt.show()
    plt.savefig('my_plot.png')

 
def plotGraphPerSentence(score):
     y = score
     x = []
    
     for token in getText():
         if not token.is_punct:
          x.append(token.text)
        
     plt.plot(x, y )

     plt.xlabel('Words')
     plt.ylabel('Score')
     plt.xticks(x)
     plt.title('Sentence Analysis')
     plt.legend()
     plt.show()
     plt.savefig('plotsentence.png')




def plotEachSentence(ent):
        #findkeywords
        print("BELLO"+ent.text)
        scoring = 0
        text_doc = getText()
        score = []
        foundNeg = False
                                        
        for token in text_doc:
                 #if there is a negation such as 'not' in the text phrase
                    if token.dep_ == 'neg':
                        foundNeg = True

                    
        if not foundNeg:
            for token in text_doc:
                if token.text != ent.text:
                    score.append(0)
                else:
                    if ent.label_ == "Negative":
                        scoring =  -negativedic.get(ent.text.lower()) 
                        score.append(scoring)
                    elif ent.label_ == "Positive":
                        scoring = positivedic.get(ent.text.lower()) 
                        score.append(scoring)             
        elif foundNeg:


              for token in text_doc:
                 if token.text != ent.text:
                    score.append(0)
               
                 else:
                        action = token.head.text
                      
                        #if it is a keyword then the idea is inverted like 'not depressed'
                        if ent.text == action and ent.label_ == "Negative":
                                #becomes neutral x = 0
                                scoring =  negativedic.get(ent.text.lower()) * 0
                                score.append(0)
                                score.append(0)
                                                
                        #if is not happy inverted positive to negative
                        elif ent.text == action and ent.label_ == "Positive":
                                scoring = positivedic.get(ent.text.lower()) * -1
                                score.append(scoring)
                                score.append(scoring)

                        else:
                                
                                
                                if token.dep_ == 'neg':
                                    
                                    if ent.label_ == "Negative" :
                                            scoring =  negativedic.get(ent.text.lower()) * 0
                                            score.append(000)
                                            
                              
                                    elif ent.label_ == "Positive":
                                            scoring = positivedic.get(ent.text.lower()) * -1
                                            score.append(-111)
                                
                                for i in range(len(score)):
                                    foundindex = False
                                    if score[i] == -111 or score[i] == 000:
                                        foundindex = True
                     
                                    if foundindex :
                                         if score[i] == -111:
                                          score[i] == positivedic.get(ent.text.lower()) * -1

                                         elif score[i] == 000:
                                          score[i] =  0

                                    
                                           

                        
                                        



                                # substuff = list(token.head.rights)
                                # #FIND AUX IN THE SUB TREE SUCH AS BE, HAS DONE, WILL DO, SHOULD DO
                                # if(token.n_rights > 0 and substuff[0].pos_ == 'AUX' ):

                                #     for x in range(token.n_rights):
                                #         if ent.label_ == "Negative":
                                #              scoring =  negativedic.get(ent.text.lower()) * 0
                                #              score.append(0)
                              
                                        
                                #         elif ent.label_ == "Positive":
                                #              scoring = positivedic.get(ent.text.lower()) * -1
                                #              score.append(scoring)

                       
                    
                                          


                                    
                                #     print("FOUND AUX")
                                #     t = substuff[0] 
                                #     substuff = list(t.rights)
                                #     print(str(substuff))
                                
                        #         for k in substuff:
                        #              if ent.text == k.text :
                                        
                        #                     if(ent.label_ == "Positive"):
                                               

                        #                         negationcomment += "Total Negative Score increased by" + str(positivedic.get(ent.text.lower())) +"because"

                        #                         severetotal = severetotal + positivedic.get(ent.text.lower())
                        #                         #positivetotal = positivetotal - positivedic.get(ent.text.lower())
                        #                     print("Found negation " + token.text+ ent.text)
                        #                     if(ent.label_ == "Negative"):
            
                        #                         negationcomment += "Total Ngative Score decreased by" + str(negativedic.get(ent.text.lower())) +"because"
                        #                         severetotal = severetotal - negativedic.get(ent.text.lower())
                                        
                        #                     print("Found negation " + token.text+ ent.text)
                        # negationcomment += "Found negation: " + token.text +" to keyword "+ ent.label_ + " :"+ ent.text
    
                        #score.append (positivedic.get(ent.text.lower() * -1))
                                                
                        
        
       
            
        return score; 

#def testCase(typeSent):
  #  if typeSent == "pos":

#return the type of adverb meaning 
def detect_adverb(sent):

    score = 0
   
    for ent in sent.ents:

        for token in sent:
              for child in token.children:
                if child.dep_ == 'advmod':
                    adv_function = ''
                    if child.text.lower() in ['quite','very', 'extremely', 'intensely']:
                        if child.text == 'quite':
                              score = 0.25
                        elif child.text == 'very':
                              score = 0.5
                        elif child.text == 'very':
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
                              return adv_function, score
                       
    return None





#detect adverb such as very or quite
def detect_adverbs_with_keyword(token):
        
            for child in token.children:
                if child.dep_ == 'advmod':
                    print(f"Adverb '{child.text}' modifying verb '{token.text}' detected.")


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
      
        for ent in text_doc.ents:
                    
                    print("OK")
                    print(ent, ent.label_)
                    scoring = 0
                    
                    detectedwords[ent.text] = ent.label_
                    print(detectedwords)

                    if ent.label_ == "Negative":
                        scoring = negativedic.get(ent.text.lower())
                        severetotal = severetotal + scoring

                    elif  ent.label_ == "Positive":
                        scoring = positivedic.get(ent.text.lower())
                        positivetotal = positivetotal + scoring

                    elif  ent.label_ == "Neutral":
                        neu = neu + 1
                    

                 
                            
                    for token in text_doc:
                    #if there is a negation such as 'not' in the text phrase
                        if token.dep_ == 'neg':
                            detectedwords[token.text] =  token.dep_
                            print ("Token dep" +token.dep_)

                        
                            action = token.head.text
                            #find the dependecy of this negation. 
                            print("NOT WRONG")
                            print(token.head.text, token, ent.text)
                                
                            #if it is a keyword then the idea is inverted like 'not depressed'
                            if ent.text == action and ent.label_ == "Negative":
                                    print("Found negation to keyword Negative " + token.text)
                                    print(token.head.text, token)
                                    #negativedic.get(ent.text.lower())
                                #severe of depression deducted but positive will not be changed. Take it as neutral. 
                                    #severetotal = severetotal - negativedic.get(ent.text.lower())
                                    severetotal = severetotal - scoring
                                    print(severetotal)
                                    negationcomment += "Total Negative Score decreased by" + str(positivedic.get(ent.text.lower())) +"because"
                                    
                                                    
                            #if is not happy inverted positive to negative
                            elif ent.text == action and ent.label_ == "Positive":
                                    positivetotal = positivetotal - positivedic.get(ent.text.lower())
                                    severetotal = severetotal + positivedic.get(ent.text.lower())
                                    print(severetotal)
                                
                                #severe of negative increased and positive deducted.
                                    
                                    print("Found negation to keyword Positive hi " + token.text)
                                    print(token.head.text, token)
                                    negationcomment += "Total Negative Score increased by" + str(positivedic.get(ent.text.lower())) +"because"

                                                
                            #         #if the negation is not dependent on the keywords such as 'want' or 'hope', search for keyword within the subtree
                            
                            else:
                                    substuff = list(token.head.rights)
                                    
                                    #FIND AUX IN THE SUB TREE SUCH AS BE, HAS DONE, WILL DO, SHOULD DO
                                    if(len(substuff) > 0 and substuff[0].pos_ == 'AUX' ):
                                        print("FOUND AUX")
                                        t = substuff[0] 
                                        substuff = list(t.rights)
                                        print(str(substuff))
                                    
                                    for k in substuff:
                                        if ent.text == k.text :
                                            
                                                if(ent.label_ == "Positive"):
                                                

                                                    negationcomment += "Total Negative Score increased by" + str(positivedic.get(ent.text.lower())) +"because"

                                                    severetotal = severetotal + positivedic.get(ent.text.lower())
                                                    positivetotal = positivetotal - positivedic.get(ent.text.lower())
                                                print("Found negation " + token.text+ ent.text)
                                                if(ent.label_ == "Negative"):
                
                                                    negationcomment += "Total Ngative Score decreased by" + str(negativedic.get(ent.text.lower())) +"because"
                                                    severetotal = severetotal - negativedic.get(ent.text.lower())
                                            
                                                print("Found negation " + token.text+ ent.text)
                            negationcomment += "Found negation: " + token.text +" to keyword "+ ent.label_ + " :"+ ent.text
                            
                    
                    # scores.append(positivetotal - severetotal)
                    # positivetotal = 0
                    # severetotal = 0

        
                            
                        
                        
                        

                #  print("score" + str(plotEachSentence(ent)))
                    #total analysis 
                    comment = totalScoreComment(severetotal, positivetotal, neu)
                    commentP =  totalscorePronounce(severetotal, positivetotal)

                
        count = str(sentenceAnalysis())
                
        p,n,c = sentenceAnalysis()
        #  plotGraph(p,n,c)

        if not detectedwords:
                result = "no word detected" + count 
        else:    
                result = comment + negationcomment+ commentP + count 

        return result

            

print(str(calculatescore_function()))


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
