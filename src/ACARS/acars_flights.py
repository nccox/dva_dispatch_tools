import xml.sax
from bs4 import BeautifulSoup

class ACARS_Handler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.X = ""
        self.Y = ""
        self.Name_Raw = ""
        self.Description_Raw = ""
        self.Altitude_Mode = ""
        self.Visibility = ""
        self.Snippet = ""

    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        #print(tag)
        #print(attributes)
        if tag == "Placemark":
            print("*****AIRCRAFT*****")
            #title = attributes["name"]
            #print("Name:", name)

   # Call when an elements ends
    def endElement(self, tag):
        if self.CurrentData == "longitude":
            print("longitude:", self.Longitude)
        elif self.CurrentData == "latitude":
            print("latitude:", self.Latitude)
        elif self.CurrentData == "name":
            print("Name:", self.Name_Raw)
        elif self.CurrentData == "description":
            print("Description (raw):", self.Description_Raw)
            soup = BeautifulSoup(self.Description_Raw, 'html.parser')
            #print("Description:")
            #print(soup.prettify())
        elif self.CurrentData == "altitudeMode":
            print ("Altitude Mode:", self.Altitude_Mode)
        elif self.CurrentData == "visibility":
            print ("Visibility:", self.Visibility)
        elif self.CurrentData == "snippet":
            print ("Visibility:", self.snippet)
        self.CurrentData = ""

    # Call when a character is read
    def characters(self, content):
        if self.CurrentData == "longitude":
            self.Longitude = content
        elif self.CurrentData == "latitude":
            self.Latitude = content
        elif self.CurrentData == "altitude":
            self.Altitude = content
        elif self.CurrentData == "heading":
            self.Heading == content
        elif self.CurrentData == "name":
            self.Name_Raw = content
        elif self.CurrentData == "description":
            self.Description_Raw = content
        elif self.CurrentData == "altitudeMode":
            self.Altitude_Mode = content
        elif self.CurrentData == "visibility":
            self.Visibility = content
        elif self.CurrentData == "snippet":
            self.Snippet == content


if ( __name__ == "__main__"):
   
   # create an XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)

   # override the default ContextHandler
   Handler = ACARS_Handler()
   parser.setContentHandler( Handler )
   
   parser.parse("acarsFlights.kml")
