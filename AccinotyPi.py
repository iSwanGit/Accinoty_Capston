import threading
import Recorder, Sender, Gyro, GPSLogger
import builtins #for sharing variables

# Making Enum
def enum(**named_values):
    return type('Enum', (), named_values)

##### SHARING VARS #####

# original car num
builtins.CAR_INDEX = '14허 3810' #const

builtins.VIDEO_CNT = 0  #녹화중인 걸 포함한 파일개수
builtins.MAX_VIDEO= 30
builtins.EVENT_CNT= 0
builtins.MAX_EVENT= 50

builtins.RECORDING_TIME = 5

builtins.videoPath= './video/'
builtins.eventPath= './event/'

# Status
builtins.Status = enum(IDLE=0, OCCUR=1, AROUND=2)
builtins.curStatus= builtins.Status.IDLE

# Accident FLAG
builtins.accidentOccured= False

##########################

if __name__ == '__main__':


    # 충격이후 파일 event + 시간 표시 변경

    recorder= Recorder.Recorder()
    gps= GPSLogger.GPSLogger()
    gyro= Gyro.Gyro()
    sender= Sender.Sender()

    gps.start()
    gyro.start()
    recorder.start()
    sender.start()

    lock= threading.Lock() # 필요?



#carIndex= '14허 3810'
#receivedIndex= '69호 5366' #주변의 사고차량 번호
##################