
import re
import spacy
from spacy.symbols import ORTH
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
#from spacy import displacy

#nlp = spacy.load('en_core_web_sm', disable=['ner']) 

#matcher = PhraseMatcher(nlp.vocab)


# pattern = re.compile(r'"(.*?)"\s+=\s+"(.*?)"')
# ruler = nlp.add_pipe("entity_ruler", config={"phrase_matcher_attr": "LOWER"})

#create the list of words to match
negativedic = {}
positivedic = {}
neutraldic = {}

def addnewKeyWordNegative_function(negdicfile):

        with open(negdicfile, 'r') as f:
            for line in f:
              
                        (key, val) = line.split() 
                        if(negativedic.get(key) is None):
                         negativedic[key] = int(val)
            
            
            # for p in negativedic:
            #     ruler.add_patterns([{"label": "Negative", "pattern": p}])

       
            return negativedic

def addnewKeyWordNeu_function(neudicfile):
          with open(neudicfile, 'r') as f:
              for line in f:
                            
                            (key, val) = line.split()
                            if(neutraldic.get(key) is None):

                                 neutraldic[key] = int(val)
            #   for p in neutraldic:
            #          ruler.add_patterns([{"label": "Neutral", "pattern": p}])

 #   print (neutraldic)
          return neutraldic

def addnewKeyWordPositive_function(posdicfile):
        with open(posdicfile, 'r') as f:
            for line in f:
                        (key, val) = line.split()
                        if(positivedic.get(key) is None):

                            positivedic[key] = int(val)
                        
            # for p in positivedic:
            #   ruler.add_patterns([{"label": "Positive", "pattern": p}])

        
     #   print(positivedic)
        return positivedic


