# Caroline Gallagher
# office.py
# December 17, 2012

import os
from bs4 import BeautifulSoup
import operator

officedir='/home/wendy/cs342_securityproj/office2010outlet/'
datafiles=os.listdir(officedir)

csvfile=open('/home/wendy/cs342_securityproj/data_csvs/officeprogs.csv','wb')
csvfile.write('software,fullPrice,discountPrice\n')

for filename in datafiles:
    f=open(officedir+filename,'rb')
    soup=BeautifulSoup(f)
    mains=soup.find_all(class_='main')
    for main in mains:
        ind=mains.index(main)-1
        if operator.mod(ind,3)==0:
            info=main.stripped_strings
            progName=info.next()
            info.next()
            priceInfo=info.next()
            priceArray=priceInfo.split()
            if len(priceArray)==1:
                fullPrice=info.next()
                discountedPrice=info.next()
            else:
                fullPrice=priceArray[1]
                discountedPrice=priceArray[1]
            csvfile.write(progName+','+fullPrice+','+discountedPrice+'\n')

csvfile.close()
    
