from bs4 import BeautifulSoup
import xlsxwriter
import time
from selenium import webdriver #This allows us to read the webpage if uses Javascript
driver = webdriver.PhantomJS() #Use phantonJS as our webdriver, which runs in the background (e.g. doesn't open up a new window) and allows us to collect javascript items (which we might not need for this tutorial, but could be useful for you in the future)

def print_line():
    print " "
    print "----------------------------------------------------------------------------------------------------------------------"
    print " "
    
homepage_url = "http://wayback.archive-it.org/7993/20170111082703/http://www.fda.gov/Drugs/DevelopmentApprovalProcess/HowDrugsareDevelopedandApproved/DrugandBiologicApprovalReports/ANDAGenericDrugApprovals/ucm050527.htm"

driver.get(homepage_url) #get the webpage
time.sleep(1)

homepage_soup = BeautifulSoup(driver.page_source,"lxml") #Feed the URL into beautiful soup, which turns the HTML code underlying the website into a format the Python can parse
#print soup.prettify() #Print the page source

for YYYY in range(2001,2015):
    print_line()
    print "YEAR =",YYYY
    year_tag = homepage_soup.find_all('a',href=True,text="ANDA (Generic) Drug Approvals in %s" %(YYYY))
    print "YEAR TAG:",year_tag
    #year_link = "http://wayback.archive-it.org" + year_tag.get('href')
    #print "YEAR LINK:",year_link
    
    # if YYYY<2007:
    #     print "YEAR BEFORE 2007"
    # elif YYYY>2006:
    #     print "YEAR AFTER 2006"
    