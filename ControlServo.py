from pyfirmata import Arduino
from pyfirmata import SERVO
from time import sleep
import sys
import glob
import serial

# Setting up the Arduino board
#port = 'COM5'   # win
#port = '/dev/ttyACM0'  # linux
ports = []
boards = []

# list of serial ports available
def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith ('linux'):
        temp_list = glob.glob ('/dev/tty[A-Za-z]*')

    result = []
    for a_port in temp_list:

        try:
            s = serial.Serial(a_port)
            s.close()
            result.append(a_port)
        except serial.SerialException:
            pass

    return result


def setupArduino(pin_El, pin_Az, mode=SERVO):
	i=0
	#setup serial ports
	for p in serial_ports():
		ports.append(p)
		boards.append(Arduino(p))
		boards[i].digital[pin_El].mode = mode  # Set mode of pins 8 & 9 as SERVO
		boards[i].digital[pin_Az].mode = mode
		sleep(2)	# Need to give some time to pyFirmata and Arduino to synchronize
		print(ports)
		print(boards)
		i +=1
	return boards
	

	
# Custom angle to set Servo motor angle
def setServoAngle(board, pin, angle):
	board.digital[pin].write(angle)
    	sleep(0.015)

	

if __name__ == '__main__':
	for b in setupArduino(8,9)
		setServoAngle(b,8,30)
		setServoAngle(b,9,30)


