from selenium import webdriver
from bs4 import BeautifulSoup as bs
import re
import pymongo
import time

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["agents"]

driver = webdriver.Chrome()
driver.get("https://agent.cma.gov.il/sochnim_search/newFind.aspx")
driver.find_element_by_xpath("//*[@id='tNumLines']/option[4]").click()
driver.execute_script("searchButton_onclick()")
numOfPagesTxt = driver.find_element_by_xpath("//*[@id='lblResultsPages']").text
numOfPages = int(re.findall(r'\d+', numOfPagesTxt)[0])
print('Found '+str(numOfPages)+' pages')


for i in range(numOfPages-1):
    source = driver.page_source
    soup = bs(source)
    agent = {}

    agentsIDs = soup.find_all(id=re.compile("ResultsDG_lblZehut_"))
    agentsNames = soup.find_all(id=re.compile("ResultsDG_lblName_"))
    agentsEmails = soup.find_all(id=re.compile("ResultsDG_lblEmail_"))
    agentsWorkPlaces = soup.find_all(id=re.compile("ResultsDG_lblWorkPlace_"))
    agentsAddresses = soup.find_all(id=re.compile("ResultsDG_lblAddress_"))
    agentsCities = soup.find_all(id=re.compile("ResultsDG_lblCity_"))
    agentsZones = soup.find_all(id=re.compile("ResultsDG_lblZone_"))
    agentsPhones = soup.find_all(id=re.compile("ResultsDG_lblTel_"))
    agentsLicenses = soup.find_all(id=re.compile("ResultsDG_lblSugLicense_"))

    j = 0
    for j in range(len(agentsIDs)):
        agent['_id'] = re.findall(r'>(.*?)<', str(agentsIDs[j]))[0]
        agent['name'] = re.findall(r'>(.*?)<', str(agentsNames[j]))[0]
        agent['email'] = re.findall(r'>(.*?)<', str(agentsEmails[j]))[0]
        agent['workplace'] = re.findall(r'>(.*?)<', str(agentsWorkPlaces[j]))[0]
        agent['address'] = re.findall(r'>(.*?)<', str(agentsAddresses[j]))[0]
        agent['city'] = re.findall(r'>(.*?)<', str(agentsCities[j]))[0]
        agent['zone'] = re.findall(r'>(.*?)<', str(agentsZones[j]))[0]
        agent['license'] = re.findall(r'>(.*?)<', str(agentsLicenses[j]))[0]
        mycol.insert_one(agent)

    driver.execute_script("__doPostBack('ResultsDG$ctl01$ctl01','')")
    # time.sleep(5)



driver.close()
