from selenium import webdriver
# Caroline Gallagher
# direct2play.py
# December 14, 2012

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

d2pPrices=open(initialdir+'direct2PlayPrices.csv','wb')
d2pPrices.write("software,class,d2pPrice,available,gameName\n")
errord2pPrices=open(initialdir+'error_direct2PlayPrices.csv','wb')
errord2pPrices.write("software\n")

driver=webdriver.Firefox()
driver.get('http://www.direct2play.com/')

for program in categoryDict.keys():
    if categoryDict[program]=='game':
        driver.get('http://www.direct2play.com/')
        searchbox=driver.find_element_by_id('search_query_top')
        searchbox.send_keys(program)
        searchbox.submit()
        elemDict={}
        error=False
        for elem in ['price','exclusive','product_link']:
            try:
                elemDict[elem]=driver.find_element_by_class_name(elem).text
                #print program,elemDict[elem]
            except:
                print "Error:",program,elem
                errord2pPrices.write(program+'\n')
                error=True
                break
        if not error:
            if elemDict['exclusive']=='No Stock':
                avail='f'
            else:
                avail='t'
            try:
                d2pPrices.write(program+","+categoryDict[program]+","+str(elemDict['price'])+','+avail+','+str(elemDict['product_link'])+'\n')
            except:
                errord2pPrices.write(program+'\n')
                print "Error",program,"incorrectly encoded"

d2pPrices.close()
errord2pPrices.close()
                
            
