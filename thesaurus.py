# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 14:34:54 2017

@author: Sacha Perry-Fagant
"""

from bs4 import BeautifulSoup as soup
import urllib2, re
import unicodedata as u

#This program takes all the main synonyms from thesaurus.com to use for something else!
#Hasn't been tested much yet

#Returns empty list for nonsense words!
def stealWords(word):
    #word=str(word) If we want to include numbers, uncomment
    if(not isinstance(word, basestring)):
        return []
    word = word.lower()
    search = "http://www.thesaurus.com/browse/"
    search = search + word + "?s=t"
    try:
        link = urllib2.urlopen(search).read()
        s = soup(link)
        return parseWords(s.getText(),word)
    except urllib2.HTTPError:
        return []

def parseWords(text,word):
    text=text.split("\n")
    words=[]
    for e in text:
        text[text.index(e)]=re.sub( '\s+', ' ', e ).strip()
    idx=0
    sText="Synonyms for " + word
    while(text[idx]!=sText):
        idx=idx+1
    while(not ("star" in text[idx])):
        idx=idx+1
    sText="Antonyms for "+word #Either this will show up
    sText2="See more synonyms for" #Or this will show up after all the main words
    while(text[idx]!=sText and not(sText2 in text[idx])):
        w=text[idx]
        if "star" in w:
            #All the main words end with star. That's what the -4 is for
            words.append(u.normalize('NFKD', w[:len(w)-4]).encode('ascii','ignore'))
        idx=idx+1
    return words
    
def errorTest():
    print stealWords("thisisntaword")

def test():
    print stealWords("neRvOus")