import pylast
import recommendations as reco
import recommtest1 as recom
import recommendationsTemplate as recoTpl

network = pylast.get_lastfm_network()

band = network.get_artist("Rihanna")

topfans = band.get_top_fans(10)
group = [a.item for a in topfans]

userDict = reco.createLastfmUserDict(group)

#matches_userDict = reco.topMatches(userDict,'weallwantlove',reco.sim_euclid)

recommendations_userDict = recom.getRecommendations(userDict, 'weallwantlove', recoTpl.sim_euclid)

print recommendations_userDict
