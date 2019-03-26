import requests
from bs4 import BeautifulSoup
import sys, os
import pireps
from datetime import datetime as dt
from datetime import timedelta
from pireps import Pirep

def Assemble_Search_URL(event_id="10043",date=dt.today(),search_type="Date"):
    url = 'https://www.deltava.org/acarsprsearch.do?eventID='+ event_id + '&viewStart=0&viewCount=20000&flightDate=' + date.strftime("%m/%d/%Y") + '&searchType=' + search_type
    return url


def Get_ACARS_Pireps_List(search_date):
    # Get the url of the search page to query the desired date
    search_URL = Assemble_Search_URL(date=search_date)
    # Get the beautiful soup html object of the search page
    search_page = Get_Page_HTML(search_URL)

    # Get a list of all the hyperlinks in the table
    #table = search_page.body
    #table = table.find_all
    all_links = search_page.body.find_all('a')
    # Get the first entry in the table of flights
    first_entry_id = 38
    first_entry = all_links[first_entry_id]
    table = first_entry.parent.parent.parent
    # Initialize the list of pireps
    pireps_list = []
    i = 0
    num_flights = len(table.find_all('a'))
    for link in table.find_all('a'):
        url = 'https://deltava.org' + link.get('href')
        pireps_list.append(Pirep(url=url))
        #print(url)
    return pireps_list
    
    
def Get_Page_HTML(url):
    # Download the page html
    response = requests.get(url)
    # Check to make sure the response is good
    if response.status_code == requests.codes.ok:
        page = BeautifulSoup(response.text, 'html.parser')
        return page
    else:
        response.raise_for_status()

def Search_Range_of_Dates(start_date,end_date):
    pireps_list = []
    timestep = timedelta(1)
    search_date = start_date
    while search_date <= end_date:
        new_list = Get_ACARS_Pireps_List(search_date)
        pireps_list.extend(new_list)
        search_date = search_date + timestep
    return pireps_list

def Process_ACARS_Pireps_List

#print(Assemble_Search_URL())
#Get_ACARS_Pireps_List(dt.today())
results = Search_Range_of_Dates(dt(2019,1,1),dt(2019,1,2))
