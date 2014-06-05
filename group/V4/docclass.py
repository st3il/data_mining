import string

def getwords(doc, minLength, maxLength):
    back = dict()
    tmp = string.split(string.lower(doc))
    for word in tmp:
        if(len(word) > minLength and len(word) < maxLength):
            back[word] = 1
    return back










doc1 = "This is a String with lover and UPPER case Letters, for testing our new Algorithm. Maybe english is better than german, who knows. thatsaprettylongwordtotestifitgetsremovedinmyfuntion"

res = getwords(doc1,3,20)
print res