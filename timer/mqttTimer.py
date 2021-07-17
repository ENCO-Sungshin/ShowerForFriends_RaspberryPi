import time
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT, MESSAGE, TOPIC, and RANGE
ENDPOINT = "endpoint"
CLIENT_ID = "RaspberryPi"
PATH_TO_CERT = "/home/pi/Desktop/Cert/"
PATH_TO_KEY = "/home/pi/Desktop/Cert/"
PATH_TO_ROOT = "/home/pi/Desktop/Cert/"
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

# timeCnt Initialize
timeCnt = 0
timeStr = ""

for i in range (RANGE):
    timeCnt = timeCnt + 1
    print(timeCnt)
    timeStr = str(timeCnt)
    # data = "{} [{}]".format(Time, timeCnt) => Time[timeCnt]

    try:
        message = { "DisplayNumber": "2", "Time" : "30"}
        myAWSIoTMQTTClient.publish(TOPIC, json.dumps(message), 0)
        print("Published: '" + json.dumps(message) + "' to the topic: " + "'device/TimeData'")
    except Exception as ex:
        print('e', ex)    


print('Publish End')
myAWSIoTMQTTClient.disconnect()
