# Caroline Gallagher
# playsc.py
# December 15, 2012

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import sys

initialdir='/home/wendy/cs342_securityproj/data_csvs/'
categoryDict={}
f=open(initialdir+'crackKeygenCategory.csv','rb')
for line in f:
    data=line.split(', ')
    progName=data[0].strip().lower()
    progCat=data[1].rstrip('\n').lower()
    categoryDict[progName]=progCat
f.close()

playscPrices=open(initialdir+'playscPrices.csv','wb')
playscPrices.write("software,class,playscPrice,gameName\n")
errorPrices=open(initialdir+'error_playscPrices.csv','wb')
errorPrices.write("software\n")

driver=webdriver.Firefox()

for program in categoryDict.keys():
    if categoryDict[program]=='game':
        driver.get('http://play-sc.com')
        searchbox=driver.find_element_by_id('st_search_input')
        searchbox.send_keys(program)
        searchbox.submit()
        try:
            gamelinks=driver.find_elements_by_css_selector('h2 a')
            gamename=''
            gametitles=[]
            for gamelink in gamelinks:
                gametitles.append(gamelink.get_attribute('href').lstrip('http://play-sc.com/').rstrip('.html'))
                # Searching for the correct game title in the search results
            for game in gametitles:
                name=game.replace("-"," ").lower()
                if name.find(program)!=-1:
                    gameName=name
                    gameListIndex=gametitles.index(game)
                    print gameName,gameListIndex
                    break
            prices=driver.find_elements_by_class_name('currency')
            print gameName, len(prices)
            price=prices[gameListIndex].text
            if gameName!='':
                    playscPrices.write(program+','+categoryDict[program]+','+str(price)+','+gameName+'\n')
        except Exception,err:
            print "error",program,str(err)
            errorPrices.write(program+'\n')

driver.close()
playscPrices.close()
errorPrices.close()
