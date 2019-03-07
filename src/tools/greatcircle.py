#-----------------------------------------------------------------------
# greatcircle.py
#-----------------------------------------------------------------------

#import stdio
import sys
import math

def gcdist(point1,point2,unit='NM'):
    '''
    Calculates great circle distance.
    Inputs:
        point1: 2-value list or tuple of latitude and longitude in degrees
        point2: 2-value list or tuple of latitude and longitude in degrees
        unit (optional, default NM for nautical miles).  Defines unit for
            returned value.  Acceptable options include:
                - "NM" - nautical miles (default)
                - "km" - kilometers
                - "m" - meters
                - "ft" - feet
                - "mi" - statuate miles
    '''
    x1 = float(point1[0])
    y1 = float(point1[1])
    x2 = float(point2[0])
    y2 = float(point2[1])

    # The following formulas assume that angles are expressed in radians.
    # So convert to radians.

    x1 = math.radians(x1)
    y1 = math.radians(y1)
    x2 = math.radians(x2)
    y2 = math.radians(y2)

    # Compute using the law of cosines.

    # Great circle distance in radians
    angle1 = math.acos(math.sin(x1) * math.sin(x2) \
             + math.cos(x1) * math.cos(x2) * math.cos(y1 - y2))

    # Convert back to degrees.
    angle1 = math.degrees(angle1)

    # Each degree on a great circle of Earth is 60 nautical miles.
    distance1 = 60.0 * angle1

    # Compute using the Haversine formula.

    a = math.sin((x2-x1)/2.0) ** 2.0 \
        + (math.cos(x1) * math.cos(x2) * (math.sin((y2-y1)/2.0) ** 2.0))

    # Great circle distance in radians
    angle2 = 2.0 * math.asin(min(1.0, math.sqrt(a)))

    # Convert back to degrees.
    angle2 = math.degrees(angle2)

    # Each degree on a great circle of Earth is 60 nautical miles.
    distance2 = 60.0 * angle2

    if unit == 'NM':
        distance = distance2
    elif unit == 'm':
        # Convert from nautical miles to meters
        distance = distance2*1852
    elif unit == 'km':
        # Convert from nautical miles to kilometers
        distance = distance2*1.852
    elif unit == 'ft':
        # Convert from nautical miles to feet
        distance = distance2*6076.12
    elif unit == 'mi':
        # Convert from nautical miles to statuate miles
        distance = distance2*1.15078
    else:
        # If input for units was unrecognized or unsupported
        throw(ValueError)
    return distance


def unit_conversion(value,input_units,output_units):
    pass


if ( __name__ == "__main__"):
    # Accept float command-line arguments x1, y1, x2, and y2: the latitude
    # and longitude, in degrees, of two points on the earth. Compute and
    # write to standard output the great circle distance (in nautical
    # miles) between those two points.

    x1 = float(sys.argv[1])
    y1 = float(sys.argv[2])
    x2 = float(sys.argv[3])
    y2 = float(sys.argv[4])

    point1 = (x1,y1)
    point2 = (x2,y2)

    distance = gcdist(point1,point2)

    print(str(distance) + ' nautical miles')
#    stdio.writeln(str(distance) + ' nautical miles')
