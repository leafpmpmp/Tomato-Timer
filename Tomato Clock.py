import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

scale = 1.25
adaptive_scale = 1.5
on_top = True

button_state = 0
time_state = 0
count = 1800
current_time = "25:00"

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.scaleUI()
        #self.showScale()

    def initUI(self):
        self.setWindowTitle("Tomato Timer")

        self.shadow = QLabel("Tomato Timer", self)
        self.title = QLabel("Tomato Timer", self)
        self.time = QLabel("25:00", self)
        self.start = QPushButton("START", self)
        self.reset = QPushButton("RESET", self)
        self.check = QCheckBox("On Top", self)
        self.check.setChecked(True)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        
        self.start.setStyleSheet('QPushButton {background-color: #00CC66; border: none} QPushButton:hover {background-color: #00B359} QPushButton:pressed {background-color: #00b359}')
        self.reset.setStyleSheet('QPushButton {background-color: #00CC66; border: none} QPushButton:hover {background-color: #00B359} QPushButton:pressed {background-color: #00b359}')
        self.check.setStyleSheet('QCheckBox::indicator {background: transparent; border: 1px solid #00CC66} QCheckBox::indicator:checked {background: transparent; background-color: #00CC66}')

        self.start.clicked.connect(self.onStartClick)
        self.reset.clicked.connect(self.onResetClick)
        self.check.clicked.connect(self.onClick)

    def scaleUI(self):
        self.setGeometry(int(300*scale), int(300*scale), int(400*scale), int(600*scale))
        self.title.setGeometry(int(200*scale - 100*adaptive_scale), 10, int(200*adaptive_scale), int(50*adaptive_scale))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Arial", int(16*adaptive_scale)))
        self.shadow.setGeometry(int(200*scale - 100*adaptive_scale) + 2, 12, int(200*adaptive_scale), int(50*adaptive_scale))
        self.shadow.setAlignment(Qt.AlignCenter)
        self.shadow.setFont(QFont("Arial", int(16*adaptive_scale)))
        self.shadow.setStyleSheet('QLabel {color: #333333}')

        self.time.setGeometry(int(200*scale - 25*adaptive_scale), int(10 + 200*adaptive_scale + 105*scale), int(50*adaptive_scale), int(25*adaptive_scale))
        self.time.setAlignment(Qt.AlignCenter)
        self.time.setFont(QFont("Arial", int(10*adaptive_scale)))

        self.start.setGeometry(int(200*scale - 40*adaptive_scale), int(10 + 225*adaptive_scale + 130*scale), int(80*adaptive_scale), int(30*adaptive_scale))
        self.start.setFont(QFont("Arial", int(10*adaptive_scale)))
        
        self.reset.setGeometry(int(200*scale - 30*adaptive_scale), int(10 + 255*adaptive_scale + 150*scale), int(60*adaptive_scale), int(25*adaptive_scale))
        self.start.setFont(QFont("Arial", int(7*adaptive_scale)))

    def showScale(self): # Scaling settings
        self.scaleL = QRadioButton("Large", self)
        self.scaleM = QRadioButton("Medium", self)
        self.scaleS = QRadioButton("Small", self)
        self.slider = QSlider(self)
        self.scaleM.setChecked(True)
        self.slider.setRange(10, 25)
        self.slider.setOrientation(1)
        self.slider.setTickPosition(2)
        self.slider.setTickInterval(1)
        self.slider.setValue(15)
        self.scaleL.clicked.connect(self.onLargeClick)
        self.scaleM.clicked.connect(self.onMediumClick)
        self.scaleS.clicked.connect(self.onSmallClick)
        self.slider.valueChanged.connect(self.onSliderAdjusted)
        self.scaleL.setGeometry(int(100*scale - 20*adaptive_scale), int(10 + 280*adaptive_scale + 180*scale), int(90*adaptive_scale), int(25*adaptive_scale))
        self.scaleM.setGeometry(int(200*scale - 20*adaptive_scale), int(10 + 280*adaptive_scale + 180*scale), int(90*adaptive_scale), int(25*adaptive_scale))
        self.scaleS.setGeometry(int(300*scale - 20*adaptive_scale), int(10 + 280*adaptive_scale + 180*scale), int(90*adaptive_scale), int(25*adaptive_scale))
        self.slider.setGeometry(int(200*scale - 100), int(600*scale - 40), 200, 30)

    def paintEvent(self, event):
        alen = -1*count*0.2*16
        qp = QPainter()
        qp.begin(self)
        
        qp.setPen(QPen(QColor("#CC2900"), 3*adaptive_scale))
        qp.drawArc(QRect(int(200*scale - 76*adaptive_scale) + 3, int(7 + 50*adaptive_scale + 50*scale) + 3, int(152*adaptive_scale), int(152*adaptive_scale)), 0, 360*16)
        if(time_state == 0):
            qp.setBrush(Qt.red)
            qp.setPen(QPen(QColor("#ff0000"), 3))
        else:
            qp.setBrush(Qt.cyan)
            qp.setPen(QPen(QColor("#00ffff"), 3))
        qp.drawPie(QRect(int(200*scale - 75*adaptive_scale), int(10 + 50*adaptive_scale + 50*scale), int(150*adaptive_scale), int(150*adaptive_scale)), 90*16, int(alen))
        qp.setPen(QPen(QColor("#FF3300"), 3*adaptive_scale))
        qp.drawArc(QRect(int(200*scale - 76*adaptive_scale), int(7 + 50*adaptive_scale + 50*scale), int(152*adaptive_scale), int(152*adaptive_scale)), 0, 360*16)
        qp.end()

    def onClick(self):
        global on_top
        if(self.check.isChecked()):
            self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            self.show()
        else:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
            self.show()
    
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

    def onLargeClick(self): # Window scale buttons
        global scale, adaptive_scale
        scale = 2
        adaptive_scale = 2
        self.scaleL.setChecked(True)
        self.slider.setValue(20)
        self.Scale()
    
    def onMediumClick(self):
        global scale, adaptive_scale
        scale = 1.25
        adaptive_scale = 1.5
        self.scaleM.setChecked(True)
        self.slider.setValue(15)
        self.Scale()

    def onSmallClick(self):
        global scale, adaptive_scale
        scale = 1
        adaptive_scale = 1
        self.scaleS.setChecked(True)
        self.slider.setValue(10)
        self.Scale()
        
    def onSliderAdjusted(self): # elements scale slider
        global scale, adaptive_scale
        adaptive_scale = self.slider.value() / 10
        self.Scale()
    
    def Scale(self):
        self.scaleUI()
        window.update()

app = QApplication(sys.argv)
window = Window()
window.setWindowFlag(Qt.WindowStaysOnTopHint)
window.show()

w = QWidget()
bg = w.palette()
bg.setColor(w.backgroundRole(), QColor(247, 156, 156))
window.setPalette(bg)

def tic(): # counter
    global count, time_state
    count -= 1
    calcTime()
    if(count == 300):
        time_state = 1
    elif(count == 0):
        timer.stop()
        rstTimer.start(1)
    window.update()
    window.time.setText(current_time)

def calcTime(): # Time format convter
    global current_time, time_state
    time = count - 300
    m = int(time / 60) + time_state*4
    if(m < 10):
        M = '0' + str(m)
    else:
        M = str(m)
    s = time % 60
    if(s < 10):
        S = '0' + str(s)
    else:
        S = str(s)
    current_time = M + ':' + S

def reset(): # Timer reset
    global count, time_state
    calcTime()
    
    window.time.setText(current_time)
    window.update()
    if(count == 300):
        time_state = 0
    if(count == 1800):
        count -= 1
        rstTimer.stop()
        if(button_state == 1):
            timer.start(1000)
    count += 1
        

timer = QTimer()
timer.timeout.connect(tic)

rstTimer = QTimer()
rstTimer.timeout.connect(reset)

T = QThread()
T.run = timer
T.run = rstTimer
T.start()

sys.exit(app.exec_())
