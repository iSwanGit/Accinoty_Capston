import time, threading
import picamera
import builtins
# Thread Lock과 같은 일환으로 완료된 VIDEO_CNT를 반영
class Recorder(threading.Thread):
    CURRENT_CNT = 0  # next count
    RECORDING_TIME = 5

    camera = picamera.PiCamera()



    # Constructor
    def __init__(self, count= None):
        if count is not None:
            builtins.VIDEO_CNT= count
        else:
            builtins.VIDEO_CNT= 0
        self.serialFromArduino.flushInput()

    def __del__(self):
        self.camera_stop()



    # Thread 2 : Capture to PiCamera
    def camera_run(self):
        #global VIDEO_CNT  # recording completed
        #global MAX_COUNT
        self.camera.start_preview()
        while True:
            if builtins.VIDEO_CNT < builtins.MAX_COUNT:
                self.CURRENT_CNT = builtins.VIDEO_CNT + 1
            else:
                self.CURRENT_CNT = 1
            tm = time.strftime('%y%m%d_%H%M%S', time.localtime())
            self.camera.start_recording('./video/'+'video_' + str(self.CURRENT_CNT) +'_' + tm + '.h264')
            self.camera.wait_recording(self.RECORDING_TIME)
            self.camera.stop_recording()
            builtins.VIDEO_CNT = self.CURRENT_CNT


    # Stop camera
    def camera_stop(self):
        self.camera.stop_preview()
        self.camera.stop_recording()
        self.camera.close()

        # need additional code for sending video

    # Thread run
    def run(self):
        self.camera_run()



"""

아두이노 시리얼통신 ->현규 // 한 파이에 두 아두이노 필요할듯
충격 ->GPS신호 요
JSON
파일보낼때는 사이즈먼저 (C++)

enum
0: gps (normal idle)
1: accident occur
2: accident around

"""