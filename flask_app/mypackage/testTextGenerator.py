
import re

import spacy
from spacy.symbols import ORTH
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
import random

from random import randint


def generaterandomSentTest(dictionaryFile):
      # Declaring names, verbs and nouns
        names=["You","I","They","He","She","Robert","Steve"]
        verbs=["was", "is", "are", "were"]
        nouns=["playing cricket.", "watching television.", "singing.", "fighting.", "cycling."]
        negsent = dictionaryFile
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