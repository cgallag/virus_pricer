# Caroline Gallagher
# December 13, 2012

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time
import os

initialdir='/home/wendy/cs342_securityproj/data_csvs/'
categoryDict={}
f=open(initialdir+'crackKeygenCategory.csv','rb')
for line in f:
    data=line.split(', ')
    progName=data[0].strip().lower()
    progCat=data[1].rstrip('\n').lower()
    categoryDict[progName]=progCat
f.close()

spPrices=open(initialdir+'softPlazaPrices.csv','wb')
spPrices.write("software,class,spPrice,retailPrice,platform,spName\n")
errorspPrices=open(initialdir+'error_softPlazaPrices.csv','wb')
errorspPrices.write("software,class\n")

driver=webdriver.Firefox()

for program in categoryDict.keys():
    progName=program.replace(" ","+")
    error=False
    driver.get('http://soft-plaza.net/browse/search/?q='+progName)
    try:
        #Get pricing data
        prices=driver.find_elements_by_class_name('pricing')
        firstprice=prices[0].text.split('\n')
        spPrice=firstprice[1]
        retailPrice=firstprice[0]
        #Get software title
        names=driver.find_elements_by_class_name('title')
        for name in names:
            if name.tag_name=='a':
                title=name.text
                break
        #Get platform
        platforms=driver.find_elements_by_class_name('os')
        for p in platforms:
            if p.tag_name=='div':
                platform=p.text
                break
        spPrices.write(program+','+categoryDict[program]+','+str(spPrice)+','+str(retailPrice)+','+platform+','+title+'\n')
    except:
        errorspPrices.write(program+","+categoryDict[program]+'\n')

spPrices.close()
errorspPrices.close()
    
    
