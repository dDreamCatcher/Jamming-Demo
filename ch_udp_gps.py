import socket
import sys
import math
import struct
import time
import serial
import ControlServo


def switchTest(argument):
    switcher ={
        0: "OFFLINE TEST",
        1: "ONLINE TEST"
    }
        # Create the datagram socket
        server_address1 = ('10.42.0.58', 50001)

        # Create the datagram socket - Multicast
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if argument == switcher.keys()[0]:
        #for offline test
        #print(switcher.values()[0])	
        

        #fname example rtk.txt
        fname ='rtk.txt'
        #fpath example /home/genesys/Desktop/Kubra/Jamming-Demo/
        fpath ='/home/genesys/Desktop/Kubra/Jamming-Demo/'
        f = fpath + fname
        # open and read files
        with open(f, 'r') as rtk:
           # while True:
            
            for line in rtk:
                print(line)
                #splitted =filter(None,line.split(' '))[0:5]

                #while True:
                #print >> sys.stderr, '2nd sending: "%s"' % data2.encode('hex_codec')
                time.sleep(1)
                sock.sendto(line, server_address1)
        sock.close()
            
    elif argument == switcher.keys()[1]:
        #for real time test
        #print(switcher.values()[1])
        # open serail port
        #serial_port = '/dev/ttyACM1'
        serial_port = ControlServo.serial_ports()[0] #rtk gps serial port
        baud_rate = 115200 #In arduino, Serial.begin(baud_rate)
        ser = serial.Serial(serial_port, baud_rate)
      
        while True:
            line = ser.readline()
            line = line.decode("utf-8") #ser.readline returns a binary, convert to string
            if line.split(',')[0] == "$GNGGA"    #send only GNGGA info        
                print(line)

                #print >> sys.stderr, '2nd sending: "%s"' % data2.encode('hex_codec')
                time.sleep(0.001)
                sock.sendto(line, server_address1)

        sock.close()

    else:
        print("wrong argument")

if __name__ == '__main__':

    switchTest(0)  # start broadcasting data
    #switchTest(1)


