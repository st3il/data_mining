import recommendationsTemplate as reco


# Aufgabe 2.2
def topMatches(pref, person, similarity):
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
    print(dictPerson)
    tmp = dict()
    for person in dictPerson:
        tmp[person[0]] = person[1]
    dictPerson = tmp

    return dictPerson


#print("Euklid")
print topMatches(reco.critics, "Toby", reco.sim_euclid)
#print("Pearson")
#print topMatches(reco.critics, "Toby", reco.sim_pearson)




#Aufgabe 2.3.1
def getRecommendations(pref, person, similarity):
    #berechne Empfehlungswerte fuer Person

    #beziehe die aehnlichen Personen, alle korrelationswerte holen
    topList = topMatches(pref, person, similarity)
    #remove movies rated with -1.0
    tmp = dict()
    for k,v in enumerate(topList):
        if(topList[v] >= 0):
            tmp[v] = topList[v]
    topList = tmp
    #print topList

    #hole alle Filme, die bewertet werden sollen
    movieList = []
    for name in pref:
        #print pref[name]
        for (i, movie) in enumerate(pref[name]):
           movieList.append(movie)

    movieList = list(set(movieList))

    #berechne fuer jeden Film den Empfehlungswert pro aenhlicher Person
    recommendationList = {}


    for j in movieList:
        #print("___________________Movie: %s_________________" %j)
        recommendationSumSingleMovie = 0
        ksum = 0

        for k,v in enumerate(topList):
            if(pref[v].has_key(j)):
                #print("Recommendation of %s : " %k[0])
                #print(pref[k[0]][j])
                recommendationSumSingleMovie = recommendationSumSingleMovie + pref[v][j] * topList[v]
                ksum = ksum + topList[v]

        #print("Summe:")
        #print(recommendationSumSingleMovie)
        #print("KSumme:")
        #print(ksum)
        #print("Empfehlung:")
        #print(recommendationSumSingleMovie/ksum)
        recommendationList[j] = recommendationSumSingleMovie/ksum
    #Sortiere list:
    recommendationList = sorted(recommendationList.items(), key=lambda x: x[1], reverse=True)

    #reverse inside tupel
    for (z,i) in enumerate(recommendationList):
        recommendationList[z] = recommendationList[z][::-1]

   # print("Recommendation List for %s: " %person)
    #print(recommendationList)
    return recommendationList



#getRecommendations(reco.critics, "Toby", reco.sim_pearson)


#Aufgabe 2.4

#transformiere
def transformCritics(critics):

    newCritics  ={}
    movieList = []

    for name in critics:
        #print pref[name]
        for (i, movie) in enumerate(critics[name]):
           movieList.append(movie)
    movieList = list(set(movieList))

    for z in movieList:
        personDict = {}
        for name in critics:
            if(critics[name].has_key(z)):
                personDict[name] = critics[name][z]


        newCritics[z] = personDict
    #print("New Critics")
    #print(newCritics)
    return newCritics


transCritics = transformCritics(reco.critics)
#print topMatches(transCritics, "Lady in the Water", reco.sim_pearson)


def calculateSimilarItems(critics, similarity):
    #berechne eine Dictionary, welches die Aehnlichkeit zw allen Filmen darstellt
    # Vorraussetzung: Keys sind Filme, keine Personen

    similarityItems = {}


    for i in critics:
        similarityItems[i] = topMatches(critics, i,  similarity)


    #print(similarityItems)
    return similarityItems;

#calculateSimilarItems(transCritics, reco.sim_euclid)



def getRecommendedItems(critics, person, similarity):
    #berechne empfehlungswerte fuer die noch nicht gekauften Filme

    recommendedItems = {}


    #transformiere critics
    transCritics = transformCritics(reco.critics)

    #von Person bewertete Filme
    personalMovies = {x for x in critics[person]}

    #alle Filme
    allMovies = {y for y in transCritics}

    #noch nicht von Person bewertet
    unboughtItems = allMovies.difference(personalMovies)

    similarItems = calculateSimilarItems(transCritics, similarity)

    for k in unboughtItems:
         sumfactor = 0
         sum = 0

         for l in personalMovies:
             #Pearson falls Wert <0
             if similarItems[k][l]>0:
                 sum = sum + similarItems[k][l]
                 sumfactor = sumfactor + (critics[person][l] * similarItems[k][l])
         if(sum != 0):
            normalized = sumfactor/sum
         else:
            normalized = 0
         recommendedItems[k] = normalized

    return recommendedItems;

#recomItem = getRecommendedItems(reco.critics, "Toby", reco.sim_euclid)
#print recomItem
#transCritics = transformCritics(reco.critics)
#print topMatches(transCritics, "Lady in the Water", reco.sim_euclid)