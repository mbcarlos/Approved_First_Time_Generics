from bs4 import BeautifulSoup
import xlsxwriter
import time
import re
from selenium import webdriver #This allows us to read the webpage if uses Javascript
driver = webdriver.PhantomJS() #Use phantonJS as our webdriver, which runs in the background (e.g. doesn't open up a new window) and allows us to collect javascript items (which we might not need for this tutorial, but could be useful for you in the future)

def print_line():
    print " "
    print "----------------------------------------------------------------------------------------------------------------------"
    print " "
    
    
month_list = ["January"] #,"February","March","April","May","June","July","August","September","October","November","December"]

homepage_url = "http://wayback.archive-it.org/7993/20170111082703/http://www.fda.gov/Drugs/DevelopmentApprovalProcess/HowDrugsareDevelopedandApproved/DrugandBiologicApprovalReports/ANDAGenericDrugApprovals/ucm050527.htm"

driver.get(homepage_url) #get the webpage
time.sleep(1)

homepage_soup = BeautifulSoup(driver.page_source,"lxml") #Feed the URL into beautiful soup, which turns the HTML code underlying the website into a format the Python can parse
#print homepage_soup.prettify() #Print the page source

#for YYYY in range(2001,2015):
for YYYY in [2002,2012]:
    print_line()
    print "YEAR =",YYYY
    #year_tag = homepage_soup.find_all('a',href=True,text="%s"%(YYYY))
    year_tag = homepage_soup.find('a',href=True,text=re.compile('%s'%(YYYY)))
    print "YEAR TAG:",year_tag
    year_link = "http://wayback.archive-it.org" + year_tag.get('href')
    print "YEAR LINK:",year_link
    
    #Go to the link for that page and turn it into beautiful soup:
    driver.get(year_link)
    year_soup = BeautifulSoup(driver.page_source,"lxml")
    
    
    for month in month_list:
        #Find the URL for that month:
        if YYYY<2007:
            #print year_soup.prettify()
            
            #Figure out which column has "first generics" as the header:
            if month_list.index(month)==0:
                col_num = -1
                for header_tag in year_soup.find_all('th'):
                    col_num += 1
                    if "first generics" in header_tag.get_text().lower():
                        first_generic_col = col_num
            
            #Find the URL for that month:
            month_tag = year_soup.find_all('a',href=True,text=re.compile(month))[first_generic_col]
            print "Month tag for ",month,"is:"
            print month_tag
            month_link = month_tag.get('href')
            print "Month URL is:", month_link
    
        elif YYYY>2006:
            print "YEAR AFTER 2006"
            #print year_soup.prettify()
            
            month_tag = year_soup.find('a',href=True,text=re.compile(month))
            month_link = month_tag.get('href')
            print "Month URL is:", month_link
            print "NUMBER OF TAGS WITH MONTH IN THE NAME:",len(year_soup.find_all('a',href=True,text=re.compile(month)))
    
        #Go to the URL for that month and turn it into soup:
        driver.get(month_link)
        month_soup = BeautifulSoup(driver.page_source,"lxml")
        
        print month_soup.prettify()
    
driver.quit() #Close the driver
    