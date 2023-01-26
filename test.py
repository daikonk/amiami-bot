from bishoujoScrape import newFigs as nf
import yfinance as yf

with open('lastFig.txt', 'w') as f:
    f.write("")

newFigList = nf()

for i in newFigList:
    print(newFigList[i])