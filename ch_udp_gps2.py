import socket
import sys
import math
import struct
import time
import serial

# open serail port
serial_port = '/dev/ttyACM1';
baud_rate = 115200; #In arduino, Serial.begin(baud_rate)
ser = serial.Serial(serial_port, baud_rate)

# Create the datagram socket
server_address1 = ('10.42.0.59', 50001)

# Create the datagram socket - Multicast
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    line = ser.readline();
    line = line.decode("utf-8") #ser.readline returns a binary, convert to string
    print(line);

    #print >> sys.stderr, '2nd sending: "%s"' % data2.encode('hex_codec')
    time.sleep(0.001)
    sock1.sendto(line, server_address1)

sock1.close()
