import os
import os.path
from lxml import etree
import json

progDict={}
initialdir = "/Users/cagallagher/Desktop/cs342_finalproj/crackKeygenArchives"
os.chdir(initialdir)

for program in os.listdir(initialdir):
    progDict[program]={}
    #print program
    progDir=initialdir+'/'+program
    for source in ['OCH','torrent','Usenet']:
        sourceDir=progDir+'/'+source
        try:
            metrics=os.listdir(sourceDir)
            progDict[program][source]={"anubis":{},"virustotal_new":{},"virustotal_existing":{},'links':0}
            for metric in metrics:
                metricDir=sourceDir+'/'+metric
                if os.listdir(metricDir)!=[]:
                    if metric=="anubis" or metric=="virustotal_new" or metric=="virustotal_existing":
                        for virusfile in os.listdir(metricDir):
                            viruspath=metricDir+'/'+virusfile
                            virusname=os.path.splitext(virusfile)[0]
                            if metric=="anubis":
                                try:
                                    tree=etree.parse(viruspath)
                                    root=tree.getroot()
                                    progDict[program][source]['anubis'][virusname]={}
                                    for element in root.iter('av_hit','severity_level'):
                                        progDict[program][source]['anubis'][virusname][element.tag]=element.text
                                        #print virusname, ":", progDict[program][source]['anubis'][virusname]
                                except:
                                    print "Could not open", viruspath
                            if metric=="virustotal_new" or metric=="virustotal_existing":
                                if os.path.splitext(viruspath)[1]==".json":
                                    try:
                                        jsonfile=open(viruspath)
                                        jsondict= json.loads(jsonfile.read())
                                        numHits=0
                                        scanners=jsondict['report'][1]
                                        for scanner in scanners.keys():
                                            if scanners[scanner]!='':
                                                numHits=numHits+1
                                        progDict[program][source][metric][virusname]=float(numHits)/float(len(scanners.keys()))
                                        #print metric, virusname, ": Percentage of viruses= ", progDict[program][source][metric][virusname]
                                    except:
                                        print "Could not open", viruspath
                    if metric=="download_links":
                        try:
                            linksfile=open(metricDir+"/links.txt")
                            progDict[program][source]['links']=len(linksfile.readlines())
                            
                        except:
                            print "Could not open",linksfile
        except:
            print sourcedir, "is empty"

print "Dictionary created."

categoryDict={}
f=open('/Users/cagallagher/Desktop/cs342_finalproj/data_csvs/crackKeygenCategory.csv','rb')
for line in f:
    data=line.split(', ')
    progName=data[0].strip().lower()
    progCat=data[1].rstrip('\n').lower()
    categoryDict[progName]=progCat
f.close()

dataDir='/Users/cagallagher/Desktop/cs342_finalproj/data_csvs/'
och=open(dataDir+'och.csv','wb')
torrent=open(dataDir+'torrent.csv','wb')
usenet=open(dataDir+'usenet.csv','wb')

for filename in [och,torrent,usenet]:
    filename.write("software,class,# links,test type,score,hasmalware\n")

#print progDict.keys()

errors=open(dataDir+'errors.csv','wb')
errors.write('virus,software,class,test type,missing element\n')

numav_hit=0
numsev_level=0
numvt_new=0
numvt_exist=0
for program in progDict.keys():
    try:
        progClass = categoryDict[program]
    except:
        raise
        print program
    for source in progDict[program]:
        numlinks=progDict[program][source]["links"]
        if source=="OCH":
            writefile=och
        elif source=="torrent":
            writefile=torrent
        else:
            writefile=usenet

        for virus in progDict[program][source]["anubis"]:
            try:
                score=int(progDict[program][source]["anubis"][virus]["severity_level"])
                if score>=3:
                    hasmalware='t'
                else:
                    hasmalware='f'
                writefile.write(program+","+progClass+","+str(numlinks)+",anubis,"+str(score)+","+hasmalware+"\n")
            except:
                errors.write(virus+","+program+","+progClass+","+source+",severity_level\n")
                numsev_level+=1
                #print program, source, "anubis", virus, "missing severity_level"
                
            try:
                hasmalware=progDict[program][source]["anubis"][virus]["av_hit"][0]
            except:
                errors.write(virus+","+program+","+progClass+","+source+",av_hit\n")
                numav_hit+=1
                #print program, source, "anubis", virus, "missing av_hit"
                
            #print source, "virustotal_new", progDict[program][source]['virustotal_new']
        for virus in progDict[program][source]["virustotal_new"]:
            try:
                score=progDict[program][source]["virustotal_new"][virus]
                if score>=.3:
                    hasmalware='t'
                else:
                    hasmalware='f'
                writefile.write(program+","+progClass+","+str(numlinks)+",virustotal_new,"+str(score)+","+hasmalware+"\n")
            except:
                errors.write(virus+","+program+","+progClass+","+source+",virustotal_new\n")
                numvt_new+=1
                #print program, source, "virustotal_new", virus
                

            #print source, "virustotal_existing", progDict[program][source]['virustotal_existing'] 
        for virus in progDict[program][source]["virustotal_existing"]:
            try:
                score=progDict[program][source]["virustotal_existing"][virus]
                if score>=.3:
                    hasmalware='t'
                else:
                    hasmalware='f'
                writefile.write(program+","+progClass+","+str(numlinks)+",virustotal_existing,"+str(score)+","+hasmalware+"\n")
            except:
                errors.write(virus+","+program+","+progClass+","+source+",virustotal_existing\n")
                numvt_exist+=1
                #print program, source, "virustotal_existing", virus
                

print "errors: avhit=%i, sev_level=%i, vt_new=%i, vt_exist=%i" %(numav_hit,numsev_level,numvt_new,numvt_exist)
och.close()
torrent.close()
usenet.close()
errors.close()
            
