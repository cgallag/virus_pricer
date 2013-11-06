# Caroline Gallagher
# December 26, 2012
# virusdata_reorganizer_allsources_amazononly.py

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
pricingFile.close()

virusFile=open(initialdir+'merged.csv','rb')
newVirusFile=open(initialdir+'virusnew_allsources_amazononly.csv','wb')
newVirusFile.write("software,class,links,numVirus,avgSeverity,virusScanner,downloadSource,price,priceSource\n")

numProgDict={'game':0,'application':0}

for line in virusFile:
        data=line.split(',')
        numElements=len(data)-1
	try:
		if data[2]=='' or data[9]=='' or data[16]=='':
			continue
	except:
		continue
        if data[0]!='software':
            program=data[0]
            category=data[1]
	    try:
		amazonPrice=pricingDict[program]['amazon']
		if amazonPrice=='':
			continue
	    except:
		continue
	    numProgDict[category]+=1
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
		    # newVirusFile.write(program+','+category+','+sourceLinks+','+numViruses+','+avgSeverity+','+scanner+','+source+','+shadyPrice+',shady\n')

print 'Number of games', numProgDict['game']
print 'Number of applications', numProgDict['application']

virusFile.close()
newVirusFile.close()
