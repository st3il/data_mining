from math import sqrt

def createLastfmUserDict(group):
    userDict = dict()
    AllBands = set()

    #loop through all users
    for user in group:
        #create new dict with username as key
        userDict[user.get_name()] = dict()
        #select top artists of given user
        topartists = user.get_top_artists()[0:20]
        #loop through artists and add them to the userdict with value 1, additionally add band to AllBands set
        for artist in topartists:
            userDict[user.get_name()][artist.item.get_name()] = 1
            AllBands.add(artist.item.get_name())
    #loop again through all users
    for user in group:
        #loop through all bands
        for artist in AllBands:
            #if given artist is not already in users dict, add it with value 0
            if artist not in userDict[user.get_name()]:
                userDict[user.get_name()][artist] = 0
    #return new created dict
    return userDict