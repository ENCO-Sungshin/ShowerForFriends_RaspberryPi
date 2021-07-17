import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QTime

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

    def timeCount(self):
        global cntTime
        cntTime = cntTime + 1
        
        self.lcd.display(time.strftime('%H:%M:%S', time.gmtime(cntTime)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())