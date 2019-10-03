"""import pynmea2 can be also used to parse nmea sentence"""

def parseGNGGA(sentence):
    parse = { 
        'Time': '', 
        'Latitude': '', 
        'Longitude': '', 
        'Altitude': ''
    }

    new_line =sentence.split(',')
    parse['Time'] = time(new_line[1])
    parse['Latitude'] = lat_dir(new_line[3])+latitude(new_line[2])
    parse['Longitude'] = lon_dir(new_line[5])+longitude(new_line[4])
    parse['Altitude'] = altitude(new_line[9],new_line[11])
    return parse

def time(t):
    splitted = t.split('.')
    new_t = [splitted[0][i:i+2] for i in range(0,len(splitted[0])-1,2)]
    return new_t[0]+':'+ new_t[1]+':'+new_t[2]+'.'+splitted[1]+'0'

def lat_dir(d_lat):
    return '-' if d_lat == 'S' else ''

def lon_dir(d_lon):
    return '-' if d_lon == 'W' else ''

def latitude(lat):
    #latitude is in format DDMM.MMMMM
    DD = int(float(lat)/100) 
    MM = float(lat) - DD * 100
    return str(DD + MM/60) 

def longitude(lon):
    #longtitude is in format DDMM.MMMMM
    DD = int(float(lon)/100) 
    MM = float(lon) - DD * 100
    return str(DD + MM/60)

def altitude(alt, geo):
    
    return float(alt)+float(geo)

"""
if __name__ == '__main__':
	# test
	print(parseGNGGA('$GNGGA,213659.20,4220.3190747,N,07105.1751820,W,1,17,0.6,16.686,M,-28.724,M,0.0,*5F'))
print(parseGNGGA('$GNGGA,213658.20,4220.3193477,N,07105.1753880,W,1,17,0.6,17.757,M,-28.724,M,0.0,*59'))
"""

