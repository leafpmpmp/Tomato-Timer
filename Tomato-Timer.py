import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

scale = 1.25
adaptive_scale = 1.5
on_top = True
QT_SCALE_FACTOR = 3
button_state = 0
time_state = 0
settings_state = 0
rotation = 0
count = 350
width = 400
height = 700
bg_color = "#fad8d8"
#current_time = "25:00"

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.scaleUI()
        #self.showScale()
        self.updateScale()
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        self.titleBar = Bar(self)
        self.setContentsMargins(0, self.titleBar.height(), 0, 0)

    def resizeEvent(self, event):
        self.titleBar.resize(self.width(), self.titleBar.height())
    
    def initUI(self):
        self.setWindowTitle("Tomato Timer")
        self.setGeometry(int(300*scale), int(300*scale), int(400*scale), int(600*scale))
        self.tomato = QLabel(self)
        #self.tomato.setPixmap(QPixmap("img/tomato_stem.png"))
        self.title = QLabel(self)
        #self.time = QLabel("25:00", self)
        self.min_1 = QLabel("", self)
        self.min_2 = QLabel("", self)
        self.dot = QLabel("", self)
        self.sec_1 = QLabel("", self)
        self.sec_2 = QLabel("", self)
        self.start = QPushButton("", self)
        self.reset = QPushButton("", self)
        self.check = QCheckBox("", self)
        self.check.setChecked(True)
        self.settings = QPushButton("", self)
        self.rotate = QVariantAnimation(self)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        
        self.start.setStyleSheet('QPushButton {background-color: #00CC66; border: none; border-radius: 10px} QPushButton:hover {background-color: #00B359} QPushButton:pressed {background-color: #00c161}')
        self.reset.setStyleSheet('QPushButton {background-color: #d8311e; border: none; border-radius: 10px} QPushButton:hover {background-color: #cc1400} QPushButton:pressed {background-color: #cc1400}')
        self.check.setStyleSheet('QCheckBox::indicator {background: transparent; border: 1px solid #00CC66} QCheckBox::indicator:checked {background: transparent; background-color: #00CC66}')
        self.settings.setStyleSheet('QPushButton {background-color: transparent; border: none}')

        self.start.clicked.connect(self.onStartClick)
        self.reset.clicked.connect(self.onResetClick)
        self.check.clicked.connect(self.onClick)
        self.settings.clicked.connect(self.showSettings)

        self.rotate.setStartValue(360)
        self.rotate.setEndValue(0)
        self.rotate.setDuration(500)
        self.rotate.setEasingCurve(QEasingCurve.OutQuad)
        self.rotate.valueChanged.connect(self.updateIcon)

        self.scaleL = QRadioButton("Large", self)
        self.scaleM = QRadioButton("Medium", self)
        self.scaleS = QRadioButton("Small", self)
        self.slider = QSlider(self)
        self.scaleM.setChecked(True)
        self.slider.setRange(12, 18)
        self.slider.setOrientation(1)
        self.slider.setTickPosition(2)
        self.slider.setTickInterval(1)
        self.slider.setValue(15)
        self.scaleL.clicked.connect(self.onLargeClick)
        self.scaleM.clicked.connect(self.onMediumClick)
        self.scaleS.clicked.connect(self.onSmallClick)
        self.slider.valueChanged.connect(self.onSliderAdjusted)
        
        self.shortcut = QShortcut(QKeySequence("Space"), self)
        self.shortcut.activated.connect(self.onStartClick)

    def scaleUI(self):
        self.setFixedSize(int(width*scale), int(height*scale))
        self.title.setGeometry(int(200*scale - 100*adaptive_scale), 20, int(200*adaptive_scale), int(50*adaptive_scale))
        self.title.setPixmap(QPixmap("img/title.png").scaled(int(200*adaptive_scale), int(50*adaptive_scale), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.title.setAlignment(Qt.AlignCenter)

        #self.time.setGeometry(int(200*scale - 25*adaptive_scale), int(10 + 200*adaptive_scale + 105*scale), int(50*adaptive_scale), int(25*adaptive_scale))
        #self.time.setAlignment(Qt.AlignCenter)
        #self.time.setFont(QFont("Times New Roman", int(10*adaptive_scale)))
        self.min_1.setGeometry(int(200*scale - 80*adaptive_scale), int(20 + 200*adaptive_scale + 105*scale), int(40*adaptive_scale), int(45*adaptive_scale))
        self.min_2.setGeometry(int(200*scale - 50*adaptive_scale), int(20 + 200*adaptive_scale + 105*scale), int(40*adaptive_scale), int(45*adaptive_scale))
        self.dot.setGeometry(int(200*scale - 20*adaptive_scale), int(20 + 200*adaptive_scale + 105*scale), int(40*adaptive_scale), int(40*adaptive_scale))
        self.dot.setAlignment(Qt.AlignCenter)
        self.dot.setPixmap(QPixmap("img/dot.png").scaled(int(25*adaptive_scale), int(25*adaptive_scale), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.sec_1.setGeometry(int(200*scale + 10*adaptive_scale), int(20 + 200*adaptive_scale + 105*scale), int(40*adaptive_scale), int(45*adaptive_scale))
        self.sec_2.setGeometry(int(200*scale + 40*adaptive_scale), int(20 + 200*adaptive_scale + 105*scale), int(40*adaptive_scale), int(45*adaptive_scale))
        self.min_1.setAlignment(Qt.AlignCenter)
        self.min_2.setAlignment(Qt.AlignCenter)
        self.sec_1.setAlignment(Qt.AlignCenter)
        self.sec_2.setAlignment(Qt.AlignCenter)

        self.check.setIcon(QIcon("img/on_top.png"))
        self.check.setIconSize(QSize(150, 30))
        self.check.setGeometry(int(200*scale - 75), int(height*scale - 120), 150, 30)

        self.start.setGeometry(int(200*scale - 50*adaptive_scale), int(20 + 225*adaptive_scale + 140*scale), int(100*adaptive_scale), int(30*adaptive_scale))
        self.start.setIcon(QIcon("img/start.png"))
        self.start.setIconSize(QSize(int(100*adaptive_scale), int(30*adaptive_scale)))
        
        self.reset.setGeometry(int(200*scale - 50*adaptive_scale), int(20 + 255*adaptive_scale + 160*scale), int(100*adaptive_scale), int(30*adaptive_scale))
        self.reset.setIcon(QIcon("img/reset.png"))
        self.reset.setIconSize(QSize(int(100*adaptive_scale), int(30*adaptive_scale)))

        self.scaleL.hide()
        self.scaleM.hide()
        self.scaleS.hide()
        self.slider.hide()
        self.check.hide()
        self.settings.setGeometry(int(width*scale - 40), int(height*scale - 40), 30, 30)
        #self.settings.setIcon(QIcon("img/settings.png"))
        #self.settings.setIconSize(QSize(30, 30))
    
    def updateIcon(self, value):
        global rotation
        rotation = value
        self.update()
        #print(rotation)
    
    def showSettings(self): # Scaling settings
        global settings_state, rotation
        if(rotation == 0):
            if(settings_state == 0):
                self.scaleL.show()
                self.scaleM.show()
                self.scaleS.show()
                self.slider.show()
                self.check.show()
                settings_state = 1
            else:
                self.scaleL.hide()
                self.scaleM.hide()
                self.scaleS.hide()
                self.slider.hide()
                self.check.hide()
                settings_state = 0
            self.rotate.start()
        
    def paintEvent(self, event):
        alen = -1*(count-300)*0.24*16
        qp = QPainter()
        qp.begin(self)
        qp.drawPixmap(int(200*scale - 75*adaptive_scale), int(19 + 50*adaptive_scale + 50*scale), int(151*adaptive_scale), int(151*adaptive_scale), QPixmap("img/tomato_slice.png"))

        if(time_state == 0):
            tomato_image = QImage("img/tomato_peel.png").scaled(int(150*adaptive_scale), int(150*adaptive_scale), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            brush = QBrush(tomato_image)
            # Calculate the top-left corner of where the pie will be drawn
            pie_x = int(200*scale - 75*adaptive_scale)
            pie_y = int(20 + 50*adaptive_scale + 50*scale)
            # Adjust the brush transformation
            brush_transformation = QTransform()
            brush_transformation.translate(pie_x, pie_y)
            brush.setTransform(brush_transformation)
            qp.setBrush(brush)
            qp.setPen(Qt.NoPen)
        else: # 5 minutes break
            qp.setBrush(Qt.cyan)
            qp.setPen(Qt.NoPen)
        # drawing the timer circle
        qp.drawPie(QRect(int(200*scale - 75*adaptive_scale), int(20 + 50*adaptive_scale + 50*scale), int(150*adaptive_scale), int(150*adaptive_scale)), 90*16, int(alen))
        qp.setPen(QPen(QColor("#FF3300"), 3*adaptive_scale))
        #qp.drawArc(QRect(int(200*scale - 76*adaptive_scale), int(7 + 50*adaptive_scale + 50*scale), int(152*adaptive_scale), int(152*adaptive_scale)), 0, 360*16)
        qp.end()

        st = QPainter()
        st.begin(self)
        st.translate(int(width*scale - 25), int(height*scale - 25))
        st.rotate(rotation)
        st.drawPixmap(-15, -15, 30, 30, QPixmap("img/settings.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        st.end()

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
            self.start.setIcon(QIcon("img/stop.png"))
            button_state = 1
            timer.start(1000)
        else:
            self.start.setIcon(QIcon("img/start.png"))
            button_state = 0
            timer.stop()

    def onResetClick(self): # RESET button
        global button_state, count, time_state
        self.start.setIcon(QIcon("img/start.png"))
        timer.stop()
        button_state = 0
        if count <= 300:
            count = 300
            time_state = 0
        rstTimer.start(1)

    def onLargeClick(self): # Window scale buttons
        global scale, adaptive_scale
        scale = 2
        adaptive_scale = 2
        self.scaleL.setChecked(True)
        self.slider.setRange(18, 27)
        self.slider.setValue(20)
        self.Scale()
    
    def onMediumClick(self):
        global scale, adaptive_scale
        scale = 1.25
        adaptive_scale = 1.5
        self.scaleM.setChecked(True)
        self.slider.setRange(12, 18)
        self.slider.setValue(15)
        self.Scale()

    def onSmallClick(self):
        global scale, adaptive_scale
        scale = 1
        adaptive_scale = 1
        self.scaleS.setChecked(True)
        self.slider.setRange(10, 13)
        self.slider.setValue(10)
        self.Scale()
        
    def onSliderAdjusted(self): # elements scale slider
        global scale, adaptive_scale
        adaptive_scale = self.slider.value() / 10
        self.Scale()
            
    def updateClock(self, M, S):
        self.min_1.setPixmap(QPixmap("img/" + M[0] + ".png").scaled(int(30*adaptive_scale), int(30*adaptive_scale), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.min_2.setPixmap(QPixmap("img/" + M[1] + ".png").scaled(int(30*adaptive_scale), int(30*adaptive_scale), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.sec_1.setPixmap(QPixmap("img/" + S[0] + ".png").scaled(int(30*adaptive_scale), int(30*adaptive_scale), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.sec_2.setPixmap(QPixmap("img/" + S[1] + ".png").scaled(int(30*adaptive_scale), int(30*adaptive_scale), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    
    def calcTime(self): # Time format convter
        global time_state
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
        self.updateClock(M, S)

    def updateScale(self):
        self.scaleL.setGeometry(int(200*scale - 180), int(height*scale - 80), 135, 30)
        self.scaleM.setGeometry(int(200*scale - 45), int(height*scale - 80), 135, 30)
        self.scaleS.setGeometry(int(200*scale + 90), int(height*scale - 80), 135, 30)
        self.slider.setGeometry(int(200*scale - 100), int(height*scale - 40), 200, 30)
        self.calcTime()
    
    def Scale(self):
        self.scaleUI()
        self.updateScale()
        window.update()

class Bar(QWidget):
    clickPos = None
    def __init__(self, parent):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        
        #self.setBackgroundRole(QPalette.Shadow)
        # alternatively:
        # palette = self.palette()
        # palette.setColor(palette.Window, Qt.black)
        # palette.setColor(palette.WindowText, Qt.white)
        # self.setPalette(palette)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addStretch()

        self.title = QLabel("")
        # if setPalette() was used above, this is not required
        self.title.hide()

        style = self.style()
        ref_size = self.fontMetrics().height()
        ref_size += style.pixelMetric(style.PM_ButtonMargin) * 2
        self.setMaximumHeight(ref_size + 2)

        btn_size = QSize(ref_size, ref_size)
        for target in ('min', 'normal', 'close'):
            btn = QToolButton(self, focusPolicy=Qt.NoFocus)
            layout.addWidget(btn)
            btn.setFixedSize(btn_size)

            iconType = getattr(style, 
                'SP_TitleBar{}Button'.format(target.capitalize()))
            btn.setIcon(style.standardIcon(iconType))

            """"""
            if target == 'close':
                colorNormal = bg_color
                colorHover = 'red'
            else:
                colorNormal = bg_color
                colorHover = '#d6b8b8'
            btn.setStyleSheet('''
                QToolButton {{
                    background-color: {};
                    border: none;
                }}
                QToolButton:hover {{
                    background-color: {};
                    border: none;
                }}
            '''.format(colorNormal, colorHover))
            

            signal = getattr(self, target + 'Clicked')
            btn.clicked.connect(signal)

            setattr(self, target + 'Button', btn)

        self.normalButton.hide()
        # to make the title buttons flat
        self.minButton.setAutoRaise(True)
        self.closeButton.setAutoRaise(True)

        self.updateTitle(parent.windowTitle())
        parent.windowTitleChanged.connect(self.updateTitle)

    def updateTitle(self, title=None):
        if title is None:
            title = self.window().windowTitle()
        width = self.title.width()
        width -= self.style().pixelMetric(QStyle.PM_LayoutHorizontalSpacing) * 2
        self.title.setText(self.fontMetrics().elidedText(
            title, Qt.ElideRight, width))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clickPos = event.windowPos().toPoint()

    def mouseMoveEvent(self, event):
        if self.clickPos is not None:
            self.window().move(event.globalPos() - self.clickPos)

    def mouseReleaseEvent(self, QMouseEvent):
        self.clickPos = None

    def closeClicked(self):
        self.window().close()

    def normalClicked(self):
        self.window().showNormal()

    def minClicked(self):
        self.window().showMinimized()
    
    def resizeEvent(self, event):
        self.title.resize(self.minButton.x(), self.height())
        self.updateTitle()

app = QApplication(sys.argv)
window = Window()
window.setWindowFlag(Qt.WindowStaysOnTopHint)
window.show()

w = QWidget()
bg = w.palette()
bg.setColor(w.backgroundRole(), QColor(bg_color))
window.setPalette(bg)

def tic(): # counter
    global count, time_state
    count -= 1
    window.calcTime()
    if(count == 300):
        time_state = 1
    elif(count == 0):
        timer.stop()
        rstTimer.start(1)
    window.update()

def reset(): # Timer reset
    global count, time_state
    if(count >= 1799):
        print(count)
        count = 1800
        rstTimer.stop()
        if(button_state == 1):
            timer.start(1000)
    else:
        count += 3
    window.calcTime()
    window.update()
    
def rotate():
    global rotation
    rotation -= 1
    if(rotation == 0):
        sTimer.stop()
    window.update()


window.calcTime()
timer = QTimer()
timer.timeout.connect(tic)

rstTimer = QTimer()
rstTimer.timeout.connect(reset)

sTimer = QTimer()
sTimer.timeout.connect(rotate)

T = QThread()
T.run = timer
T.run = rstTimer
T.start()

sys.exit(app.exec_())