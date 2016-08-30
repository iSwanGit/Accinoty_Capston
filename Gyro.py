import serial
import threading
import builtins

class Gyro(threading.Thread):
    # var port : connected port into arduino
    # port number 9600
    port = "/dev/ttyACM0"
    serialPipe = serial.Serial(port, 9600)  # Thread 1 : Receive serial output by Arduino

    def __init__(self):
        threading.Thread.__init__(self)

    # Thread 1 : Receive serial output by Arduino
    def receive_serial(self):

        # reading serial println
        if (self.serialPipe.inWaiting() > 0):
            input = self.serialPipe.readline().decode()

            #if (input[:-2] == 'accident'):
            #    return True
            #else:
            return False

    def run(self):
        while True:
            if self.receive_serial() is True:
                builtins.accidentOccured= True
                # ->False 는 Sender에서