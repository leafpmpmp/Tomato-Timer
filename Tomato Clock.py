import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

button_state = 0
time_state = 0
count = 0
current_time = "00:00"

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 600, 800, 1200)
        self.setWindowTitle("Tomato Clock")

        self.title = QLabel("Tomato Clock", self)
        self.title.setGeometry(100, 10, 600, 100)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Arial", 32))

        self.time = QLabel("00:00", self)
        self.time.setGeometry(350, 700, 100, 50)
        self.time.setAlignment(Qt.AlignCenter)
        self.time.setFont(QFont("Arial", 20))

        self.start = QPushButton("START", self)
        self.start.setGeometry(325, 800, 150, 60)
        self.start.setFont(QFont("Arial", 20))
        self.start.clicked.connect(self.onStartClick)

        self.reset = QPushButton("RESET", self)
        self.reset.setGeometry(350, 900, 100, 40)
        self.start.setFont(QFont("Arial", 14))
        self.reset.clicked.connect(self.onResetClick)

    def paintEvent(self, event):
        alen = -1*count*0.2*16
        qp = QPainter()
        qp.begin(self)
        
        if(time_state == 0):
            qp.setBrush(Qt.red)
            qp.setPen(QPen(QColor("#ff0000"), 3))
        else:
            qp.setBrush(Qt.cyan)
            qp.setPen(QPen(QColor("#00ffff"), 3))
        qp.drawPie(QRect(250, 250, 300, 300), 90*16, int(alen))
        qp.setPen(QPen(QColor("#000000"), 6))
        qp.drawArc(QRect(247, 247, 306, 306), 0, 360*16)
        qp.end()

    def onStartClick(self): # START/STOP button
        global button_state
        if(button_state == 0):
            self.start.setText("STOP")
            button_state = 1
            timer.start(1000)
        else:
            self.start.setText("START")
            button_state = 0
            timer.stop()

    def onResetClick(self): # RESET button
        global button_state, count, time_state
        self.start.setText("START")
        timer.stop()
        button_state = 0
        rstTimer.start(1)

app = QApplication(sys.argv)
window = Window()
window.show()

def tic(): # counter
    global count, time_state
    count += 1
    calcTime()
    if(count == 1500):
        time_state = 1
    elif(count == 1800):
        timer.stop()
        rstTimer.start(1)
    window.update()
    window.time.setText(current_time)

def calcTime(): # Time format convter
    global current_time, time_state
    m = int(count / 60) - time_state*25
    if(m < 10):
        M = '0' + str(m)
    else:
        M = str(m)
    s = count % 60
    if(s < 10):
        S = '0' + str(s)
    else:
        S = str(s)
    current_time = M + ':' + S

def reset(): # Timer reset
    global count, time_state
    count -= 1
    calcTime()
    window.time.setText(current_time)
    window.update()
    if(count == 1500):
        time_state = 0
    if(count == 0):
        rstTimer.stop()
        if(button_state == 1):
            timer.start(1000)

timer = QTimer()
timer.timeout.connect(tic)

rstTimer = QTimer()
rstTimer.timeout.connect(reset)

T = QThread()
T.run = timer
T.run = rstTimer
T.start()

sys.exit(app.exec_())
