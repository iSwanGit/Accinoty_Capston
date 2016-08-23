import threading
from record_video import Recorder
import Sender, ExternalLogger


# all different original values
CAR_INDEX = '14허 3810' #const
VIDEO_CNT = 0

if __name__ == '__main__':
    recorder= Recorder()

#### TEST DATA ####
latitude= 36.0
longitutde= 126.0
curStatus= Status.IDLE
carIndex= '14허 3810'
receivedIndex= '69호 5366' #주변의 사고차량 번호
##################