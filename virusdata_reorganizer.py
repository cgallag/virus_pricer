# Caroline Gallagher
# December 26, 2012
# virusdata_reorganizer.py

initialdir='/Users/cagallagher/Desktop/cs342_finalproj/pricing_data/'

pricingFile=open(initialdir+'pricesnew.csv','rb')
pricingDict={}
for line in pricingFile:
	data=line.split(',')
	if data[0]!='software':
		program=data[0]
		price=data[2]
		priceSource=data[3].rstrip('\n')
		try:
			pricingDict[program][priceSource]=price
		except:
			pricingDict[program]={}
			pricingDict[program][priceSource]=price
print pricingDict
pricingFile.close()

virusFile=open(initialdir+'merged.csv','rb')
newVirusFile=open(initialdir+'virusnew.csv','wb')
newVirusFile.write("software,class,links,numVirus,avgSeverity,virusScanner,downloadSource,price,priceSource\n")

for line in virusFile:
        data=line.split(',')
        numElements=len(data)-1
        if data[0]!='software':
            program=data[0]
            category=data[1]
	    try:
		amazonPrice=pricingDict[program]['amazon']
		shadyPrice=pricingDict[program]['shady']
	    except:
		continue    
            for sourceNum in [2,9,16]:
                if numElements>=sourceNum:
                    sourceLinks=data[sourceNum]
                else:
                    sourcelinks=''
                if sourceNum==2:
                    source="och"
                elif sourceNum==9:
                    source="torrent"
                else:
                    source="usenet"
                for scannerNum in [1,3,5]:
                    if numElements>=sourceNum+scannerNum+1:
                        numViruses=data[sourceNum+scannerNum]
                        avgSeverity=data[sourceNum+scannerNum+1].rstrip('\n')
                    else:
                        numViruses=''
                        avgSeverity=''
                    if scannerNum==1:
                        scanner="anubis"
                    elif scannerNum==3:
                        scanner="vt_new"
                    else:
                        scanner="vt_existing"
                    newVirusFile.write(program+','+category+','+sourceLinks+','+numViruses+','+avgSeverity+','+scanner+','+source+','+amazonPrice+',amazon\n')
		    newVirusFile.write(program+','+category+','+sourceLinks+','+numViruses+','+avgSeverity+','+scanner+','+source+','+shadyPrice+',shady\n')

virusFile.close()
newVirusFile.close()
