import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv
import gc
gc.enable()
import datetime
import logging
from os import path

DEFAULT_LOG_FILE = "D:\\coxna\\Documents\\Flight Sim\\Dispatch\\Python\\DVA_Roster_Processing\\Logs\\"
# Record the time the program was started
START_TIME = datetime.datetime.now()
programStartTimeStr = START_TIME.strftime('%Y%m%d-%H%M%S')

# Get the current logger if there is one being used by a higher module
logger = logging.getLogger(__name__)

class pilot:
    # Attributes:
    #   Name
    #   ID
    #   URL
    #   Equipment
    #   Rank
    #   Ratings
    #   VATSIM_ID
    #   VATSIM_Ratings
    #   IVAO_ID

    def __init__(self):
        self.Name = ''
        self.ID = ''
        self.URL = ''
        self.Equipment = ''
        self.Rank = ''
        self.Ratings = ''
        self.VATSIM_IF = ''
        self.VATSIM_Ratings = ''
        self.IVAO_ID = ''
    
    def create_from_table_row(self,row):
        #print(row)
        #print(row.find_all('td'))
        tds = row.find_all('td')
        id_elem = tds[0]
        #print(id_elem)
        self.ID = id_elem.string
        name_elem = tds[1]
        #print(name_elem)
        self.Name = name_elem.string
        url_elem = name_elem.a
        self.URL = name_elem.a.get('href')
        #print(self.ID)
        #print(self.Name)
        #print(self.URL)
        self.Equipment = tds[2].string
        self.Rank = tds[3].string
        #print(self.Equipment)
        #print(self.Rank)
        # Get the soup object of the pilot's profile page
        profile_page = self.get_pilot_page(self.URL)
        # Retrieve the pilot's additional ratings from their profile page
##        addl_ratings_str = self.get_profile_stat(profile_page,'Additional Ratings')
##        #print(addl_ratings_str)
##        self.Ratings = addl_ratings_str
##        # Retrieve the pilot's VATSIM ID from their profile page
##        vatsim_id = self.get_profile_stat(profile_page,'VATSIM ID')
##        #print(vatsim_id)
##        self.VATSIM_ID = vatsim_id
##        # Retrieve the pilot's VATSIM ratings from their profile page
##        vatsim_ratings_str = self.get_profile_stat(profile_page,'VATSIM Ratings')
##        #print(vatsim_ratings_str)
##        self.VATSIM_Ratings = vatsim_ratings_str
##        # Retrieve the pilot's VATSIM ID from their profile page
##        ivao_id = self.get_profile_stat(profile_page,'IVAO ID')
##        #print(ivao_id)
##        self.IVAO_ID = ivao_id
        self.fill_profile_info(profile_page)

    def create_from_profile_page(self,profile_URL):
        self.URL = profile_URL
        profile_page = self.get_pilot_page(self.URL)
        self.Ratings = "N/A"
        self.VATSIM_ID = "N/A"
        self.VATSIM_Ratings = "N/A"
        self.IVAO_ID = "N/A"
        main_div = profile_page.find(id="main")
        # find all table rows in the main div
        trs = main_div.find_all('tr')
        # Process the rank, name, and pilot ID from the first row
        # Take the first row of the table
        name_hdr = trs[0].string
        self.Rank = self.__get_rank__(name_hdr)
        # Get the pilot's ID
        split_str = name_hdr.split()
        id_str = split_str[-1]
        self.ID = id_str[1:-1]
        # Get the pilots name
        self.Name=' '.join(split_str[len(self.Rank.split()):-1])
        # Get the rest of the info from the profile page
        for row in trs:
            tds = row.find_all('td')
            if len(tds) > 0:
                key = tds[0].string
                val = tds[1].string
                if key ==  'Additional Ratings':
                    self.Ratings = val
                elif key == 'VATSIM ID':
                    self.VATSIM_ID = val
                elif key == 'VATSIM Ratings':
                    self.VATSIM_Ratings = val
                elif key == 'IVAO ID':
                    self.VATSIM_ID = val
                elif key == 'Equipment Type':
                    self.Equipment = val
                #elif key == 'Home Airport':
                #    self.Home_Airport = val.split()[-1][1:-1]
                #elif key = 'E-Mail Address':
                #    self.Email = val
                
    def __get_rank__(name_hdr):
        str_split = name_hdr.split()
        if str_split[0] == 'CAPTAIN':
            return 'Captain'
        elif str_split[0] == 'FIRST':
            return 'First Officer'
        elif str_split[0] == 'SENIOR':
            return 'Senior Captain'
        elif str_split[0] == 'ASSISTANT':
            return 'Assistant Chief Pilot'
        elif str_split[0] == 'CHIEF':
            return 'Chief Pilot'
        else:
            print('Unable to parse rank from header: ',name_hdr)
            return 'N/A'

    def fill_profile_info(self,profile_page):
        self.Ratings = "N/A"
        self.VATSIM_ID = "N/A"
        self.VATSIM_Ratings = "N/A"
        self.IVAO_ID = "N/A"
        main_div = profile_page.find(id="main")
        # find all table rows in the main div
        trs = main_div.find_all('tr')
        for row in trs:
            tds = row.find_all('td')
            if len(tds) > 0:
                if tds[0].string ==  'Additional Ratings':
                    self.Ratings = tds[1].string
                elif tds[0].string == 'VATSIM ID':
                    self.VATSIM_ID = tds[1].string
                elif tds[0].string == 'VATSIM Ratings':
                    self.VATSIM_Ratings = tds[1].string
                elif tds[0].string == 'IVAO ID':
                    self.VATSIM_ID = tds[1].string

    def get_profile_stat(self,profile_page,stat):
        main_div = profile_page.find(id="main")
        # find all table rows in the main div
        trs = main_div.find_all('tr')
        for row in trs:
            tds = row.find_all("td")
            if len(tds) > 0:
                if tds[0].string ==  stat:
                    return tds[1].string
        return 'N/A'

    def get_pilot_page(self,profile_url):
        """
        Download the pilot's profile page from a given URL.
        """
        # Download the profile web page html
        response = requests.get('https://www.deltava.org' + profile_url)
        # Check to make sure the response is good
        if response.status_code == requests.codes.ok:
            pilot_page = BeautifulSoup(response.text, 'html.parser')
            return pilot_page
        else:
            Response.raise_for_status()

    def get_attribs_list_for_printing(self):
        attribs = []
        attribs.append(self.ID)
        attribs.append(self.Name)
        attribs.append(self.URL)
        attribs.append(self.Equipment)
        attribs.append(self.Rank)
        attribs.append(self.Ratings)
        attribs.append(self.VATSIM_ID)
        attribs.append(self.VATSIM_Ratings)
        attribs.append(self.IVAO_ID)
        return attribs

    
class HTMLTableParser:
    
    def parse_pilot_roster(self,roster_url):
        table = self.get_roster_table(roster_url)

    def write_pilots_roster_csv(self,roster_url):
        dest_file = 'D:\\coxna\\Documents\\Flight Sim\\Dispatch\\DVA_Roster_Processing\\roster_basic.csv'
        pilots_list = self.assemble_pilots_list(roster_url)
        self.write_roster_to_file(pilots_list,dest_file)
            
    def write_roster_to_file(self,pilots_list,dest_file):
        with open(dest_file, 'w', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            #attribs_list = []
            headers = ['Pilot Code','Name','URL','Equipment','Rank','Ratings','VATSIM ID','VATSIM Ratings','IVAO ID']
            writer.writerow(headers)
            for p in pilots_list:
                #attribs_list.append(p.get_attribs_list_for_printing())
                #writer.writerows(attribs_list)
                writer.writerow(p.get_attribs_list_for_printing())

    def assemble_pilots_list(self,roster_url):
        response = requests.get(roster_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(len(soup.find_all('a')))
        #print(soup.find_all('a'))
        ptable = soup.find_all('a')[41].parent.parent.parent
        pilots = []
        i = 0
        num_pilots = len(ptable.find_all('a'))
        for link in ptable.find_all('a'):
            row = link.parent.parent
            if ((link.string != "PAGE DOWN") & (link.string != "PAGE UP")):
                test_pilot = pilot()
                test_pilot.create_from_table_row(row)    
                pilots.append(test_pilot)
                i += 1
                #print(datetime.datetime.now(),'  ',str(i),' of ',str(num_pilots))
                print(test_pilot.get_attribs_list_for_printing(),sep='    ')
        return(pilots)

    def get_roster_table(self,roster_url):
        response = requests.get(roster_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        random_elem = soup.find_all('a')[45]
        table = random_elem.parent.parent.parent
        print(table.prettify())
        return table


def create_pilot_roster_csv():
    url = 'https://www.deltava.org/roster.do?sortType=P.PILOT_ID&viewStart=0&viewCount=30000'
    hp = HTMLTableParser()
    print(datetime.datetime.now())
    hp.write_pilots_roster_csv(url)
    print(datetime.datetime.now())

def test_create_pilot_roster_csv():
    url = 'https://www.deltava.org/roster.do?sortType=P.PILOT_ID&viewStart=0&viewCount=5'
    hp = HTMLTableParser()
    print(datetime.datetime.now())
    hp.write_pilots_roster_csv(url)
    print(datetime.datetime.now())

def print_test_pilot_page(profile_URL):
    test_pilot = pilot()
    #pilot.URL = profile_URL
    test_pilot.create_from_profile_page(profile_URL)
    print(pilot)
    print(" ")
    print(" ")
    print(" ")
    profile_page = test_pilot.get_pilot_page(profile_URL)
    main_div = profile_page.find(id="main")
    print(main_div.prettify())

def main():
    create_pilot_roster_csv():

if __name__ == "__main__":
    # Configure info level log
    log_name = "DVA_Roster_Processing_Log" + programStartTimeStr + ".txt"
    log_file = os.path.join(DEFAULT_LOG_FILE,log_name)
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s')

    # Call the main function
    main()
