# cmd: auto-py-to-exe
# Console based, One file
# 4 Days of Daily Forecast, each day printed in different output file
# Resource URL:
# "http://dataservice.accuweather.com/forecasts/v1/daily/5day/{locationsapi}?apikey={
# apikey}&language=ro&details=false&metric=true"

import sys
import os
import time
import requests

#file decriptors
global firstday
global secondday
global thirdday
global fourthday
global apikey

# Locations API
# Arad,Beszterce, Brassó, Budapest, Bukarest, Csíkszereda, Déva, Gyergyószentmiklós, Kézdivásárhely, Kolozsvár,
# Marosvásárhely, Nagybánya Nagybánya, Nagyszeben, Nagyvárad, Sepsiszentgyörgy, Szatmárnémeti, Székelyudvarhely,
# Temesvár
# city["City name", Locations API]
city = [["Arad", 286942], ["Beszterce", 272286], ["Brassó", 287345], ["Budapest", 187423], ["Bukarest", 287430],
        ["Csíkszereda", 273485], ["Déva", 273576], ["Gyergyószentmiklós", 273486], ["Kézdivásárhely", 272906],
        ["Kolozsvár", 287713], ["Marosvásárhely", 289415], ["Nagybánya", 274475], ["Nagyszeben", 290499],
        ["Nagyvárad", 287292], ["Sepsiszentgyörgy", 272904], ["Szatmárnémeti", 275551],
        ["Székelyudvarhely", 273487], ["Temesvár", 290867]]

datestr = "{}. {}. {}."
datumstr = "datum=[\"{}. {}. {}.\"]\n"
strurl = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/{}?apikey={}&language=ro&details=false&metric=true"

n = 0  # number of apikeys
nused = 0  # number of apikeys used already twice
code = [] #array of apikeys
number = []
if os.path.exists("api.txt"):
    f = open("api.txt", "r")
    for line in f:
        code.append(line[0:32])
        number.append(int(line[33:34]))
        n += 1
        if number[n - 1] == 2:
            nused += 1
    f.close()
else:
    print("Nincs az aktuális katalógusban api.txt\n")
    time.sleep(5)
    sys.exit()


if nused != n: #if the last was already used twice
    apikey = code[nused]
else:
    apikey = code[0]

#Apikey-file update
os.remove('api.txt')
g = open("api.txt", 'w')
for i in range(0, n):
    line = code[i] + ' '
    if i == nused:
        number[i] += 1

    if nused == 16:
        if i == 0:
            line = line + "1"
        else:
            line = line + "0"
    else:
        line = line + str(number[i])

    g.write(line)
    g.write('\n')

g.close()


response = requests.get(strurl.format(city[0][1], apikey))
if response.status_code == 200: #if there's no response error
    r = response.json()

    # DAY 1
    date = r["DailyForecasts"][1]["Date"]  #Starting from 1, not 0, because today's forecast needs to be skipped over
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    firstline = datumstr.format(year, month, day)

    if os.path.exists("idojaras1.txt"):
        os.remove("idojaras1.txt")
    else:
        f = open("idojaras1.txt", "x")
        f.close()

    firstday = open('idojaras1.txt', "w")
    firstday.write(firstline)

    # DAY 2
    date = r["DailyForecasts"][2]["Date"]
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    firstline = datumstr.format(year, month, day)

    if os.path.exists("idojaras2.txt"):
        os.remove("idojaras2.txt")
    else:
        f = open("idojaras2.txt", "x")
        f.close()

    secondday = open("idojaras2.txt", "w")
    secondday.write(firstline)

    # DAY 3
    date = r["DailyForecasts"][3]["Date"]
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    firstline = datumstr.format(year, month, day)

    if os.path.exists("idojaras3.txt"):
        os.remove("idojaras3.txt")
    else:
        f = open("idojaras3.txt", "x")
        f.close()

    thirdday = open("idojaras3.txt", "w")
    thirdday.write(firstline)

    # DAY 4
    date = r["DailyForecasts"][4]["Date"]
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    firstline = datumstr.format(year, month, day)

    if os.path.exists("idojaras4.txt"):
        os.remove("idojaras4.txt")
    else:
        f = open("idojaras4.txt", "x")
        f.close()

    fourthday = open("idojaras4.txt", "w")
    fourthday.write(firstline)

    maxtemp = round(r["DailyForecasts"][1]["Temperature"]["Maximum"]["Value"])
    mintemp = round(r["DailyForecasts"][1]["Temperature"]["Minimum"]["Value"])
    icon = r["DailyForecasts"][1]["Day"]["Icon"]
    firstday.write("varos{}=[\"{}\",\"{}°\",\"/{}°\",\"{}\"]\n".format(1, city[0][0], maxtemp, mintemp, icon))
    maxtemp = round(r["DailyForecasts"][2]["Temperature"]["Maximum"]["Value"])
    mintemp = round(r["DailyForecasts"][2]["Temperature"]["Minimum"]["Value"])
    icon = r["DailyForecasts"][2]["Day"]["Icon"]
    secondday.write("varos{}=[\"{}\",\"{}°\",\"/{}°\",\"{}\"]\n".format(1, city[0][0], maxtemp, mintemp, icon))
    maxtemp = round(r["DailyForecasts"][3]["Temperature"]["Maximum"]["Value"])
    mintemp = round(r["DailyForecasts"][3]["Temperature"]["Minimum"]["Value"])
    icon = r["DailyForecasts"][3]["Day"]["Icon"]
    thirdday.write("varos{}=[\"{}\",\"{}°\",\"/{}°\",\"{}\"]\n".format(1, city[0][0], maxtemp, mintemp, icon))
    maxtemp = round(r["DailyForecasts"][4]["Temperature"]["Maximum"]["Value"])
    mintemp = round(r["DailyForecasts"][4]["Temperature"]["Minimum"]["Value"])
    icon = r["DailyForecasts"][4]["Day"]["Icon"]
    fourthday.write("varos{}=[\"{}\",\"{}°\",\"/{}°\",\"{}\"]\n".format(1, city[0][0], maxtemp, mintemp, icon))

else:
    print("Response Error")

for citynr in range(1, len(city)):
    response = requests.get(strurl.format(city[citynr][1], apikey))
    if response.status_code == 200: #if there's no response error
        r = response.json()
        maxtemp = round(r["DailyForecasts"][1]["Temperature"]["Maximum"]["Value"])
        mintemp = round(r["DailyForecasts"][1]["Temperature"]["Minimum"]["Value"])
        icon = r["DailyForecasts"][1]["Day"]["Icon"]
        firstday.write(
            "varos{}=[\"{}\",\"{}°\",\"/{}°\",\"{}\"]\n".format(citynr, city[citynr][0], maxtemp, mintemp, icon))
        maxtemp = round(r["DailyForecasts"][2]["Temperature"]["Maximum"]["Value"])
        mintemp = round(r["DailyForecasts"][2]["Temperature"]["Minimum"]["Value"])
        icon = r["DailyForecasts"][2]["Day"]["Icon"]
        secondday.write(
            "varos{}=[\"{}\",\"{}°\",\"/{}°\",\"{}\"]\n".format(citynr, city[citynr][0], maxtemp, mintemp, icon))
        maxtemp = round(r["DailyForecasts"][3]["Temperature"]["Maximum"]["Value"])
        mintemp = round(r["DailyForecasts"][3]["Temperature"]["Minimum"]["Value"])
        icon = r["DailyForecasts"][3]["Day"]["Icon"]
        thirdday.write(
            "varos{}=[\"{}\",\"{}°\",\"/{}°\",\"17\"]\n".format(citynr, city[citynr][0], maxtemp, mintemp, icon))
        maxtemp = round(r["DailyForecasts"][4]["Temperature"]["Maximum"]["Value"])
        mintemp = round(r["DailyForecasts"][4]["Temperature"]["Minimum"]["Value"])
        icon = r["DailyForecasts"][4]["Day"]["Icon"]
        fourthday.write(
            "varos{}=[\"{}\",\"{}°\",\"/{}°\",\"{}\"]\n".format(citynr, city[citynr][0], maxtemp, mintemp, icon))
    else:
        print("Response Error")

firstday.close()
secondday.close()
thirdday.close()
fourthday.close()

close = input(">>> Kilépéshez Enter <<<")
# ©Magyari Zsuzsanna, 2019
