from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
import datetime
import os

def newFigs():

    JPYConversion = 0.0077

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, service_log_path=os.devnull)
    driver.get('https://www.amiami.com/eng/c/bishoujo/')
    driver.implicitly_wait(10)

    price = driver.find_elements(By.CLASS_NAME, 'newly-added-items__item__price')
    brand = driver.find_elements(By.CLASS_NAME, 'newly-added-items__item__brand')
    imageContainers = driver.find_elements(By.CLASS_NAME, 'newly-added-items__item__image_item')
    time = datetime.datetime.now()
    loopCompleted = False

    figureDict = {}

    with open('lastFig.txt', 'r') as f:
        lastElementParsed = f.read()


    recentFigName = imageContainers[0].find_element(By.TAG_NAME, "img").get_attribute("alt")

    for i in range(30):
        
        itemName = imageContainers[i].find_element(By.TAG_NAME, "img").get_attribute("alt")

        if itemName == lastElementParsed:
            break
        
        itemPriceParsed = price[i].text.split()
        itemPrice = itemPriceParsed[0].replace(',', "")


        if i < 4:
            parsedImgLink = imageContainers[i].find_element(By.TAG_NAME, "img").get_attribute("src").split('/')
        else:
            parsedImgLink = imageContainers[i].find_element(By.TAG_NAME, "img").get_attribute("data-src").split('/')

        gCode = parsedImgLink[7].split('.')
        catCode = parsedImgLink[6]
        figureDict[i] = {
                        'image': {'url': f'https://img.amiami.com/images/product/main/{catCode}/{gCode[0]}.jpg'}, 
                        'author': {'name': 'FigureBot', 'icon_url': 'https://cdn.discordapp.com/app-icons/1065544110074757150/793cbde528fc5794475509a7e37dae20.png?size=256'}, 
                        'fields': [{'inline': True, 'name': f'{itemPrice} JPY', 'value': f'{round(JPYConversion * int(itemPrice))} USD'}],
                        'color': 8388863, 'timestamp': f'{time}', 'type': 'rich', 'description': f'{brand[i].text}', 'url': f'https://www.amiami.com/eng/detail/?gcode={gCode[0]}', 'title': f'{itemName}'
                        }
        if i == 0:
            loopCompleted = True

    if loopCompleted:
        with open('lastFig.txt', 'w') as f:
            f.write(recentFigName)
    else:
        print("no new updates.")

    driver.quit()

    return figureDict