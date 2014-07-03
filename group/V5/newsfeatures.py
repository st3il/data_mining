# -*- coding: utf-8 -*-
import feedparser as fp
from nltk.corpus import stopwords
import re
import pandas as pd
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

feedlist =['http://feeds.reuters.com/reuters/topNews',
    'http://feeds.reuters.com/reuters/businessNews',
    'http://feeds.reuters.com/reuters/worldNews',
    'http://feeds2.feedburner.com/time/world',
    'http://feeds2.feedburner.com/time/business',
    'http://feeds2.feedburner.com/time/politics',
    'http://rss.cnn.com/rss/edition.rss ',
    'http://rss.cnn.com/rss/editiontmpWorld.rss',
    'http://newsrss.bbc.co.uk/rss/newsonlinetmpWorld_edition/business/rss.xml',
    'http://newsrss.bbc.co.uk/rss/newsonlinetmpWorld_edition/europe/rss.xml',
    'http://www.nytimes.com/services/xml/rss/nyt/World.xml',
    'http://www.nytimes.com/services/xml/rss/nyt/Economy.xml'
    ]
feedResults = list()

sw = stopwords.words("english")

def seperatewords(text):
    splitter = re.compile("\\W*")
    return [s.lower() for s in splitter.split(text) if len(s)>4 and s not in sw]

def stripHTML(h):
    p=""
    s=0
    for c in h:
        if c=="<": s=1
        elif c==">":
            s=0
            p+=" "
        elif s==0:
            p+=c
    return p

def parseFeeds():
    for feed in feedlist:
        feedResults.append(fp.parse(feed))

def getFeedInfo():
    for feed in feedResults:
        for item in feed.entries:
            print "Titel:"
            print item.title
            print "Beschreibung:"
            print stripHTML(item.description)
            print "-"*60

def getarticlewords():
    #initialize the returning lists
    allwords = dict()
    articlewords = list()
    articletitles = list()

    # gehe durch alle Feed
    for feed in feedResults:
        # hole alle Artikel eines Feeds
        for item in feed.entries:
            # füge alle Titel der articletitles Liste hinzu
            articletitles.append(item.title)
            # HTML Text säubern
            itemString = item.title +" "+ stripHTML(item.description)
            # Worte separieren
            itemWordList = seperatewords(itemString)
            # erzeuge neues Dict für jeden Artikel
            articlewords.append(dict())
            # gehe durch alle Wörter
            for word in itemWordList:
                if word not in allwords:
                    #init "wort" mit 1
                    allwords[word] = 1
                else:
                    allwords[word] += 1
                if word not in articlewords[len(articlewords)-1]:
                    articlewords[len(articlewords)-1][word] = 1
                else:
                    articlewords[len(articlewords)-1][word] += 1

    return allwords, articlewords, articletitles

def makematrix(allw, articlew):
    wordvec = list()
    wordInArt = list()

    for word in allw:
        articleCount = 0.0
        if allw[word] < 4:
            continue
        for article in articlew:
            if word not in article:
                continue
            articleCount += 1
        if articleCount/len(articlew) < 0.6:
            wordvec.append(word)

    for article in articlew:
        articleList = list()
        wordInArt.append(articleList)

        for word in wordvec:
            if word in article:
                articleList.append(article[word])
            else:
                articleList.append(0)
    return wordvec, wordInArt

def removeZerosFromMatrix(wordInArt, articletitles):
    for i, article in enumerate(wordInArt):
        #wenn alle Einträge null sind ->(summe=0) dann schmeiße leere zeile aus Array
        if sum(article) == 0:
            wordInArt.pop(i)
            articletitles.pop(i)

    return wordInArt, articletitles

def writeIntoFile(wordvec,wordInArt):
    #write into data-file
    fout = open("data/myfile.txt", "w")
    for idx, word in enumerate(wordvec):
        if idx < (len(wordvec)-1):
            fout.write(word+", ")
        else:
            fout.write(word+"\n")

    for idx1, article in enumerate(wordInArt):
        for idx2, word in enumerate(article):
            if idx2 < (len(article)-1):
                fout.write(str(word)+", ")
            else:
                fout.write(str(word))
        if idx1 < (len(wordInArt)-1):
            fout.write("\n")

    fout.close()

parseFeeds()

# Erzeuge  Matrizen
allwords, articlewords, articletitles = getarticlewords()

# erzeuge Datenstrukturen
wordvec, wordInArt = makematrix(allwords, articlewords)
# Säubere Leere Zeilen
wordInArt, articletitles = removeZerosFromMatrix(wordInArt, articletitles)

# Kosten zwischen Matrixen
def cost(A, B):
    return np.linalg.norm(A-B)

# 2.2.4:
# Matrix: A, Features: m, Iterations: it
def nnmf(A, m, it):
    r = A.shape[0]
    c = A.shape[1]

    # erstelle ein Array aus Matrix A
    _A = np.array(A)

    if c < m:
        return None, None

    # "H" mit random Werten initialisieren
    _H = np.ones((m, c))
    for i in range(0, m-1):
        for j in range(0, c-1):
            _H[i,j] = np.random.randint(0, c)

    # "W" mit random Werten initialisieren
    _W = np.ones((r, m))
    for i in range(0, r):
        for j in range(0, m):
            _W[i,j] = np.random.randint(0, r)

    for i in range(0, it):
        _Wtrans = _W.transpose()
        _Htrans = _H.transpose()

        # berechne H neu
        _H = _H * (np.dot(_Wtrans, _A) / np.dot(np.dot(_Wtrans, _W), _H))
        # berechne W neu
        _W = _W * (np.dot(_A, _Htrans) / np.dot(np.dot(_W, _H), _Htrans))

        # Kosten berechnen
        _B = _W.dot(_H)
        _cost = cost(_A,_B)
        print "Kosten:", _cost

        # wenn Kosten kleiner 5 gebe _W und _H zurück
        if _cost < 5:
            break

    return np.matrix(_W), np.matrix(_H)


def showfeatures(W, H, titles, wordvec):
    N = 6
    M = 33
    subject = list()

    # Aufgabe 2.3.1
    print "*"*150
    print "Ausgabe der wichtigsten Worte eines Merkmals"
    print "*"*150
    for i in range(H.shape[0]):
        # erzeuge eine Liste für jedes Feature in H
        featureList = list()
        for j in range(H.shape[1]):
            # füge das Gewicht von H[i,j] und j-th zu wordvec
            featureList.append([H[i,j], wordvec[j]])
        # drehe Reihenfolge um die meist relevanten Wörter als erstes zu bekommen
        featureList.sort()
        featureList.reverse()

        # gebe die 6 meist relevanten Wörter für Feature i aus
        featuresWords = ""
        print "Die "+str(N)+" meist relevanten Wörter für "+str(i)+ ":"
        # gehe durch featureList
        for feature in featureList[0:N]:
            # füge wörter zu einem String zusammen
            featuresWords = featuresWords + " " + str(feature[1])
            # gebe das Wort und die Gewichtung aus
            print str(feature[0])+" "*(20-len(str(feature[0])))+str(feature[1])

        subject.append(featuresWords)


    print "*"*150
    print "Gebe die meist relevanten Features für jeden Artikel aus"
    print "*"*150
    # Aufgabe 2.3.2
    # gebe die 3 meist relevanten Features aus
    for i in range(W.shape[0]):
        # erzeugen eine Liste mit jeden Artikel aus W
        relevanceList = list()
        for j in range(W.shape[1]):
            # füge das Gewicht des Features zu W[i,j] hinzu
            relevanceList.append([W[i,j],subject[j]])
        # drehe Reihenfolge um die meist relevanten als erstes zu bekommen
        relevanceList.sort()
        relevanceList.reverse()


        # Ausgabe
        print "Atikel "+str(i)+": \""+titles[i]+"\""
        for x, item in enumerate(relevanceList[0:M]):
            print str(item[0]) +" "*(20-len(str(item[0]))) + str(item[1])
            x+=1
            if(x == 3):
                break

    print "*"*150
    print "Gebe die meist relevanten Artikel für jedes Feature aus"
    print "*"*150
    # gebe die 3 meist relevanten Artikel für jedes Feature aus
    for i in range(W.shape[1]):
        # erstelle eine liste mit allen Features eines Artikels
        bestArticleForFeature = list()
        for j in range(W.shape[0]):
            # füge das Gewicht zu W[j,i] hinzu
            bestArticleForFeature.append([W[j, i], titles[j]])
         # drehe Reihenfolge um die meist relevanten als erstes zu bekommen
        bestArticleForFeature.sort()
        bestArticleForFeature.reverse()

        # Ergebnis ausgeben
        print "Feature "+str(i)+": \"" + subject[i] +"\""
        for k, features in enumerate(bestArticleForFeature[0:M]):
            print str(features[0]) + " "*(20-len(str(features[0]))) + str(features[1])
            k+=1
            if(k == 8):
                break


# erstelle numpy matrix von word/article-matrix
#wordInArtMatrix = np.matrix(wordInArt)

#print "*"*150
#print "Berechne NNMF"
#print "*"*150
#W, H = nnmf(wordInArtMatrix, 40, 10)

#print "*"*150
#print "Berechne ShowFeatures"
#print "*"*150
#showfeatures(W, H, articletitles, wordvec)


