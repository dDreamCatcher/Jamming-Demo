import socket
import sys
import time
import struct
# import statistics
import math


# Create UDP socket 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('', 50001)
sock.bind(server_address)
# sock.setblocking(0)
print >>sys.stderr, 'starting up on %s port %s' % server_address  # Default print

updateIdx = 0
counter=0
d=dict()
while True:
    var1 = time.time()
    data, address = sock.recvfrom(1024)

    if data:
        #print "Received data: %s" % data.encode('hex_codec')
        print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
        #print "Received data: %s" % data.encode('hex_codec')
        print "Received data: %s" % data

        if data=="\n":
            if d.get('Fix')=='1':
                print("GPS locked")
                #do calculation
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
            var2 = time.time()
            updateIdx = updateIdx + 1
            #print "update %s - time: %.2f ms" % (str(updateIdx), round(1000.0*(var2-var1),2))

    else:
        print >> sys.stderr, 'Done', address
        break


             
# Clean up the connection
sock.close()


