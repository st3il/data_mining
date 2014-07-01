import feedparser
from nltk.corpus import stopwords
import re
import numpy

sw = stopwords.words('english')

### FUNCTIONS START ###

def separatewords(text):
    splitter = re.compile("\\W*")
    return [s.lower() for s in splitter.split(text) if len(s) > 4 and s not in sw]

def stripHTML(h):
  p=''
  s=0
  for c in h:
    if c=='<': s=1
    elif c=='>':
      s=0
      p+=' '
    elif s==0:
      p+=c
  return p

def getarticlewords():
    feedlist =['http://feeds.reuters.com/reuters/topNews',
    'http://feeds.reuters.com/reuters/businessNews',
    'http://feeds.reuters.com/reuters/worldNews',
    'http://feeds2.feedburner.com/time/world',
    'http://feeds2.feedburner.com/time/business',
    'http://feeds2.feedburner.com/time/politics',
    'http://rss.cnn.com/rss/edition.rss ',
    'http://rss.cnn.com/rss/edition_world.rss',
    'http://newsrss.bbc.co.uk/rss/newsonline_world_edition/business/rss.xml',
    'http://newsrss.bbc.co.uk/rss/newsonline_world_edition/europe/rss.xml',
    'http://www.nytimes.com/services/xml/rss/nyt/World.xml',
    'http://www.nytimes.com/services/xml/rss/nyt/Economy.xml'
    ]
    allwords = dict()
    articlewords = list()
    articletitles = list()
    parseResult = dict()
    for url in feedlist:
        parseResult[url] = feedparser.parse(url)
    i = 0
    for url in parseResult:
        #print parseResult[res]['entries']
        #print "\n"
        #print "title: "+ parseResult[url]['feed']['title']
        #print "description: "+parseResult[url]['feed']['subtitle_detail']['value']
        #print "-------"

        #loop through all feeds
        for (index,feed) in enumerate(parseResult[url]['entries']):
            #create append dict to articlewords
            articlewords.append(dict())
            #append feed title to articletitles
            articletitles.append(feed['title'])
            #strip html code
            content = stripHTML(feed['summary'])
            #get list of words of feed
            feedString = feed['title'] + content
            words = separatewords(feedString)
            #loop through words
            for word in words:
                #if word is not already in dict add it with value 1
                if(allwords.has_key(word) == False):
                    allwords[word] = 1
                #else increment word appearance
                else:
                    allwords[word] += 1
                #if word is not already in feed in articlewords add it with value 1
                if(articlewords[i].has_key(word) == False):
                    articlewords[i][word] = 1
                #else increment word apearance
                else:
                    articlewords[i][word] += 1
            i += 1

    return allwords, articlewords, articletitles

def makematrix(allw,articlew):
    #create returning lists
    wordvec = list()
    wordInArt = list()
    #loop through all words
    for word in allw:
        appearanceCounter = 0
        #if appearance is gt 4
        if(allw[word] > 4):
            #loop through articles
            for article in articlew:
                #loop through all words in article
                for articleWord in article:
                    #check if word is equal
                    if(word == articleWord):
                        #increase word appearance counter
                        appearanceCounter += 1
            #calculate percentage of appearance
            percentage = (100.0 / len(articlew)) * appearanceCounter
            #if appearing percentage is less than 60% append word to wordvec
            if(percentage < 60.0):
                wordvec.append(word)
    #loop through all articles
    for article in articlew:
        #create articleList and append it to wordInArt
        articleList = list()
        wordInArt.append(articleList)
        #loop through all words
        for word in wordvec:
            #if word is in article add appearance otherwise add 0
            if word in article:
                articleList.append(article[word])
            else:
                articleList.append(0)
    return wordvec, wordInArt

def cost(A,B):
    return numpy.linalg.norm(A-B)

def nnmf(A,m,it):
    maxcosts = 5
    r = A.shape[0]
    c = A.shape[1]

    #a = A * v
    #A = W * H

    #f = H * v
    #a = W * f

    _A = numpy.array(A)

    if c < m:
        return None, None

    _H = numpy.ones((m, c))
    for i in range(0, m-1):
        for j in range(0, c-1):
            _H[i,j] = numpy.random.randint(0, c)
    _W = numpy.ones((r, m))
    for i in range(0, r):
        for j in range(0, m):
            _W[i,j] = numpy.random.randint(0, r)

    for i in range(0, it):
        _Wtrans = _W.transpose()
        _Htrans = _H.transpose()

        _H = _H * (numpy.dot(_Wtrans, _A) / numpy.dot(numpy.dot(_Wtrans,_W),_H))

        _W = _W * (numpy.dot(_A, _Htrans) / numpy.dot(numpy.dot(_W, _H),_Htrans))

        _B = _W.dot(_H)
        costTmp = cost(_A,_B)

        if costTmp < maxcosts:
            break
    return numpy.matrix(_W), numpy.matrix(_H)

def writeIntoFile(wordvec,wordInArt):
    #open textfile
    f = open('data/myfile','w')
    #loop through wordvec
    for (index,word) in enumerate(wordvec):
        #if word is not the last word add it without backslash
        if(index+1 != len(wordvec)):
            f.write('%s,'%word)
        else:
            f.write('%s\n'%word)
    #loop through articles
    for (index,wordArt) in enumerate(wordInArt):
        #loop through words in article
        for (index2,number) in enumerate(wordArt):
            #if number is not the last number add it without backslash
            if(index2+1 != len(wordArt)):
                f.write('%d,'%number)
            else:
                f.write('%d\n'%number)
    #close file
    f.close()

def cleanZeroWordMatrix(wordInArt, articletitles):
    for idx, article in enumerate(wordInArt):
        if sum(article) == 0:
            wordInArt.pop(idx)
            articletitles.pop(idx)
    return wordInArt, articletitles

def showfeatures(w,h,titles,wordvec):
    return

### FUNCTIONS END ###


allwords, articlewords, articletitles = getarticlewords()

wordvec, wordInArt = makematrix(allwords,articlewords)

#writeIntoFile(wordvec,wordInArt)

wordInArt, articletitles = cleanZeroWordMatrix(wordInArt, articletitles)

wordInArtMatrix = numpy.matrix(wordInArt)

W,H = nnmf(wordInArtMatrix, 40, 10)

#showfeatures(W,H,articletitles,wordvec)

print W