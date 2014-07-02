# -*- coding: utf-8 -*-
import feedparser as fp
import newsfeatures as nf
from newsfeatures import *
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")


nf.parseFeeds()

print "#"*50,"\n"

print "Aufgabe 2.2.1"
print "Erzeuge Matrix"
allwords, articlewords, articletitles = getarticlewords()

print "#"*50,"\n"

print "Aufgabe 2.2.2"
print "Erzeuge Word-/Article-Matrix und Wordvector"
wordvec, wordInArt = makematrix(allwords, articlewords)

print "#"*50,"\n"

print "Aufgabe 2.2.3"
print "Matrizen säubern"
wordInArt, articletitles = cleanMatrix(wordInArt, articletitles)

print "#"*50,"\n"

print "Aufgabe 2.2.4"
wordInArtMatrix = np.matrix(wordInArt)
print "NNMF"
W, H = nnmf(wordInArtMatrix, 40, 10)

print "#"*50,"\n"

print "Aufgabe 2.3"
showfeatures(W, H, articletitles, wordvec)