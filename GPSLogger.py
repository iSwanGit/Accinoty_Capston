import serial
import threading
import MyLocation
import time

class GPSLogger(threading.Thread):
    location= MyLocation.MyLocation()
    # var port : connected port into arduino
    # port number 9600
    port = "/dev/ttyACM1"
    serialPipe= None

    def __init__(self):
        threading.Thread.__init__(self)

        while True:
            try:
                self.serialPipe = serial.Serial(self.port, 9600)  # Thread 1 : Receive serial output by Arduino
            except Exception as e:
                print('gpslogger error')
                time.sleep(10)
                continue
            finally:
                break

    # Thread 1 : Receive serial output by Arduino
    def receive_serial(self):
        # reading serial println
        self.location.latitude= 37.239644838579245
        self.location.longitude= 127.08324987629406
        """
        if (self.serialPipe.inWaiting() > 0):
            input1 = self.serialPipe.readline().decode()[:-2]
            input2 = self.serialPipe.readline().decode()[:-2]

            if input1.startswith('latitude'):
                self.location.latitude= input1
                self.location.longitude= input2
            else:
                self.location.latitude = input2
                self.location.longitude = input1
        """
    def run(self):
        while True:
            self.receive_serial()
