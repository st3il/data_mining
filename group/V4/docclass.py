import string

class Classifier:
    # Dictionairy for words
    fc = dict()
    # Dictionairy for category
    cc = dict()
    # Function
    getfeatures = 0

    # minimal length
    minWordlength = 2

    # maximal length
    maxWordLength = 20

    def __init__(self,fn):
        #init cc with both categories
        self.cc = dict()
        self.getfeatures = fn

    #increments word counter
    def incf(self,f,cat):
        #check f word is already in fc
        if(self.fc.has_key(f)!=True):
            self.fc[f] = dict()

        if self.fc[f].has_key(cat) != True:
            self.fc[f][cat] = 0

        self.fc[f][cat] += 1

    #increments category counter
    def incc(self,cat):
        if(self.cc.has_key(cat) != True):
            self.cc[cat] = 0
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
        return sum(self.cc.values())

    #train given sentence for given category
    def train(self,item,cat):
        #get words of sentence
        words = self.getfeatures(item,self.minWordlength,self.maxWordLength)
        for word in words:
            #add each word to cf
            #print "Word: '%s'" % word
            #print "added to: '%s'" % cat
            self.incf(word,cat)
        #increment category counter
        self.incc(cat)

    #return probability of given word in given category
    def fprob(self,f,cat):
        fprobresult = 0.0
        fcount = float(self.fcount(f,cat))
        catcount = float(self.catcount(cat))

        if(self.catcount(cat) != 0):
            fprobresult = fcount/catcount
            return fprobresult
        else:
            return 0

    #add smoothing to avoid extreme probabilities
    def weightedprob(self,f,cat):

        initprob = 1.0/len(self.cc)
        if(self.fc.has_key(f)):
            count = sum(self.fc[f].values())
        else:
            count = 0.0

        fprob = float(self.fprob(f,cat))
        result = float((initprob + count * fprob)/(1 + count))

        #print("Prob of Word '%s' in %s : %s" %(f, cat, result))

        return result

    #return probability of given category
    def catprob(self,cat):
        catprobresult = 0.0
        amountCat = float(self.catcount(cat))
        totalCount = float(self.totalcount())
        catprobresult = (amountCat / totalCount)
        return catprobresult


    #returns probability if given document is in given category
    def prob(self,item,cat):
        probresult = 0.0
        words = self.getfeatures(item, self.minWordlength, self.maxWordLength)
        tmp = 1.0

        for word in words:
            tmp *= self.weightedprob(word,cat)

        #print("Prob of '%s' in %s : %s" %(item, cat, tmp * self.catprob(cat)))

        catprob = self.catprob(cat)
        probresult = tmp * catprob

        return probresult



def getwords(doc, minLength, maxLength):
    back = dict()
    tmp = string.split(string.lower(doc))
    for word in tmp:
        if(len(word) >= minLength and len(word) <= maxLength):
            back[word] = 1
    return back


#doc1 = "This is a String with lower and UPPER case Letters, for testing our new Algorithm. Maybe english is better than german, who knows. thatsaprettylongwordtotestifitgetsremovedinmyfuntion"



def showProb(string ):
    #get probability of string is in good category
    g = classifier.prob(string, "good")

    #get probability of string is in bad category
    b = classifier.prob(string, "bad")

    #calculate probabilities
    probGood = g/(g+b)
    probBad = b/(g+b)

    print("Probability of Good:")
    print(probGood)

    print("Probability of Bad")
    print(probBad)
    print "Result: " + max({"Good": probGood, "Bad": probBad})



if __name__ == "__main__":

    doc1 = "This is a String with lower and UPPER case Letters, for testing our new Algorithm. Maybe english is better than german, who knows. thatsaprettylongwordtotestifitgetsremovedinmyfuntion"

    classifier = Classifier(getwords)

    corpus = [["nobody owns the water", "good"],
          ["the quick rabbit jumps fences", "good"],
          ["buy pharmaceuticals now","bad"],
          ["make quick money at the online casino","bad"],
          ["the quick brown fox jumps","good"] ,
          ["next meeting is at night","good"],
          ["meeting with your superstar","bad"] ,
          ["money like water","bad"]]

    for sentence in corpus:
        classifier.train(sentence[0], sentence[1])

    showProb("the money jumps")




