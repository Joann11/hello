
import re

import spacy
from spacy.symbols import ORTH
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
import random
import keywords

from random import randint
negativedic = keywords.negativedic
positivedic = keywords.positivedic
neutraldic =  keywords.neutraldic


def generaterandomSentTest(keywordtype):
      # Declaring names, verbs and nouns
        names=["You","I","They","He","She","Robert","Steve"]
        verbs=["was", "is", "are", "were"]
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


# #create the list of words to match