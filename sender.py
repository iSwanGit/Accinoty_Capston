# -*- coding: utf8 -*-
import sys, random, time, os, threading
import socket
import json
import builtins #for sharing variables
import MyLocation

class Sender(threading.Thread):
    #global VIDEO_CNT
    # const data
    HOST = "accinoty.pendual.net"
    PORT = 8088
    BUFSIZE = 1024
    ADDR = (HOST, PORT)

    mySocket= None
    location= MyLocation.MyLocation()

    #triggeredCount= 0   #사고발생 혹은 사고수신시 녹화완료된 파일
    triggeredPath= None
    nextPath= None

    def __init__(self):
        threading.Thread.__init__(self)

    def __del__(self):
        jsonEnd= { 'flag': 6 }
        self.mySocket.send(json.dumps(jsonEnd).encode())
        self.mySocket.close()

    def run(self):
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.mySocket.connect(self.ADDR)
            print('Connected to server successfully')
        except Exception as e:
            print('Cannot connect server')
            sys.exit()

        returnJSON= None
        returnJSONParsed= 0
        random.seed()
        while True:
            if returnJSONParsed == builtins.Status.IDLE:
                time.sleep((4700+random.randint(0, 500))/100)
                self.SendCycle()
            elif builtins.accidentOccured is True:
                self.SetTrigger(builtins.Status.OCCUR)
                self.SendAccidentOccur()
            else:       #logic check
                self.SetTrigger(builtins.Status.AROUND)
                self.SendAccidentAround(returnJSONParsed)
            self.ResetTrigger()
            returnJSON= json.loads(self.mySocket.recv(self.BUFSIZE).decode())
            returnJSONParsed= returnJSON['ack']


    def SendCycle(self):
        #global curStatus, CAR_INDEX
        #if self.location.latitude is None and self.location.longitude is None:  #lat long 둘중 하나만 없어도
        #    return
        print(self.location.latitude)
        print(self.location.longitude)
        jsonObj= {
            'flag': builtins.curStatus,
            'car_index': builtins.CAR_INDEX,
            'latitude': self.location.latitude,
            'longitude': self.location.longitutde
        }
        jsonString= json.dumps(jsonObj)
        self.mySocket.send(jsonString.encode())



    def SetTrigger(self, type):
        #self.triggeredCount= builtins.VIDEO_CNT  #trigger video count
        #처음 녹화중에 대한 예외처리
        while True:
            if len(os.listdir(builtins.videoPath)) == 1:
                time.sleep(5)
            else:
                break
        self.triggeredPath= sorted(os.listdir(builtins.videoPath))[-2]
        self.nextPath= sorted(os.listdir(builtins.videoPath))[-1]
        builtins.curStatus= type
        builtins.accidentOccured= False #curStatus 반영했으니 다음 충격을 기다림


    def ResetTrigger(self):
        #self.triggeredCount= 0
        self.triggeredPath= None
        builtins.curStatus= builtins.Status.IDLE

    def SendAccidentOccur(self):
        if self.location.latitude is None:
            return
        jsonObj = {
            'flag': builtins.Status.OCCUR,
            'car_index': builtins.CAR_INDEX,
            'latitude': self.location.latitude,
            'longitude': self.location.longitutde
        }
        jsonString= json.dumps(jsonObj)
        self.mySocket.send(jsonString.encode())
        self.SendFile()

    def SendAccidentAround(self, receivedIndex):
        if self.location.latitude is None:
            return
        jsonObj = {
            'flag': builtins.Status.AROUND,
            'car_index': builtins.CAR_INDEX,
            'accident_index': receivedIndex,     # 사고번호
            'latitude': self.location.latitude,
            'longitude': self.location.longitutde
        }
        jsonString= json.dumps(jsonObj)
        self.mySocket.send(jsonString.encode())
        self.SendFile()

    def SendFile(self):
        #curCompletedCnt= builtins.VIDEO_CNT
        fname= ''
        if builtins.curStatus == builtins.Status.OCCUR:  #event 로 변경
            os.rename(builtins.videoPath + self.triggeredPath, builtins.eventPath + 'event_'+self.triggeredPath[6:])
            fname= sorted(os.listdir(builtins.eventPath))[-1]
            fsize= os.path.getsize(builtins.eventPath+fname)
            self.mySocket.send(str(fsize).encode())
            self.mySocket.sendfile(builtins.eventPath+fname)    # first file

        while self.nextPath == sorted(os.listdir(builtins.videoPath))[-1]:      # 새로운 파일이 기록되기 전에는
            time.sleep(5)   # 바뀔때까지 기다림

        os.rename(builtins.videoPath + self.nextPath, builtins.eventPath + 'event_'+self.nextPath[6:])
        fname= sorted(os.listdir(builtins.eventPath))[-1]
        fsize= os.path.getsize(builtins.eventPath+fname)
        self.mySocket.send(str(fsize).encode())
        self.mySocket.sendfile(builtins.eventPath + fname)  # second/first file


            # 사고차는 전파일 촬영중파일 두개
            # 주변차는 전파일 하나 / 없으면 녹화중인 파일 완료 후 전송
        #일단은 이벤트는 무한정 녹화.  TODO: 용량이 꽉찰 경우에 대비



# TODO: socket, json?multisend?, thread

