import time
import picamera

class Recorder:
    VIDEO_CNT= 1
    def __init__(self, count= None):
        if count is not None:
            self.VIDEO_CNT= count
        else:
            self.VIDEO_CNT= 1

    def Run(self):
        with picamera.PiCamera() as camera:
            camera.start_preview()
            while True:
                camera.start_recording('video' + str(VIDEO_CNT) + '.h264')
                camera.wait_recording(5)
                camera.stop_recording()

                if VIDEO_CNT <= 5:
                    VIDEO_CNT = VIDEO_CNT + 1
                else:
                    VIDEO_CNT = 1

            camera.stop_preview()
            camera.close()



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