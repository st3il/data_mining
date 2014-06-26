import feedparser
from nltk.corpus import stopwords
import re

sw = stopwords.words('english')

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

    print allwords



getarticlewords()