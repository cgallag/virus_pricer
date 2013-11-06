# Caroline Gallagher
# December 26, 2012
# pricingdata_reorganizer.py

initialdir='/Users/cagallagher/Desktop/cs342_finalproj/pricing_data/'

pricingFile=open(initialdir+'mergedprices.csv','rb')
newPricingFile=open(initialdir+'pricesnew.csv','wb')
newPricingFile.write('software,class,price,priceSource\n')

for line in pricingFile:
    data=line.split(',')
    numElements=len(data)-1
    if data[0]!='software':
        program=data[0]
        category=data[1]
        if numElements>=2:
            amazonPrice=data[2]
        else:
            amazonPrice=''
        if numElements>=7:
            shadyPrice=data[7].rstrip('\n')
        else:
            shadyPrice=''
        newPricingFile.write(program+','+category+','+amazonPrice+',amazon\n'+program+','+category+','+shadyPrice+',shady\n')

pricingFile.close()
newPricingFile.close()
