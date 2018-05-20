from bs4 import BeautifulSoup
import time
import string
printable=set(string.printable)
import csv
import re
from selenium import webdriver #This allows us to read the webpage if uses Javascript
driver = webdriver.PhantomJS() #Use phantonJS as our webdriver, which runs in the background (e.g. doesn't open up a new window) and allows us to collect javascript items (which we might not need for this tutorial, but could be useful for you in the future)

def print_line():
    print " "
    print "----------------------------------------------------------------------------------------------------------------------"
    print " "
    
month_list_input = raw_input("What months do you want to scrape? Type ALL for all months. Separate months using commas. ")
start_year = raw_input("What is the start year? Earliest option is 2001. ")
end_year = raw_input("What is the end year? Latest option is 2015. ")
    
if month_list_input.upper() == "ALL":
    month_list = ["January","February","March","April","May","June","July","August","September","October","November","December"]

else:
    month_list = month_list_input.split(',')

homepage_url = "http://wayback.archive-it.org/7993/20170111082703/http://www.fda.gov/Drugs/DevelopmentApprovalProcess/HowDrugsareDevelopedandApproved/DrugandBiologicApprovalReports/ANDAGenericDrugApprovals/ucm050527.htm"

driver.get(homepage_url) #get the webpage
time.sleep(1)

homepage_soup = BeautifulSoup(driver.page_source,"lxml")
print homepage_soup.prettify() 

for YYYY in range(int(start_year),int(end_year)+1):
    print_line()
    print "YEAR =",YYYY
    
    year_tag = homepage_soup.find('a',href=True,text=re.compile('%s'%(YYYY)))
    year_link = "http://wayback.archive-it.org" + year_tag.get('href')
    
    #Go to the link for that page and turn it into beautiful soup:
    driver.get(year_link)
    year_soup = BeautifulSoup(driver.page_source,"lxml")
    
    
    for month in month_list:
        month = month.strip()
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
            month_link = "http://wayback.archive-it.org" + month_tag.get('href')
            print "Month URL is:", month_link
    
        elif YYYY>2006:
            print "YEAR AFTER 2006"
            #print year_soup.prettify()
            
            month_tag = year_soup.find('a',href=True,text=re.compile(month))
            month_link = "http://wayback.archive-it.org" + month_tag.get('href')
            print "Month URL is:", month_link
            print "NUMBER OF TAGS WITH MONTH IN THE NAME:",len(year_soup.find_all('a',href=True,text=re.compile(month)))
    
        #Go to the URL for that month and turn it into soup:
        driver.get(month_link)
        month_soup = BeautifulSoup(driver.page_source,"lxml")
        
        #print month_soup.prettify()
        
        #Pull all of the table elements out of the table and store them in a csv file named year_month
        csv_filename = "Data/"+str(YYYY)+month+".csv"
        with open(csv_filename,'w') as csv_file:
            
            #Create a list containing all the th and then tr tags:
            #Find the first th tag, then find it's parent, then that one's parent, and then get all the TR/TH tags in that tag:
            # first_th_tag = month_soup.find('th')
            # th_parent = first_th_tag.parent
            # th_grandparent = th_parent.parent
            
            
            #Find the first td tag (table data), then find it's parent (which is the tr tag) and then that one's parent, which is the tag that should have ALL the rows in the table we care about
            # first_td_tag = month_soup.find('td')
            # td_parent = first_td_tag.parent
            # th_grandparent = td_parent.parent
            
            
            #Find the LAST td tag, get the parent, and then its parent:
            all_td_tags = month_soup.find_all('td')
            last_td_tag = all_td_tags[len(all_td_tags)-1]
            td_parent = last_td_tag.parent
            th_grandparent = td_parent.parent
            
            #Pull out all the TR tags (table rows), and then take each TH (header) OR TD (table data) and write as a new cell to CSV file
            for tr_tag in th_grandparent:
                for cell in tr_tag.find_all(['th','td']):
                    cell_value = cell.get_text().replace(",","")
                    cell_value = filter(lambda x: x in printable, cell_value)
                    
                    csv_file.write(cell_value+",")
                csv_file.write("\n")
    
driver.quit() #Close the driver
    