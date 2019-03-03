"""
Converts DVA Acars KMZ file with ACARS data sources to CSV file of all active ACARS flights
"""

import requests
import keyholemarkup_converter as keyhole

def get_ACARS_KMZ_file(filename='acarsMap.kmz'):
    url = 'https://www.deltava.org/acars_map_eprog.ws'
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    #filename2 = 'acarsMap.kml'
    #kmz = ZipFile(filename, 'r')
    #open(filename2, 'wb').write(kmz)
    return r

def convert_KMZ_to_CSV(kmzfile):
    result = keyhole.keyholemarkup2x(kmzfile,output='csv'):
    return result

def main():
    """
    Open the KML. Read the KML. Open a CSV file. Process a coordinate string to be a CSV row.
    """
    kmz_filename = 'acarsMap.kmz';
    kmz = get_ACARS_KMZ_file(filename=kmz_filename)
    csv = convert_KMZ_to_CSV
    
if __name__ == "__main__":
    main()
