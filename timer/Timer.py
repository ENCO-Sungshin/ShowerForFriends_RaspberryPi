import sys
import time
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QTime

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a3skt3bylhqk7y-ats.iot.ap-northeast-2.amazonaws.com"
CLIENT_ID = "RaspberryPi"
PATH_TO_CERT = "/home/pi/Desktop/Cert/da928ed9d2-certificate.pem.crt"
PATH_TO_KEY = "/home/pi/Desktop/Cert/da928ed9d2-private.pem.key"
PATH_TO_ROOT = "/home/pi/Desktop/Cert/AmazonRootCA1.pem"
# MESSAGE = "Hello World"
TOPIC = "device/TimeData"
RANGE = 1


myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)

# myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  
# myAWSIoTMQTTClient.configureDrainingFrequency(2)  
# myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10) 
# myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  

myAWSIoTMQTTClient.connect()
print('Begin Publish')

cntTime = 0

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timeCount)
        self.setWindowTitle('QTimer')
        self.setGeometry(100, 100, 600, 280)
        currentTime = "00:00:00"

        # GUI 
        layout = QVBoxLayout()
 
        self.lcd = QLCDNumber()
        self.lcd.display('')
        self.lcd.setDigitCount(8)
        subLayout = QHBoxLayout()
        
        self.btnStart = QPushButton("start")
        self.btnStart.clicked.connect(self.onStartButtonClicked)
 
        self.btnStop = QPushButton("stop")
        self.btnStop.clicked.connect(self.onStopButtonClicked)
 
        layout.addWidget(self.lcd)
        
        subLayout.addWidget(self.btnStart)
        subLayout.addWidget(self.btnStop)
        layout.addLayout(subLayout)
 
        self.btnStop.setEnabled(False)
        self.setLayout(layout)     

        self.lcd.display(currentTime)

    def onStartButtonClicked(self):
        self.timer.start()
        self.btnStop.setEnabled(True)
        self.btnStart.setEnabled(False)

    def onStopButtonClicked(self):
        self.timer.stop()
        self.btnStop.setEnabled(False)
        self.btnStart.setEnabled(True)
        try:
            message = { "DisplayNumber": "99", "Time" : cntTime}
            myAWSIoTMQTTClient.publish(TOPIC, json.dumps(message), 0)
            print("Published: '" + json.dumps(message) + "' to the topic: " + "'device/TimeData'")
        except Exception as ex:
            print('eeeeeeeeeeeeeeee', ex)

    def timeCount(self):
        global cntTime
        cntTime = cntTime + 1
        
        self.lcd.display(time.strftime('%H:%M:%S', time.gmtime(cntTime)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())

# timeCnt Initialize
timeCnt = 0
timeStr = ""


# for i in range (RANGE):
#     timeCnt = timeCnt + 1
#     print(timeCnt)
#     timeStr = str(timeCnt)
#     # data = "{} [{}]".format(Time, timeCnt) => Time[timeCnt]

#     try:
#         message = { "DisplayNumber": "99", "Time" : "30"}
#         myAWSIoTMQTTClient.publish(TOPIC, json.dumps(message), 0)
#         print("Published: '" + json.dumps(message) + "' to the topic: " + "'device/TimeData'")
#     except Exception as ex:
#         print('eeeeeeeeeeeeeeee', ex)

print('Publish End')
myAWSIoTMQTTClient.disconnect()
