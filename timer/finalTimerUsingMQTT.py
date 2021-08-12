import sys
import time
import datetime as dt
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QTime

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a3skt3bylhqk7y-ats.iot.ap-northeast-2.amazonaws.com"
CLIENT_ID = "RaspberryPi"
PATH_TO_CERT = "/home/pi/Desktop/Cert/device.pem.crt"
PATH_TO_KEY = "/home/pi/Desktop/Cert/private.pem.key"
PATH_TO_ROOT = "/home/pi/Desktop/Cert/AmazonRootCA1.pem"
TOPIC = "device/TimeData"
RANGE = 1
myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)

# Function to make timer start
def getPower_state(powerJson):
    print("Printing current power status")
    global currPower
    currPower = powerJson['power']
    print(currPower) # to check data
    
    if currPower == True: #display ON
        print("Display ON")
        myWindow = MyWindow()
        myWindow.show()
        MyWindow.onStartButtonClicked()
    
    elif currPower == False:
        print("Display OFF")
        sys.exit(app.exec_()) 
    

# Function to process the MQTT message and takes necessary action 
def getPower_message(awsIOTMQTTClient, userData, message):
    print("Received Message")
    print(message)
    powerJson = json.loads(message.payload)
    print(powerJson)
    getPower_state(powerJson)
    # logger.info(powerJson['value'])
    # change_fan_state(fanJson)

myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe("display_power", 0, getPower_message)
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
            message = { "DisplayNumber": "99", "Time" : cntTime, "date" : dt.datetime.now()}
            myAWSIoTMQTTClient.publish(TOPIC, json.dumps(message), 0)
            print("Published: '" + json.dumps(message) + "' to the topic: " + "'device/TimeData'")
        except Exception as ex:
            print('eeeeeeeeeeeeeeee', ex)

    def timeCount(self):
        global cntTime
        cntTime = cntTime + 1
        self.lcd.display(time.strftime('%H:%M:%S', time.gmtime(cntTime)))

# main function
if __name__ == "__main__":
    while True:
        time.sleep(1)

# timeCnt Initialize
timeCnt = 0
timeStr = ""

print('Publish End')
myAWSIoTMQTTClient.disconnect()

