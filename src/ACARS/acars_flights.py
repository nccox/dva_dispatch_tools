import xml.sax
from bs4 import BeautifulSoup

class ACARS_Handler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.Longitude = ""
        self.Latitude = ""
        self.Heading = ""
        self.Altitude = ""
        self.Name_Raw = ""
        self.Description_Raw = ""
        self.Altitude_Mode = ""
        self.Visibility = ""
        self.Snippet = ""
        self.Orig = ""
        self.Orig_ICAO = ""
        self.Dest = ""
        self.Dest_ICAO = ""
        self.Airspeed = ""
        self.GS = ""
        self.Mach = ""
        self.Fuel_Flow = ""
        self.Vertical_Speed = ""
        self.Network = ""
        self.N1 = ""
        self.N2 = ""
        self.PID = ""
        self.Flight_Number = ""
        self.Name = ""
        self.Aircraft_Type = ""

    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        #print(tag)
        #print(attributes)
        #if tag == "Placemark":
            #print("*****AIRCRAFT*****")
            #title = attributes["name"]
            #print("Name:", name)

   # Call when an elements ends
    def endElement(self, tag):
        #if self.CurrentData == "longitude":
        #    print("longitude:", self.Longitude)
        #elif self.CurrentData == "latitude":
        #    print("latitude:", self.Latitude)
        #if self.CurrentData == "coordinates":
            #print("Latitude:", self.Latitude)
            #print("Longitude:", self.Longitude)
        #elif self.CurrentData == "altitude":
            #print("Altitude:", self.Altitude)
        #elif self.CurrentData == "heading":
            #print("Heading:", self.Heading)
        #elif self.CurrentData == "name":
            #print("Name:", self.Name_Raw)
        #elif self.CurrentData == "description":
            #print("Description (raw):", self.Description_Raw)
            #soup = BeautifulSoup(self.Description_Raw, 'html.parser')
            #print("Description:")
            #print(soup.prettify())
            #print("From:",self.Orig)
            #print("To:",self.Dest)
            #print("Network",self.Network)
            #print("Altitude:",self.Altitude," feet")
            #print("Heading:",self.Heading," degrees")
            #print("Airspeed:",self.Airspeed," kts")
            #print("Ground speed:",self.GS," kts")
            #print("Mach:",self.Mach)
            #print("Vertical Speed:",self.Vertical_Speed," ft/s")
            #print("N1:",self.N1)
            #print("N2:",self.N2)
            #print("Fuel Flow:",self.Fuel_Flow," lbs/hr")
        #elif self.CurrentData == "altitudeMode":
            #print ("Altitude Mode:", self.Altitude_Mode)
        #elif self.CurrentData == "visibility":
            #print ("Visibility:", self.Visibility)
        #elif self.CurrentData == "snippet":
            #print ("Visibility:", self.snippet)
        if tag == "Placemark":
            # Print the data to the csv
            data_list = [self.PID, self.Flight_Number, self.Name, self.Aircraft_Type, self.Orig, self.Orig_ICAO, self.Dest, self.Dest_ICAO, self.Latitude, self.Longitude, self.Altitude, self.Airspeed, self.GS, self.Mach, self.Fuel_Flow, self.Vertical_Speed, self.Network, self.N1, self.N2]
            print("\t".join(data_list))
            # Reset the data
            self.Longitude = ""
            self.Latitude = ""
            self.Heading = ""
            self.Altitude = ""
            self.Name_Raw = ""
            self.Description_Raw = ""
            self.Altitude_Mode = ""
            self.Visibility = ""
            self.Snippet = ""
            self.Orig = ""
            self.Orig_ICAO = ""
            self.Dest = ""
            self.Dest_ICAO = ""
            self.Airspeed = ""
            self.GS = ""
            self.Mach = ""
            self.Fuel_Flow = ""
            self.Vertical_Speed = ""
            self.Network = ""
            self.N1 = ""
            self.N2 = ""
            self.PID = ""
            self.Flight_Number = ""
        self.CurrentData = ""

    # Call when a character is read
    def characters(self, content):
        #if self.CurrentData == "longitude":
            #self.Longitude = content
        #elif self.CurrentData == "latitude":
            #self.Latitude = content
        if self.CurrentData == "coordinates":
            coords = self.parse_coordinates(content)
            self.Latitude = coords[0]
            self.Longitude = coords[1]
        #elif self.CurrentData == "altitude":
            #self.Altitude = content
        #elif self.CurrentData == "heading":
            #self.Heading == content
        elif self.CurrentData == "name":
            self.Name_Raw = content
            if content == "Flight Progress":
                raise end_of_flights()
        elif self.CurrentData == "description":
            self.Description_Raw = content
        elif self.CurrentData == "altitudeMode":
            self.Altitude_Mode = content
        elif self.CurrentData == "visibility":
            self.Visibility = content
        elif self.CurrentData == "snippet":
            self.Snippet == content
            self.process_description(content)

    def parse_coordinates(self,content):
        coords = content.split(',')
        return coords

    def process_description(self,content):
        # Find altitude
        index = content.find("Altitude: ")
        if content != -1:
            alt_str = content[index+10:index+16]
            alt_str = remove_from_string(alt_str,[' ','f','e','t'])
            self.Altitude = alt_str
        # Find altitude AGL (INCOMPLETE)
        index = content.find(' feet AGL')
        if content != -1:
            AGL_str = content[index-12:index-6]
        # Find airspeed
        index = content.find("Speed: ")
        if content != -1:
            str_seg = content[index+7:index+11]
            str_seg = remove_from_string(str_seg,[' ','k','t','s','(',')'])
            self.Airspeed = str_seg
        # Find groundspeed
        index = content.find("GS: ")
        if content != -1:
            str_seg = content[index+4:index+8]
            str_seg = remove_from_string(str_seg,[' ','k','t','s',')'])
            self.GS = str_seg
        # Find Mach
        index = content.find("Mach:")
        if content != -1:
            str_seg = content[index+5:index+10]
            str_seg = remove_from_string(str_seg,[' ','<','/','i','>'])
            self.Mach = str_seg
        # Find heading
        index = content.find("Heading: ")
        if content != -1:
            str_seg = content[index+9:index+12]
            self.Heading = str_seg
        # Find vertical speed
        index = content.find("Verical Speed: ")
        if content != -1:
            str_seg = content[index+15:index+21]
            str_seg = remove_from_string(str_seg,[' ','f','e','t','/','m','i','n'])
            self.Vertical_Speed = str_seg
        # Find N1
        index = content.find("N<sub>1</sub>: ")
        if content != -1:
            str_seg = content[index+15:index+51]
            str_seg = remove_from_string(str_seg,[' ',',','N'])
            self.N1 = str_seg
        # Find N2
        index = content.find("N<sub>2</sub>: ")
        if content != -1:
            str_seg = content[index+15:index+51]
            str_seg = remove_from_string(str_seg,[' ',',','N'])
            self.N2 = str_seg
        # Find fuel flow
        index = content.find("Fuel Flow:")
        if content != -1:
            str_seg = content[index+10:index+201]
            str_seg = remove_from_string(str_seg,[' ','l','b','s','/','h','r','<'])
            self.Fuel_Flow = str_seg
        # Find flaps (INCOMPLETE)
        
        # Find autopilot modes (INCOMPLETE)

        # Find autothrottle modes (INCOMPLETE)

        # Find aircraft type
        index1 = content.find('<span class="sec bld">')
        if index1 != -1:
            index2 = content.find('</span>',beg=index1)
            self.Aircraft_Type = content[index1+22:index2-1]
        # Find origin
        index1 = content.find("From: ")
        if index1 != -1:
            index2 = content.find("<br",beg=index1)
            self.Orig = content[index1+6:index2-1]
            self.Orig_ICAO = self.Origin[-5:-2]
        # Find destination
        index1 = content.find("To: ")
        if index1 != -1:
            index2 = content.find("<br",beg=index1)
            self.Dest = content[index1+4:index2-1]
            self.Dest_ICAO = self.Dest[-5:-2]
        # Find flight sim version
        index1 = content.find("Using ")
        if index1 != -1:
            index2 = content.find("<br",beg=index1)
            self.Sim_Version = content[index1+6:index2-1]
        # Find online network
        if content.find("VATSIM") != -1:
            self.Network = "VATSIM"
        elif content.find("IVAO") != -1:
            self.Network = "IVAO"
        elif content.find("PilotEdge") != -1:
            self.Network = "PilotEdge"

def remove_from_string(string,list_to_remove):
    for item in list_to_remove:
        string = string.replace(item,'')
    return string

class end_of_flights(Exception):
    pass

if ( __name__ == "__main__"):
    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    Handler = ACARS_Handler()
    parser.setContentHandler( Handler )
   
    try:
        parser.parse("acarsFlights.kml")
    except end_of_flights:
        print("End of flights")
