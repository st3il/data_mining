import feedparser
import docclass as doc
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

# create own classifier
myClassifier = doc.Classifier(doc.getwords)

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


trainTech=['http://rss.chip.de/c/573/f/7439/index.rss',
           'http://feeds.feedburner.com/netzwelt',
           'http://rss1.t-online.de/c/11/53/06/84/11530684.xml',
           'http://www.computerbild.de/rssfeed_2261.xml?node=13',
           'http://www.heise.de/newsticker/heise-top-atom.xml']

trainNonTech=['http://newsfeed.zeit.de/index',
              'http://newsfeed.zeit.de/wirtschaft/index',
              'http://www.welt.de/politik/?service=Rss',
              'http://www.spiegel.de/schlagzeilen/tops/index.rss',
              'http://www.sueddeutsche.de/app/service/rss/alles/rss.xml'
              ]
test=["http://rss.golem.de/rss.php?r=sw&feed=RSS0.91",
          'http://newsfeed.zeit.de/politik/index',
          'http://www.welt.de/?service=Rss'
           ]

freedcounter={}
freedcounter['tech']=0
freedcounter['nontech']=0
freedcounter['test']=0

print "--------------------Training Tech------------------------"
for feed in trainTech:
    f=feedparser.parse(feed)
    for e in f.entries:
      newsString = stripHTML(e.title+' '+e.description)
      myClassifier.train(newsString, "Tech")
      freedcounter['tech']+=1
print "--------------------Training NonTech------------------------"
for feed in trainNonTech:
    f=feedparser.parse(feed)
    for e in f.entries:
      newsString = stripHTML(e.title+' '+e.description)
      myClassifier.train(newsString, "NonTech")
      freedcounter['nontech']+=1
print "--------------------Testing------------------------"
#loop through test feeds
for feed in test:
    #get feeds
    f=feedparser.parse(feed)
    #get text of every feed
    for e in f.entries:
        print "________________________________"
        #remove html entities
        newsString = stripHTML(e.title+' '+e.description)
        #get probabilities of tech and nontech
        tech = myClassifier.prob(newsString, 'Tech')
        nontech = myClassifier.prob(newsString, 'NonTech')
        
        #calculate probabilities
        resultTech = tech / (tech+nontech)
        resultNonTech = nontech / (tech+nontech)

        # print result
        print newsString
        print "Results for (Tech:%.3f / NonTech: %0.3f)" % (resultTech, resultNonTech)

        #increase test counter
        freedcounter['test']+=1
print "\n----------------------------------------------------------------"

print 'Number of used trainingsamples in categorie tech',freedcounter['tech']
print 'Number of used trainingsamples in categorie notech',freedcounter['nontech']


print 'Number of used test samples',freedcounter['test']

