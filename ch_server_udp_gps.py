import socket
import sys
import time
import struct
# import statistics
import math
import gps_service

# Create UDP socket 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('', 50001)
sock.bind(server_address)
# sock.setblocking(0)
print >>sys.stderr, 'starting up on %s port %s' % server_address  # Default print


d=dict()
while True:
    #var1 = time.time()
    data, address = sock.recvfrom(1024)

    if data:
        #print "Received data: %s" % data.encode('hex_codec')
        print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
        #print "Received data: %s" % data.encode('hex_codec')
        print "Received data: %s" % data

        if data=="\n":
            if d.get('Fix')=='1':
                print("GPS locked")
		pt = gps_service.GPSPoint(
			float(d.get("Location")[0]),
			float(d.get("Location")[1]),
			float(d.get("Altitude"))
		)

                #do calculation
		b_angles = dict()
		e_angles = dict()
		for jAntenna in gps_service.JAMMING_ANTENNAS.keys():
			
			b_angles.update(
				{jAntenna: 
					gps_service.JAMMING_ANTENNAS[jAntenna].bearingAngle(pt)})
			e_angles.update(
				{jAntenna: 
					gps_service.JAMMING_ANTENNAS[jAntenna].elevationAngle(pt)})
                d.clear()
        elif ": " not in data:
            continue
        else:
            line = data.split(': ')
            key, value = line[0], line[1].strip()
            if key == 'Location':
                value = tuple(value.split(', '))
            d.update({key: value})
            print "Dict: ", d
          
    else:
        print >> sys.stderr, 'Done', address
        break


             
# Clean up the connection
sock.close()


