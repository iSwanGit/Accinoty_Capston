# -*- coding: utf8 -*-
import sys, random, time, os, threading
import socket
import json
import MyLocation
import builtins #for sharing variables


class Sender(threading.Thread):
    #global VIDEO_CNT
    # const data
    HOST = "accinoty.pendual.net"
    PORT = 8088
    BUFSIZE = 1024
    ADDR = (HOST, PORT)

    mySocket= None
    location= MyLocation()

    triggeredCount= 0   #사고발생 혹은 사고수신시 녹화완료된 파일

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
        if self.location.latitude is None:  #lat long 둘중 하나만 없어도
            return
        jsonObj= {
            'flag': builtins.curStatus,
            'car_index': builtins.CAR_INDEX,
            'latitude': self.location.latitude,
            'longitude': self.location.longitutde
        }
        jsonString= json.dumps(jsonObj)
        self.mySocket.send(jsonString.encode())



    def SetTrigger(self, type):
        self.triggeredCount= builtins.VIDEO_CNT  #trigger video count
        builtins.curStatus= type
        builtins.accidentOccured= False #curStatus 반영했으니 다음 충격을 기다림


    def ResetTrigger(self):
        self.triggeredCount= 0
        builtins.curStatus= builtins.curStatus.IDLE

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
        if self.triggeredCount != 0:
            for filename in os.listdir('./video'):
                if filename.startswith('video_'+self.triggeredCount):
                    os.rename(filename, '../event/event_' + filename[6:])
                    fname= 'event_'+filename[6:]
                    break
            fsize= os.path.getsize('./event/'+fname)
            self.mySocket.send(str(fsize).encode())
            self.mySocket.sendfile('./event/'+fname)    # first file

        while self.triggeredCount == builtins.VIDEO_CNT:
            time.sleep(5)   # 바뀔때까지 기다림
        for filename in os.listdir('./video'):
            if filename.startswith('video_' + builtins.VIDEO_CNT):
                os.rename(filename, '../event/event_' + filename[6:])
                fname = 'event_' + filename[6:]
                break
        fsize = os.path.getsize('./event/' + fname)
        self.mySocket.send(str(fsize).encode())
        self.mySocket.sendfile('./event/' + fname)  # second/first file


            # 사고차는 전파일 촬영중파일 두개
            # 주변차는 전파일 하나 / 없으면 녹화중인 파일 완료 후 전송
        #일단은 이벤트는 무한정 녹화.  TODO: 용량이 꽉찰 경우에 대비



# TODO: socket, json?multisend?, thread

