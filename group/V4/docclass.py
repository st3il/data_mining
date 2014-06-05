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
        if(self.fc.has_key(f)):
            #check if word already has category cat
            if(self.fc[f].has_key(cat)):
                #increment counter
                self.fc[f][cat] = self.fc[f][cat] + 1
            else:
                #category doesn't exist, add it with value 1
                self.fc[f][cat] = 1
        else:
            #word and category don't exist, add both with value 1
            self.fc[f][cat] = 1

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
        words = self.getfeatures(item)
        for word in words:
            #add each word to cf
            self.incf(word,cat)
        #increment category counter
        self.incc(cat)

    #return probability of given word in given category
    def fprob(self,f,cat):
        if(self.catcount(cat) != 0):
            return self.fcount(f,cat) / self.catcount(cat)
        else:
            return 0

    #add smoothing to avoid extreme probabilities
    def weightedprob(self,f,cat):
        initprob = 0.5
        return (initprob + self.fcount(f,cat) * self.fprob(f,cat))/1 + self.fcount(f,cat)

    #returns probability if given document is in given category
    def prob(self,item,cat):
        words = self.getfeatures(item)
        tmp = 0
        for word in words:
            if(tmp == 0):
                tmp = self.weightedprob(word,cat)
            else:
                tmp = tmp * self.weightedprob(word,cat)
        return 0



def getwords(doc, minLength, maxLength):
    back = dict()
    tmp = string.split(string.lower(doc))
    for word in tmp:
        if(len(word) > minLength and len(word) < maxLength):
            back[word] = 1
    return back


doc1 = "This is a String with lower and UPPER case Letters, for testing our new Algorithm. Maybe english is better than german, who knows. thatsaprettylongwordtotestifitgetsremovedinmyfuntion"

res = getwords(doc1,3,20)
print res

classifier = Classifier(getwords)