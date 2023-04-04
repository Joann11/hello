


import re
import spacy
import keywords
import matplotlib.pyplot as plt
from spacy.symbols import ORTH
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from spacy.pipeline import EntityRuler


nlp = spacy.load('en_core_web_sm', disable=['ner']) 


def getWordCount(sent):
    # Count words without counting punctuation 
        temp = 0
        clean_text = [token for token in sent if not token.is_punct]

        temp = temp + 1
        wordcount = len(clean_text)
    
        return wordcount


def sentenceAnalysis(text):
    totaleachSent = []
   
  
    averageC = []

   
    for sent in text.sents:
        count = 0
        score = 0   
        key = ""
       
        for ent in sent.ents:
              
            word = nlp(ent.text)[0]
            key = word.lemma_

            if ent.label_ == "Negative":
                   score -= keywords.negativedic.get(key)
                      
            elif  ent.label_ == "Positive":
                    score += keywords.positivedic.get(key)

            count +=1           
        if count > 0:
      
            averageC.append(score/count) 
            print(len(sent)) 
        
    
    
    print(averageC)
    return averageC


def sentenceAnalysisNew(text):
    totaleachSent = []
   
    averageN = []
    averageP = []
    averageC = []


    for sent in text.sents:
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
        averageN.append((-1*countNegative) / getWordCount(sent))
        averageC.append(countK / getWordCount(sent))        
    
  
    return averageP, averageN, averageC


                                           

                        
def plotGraphC(averageC):
   
    y = averageC
    x = []
    
    for i in range(len(averageC)):
        x.append(i)
        print(i)
    
    plt.clf()
   
    plt.plot(x, y, label = "Total")

    plt.xlabel('Sentences')
    plt.ylabel('Average Score ')
    plt.xticks(x)
    plt.title('Ratio of Average Per Sentence(Keyword)')
    plt.legend()
    #plt.show()
    plt.savefig('static/my_plot.png')
    return 'my_plot.png'



def plotGraphS(averageP, averageN, averageC):
    y1 = averageP
    y2 = averageN
    y3 = averageC
    x = []
    
    for i in range(len(averageC)):
        x.append(i+1)
        print(i)
    
    plt.clf()
    plt.plot(x, y1, label= "Positive")
    plt.plot(x, y2, label = "Negative")
    plt.plot(x, y3, label = "Total")

    plt.xlabel('Sentences')
    plt.ylabel('Average of keywords')
    plt.xticks(x)
    plt.title('Average of keywords/Total Words Per Sentence')
    plt.legend()
    #plt.show()
    plt.savefig('static/my_plot.png')
    return 'my_plot.png'

def plotGraphPerSentence(score, text):
     y = score
     x = []
    
     for token in text:
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




def plotEachSentence(ent, text):
        #findkeywords
        print("BELLO"+ent.text)
        scoring = 0
        text_doc = text.getText()
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
                        scoring =  -keywords.negativedic.get(ent.text.lower()) 
                        score.append(scoring)
                    elif ent.label_ == "Positive":
                        scoring = keywords.positivedic.get(ent.text.lower()) 
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
                                scoring =  keywords.negativedic.get(ent.text.lower()) * 0
                                score.append(0)
                                score.append(0)
                                                
                        #if is not happy inverted positive to negative
                        elif ent.text == action and ent.label_ == "Positive":
                                scoring = keywords.positivedic.get(ent.text.lower()) * -1
                                score.append(scoring)
                                score.append(scoring)

                        else:
                                
                                
                                if token.dep_ == 'neg':
                                    
                                    if ent.label_ == "Negative" :
                                            scoring =  keywords.negativedic.get(ent.text.lower()) * 0
                                            score.append(000)
                                            
                              
                                    elif ent.label_ == "Positive":
                                            scoring = keywords.positivedic.get(ent.text.lower()) * -1
                                            score.append(-111)
                                
                                for i in range(len(score)):
                                    foundindex = False
                                    if score[i] == -111 or score[i] == 000:
                                        foundindex = True
                     
                                    if foundindex :
                                         if score[i] == -111:
                                          score[i] == keywords.positivedic.get(ent.text.lower()) * -1

                                         elif score[i] == 000:
                                          score[i] =  0

        return score;                     