import recommendationsTemplate as reco


# Aufgabe 2.2
def topMatches(pref, person, similarity):
    #todo return List with similar person
    #print "def topMatches"

    #sim_euclid(prefs,person1,person2,normed=False):
    person2 = "Gene Seymour"


    dictPerson = {}

    for i in pref:

        if person != i:
            #unterscheide Euklid Methode oder Pearson
            if(similarity == reco.sim_euclid):
                #Euklid Methode, normed = true
                similarityList = similarity(pref, person, i, True)
            else:
                #Pearson Methode
                similarityList = similarity(pref, person, i)


            #print("Similarity between %s and %s" % (person, i))
            #print(similarityList)
            #print("_________________________________________________________")

            dictPerson[i] = similarityList

    #print("Unsorted Dict:")
    #print(dictPerson)

    #print("_________________________________________________________")
    #print("Sorted Dict:")
    #sort Lisr
    dictPerson = sorted(dictPerson.items(), key=lambda x: x[1], reverse=True)
    #print(dictPerson)

    return  dictPerson


print("Euklid")
topMatches(reco.critics, "Toby", reco.sim_euclid)
print("Pearson")
topMatches(reco.critics, "Toby", reco.sim_pearson)




#Aufgabe 2.3.1
def getRecommendations(pref, person, similarity):
    #todo berechne Empfehlungswerte fuer Person

    #beziehe die aehnlichen Personen todo alle korrelationswerte holen
    topList = topMatches(reco.critics, person, reco.sim_pearson)
    print(topList)

    #todo hole alle Filme, die bewertet werden sollen



    #todo berechne fuer jeden Film den Empfehlungswert pro aenhlicher Person

    #todo berechne Summe fuer jeden Film

    #todo berechne Mittelwert fuer jeden Film

    #todo berechne Mittelwert durch Summe --> das ist der jeweilige Empfehlungswert




    #todo



    return 0;



getRecommendations(reco.critics, "Toby", reco.sim_pearson)