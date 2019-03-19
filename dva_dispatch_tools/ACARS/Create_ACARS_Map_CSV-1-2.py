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
    result = keyhole.keyholemarkup2x(kmzfile,output='csv')
    print("4")
    print(result)
    return result

def main():
    #kmz_filename = 'D:\\coxna\\Documents\\Flight Sim\\Dispatch\\dva_dispatch_tools\\data\\ACARS\\acarsMap.kmz';
    kmz_filename = 'acarsMap.kmz';
    kmz = get_ACARS_KMZ_file(filename=kmz_filename)
    csv = convert_KMZ_to_CSV(kmz_filename)
    
if __name__ == "__main__":
    main()
