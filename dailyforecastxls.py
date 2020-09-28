# cmd: auto-py-to-exe
# Console based, One file
# 1 Day of Daily Weather Forecasts, printed into an xlsx file
# Resource URL: http://dataservice.accuweather.com/forecasts/v1/daily/1day/{locationsapi}?apikey={apikey}

import sys
import os
import time
import requests
import xlsxwriter

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


strurl = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/{}?apikey={}&language=ro&details=false&metric=true"
path = r"\\ST1\NewsRoom\GraphicModels\Mozaik\Kellekek\{}.png "

n = 0  # number of apikeys
nused = 0  # number of apikeys used already twice
code = []  # array of apikeys
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

if nused != n:  # if the last was already used twice
    apikey = code[nused]
else:
    apikey = code[0]

# Apikey-file update
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


# xlsx
file = xlsxwriter.Workbook("idojaras.xlsx")
worksheet = file.add_worksheet()
row = 0
column = 0
worksheet.set_column(0, 0, 20)
worksheet.set_column(3, 3, 60)

for citynr in range(len(city)):
    response = requests.get(strurl.format(city[citynr][1], apikey))
    if response.status_code == 200:
        r = response.json()
        maxtemp = round(r["DailyForecasts"][0]["Temperature"]["Maximum"]["Value"])
        mintemp = round(r["DailyForecasts"][0]["Temperature"]["Minimum"]["Value"])
        icon = r["DailyForecasts"][0]["Day"]["Icon"]
        worksheet.write(row, column, city[citynr][0])
        worksheet.write(row, column + 1, maxtemp)
        worksheet.write(row, column + 2, mintemp)
        newpath = path.format(icon)
        worksheet.write(row, column + 3, newpath)
        row += 1

    else:
        print("Response Error")

close = input(">>> Kilépéshez Enter <<<")
file.close()
# ©Magyari Zsuzsanna, 2019
