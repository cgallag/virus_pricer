# Caroline Gallagher
# pricingDataMerger.py
# December 19, 2012

import os

initialdir='/Users/cagallagher/Desktop/cs342_finalproj/pricing_data/'

amazonDict={}
f=open(initialdir+'amazonPricesNew.csv','rb')
for line in f:
    data=line.split(',')
    progName=data[0]
    listPrice=data[3]
    if listPrice==' ':
        listPrice=data[2]
    amazonDict[progName]={'amazonPrice':data[2].strip('$ '),'listPrice':data[3].strip('$ '),'compType':data[4],'title':data[5].rstrip('\n')}
f.close()
print 'amazonDict',amazonDict

officeDict={}
f=open(initialdir+'officeprogs2.csv','rb')
for line in f:
    data=line.split(',')
    if data[0]=='':
        break
    else:
        progName=data[0]
        officeDict[progName]={'listPrice':data[1].strip('$ '),'fakePrice':data[2].strip('$ '), 'title':data[3].rstrip('\n')}
f.close()
print 'officeDict',officeDict

directDict={}
f=open(initialdir+'direct2playPrices2.csv','rb')
for line in f:
    data=line.split(',')
    progName=data[0]
    directDict[progName]={'fakePrice':data[2].strip('$ '), 'title':data[4].rstrip('\n')}
f.close()
print 'directDict',directDict

softplazaDict={}
f=open(initialdir+'softPlazaPrices2.csv','rb')
for line in f:
    data=line.split(',')
    progName=data[0]
    softplazaDict[progName]={'listPrice':data[3].strip('$ '), 'fakePrice':data[2].strip('$ '), 'compType':data[4], 'title':data[5].rstrip('\n')}
f.close()
print 'softplazaDict',softplazaDict

playscDict={}
f=open(initialdir+'playscPrices2.csv','rb')
for line in f:
    data=line.split(',')
    progName=data[0]
    playscDict[progName]={'fakePrice':data[2].strip('$ '), 'title':data[3].rstrip('\n')}
f.close()
print 'playscDict',playscDict

categoryDict={}
f=open('/Users/cagallagher/Desktop/cs342_finalproj/data_csvs/crackKeygenCategory.csv','rb')
for line in f:
    data=line.split(', ')
    progName=data[0].strip().lower()
    progCat=data[1].rstrip('\n').lower()
    categoryDict[progName]=progCat
f.close()

mergedprices=open(initialdir+'mergedprices.csv','wb')
mergedprices.write('software,class,amazonPrice,office2010Price,softplazaPrice,playscPrice,direct2playPrice,fakePrice\n')
for program in categoryDict.keys():
    numShadyPrices=0
    fakeNumerator=0.0
    priceTotal=0.0
    try:
        amazonprice=float(amazonDict[program]['amazonPrice'])
        priceTotal+=amazonprice
    except:
        amazonprice=''
        
    try:
        office2010price=float(officeDict[program]['fakePrice'])
        numShadyPrices+=1
        fakeNumerator+=office2010price
        priceTotal+=office2010price
    except:
        office2010price=''

    try:
        softplazaprice=float(softplazaDict[program]['fakePrice'])
        numShadyPrices+=1
        fakeNumerator+=softplazaprice
        priceTotal+=softplazaprice
    except:
        softplazaprice=''

    try:
        directprice=float(directDict[program]['fakePrice'])
        numShadyPrices+=1
        fakeNumerator+=directprice
        priceTotal+=directprice
    except:
        directprice=''

    try:
        playscprice=float(playscDict[program]['fakePrice'])
        numShadyPrices+=1
        fakeNumerator+=playscprice
        priceTotal+=playscprice
    except:
        playscprice=''

        # Averaging the shady prices into one price.
    if numShadyPrices>0:
        fakePrice=fakeNumerator/numShadyPrices
    else:
        fakePrice=''

    print program, str(amazonprice), str(office2010price), str(directprice), str(playscprice), str(fakePrice) 
    if priceTotal!=0.0:
        mergedprices.write(program+','+categoryDict[program]+','+str(amazonprice)+','+str(office2010price)
                           +','+str(softplazaprice)+','+str(playscprice)+','+str(directprice)+','
            +str(fakePrice)+'\n')

mergedprices.close()
    
    
