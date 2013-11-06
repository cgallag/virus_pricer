# Caroline Gallagher
# amazonParser.py
# December 13, 2012

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time
import os

initialdir='/Users/cagallagher/Desktop/cs342_finalproj/data_csvs/'
categoryDict={}
f=open(initialdir+'crackKeygenCategory.csv','rb')
for line in f:
    data=line.split(', ')
    progName=data[0].strip().lower()
    progCat=data[1].rstrip('\n').lower()
    categoryDict[progName]=progCat
f.close()

#appDict={'game':[],'application':[]}
#for program in categoryDict.keys():
#if categoryDict[program]=='game':
#appDict['game'].append(program)
#else:
#appDict['application'].append(program)

amazonPrices=open(initialdir+'amazonPrices2.csv','wb')
amazonPrices.write("software,class,amazonPrice,listPrice,platform,amazonName\n")
errorAmazonPrices=open(initialdir+'error_amazonPrices2.csv','wb')
errorAmazonPrices.write("software,class\n")

driver=webdriver.Firefox()

for program in categoryDict.keys():
    progName=program.replace(" ","+")
    if categoryDict[program]=='application':
        driver.get('http://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Dsoftware&field-keywords='+progName)
    else:
        driver.get('http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dvideogames&field-keywords='+progName+'+pc')
    elemDict={}
    error=False 
    for elem in ["toeOurPrice","toeListPrice","title"]:
        try:
            values=driver.find_elements_by_class_name(elem)
            elemDict[elem]=values[0].text
        except:
            print "Error:",program,categoryDict[program]
            errorAmazonPrices.write(program+","+categoryDict[program]+"\n")
            error=True
            break
    try:
        platforms=driver.find_elements_by_class_name("toeLinkText")
        platform=platforms[0].text
    except:
        platform="unidentified"

    if not error:
        amazonPrices.write(program+","+categoryDict[program]+","+str(elemDict['toeOurPrice'])+','+str(elemDict['toeListPrice'])+','+platform+','+elemDict['title']+'\n')

amazonPrices.close()
errorAmazonPrices.close()

    
