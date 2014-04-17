fin = open("beispiel.txt", "r")

dateiinhalt = fin.read()

print "Typ: ", type(dateiinhalt)
print "Inhalt: \n", dateiinhalt

fin.close()

fout = open("bspwrite.txt", "w")
fout.write("der Cock oder")
fout.write(" das Cock")
fout.close()
