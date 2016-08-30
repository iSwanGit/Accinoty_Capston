import time, threading, os
import picamera
import builtins
# Thread Lock과 같은 일환으로 완료된 VIDEO_CNT를 반영
class Recorder(threading.Thread):
    CURRENT_CNT = 0  # next count


    camera = picamera.PiCamera()




    # Constructor
    def __init__(self):
        threading.Thread.__init__(self)
        builtins.VIDEO_CNT= len(os.listdir(builtins.videoPath))
        builtins.EVENT_CNT= len(os.listdir(builtins.eventPath))

    def __del__(self):
        self.camera_stop()



    # Thread 2 : Capture to PiCamera
    def camera_run(self):
        #global VIDEO_CNT  # recording completed
        #global MAX_COUNT
        self.camera.start_preview()
        while True:

            if builtins.VIDEO_CNT < builtins.MAX_VIDEO:
                builtins.VIDEO_CNT += 1
                #self.CURRENT_CNT = builtins.VIDEO_CNT + 1
            else:
                os.remove(builtins.videoPath+sorted(os.listdir(builtins.videoPath))[0])
                #self.CURRENT_CNT = 1
            tm = time.strftime('%y%m%d_%H%M%S', time.localtime())
            print('recording start')
            self.camera.start_recording(builtins.videoPath+'video_' + tm + '.h264')
            self.camera.wait_recording(builtins.RECORDING_TIME)
            self.camera.stop_recording()
            print('recording stop')
            #builtins.VIDEO_CNT = self.CURRENT_CNT


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