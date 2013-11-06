initialdir='/Users/cagallagher/Desktop/cs342_finalproj/data_csvs/'
och=open(initialdir+'och.csv','rb')
torrent=open(initialdir+'torrent.csv','rb')
usenet=open(initialdir+'usenet.csv','rb')

def recordVirusnum(f):
    sourceDict={}
    programDict={}
    linenum=0
    for line in f:
        if linenum==0:
            headings=line
            linenum+=1
        else:
            data=line.split(',')
            #print data
            # Create a record of how many downloads have viruses
            try:
                sourceDict[data[0]][data[3]]
            except:
                try:
                    sourceDict[data[0]]
                except:
                    sourceDict[data[0]]={}
                    
                sourceDict[data[0]][data[3]]={'avgScore':0.0, 'numOccur':0}
                
            #Record a new occurrance of the virus
            if data[5]=='t\n':
                sourceDict[data[0]][data[3]]['numOccur']+=1
                oldScore=sourceDict[data[0]][data[3]]['avgScore']*float(sourceDict[data[0]][data[3]]['numOccur']-1)
                sourceDict[data[0]][data[3]]['avgScore']=(oldScore+float(data[4]))/sourceDict[data[0]][data[3]]['numOccur']

            #Record the number of links and class if this has not been previously recorded
            try:
                programDict[data[0]]
            except:
                programDict[data[0]]=data[2]
                
    return [sourceDict, programDict]

linksDict={}
sourceDict={}

ochData=recordVirusnum(och)
sourceDict['och']=ochData[0]
linksDict['och']=ochData[1]

torrentData=recordVirusnum(torrent)
sourceDict['torrent']=torrentData[0]
linksDict['torrent']=torrentData[1]

usenetData=recordVirusnum(usenet)
sourceDict['usenet']=usenetData[0]
linksDict['usenet']=usenetData[1]

och.close()
torrent.close()
usenet.close()

print 'Source and link dictionaries created.'

categoryDict={}
f=open(initialdir+'crackKeygenCategory.csv','rb')
for line in f:
    data=line.split(', ')
    progName=data[0].strip().lower()
    progCat=data[1].rstrip('\n').lower()
    categoryDict[progName]=progCat
f.close()

progDict={}
for program in categoryDict.keys():
    progDict[program]={}
    for source in ['och','torrent','usenet']:
        try:
            progDict[program][source]=sourceDict[source][program]
        except:
            continue
            #progDict[program][source]=''

            #print progDict
            #print linksDict

merged=open(initialdir+"merged.csv",'wb')
merged.write("software,class,linksOCH,numAnubisOCH,avgAnubisOCH,numVT_newOCH,avgVT_newOCH,numVT_existOCH,avgVT_existOCH,linksTORRENT,numAnubisTORRENT,avgAnubisTORRENT,numVT_newTORRENT,avgVT_newTORRENT,numVT_existTORRENT,avgVT_existTORRENT,linksUSENET,numAnubisUSENET,avgAnubisUSENET,numVT_newUSENET,avgVT_newUSENET,numVT_existUSENET,avgVT_existUSENET\n")

for program in progDict.keys():
    progLine=program+","+categoryDict[program]+","
    print progLine
    for source in ['och','torrent','usenet']:
        #links
        try:
            progLine+=str(linksDict[source][program])+','
        except:
            progLine+=','
        print progLine  
        for testType in ['anubis','virustotal_new','virustotal_existing']:
            for metric in ['numOccur','avgScore']:
                try:
                    progLine+=str(progDict[program][source][testType][metric])+","
                except:
                    progLine+=','
                print progLine
                
    progLine=progLine.rstrip(',')   
    progLine+='\n'
    merged.write(progLine)

merged.close()
print "merged csv written."
                                    
            
                
              
