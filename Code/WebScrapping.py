from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import re
import requests,grequests
import matplotlib.pyplot as plt
def getlinks(linkse):
    reqs = [grequests.get(link) for link in linkse]
    resps = grequests.map(reqs)
    return resps
colleges_count=[]

filename="products1.csv"
f=open(filename,"w")
headers="College ID,College Name,CollegeUrl,Email,Address,Contact No,TPO Name,TPO Number\n"
f.write(headers)
regions=['Amravati','Aurangabad','Mumbai','Nagpur','Nashik','Pune']
k=0
for k in range(1,6):
    page_soup=soup(requests.get('http://dtemaharashtra.gov.in/frmInstituteList.aspx?RegionID='+str(k)+'&RegionName='+regions[k]).text,"html.parser")
    containers=page_soup.findAll("tr")
    print(len(containers))
    colleges_count.append(len(containers))
    srno=[]
    links=[]
    collegename=[]
    collegeurl=[]
    for i in range(5,len(containers)):
        contain=containers[i].find("td",string=re.compile('Engi|Tech|TECH'))
        if contain!=None:
            container=containers[i].findAll("td",{"class":"Item"})
            srno.append(container[0].text)
            links.append('http://dtemaharashtra.gov.in/'+container[1].findAll("a")[1]['href'])
            collegename.append(contain.text)    
    resps=getlinks(links)
    j=0
    for resp in resps:
        collegepage_soup=soup(resp.text,"html.parser")
        details=collegepage_soup.findAll("tr")
        email=details[12].findAll("td")[1].text
        collegeurl.append(details[11].findAll("td")[3].text)
        address=details[8].findAll("td")[1].text
        contactno=(details[22].findAll("td")[1].text)
        f.write(srno[j]+','+collegename[j].replace(',','  ')+','+collegeurl[j]+','+email.replace(',','  ')+','+address.replace(',','  ')+','+contactno+"\n")
        j=j+1

url=uReq('http://jbims.edu'+'/committees/placement-committee/')
collegepage=url.read()
url.close()
collegepage_soup=soup(collegepage,"html.parser")
details=collegepage_soup.findAll("div",{"class":"gmail_default"})
tponame=details[1].text.split()[1]
tpono=details[2].text.split()
tponumber=tpono[1]+tpono[2]
print("TPO Name : "+tponame+"\n"+"TPO Number : "+tponumber)
f.close()
reg = ['Amravati','Aurangabad','Mumbai','Nagpur','Nashik']
cols=['c','m','r','b','y']

plt.pie(colleges_count,labels=reg,colors=cols,startangle=90,shadow=True,explode=(0,0,0,0,0),autopct='%1.1f%%')

plt.title('Pie Plot')
plt.show()
'''
    collegeurls=getlinks(collegeurls)
    for collegeurl in collegeurls:
        collegepage_soup=soup(collegeurl.text,"html.parser")
        print(collegepage_soup)
    break'''
