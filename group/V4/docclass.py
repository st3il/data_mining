import string

class Classifier:
    fc = dict()
    cc = dict()
    getfeatures = 0
    def __init__(self,fn):
        #init cc with both categories
        self.cc['good'] = 0
        self.cc['bad'] = 0
        self.getfeatures = fn

    def incf(self,f,cat):
        #check f word is already in fc

        if(self.fc.has_key(f)!=True):
            self.fc[f] = {"good":0, "bad":0}

        self.fc[f][cat] = self.fc[f][cat] + 1

    #increments category counter
    def incc(self,cat):
        if(self.cc.has_key(cat)):
            self.cc[cat] = self.cc[cat] + 1

    #returns amount of given word in given category
    def fcount(self,f,cat):
        if(self.fc.has_key(f)):
            if(self.fc[f].has_key(cat)):
                return self.fc[f][cat]
            else:
                return 0
        else:
            return 0

    #returns counter of given category
    def catcount(self,cat):
        return self.cc[cat]

    #returns counters of both categories
    def totalcount(self):
        return self.cc['good'] + self.cc['bad']

    #train given sentence for given category
    def train(self,item,cat):
        #get words of sentence
        words = self.getfeatures(item,3,20)
        for word in words:
            #add each word to cf
            self.incf(word,cat)
        #increment category counter
        self.incc(cat)

    #return probability of given word in given category
    def fprob(self,f,cat):
        if(self.catcount(cat) != 0):
            return float(self.fcount(f,cat)) / float(self.catcount(cat))
        else:
            return 0

    #add smoothing to avoid extreme probabilities
    def weightedprob(self,f,cat):

        initprob = float(0.5)
        fcount = float(self.fcount(f,cat))
        fprob = float(self.fprob(f,cat))
        print(fcount)
        print(fprob)
        result = float(initprob + fcount * fprob/(1 + fcount))

        print("Prob of Word '%s' in %s : %s" %(f, cat, result))

        return result

    #return probability of given category
    def catprob(self,cat):
        amountCat = float(self.catcount(cat))
        totalCount = float(self.totalcount())

        return (amountCat / totalCount)


    #returns probability if given document is in given category
    def prob(self,item,cat):
        words = self.getfeatures(item, 3, 10)
        tmp = 0
        for word in words:
            if(tmp == 0):
               # print "temp init"
                tmp = self.weightedprob(word,cat)
               # print tmp

            else:
                tmp = tmp * self.weightedprob(word,cat)
               # print tmp
        print("Prob of '%s' in %s : %s" %(item, cat, tmp * self.catprob(cat)))
        return tmp * self.catprob(cat)



def getwords(doc, minLength, maxLength):
    back = dict()
    tmp = string.split(string.lower(doc))
    for word in tmp:
        if(len(word) > minLength and len(word) < maxLength):
            back[word] = 1
    return back


doc1 = "This is a String with lower and UPPER case Letters, for testing our new Algorithm. Maybe english is better than german, who knows. thatsaprettylongwordtotestifitgetsremovedinmyfuntion"

#res = getwords(doc1,3,20)
#print res

classifier = Classifier(getwords)

corpus = [["nobody owns the water", "good"], ["the quick rabbit jumps fences", "good"], ["buy pharmaceuticals now","bad"], ["make quick money at the online casino","bad"], ["the quick brown fox jumps","good"] , ["next meeting is at night","good"], ["meeting with your superstar","good"] , ["money like water","bad"]]

for sentence in corpus:
    classifier.train(sentence[0], sentence[1])


#print classifier.fc
#print classifier.cc


def showProb(string ):
    g = classifier.prob(string, "good")
    b = classifier.prob(string, "bad")

    probGood = g/(g+b)
    probBad = b/(g+b)

    print("good")
    print(probGood)
    print("bad")
    print(probBad)

print classifier.fc
showProb(" money ")




