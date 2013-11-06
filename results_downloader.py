import urllib2
from bs4 import BeautifulSoup
import os
import os.path
import sys
import zipfile

password_mgr=urllib2.HTTPPasswordMgrWithDefaultRealm()
password_mgr.add_password(None,'http://amnesiac.seclab.tuwien.ac.at/','notrealusername','notrealpassword')
handler=urllib2.HTTPBasicAuthHandler(password_mgr)
opener=urllib2.build_opener(handler)
opener.open('http://amnesiac.seclab.tuwien.ac.at/')
urllib2.install_opener(opener)

response=urllib2.urlopen('http://amnesiac.seclab.tuwien.ac.at/')
soup = BeautifulSoup(response)

initialdir = os.getcwd()

crackdir='crackKeygenArchives'
os.mkdir(crackdir)
os.chdir(initialdir + '/' + crackdir)

for list in soup.find_all('li'):
    progname=list.contents[0]
    print(progname)
    #os.mkdir(progdir)
    #os.chdir(initialdir + '/' + crackdir + '/' + progdir)
    for link in list.find_all('a'):
        if link.contents[0]=='[Results]':
            result_link=link.get('href')
            print(result_link)
            opener.open(result_link)
            urllib2.install_opener(opener)
            download=urllib2.urlopen(result_link)
            download_data=download.read()
            with open(progname + ".zip","wb") as code:
                code.write(download_data)
            code.close()
                #with zipfile.ZipFile("temp.zip",'r') as z:
                #z.extractall(os.getcwd())
                #os.remove("temp.zip")
            


        
        

