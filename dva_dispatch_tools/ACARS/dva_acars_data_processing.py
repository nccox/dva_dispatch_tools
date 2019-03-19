import xml.sax
#from bs4 import BeautifulSoup
import csv
import gc
import os
gc.enable()

class Aircraft_Handler(xml.sax.ContentHandler):
    def __init__(self,print_to_console=True,print_style="verbose",output_file=""):
        self.CurrentData = ""
        self.Print_To_Console = print_to_console
        self.Print_Style = print_style
        self.Output_File = output_file
        self.Output_Results = (self.Output_File != "")
        self.__clear_data__()
        self.Field_Names_Dict = {"name": "Name", "family": "Family", "engineType": "Engine Type", "fuelFlow": "Fuel Flow", "baseFuel": "Base Fuel", "taxiFuel": "Taxi Fuel", "pTanks": "P Tanks", "pPct": "P Pct", "sTanks": "S Tanks", "sPct": "S Pct", "oTanks": "O Tanks", "maxWeight": "MGW", "maxZFW": "MZFW", "maxTakeoffWeight": "MTOW", "maxLandingWeight": "MLW", "toRunwayLength": "TO Runway Length", "lndRunwayLength": "LND Runway Length"}
        if self.Output_Results:
            self.__start_AC_file__()

    def __clear_data__(self):
        self.AC_Type = ""
        self.Engines = ""
        self.Range = ""
        self.Seats = ""
        self.Cruise_Speed = ""
        self.Historic = ""
        self.Name = ""
        self.Family = ""
        self.Engine_Type = ""
        self.Fuel_Flow = ""
        self.Base_Fuel = ""
        self.Taxi_Fuel = ""
        self.P_Tanks = ""
        self.P_Pct = ""
        self.S_Tanks = ""
        self.S_Pct = ""
        self.O_Tanks = ""
        self.MGW = ""
        self.MZFW = ""
        self.MTOW = ""
        self.MLW = ""
        self.TO_Runway_Length = ""
        self.LND_Runway_Length = ""

    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        #print(tag)
        #print(attributes)
        if tag == "aircraft":
            if self.Print_To_Console & (self.Print_Style == "verbose"):
                print("*****AIRCRAFT*****")
            self.AC_Type = attributes["type"]
            self.Engines = attributes["engines"]
            self.Range = attributes["range"]
            self.Seats = attributes["seats"]
            self.Cruise_Speed = attributes["cruiseSpeed"]
            self.Historic = attributes["historic"]

   # Call when an elements ends
    def endElement(self, tag):
        if tag == "aircraft":
            self.__add_AC_line_to_file__()
            self.__clear_data__()
        elif self.Print_To_Console:
            if (self.Print_Style == "verbose") & (self.CurrentData in self.Field_Names_Dict):
                print(self.Field_Names_Dict[self.CurrentData], end = ': ')            
            if self.CurrentData == "name":
                print(self.Name)
            elif self.CurrentData == "family":
                print(self.Family)
            elif self.CurrentData == "engineType":
                print(self.Engine_Type)
            elif self.CurrentData == "fuelFlow":
                print(self.Fuel_Flow)
            elif self.CurrentData == "baseFuel":
                print(self.Base_Fuel)
            elif self.CurrentData == "taxiFuel":
                print(self.Taxi_Fuel)
            elif self.CurrentData == "pTanks":
                print(self.P_Tanks)
            elif self.CurrentData == "pPct":
                print(self.P_Pct)
            elif self.CurrentData == "sTanks":
                print(self.S_Tanks)
            elif self.CurrentData == "sPct":
                print(self.S_Pct)
            elif self.CurrentData == "oTanks":
                print(self.O_Tanks)
            elif self.CurrentData == "maxWeight":
                print(self.MGW)
            elif self.CurrentData == "maxZFW":
                print(self.MZFW)
            elif self.CurrentData == "maxTakeoffWeight":
                print(self.MTOW)
            elif self.CurrentData == "maxLandingWeight":
                print(self.MLW)
            elif self.CurrentData == "toRunwayLength":
                print(self.TO_Runway_Length)
            elif self.CurrentData == "lndRunwayLength":
                print(self.LND_Runway_Length)
        self.CurrentData = ""

    # Call when a character is read
    def characters(self, content):
        if self.CurrentData == "name":        
            self.Name = content
        elif self.CurrentData == "family":
            self.Family = content
        elif self.CurrentData == "engineType":
            self.Engine_Type = content
        elif self.CurrentData == "fuelFlow":
            self.Fuel_Flow = content
        elif self.CurrentData == "baseFuel":
            self.Base_Fuel = content
        elif self.CurrentData == "taxiFuel":
            self.Taxi_Fuel = content
        elif self.CurrentData == "pTanks":
            self.P_Tanks = content
        elif self.CurrentData == "pPct":
            self.P_Pct = content
        elif self.CurrentData == "sTanks":
            self.S_Tanks = content
        elif self.CurrentData == "sPct":
            self.S_Pct = content
        elif self.CurrentData == "oTanks":
            self.O_Tanks = content
        elif self.CurrentData == "maxWeight":
            self.MGW = content
        elif self.CurrentData == "maxZFW":
            self.MZFW = content
        elif self.CurrentData == "maxTakeoffWeight":
            self.MTOW = content
        elif self.CurrentData == "maxLandingWeight":
            self.MLW = content
        elif self.CurrentData == "toRunwayLength":
            self.TO_Runway_Length = content
        elif self.CurrentData == "lndRunwayLength":
            self.LND_Runway_Length = content

    def __start_AC_file__(self):
        headers = ["Type", "Engines", "Range", "Seats", "Cruise Speed", "Historic", "Name", "Family", "Engine Type", "Fuel Flow (lb/hr/eng)", "Base Fuel (lb/hr/eng)", "Taxi Fuel (lb/hr/eng)", "P Tanks", "P Pct", "S Tanks", "S Pct", "O Tanks", "MGW (lbs)", "MZFW (lbs)", "MTOW (lbs)", "MLW (lbs)", "TO Runway Length (ft)", "Landing Runway Length (ft)"]
        with open(self.Output_File, mode='w', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(headers)
            
    def __add_AC_line_to_file__(self):
        with open(self.Output_File, mode='a', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            row = self.__assemble_data_row__()
            writer.writerow(row)

    def __assemble_data_row__(self):
        row = []
        row.append(self.AC_Type)
        row.append(self.Engines)
        row.append(self.Range)
        row.append(self.Seats)
        row.append(self.Cruise_Speed)
        row.append(self.Historic)
        row.append(self.Name)
        row.append(self.Family)
        row.append(self.Engine_Type)
        row.append(self.Fuel_Flow)
        row.append(self.Base_Fuel)
        row.append(self.Taxi_Fuel)
        row.append(self.P_Tanks)
        row.append(self.P_Pct)
        row.append(self.S_Tanks)
        row.append(self.S_Pct)
        row.append(self.O_Tanks)
        row.append(self.MGW)
        row.append(self.MZFW)
        row.append(self.MTOW)
        row.append(self.MLW)
        row.append(self.TO_Runway_Length)
        row.append(self.LND_Runway_Length)
        return row

class Airport_Handler(xml.sax.ContentHandler):
    def __init__(self,print_to_console=True,print_style="verbose",output_file=""):
        self.CurrentData = ""
        self.Print_To_Console = print_to_console
        self.Print_Style = print_style
        self.Output_File = output_file
        self.Output_Results = (self.Output_File != "")
        self.__clear_data__()
        self.Field_Names_Dict = {"name": "Name", "lat": "Latitude", "lon": "Longitude", "icao": "ICAO", "iata": "IATA", "utcOffset": "UTC Offset", "maxRunwayLength": "Max Runway Length"}
        if self.Output_Results:
            self.__start_AC_file__()

    def __clear_data__(self):
        self.Lat = ""
        self.Lon = ""
        self.IATA = ""
        self.ICAO = ""
        self.Country = ""
        self.UTC_Offset = ""
        self.Max_Runway = ""
        self.Name = ""
        self.Airlines = []

    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        #print(tag)
        #print(attributes)
        if tag == "airport":
            if self.Print_To_Console & (self.Print_Style == "verbose"):
                print("*****AIRPORT****")
            self.Lat = attributes["lat"]
            self.Lon = attributes["lon"]
            self.IATA = attributes["iata"]
            self.ICAO = attributes["icao"]
            self.Country = attributes["country"]
            self.UTC_Offset = attributes["utcOffset"]
            self.Max_Runway = attributes["maxRunwayLength"]

   # Call when an elements ends
    def endElement(self, tag):
        if tag == "airport":
            self.__add_AC_line_to_file__()
            self.__clear_data__()
        elif self.Print_To_Console:
            if (self.Print_Style == "verbose") & (self.CurrentData in self.Field_Names_Dict):
                print(self.Field_Names_Dict[self.CurrentData], end = ': ')            
            if self.CurrentData == "name":
                print(self.Name)
        self.CurrentData = ""

    # Call when a character is read
    def characters(self, content):
        if self.CurrentData == "name":     
            self.Name = content
        elif self.CurrentData == "airline":
            self.Airlines.append(content)

    def __start_AC_file__(self):
        headers = ["IATA", "ICAO", "Name", "Latitude", "Longitude", "UTC Offset (s)", "Max Runway Length (ft)", "Airlines"]
        with open(self.Output_File, mode='w', newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(headers)
            
    def __add_AC_line_to_file__(self):
        with open(self.Output_File, mode='a', newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter='\t')
            row = self.__assemble_data_row__()
            writer.writerow(row)

    def __assemble_data_row__(self):
        row = []
        row.append(self.IATA)
        row.append(self.ICAO)
        row.append(self.Name)
        row.append(self.Lat)
        row.append(self.Lon)
        row.append(self.UTC_Offset)
        row.append(self.Max_Runway)
        row.append(",".join(self.Airlines))
        return row


def get_ACARS_data_path():
    ''' Returns the absolute path of /dva_dispatch_tools/Data/ACARS '''
    # Get the directory of the script
    scriptPath1 = os.path.realpath(__file__)
    # Get the absolute path of the parent directory of the script file
    #pathname = os.path.dirname(sys.argv[0])
    #scriptPath2 = os.path.abspath(pathname)

    # Get the parent directory of the file dva_dispatch_tools/src/ACARS
    parentDir1 = os.path.abspath(os.path.join(scriptPath1, os.pardir))
    # Get the absolute path of dva_dispatch_tools/src
    parentDir2 = os.path.abspath(os.path.join(parentDir1, os.pardir))
    # Get the absolute path of dva_dispatch_tools
    parentDir3 = os.path.abspath(os.path.join(parentDir2, os.pardir))

    # Get the absolute path of dva_dispatch_tools/Data
    dataDir = os.path.join(parentDir3,'Data')
    # Get the absolute path of dva_dispatch_tools/Data/ACARS
    ACARSDataDir = os.path.join(dataDir,'ACARS')
    return ACARSDataDir


def main():
    # Path of ACARS source data (hardcoded for now)
    src_data_dir = "C:\\Users\\coxna\\AppData\\Roaming\\Delta Virtual\\ACARS"

    # Get the path of where all the output data is going
    dest_data_dir = get_ACARS_data_path()
    
    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    Handler = Aircraft_Handler(output_file=os.path.join(dest_data_dir,"aircraft.txt"),print_to_console=False)
    parser.setContentHandler( Handler )
    aircraft_path = os.path.join(src_data_dir,"aircraft.xml")
    parser.parse(aircraft_path)

    # override the default ContextHandler
    Handler = Airport_Handler(output_file=os.path.join(dest_data_dir,"airports.txt"),print_to_console=False)
    parser.setContentHandler( Handler )
    airports_path = os.path.join(src_data_dir,"airports.xml")
    parser.parse(airports_path)


if ( __name__ == "__main__"):
    main()
