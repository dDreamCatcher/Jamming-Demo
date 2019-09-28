import socket
import sys
import time
import struct
# import statistics
import math
import gps_service
import ControlServo



def startMain(argument):
	pin_El, pin_Az = 8,9

	# Create UDP socket 
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_address = ('', 50001)
	sock.bind(server_address)
	boards = ControlServo.setupArduino(pin_El, pin_Az)
	keys = ['Date', 'Time', 'Langtitude', 'Longtitude', 'Altitude']	
	
	# sock.setblocking(0)
	print >>sys.stderr, 'starting up on %s port %s' % server_address  # Default print


	d_dict=dict()
	while True:
	    #var1 = time.time()
	    data, address = sock.recvfrom(1024)

	    if data:
		#print "Received data: %s" % data.encode('hex_codec')
		print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
		#print "Received data: %s" % data.encode('hex_codec')
		print "Received data: %s" % data
		
		#gps data from arduino serial
		if argument == 'Arduino':

			if data=="\n":
			    if d_dict.get('Fix')=='1':
				print("GPS locked")
				ServoControl(d_dict, argument)
				d_dict.clear()
			elif ": " not in data:
			    continue
			else:
			    line = data.split(': ')
			    key, value = line[0], line[1].strip()
			    if key == 'Location':
				value = tuple(value.split(', '))
			    d_dict.update({key: value})
			    print "Dict: ", d_dict
		#read from rtk data file offline or real time
		elif argument == 'RTK':
			new_line =filter(None,line.split(' '))[0:5]
			for k in range(len(keys)):
				d_dict[keys[k]] = new_line[k]
			ServoControl(d_dict, argument)
			d_dict.clear()
			
		else:
			print("Wrong Argument")
		  
	    else:
		print >> sys.stderr, 'Done', address
		break
		     
	# Clean up the connection
	sock.close()


# control servo angle based on gps coor calculation
def ServoControl(d, argument):
	
	if argument == 'Arduino':
		pt = gps_service.GPSPoint(
			float(d.get("Location")[0]),
			float(d.get("Location")[1]),
			float(d.get("Altitude"))
		)
	elif argument == 'RTK':
		pt = gps_service.GPSPoint(
			float(d.get("Langtitude")),
			float(d.get("Longtitude")),
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
	# write angles to servos
	i =0
	keys_b = sorted(b_angles.keys())
	keys_e = sorted(e_angles.keys())
	for a in boards:
		ControlServo.setServoAngle(a,pin_El,e_angles[keys_e[i]][0])
		ControlServo.setServoAngle(a,pin_Az,b_angles[keys_b[i]])
		i +=1

if __name__ == '__main__':
	# argument: Arduino or RTK
	startMain('RTK')


