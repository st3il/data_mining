import pylast
import recommendations as reco
import recommtest1 as recom
import recommendationsTemplate as recoTpl

network = pylast.get_lastfm_network()

#select artist
band = network.get_artist("Rihanna")

#get top fans of selected artist
topfans = band.get_top_fans(10)

#filter user objects
group = [a.item for a in topfans]

#creat user dict
userDict = reco.createLastfmUserDict(group)

#get top matches for given user
#matches_userDict = reco.topMatches(userDict,'weallwantlove',reco.sim_euclid)

#get recommendations for given user
recommendations_userDict = recom.getRecommendations(userDict, 'weallwantlove', recoTpl.sim_euclid)

print recommendations_userDict
