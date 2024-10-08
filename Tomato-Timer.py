import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

factor = 1.0
scale = 1.5
adaptive_scale = 1.5
button_state = 0
time_state = 0
settings_state = 0
rotation = 0
count = 1800
frame = 0
width = 200
half_width = width / 2
height = 350
bg_color = "#F1DEC6"
bg_hover = "#c1b19d"
st_color = "#c73030"
corner_radius = 15
figure = 1

def get_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return filename
class Window(QWidget):
    def __init__(self):
        super().__init__()
        screen = self.screen()
        size = screen.size()
        #print(size.width(), size.height())
        global width, height, scale, factor, adaptive_scale, corner_radius
        factor = size.height() / 1080
        scale = scale * factor
        adaptive_scale = adaptive_scale * factor
        
        self.initUI()
        self.scaleUI()
        self.updateScale()
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setStyleSheet("border-radius: 10px;")

        self.titleBar = Bar(self)
        self.setContentsMargins(0, self.titleBar.height(), 0, 0)

    def resizeEvent(self, event):
        global width, height
        self.titleBar.resize(self.width(), self.titleBar.height())
        #width, height = self.size().width()/scale, self.size().height()/scale
        self.scaleUI()
    
    def initUI(self):
        self.setWindowTitle("Tomato Timer")
        self.setGeometry(int(150*scale), int(150*scale), int(width*scale), int(height*scale))
        #make the main window transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.tomato = QLabel(self)
        self.title = QLabel(self)
        self.timer = QLabel(self)
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
        self.expand = QPropertyAnimation(self, b"size")
        self.scaleWindow = QVariantAnimation(self)
        self.scaleElements = QVariantAnimation(self)
        self.scaling = QParallelAnimationGroup(self)
        self.scaling.addAnimation(self.scaleWindow)
        self.scaling.addAnimation(self.expand)
        self.cutscene = QLabel("", self)
        self.fade = QPropertyAnimation(self.cutscene, b"geometry")
        self.fade.valueChanged.connect(self.fade_faucet)

        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        
        self.start.setStyleSheet('''
                QPushButton {{
                    background-color: #4b63b3;;
                    border: none;
                    border-radius: {};
                }}
                QPushButton:hover {{
                    background-color: #4158A6;
                }}
                QPushButton:pressed {{
                    background-color: #34488c;
                }}
            '''.format(5*scale))
        self.start.setIcon(QIcon(get_path("img/start.png")))
        self.reset.setStyleSheet('''
                QPushButton {{
                    background-color: #FF8343;
                    border: none;
                    border-radius: {};
                }}
                QPushButton:hover {{
                    background-color: #e2743d;
                }}
                QPushButton:pressed {{
                    background-color: #c46435;
                }}
            '''.format(5*scale))
        self.reset.setIcon(QIcon(get_path("img/reset.png")))
        self.check.setStyleSheet('QCheckBox::indicator {{background: transparent; border: 1px solid #7eb055; width: {}; height: {}}} QCheckBox::indicator:checked {{background: transparent; background-color: #7eb055}}'.format(10*scale, 10*scale))
        self.check.setIcon(QIcon(get_path("img/on_top.png")))
        self.check.setIconSize(QSize(int(40*factor), int(20*factor)))
        self.settings.setStyleSheet('QPushButton {background-color: transparent; border: none}')

        self.start.clicked.connect(self.onStartClick)
        self.reset.clicked.connect(self.onResetClick)
        self.check.clicked.connect(self.onClick)
        self.settings.clicked.connect(self.showSettings)

        self.rotate.setDuration(500)
        self.rotate.setEasingCurve(QEasingCurve.OutQuad)
        self.rotate.valueChanged.connect(self.updateIcon)
        self.rotate.setStartValue(360)
        self.rotate.setEndValue(0)

        self.expand.setDuration(500)
        self.expand.setEasingCurve(QEasingCurve.OutQuad)
        self.expand.setStartValue(height*scale)
        self.expand.setEndValue(height*scale + 120*factor)

        self.scaleWindow.setDuration(500)
        self.scaleWindow.setEasingCurve(QEasingCurve.OutQuad)
        self.scaleWindow.valueChanged.connect(self.updateSize)

        self.scaleElements.setDuration(500)
        self.scaleElements.setEasingCurve(QEasingCurve.OutQuad)
        self.scaleElements.valueChanged.connect(self.updateElements)

        
        self.scale = QLabel("", self)
        self.scaleL = QRadioButton("", self)
        self.scaleM = QRadioButton("", self)
        self.scaleS = QRadioButton("", self)
        self.scalegroup = QButtonGroup(self)
        self.scalegroup.addButton(self.scaleL)
        self.scalegroup.addButton(self.scaleM)
        self.scalegroup.addButton(self.scaleS)
        self.slider = QSlider(self)
        self.scaleM.setChecked(True)
        self.slider.setRange(int(12*factor), int(18*factor))
        self.slider.setOrientation(1)
        self.slider.setTickPosition(2)
        self.slider.setTickInterval(1)
        self.slider.setValue(int(15*factor))
        self.slider.setStyleSheet('''QSlider::groove:horizontal {{
                                    border: 1px solid #4b63b3;
                                    height: {};
                                    background: #4b63b3;
                                    margin: 0px;
                                    border-radius: {};
                                    }}
                                    QSlider::handle:horizontal {{
                                    background: #FF8343;
                                    border: 1px solid #FF8343;
                                    width: {};
                                    height: {};
                                    border-radius: {};
                                    }}'''.format(10*factor, 5*factor, 12*factor, 8*factor, 4*factor))
        self.scaleL.clicked.connect(self.onLargeClick)
        self.scaleM.clicked.connect(self.onMediumClick)
        self.scaleS.clicked.connect(self.onSmallClick)
        self.slider.valueChanged.connect(self.onSliderAdjusted)

        self.scaleL.setIcon(QIcon(get_path("img/large.png")))
        self.scaleM.setIcon(QIcon(get_path("img/medium.png")))
        self.scaleS.setIcon(QIcon(get_path("img/small.png")))
        self.scaleL.setIconSize(QSize(int(40*factor), int(20*factor)))
        self.scaleM.setIconSize(QSize(int(40*factor), int(20*factor)))
        self.scaleS.setIconSize(QSize(int(40*factor), int(20*factor)))
        self.scaleL.setStyleSheet('''QRadioButton::indicator {{
                                  background: transparent; 
                                  border: 1px solid #353637; 
                                  width: {}; 
                                  height: {};
                                  }} 
                                  QRadioButton::indicator:checked {{
                                  background: transparent; 
                                  background-color: #353637;
                                  }}
                                  '''.format(10*scale, 10*scale))
        self.scaleM.setStyleSheet('''QRadioButton::indicator {{
                                  background: transparent; 
                                  border: 1px solid #353637; 
                                  width: {}; 
                                  height: {};
                                  }} 
                                  QRadioButton::indicator:checked {{
                                  background: transparent; 
                                  background-color: #353637;
                                  }}
                                  '''.format(10*scale, 10*scale))
        self.scaleS.setStyleSheet('''QRadioButton::indicator {{
                                  background: transparent; 
                                  border: 1px solid #353637; 
                                  width: {}; 
                                  height: {};
                                  }} 
                                  QRadioButton::indicator:checked {{
                                  background: transparent; 
                                  background-color: #353637;
                                  }}
                                  '''.format(10*scale, 10*scale))

        self.fig = QLabel("", self)
        self.figtomato = QRadioButton("", self)
        self.figapple = QRadioButton("", self)
        self.figapple.clicked.connect(self.onAppleCheck)
        self.figtomato.clicked.connect(self.onTomatoCheck)
        self.figtomato.setIcon(QIcon(get_path("img/tomato.png")))
        self.figapple.setIcon(QIcon(get_path("img/apple.png")))
        self.figtomato.setIconSize(QSize(int(18*factor), int(18*factor)))
        self.figapple.setIconSize(QSize(int(18*factor), int(21*factor)))
        self.figtomato.setChecked(True)
        self.figtomato.setStyleSheet('QRadioButton::indicator {{background: transparent; border: 1px solid #c73030; width: {}; height: {}}} QRadioButton::indicator:checked {{background: transparent; background-color: #c73030}}'.format(10*scale, 10*scale))
        self.figapple.setStyleSheet('QRadioButton::indicator {{background: transparent; border: 1px solid #c73030; width: {}; height: {}}} QRadioButton::indicator:checked {{background: transparent; background-color: #c73030}}'.format(10*scale, 10*scale))
        
        self.shortcut = QShortcut(QKeySequence("Space"), self)
        self.shortcut.activated.connect(self.onStartClick)
        self.faucet = QLabel("", self)

    def scaleUI(self):
        self.title.setGeometry(int(half_width*scale - 50*adaptive_scale), int(15*factor), int(100*adaptive_scale), int(25*adaptive_scale))
        self.title.setPixmap(QPixmap(get_path("img/title.png")).scaled(int(100*adaptive_scale), int(25*adaptive_scale), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.title.setAlignment(Qt.AlignCenter)

        self.timer.setPixmap(QPixmap(get_path("img/clock.png")).scaled(int(100*adaptive_scale), int(100*adaptive_scale), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.timer.setGeometry(int(half_width*scale - 50*adaptive_scale), int(5*factor + 50*adaptive_scale + 68.5*scale), int(150*adaptive_scale), int(150*adaptive_scale))
        self.min_1.setGeometry(int(half_width*scale - 45*adaptive_scale), int(10*factor + 111*adaptive_scale + 68.5*scale), int(10*adaptive_scale + 10*scale), int(22.5*adaptive_scale))
        self.min_2.setGeometry(int(half_width*scale - 25*adaptive_scale), int(10*factor + 111*adaptive_scale + 68.5*scale), int(10*adaptive_scale + 10*scale), int(22.5*adaptive_scale))
        self.dot.setGeometry(int(half_width*scale - 10*adaptive_scale), int(12*factor + 111*adaptive_scale + 68.5*scale), int(10*adaptive_scale + 10*scale), int(20*adaptive_scale))
        self.dot.setAlignment(Qt.AlignCenter)
        self.dot.setPixmap(QPixmap(get_path("img/dot.png")).scaled(int(25*adaptive_scale), int(25*adaptive_scale), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.sec_1.setGeometry(int(half_width*scale + 5*adaptive_scale), int(10*factor + 111*adaptive_scale + 68.5*scale), int(10*adaptive_scale + 10*scale), int(22.5*adaptive_scale))
        self.sec_2.setGeometry(int(half_width*scale + 25*adaptive_scale), int(10*factor + 111*adaptive_scale + 68.5*scale), int(10*adaptive_scale + 10*scale), int(22.5*adaptive_scale))
        self.min_1.setAlignment(Qt.AlignCenter)
        self.min_2.setAlignment(Qt.AlignCenter)
        self.sec_1.setAlignment(Qt.AlignCenter)
        self.sec_2.setAlignment(Qt.AlignCenter)

        self.settings.setGeometry(int(width*scale - 20*factor), int(height*scale - 20*factor), int(15*factor), int(15*factor))
        self.check.setGeometry(int(half_width*scale - 27.5*factor), int(height*scale + 10*factor), int(67.5*factor), int(20*factor))

        self.start.setGeometry(int(half_width*scale - 37.5*adaptive_scale), int(10*factor + 147.5*adaptive_scale + 75*scale), int(75*adaptive_scale), int(22.5*adaptive_scale))
        self.start.setIconSize(QSize(int(75*adaptive_scale), int(22.5*adaptive_scale)))
        
        self.reset.setGeometry(int(half_width*scale - 37.5*adaptive_scale), int(10*factor + 172.5*adaptive_scale + 90*scale), int(75*adaptive_scale), int(22.5*adaptive_scale))
        self.reset.setIconSize(QSize(int(75*adaptive_scale), int(22.5*adaptive_scale)))

        self.cutscene.setGeometry(int(-164*adaptive_scale), int(10*factor + 25*adaptive_scale - 5*scale), int(164*adaptive_scale), int(123*adaptive_scale))
        self.faucet.setGeometry(int(width*scale + 39*adaptive_scale), int(25*factor + 5*adaptive_scale + 4.5*scale), int(37.5*adaptive_scale), int(45*adaptive_scale))
        self.faucet.setPixmap(QPixmap(get_path("img/faucet.png")).scaled(int(37.5*adaptive_scale), int(45*adaptive_scale), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    
    def updateIcon(self, value):
        global rotation
        rotation = value
        self.update()
    
    def updateElements(self, value):
        global adaptive_scale
        adaptive_scale = value
        self.scaleUI()
        self.calcTime()
        window.update()
    
    def showSettings(self): # expand or collapse settings panel
        global settings_state
        startpos = self.size()
        self.rotate.stop()
        self.expand.stop()
        if(settings_state == 0):
            newpos = QSize(int(width*scale), int(height*scale + 120*factor))
            self.expand.setStartValue(startpos)
            self.expand.setEndValue(newpos)
            self.rotate.setStartValue(rotation)
            self.rotate.setEndValue(0)
            settings_state = 1
        else:
            newpos = QSize(int(width*scale), int(height*scale))
            self.expand.setStartValue(startpos)
            self.expand.setEndValue(newpos)
            self.rotate.setStartValue(rotation)
            self.rotate.setEndValue(360)
            settings_state = 0
        self.rotate.start()
        self.expand.start()
        
    def paintEvent(self, event):
        alen = -1*(count-300)*0.24*16
        qp = QPainter()
        qp.begin(self)
        qp.setBrush(QColor(bg_color))
        qp.setPen(Qt.NoPen)
        qp.drawRoundedRect(QRect(0, 0, self.size().width(), self.size().height()), corner_radius, corner_radius)
        
        if(time_state == 0):
            if figure == 1: # tomato
                qp.drawPixmap(int(half_width*scale - 82*adaptive_scale), int(25*factor + 25*adaptive_scale + 2.5*scale), int(164*adaptive_scale), int(123*adaptive_scale), QPixmap(get_path("img/cutting_board_1.png")))
                qp.setOpacity((count-300)/1500)
                qp.drawPixmap(int(half_width*scale - 82*adaptive_scale), int(25*factor + 25*adaptive_scale + 2.5*scale), int(164*adaptive_scale), int(123*adaptive_scale), QPixmap(get_path("img/tomato_shade.png")))
                qp.setOpacity(1)
                tomato_image = QImage(get_path("img/tomato.png")).scaled(int(75*adaptive_scale), int(75*adaptive_scale), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                brush = QBrush(tomato_image)
                # Calculate the top-left corner of where the pie will be drawn
                pie_x = int(half_width*scale - 38*adaptive_scale)
                pie_y = int(25*factor + 47.5*adaptive_scale + 2.5*scale)
                # Adjust the brush transformation
                brush_transformation = QTransform()
                brush_transformation.translate(pie_x, pie_y)
                brush.setTransform(brush_transformation)
                qp.setBrush(brush)
                qp.setPen(Qt.NoPen)
                qp.drawPie(QRect(int(half_width*scale - 38*adaptive_scale), int(25*factor + 47.5*adaptive_scale + 2.5*scale), int(75*adaptive_scale), int(75*adaptive_scale)), 90*16, int(alen))
                qp.setPen(QPen(QColor("#FF3300"), 3*adaptive_scale))
            elif figure == 2: # bad apple
                qp.drawPixmap(int(half_width*scale - 82*adaptive_scale), int(25*factor + 25*adaptive_scale + 2.5*scale), int(164*adaptive_scale), int(123*adaptive_scale), QPixmap(get_path("img/cutting_board_2.png")))
                qp.setOpacity((count-300)/1500)
                qp.drawPixmap(int(half_width*scale - 82*adaptive_scale), int(25*factor + 25*adaptive_scale + 2.5*scale), int(164*adaptive_scale), int(123*adaptive_scale), QPixmap(get_path("img/apple_shade.png")))
                qp.setOpacity(1)
                apple_image = QImage(get_path("img/apple.png")).scaled(int(76*adaptive_scale), int(90*adaptive_scale), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                brush = QBrush(apple_image)
                # Calculate the top-left corner of where the pie will be drawn
                pie_x = int(half_width*scale - 38.5*adaptive_scale)
                pie_y = int(25*factor + 38.5*adaptive_scale + 2.5*scale)
                # Adjust the brush transformation
                brush_transformation = QTransform()
                brush_transformation.translate(pie_x, pie_y)
                brush.setTransform(brush_transformation)
                qp.setBrush(brush)
                qp.setPen(Qt.NoPen)
                qp.drawPie(QRect(int(half_width*scale - 38.5*adaptive_scale), int(25*factor + 38.5*adaptive_scale + 2.5*scale), int(76*adaptive_scale), int(90*adaptive_scale)), 90*16, int(alen))
                qp.setPen(QPen(QColor("#FF3300"), 3*adaptive_scale))
        elif(time_state == 1): # 5 minutes break
            qp.drawPixmap(int(half_width*scale - 82*adaptive_scale), int(25*factor+ 25*adaptive_scale + 22.5*scale), int(164*adaptive_scale), int(96*adaptive_scale), QPixmap(get_path("img/sink_back.png")))
            filename = "img/water/R_frame" + str(frame) + ".png"
            qp.drawPixmap(int(half_width*scale - 67.5*adaptive_scale), int(25*factor+ 25*adaptive_scale + 22.5*scale), int(137*adaptive_scale), int(90*adaptive_scale), QPixmap(get_path(filename)))
            qp.drawPixmap(int(half_width*scale - 82*adaptive_scale), int(25*factor+ 25*adaptive_scale + 22.5*scale), int(164*adaptive_scale), int(96*adaptive_scale), QPixmap(get_path("img/sink_front.png")))
            qp.drawPixmap(int(half_width*scale - 25*adaptive_scale), int(25*factor + 5*adaptive_scale + 4.5*scale), int(37.5*adaptive_scale), int(45*adaptive_scale), QPixmap(get_path("img/faucet.png")))

        qp.end()

        st = QPainter()
        st.begin(self)
        st.translate(int(width*scale - 12.5*factor), int(height*scale - 12.5*factor))
        st.rotate(rotation)
        st.drawPixmap(int(-7.5*factor), int(-7.5*factor), int(15*factor), int(15*factor), QPixmap(get_path("img/settings.png")).scaled(int(15*factor), int(15*factor), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        st.end()

    def onClick(self): # Always on top checkbox
        if(self.check.isChecked()):
            self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            self.show()
        else:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
            self.show()
    
    def onStartClick(self): # START/STOP button
        global button_state
        if(button_state == 0):
            self.start.setIcon(QIcon(get_path("img/stop.png")))
            self.start.setStyleSheet('''
                QPushButton {{
                    background-color: #da4a4a;
                    border: none;
                    border-radius: {};
                }}
                QPushButton:hover {{
                    background-color: #c73030;
                }}
                QPushButton:pressed {{
                    background-color: #b52323;
                }}
            '''.format(5*scale))
            button_state = 1
            timer.start(1000)
            if time_state == 1:
                aniTimer.start(42)
        else:
            self.start.setIcon(QIcon(get_path("img/start.png")))
            self.start.setStyleSheet('''
                QPushButton {{
                    background-color: #4b63b3;;
                    border: none;
                    border-radius: {};
                }}
                QPushButton:hover {{
                    background-color: #4158A6;
                }}
                QPushButton:pressed {{
                    background-color: #34488c;
                }}
            '''.format(5*scale))
            button_state = 0
            timer.stop()
            aniTimer.stop()

    def onResetClick(self): # RESET button
        global button_state, count
        self.start.setIcon(QIcon(get_path("img/start.png")))
        self.start.setStyleSheet('''
                QPushButton {{
                    background-color: #4b63b3;
                    border: none;
                    border-radius: {};
                }}
                QPushButton:hover {{
                    background-color: #4158A6;
                }}
                QPushButton:pressed {{
                    background-color: #34488c;
                }}
            '''.format(5*scale))
        button_state = 0
        if count <= 300:
            timer.start(1000)
            count = 1
            tic()
        else:
            timer.stop()
            rstTimer.start(1)

    def onLargeClick(self): # Window scale buttons
        self.scaleWindow.setStartValue(adaptive_scale)
        self.scaleWindow.setEndValue(2.0*factor)
        self.scaleL.setChecked(True)
        self.slider.setRange(int(18*factor), int(24*factor))
        self.slider.setValue(int(20*factor))
        self.Scale(2.0*factor)
    
    def onMediumClick(self):
        self.scaleWindow.setStartValue(adaptive_scale)
        self.scaleWindow.setEndValue(1.5*factor)
        self.scaleM.setChecked(True)
        self.slider.setRange(int(12*factor), int(18*factor))
        self.slider.setValue(int(15*factor))
        self.Scale(1.5*factor)

    def onSmallClick(self):
        self.scaleWindow.setStartValue(adaptive_scale)
        self.scaleWindow.setEndValue(1.0*factor)
        self.scaleS.setChecked(True)
        self.slider.setRange(int(10*factor), int(12*factor))
        self.slider.setValue(int(10*factor))
        self.Scale(1.0*factor)
        
    def onSliderAdjusted(self): # elements scale slider
        global adaptive_scale
        self.scaleElements.setStartValue(adaptive_scale)
        adaptive_scale = self.slider.value() / 10
        self.scaleElements.setEndValue(adaptive_scale)
        self.scaleElements.start()

    def onAppleCheck(self):
        global figure
        figure = 2
        window.update()
    
    def onTomatoCheck(self):
        global figure
        figure = 1
        window.update()
    
    def updateSize(self, value):
        global adaptive_scale, scale
        if value:
            adaptive_scale = scale = value
        self.setBaseSize(int(width*scale), int(height*scale))
        self.scaleUI()
        self.updateScale()
        window.update()
    
    def updateClock(self, M, S):
        self.min_1.setPixmap(QPixmap(get_path("img/" + M[0] + ".png")).scaled(int(15*adaptive_scale), int(20*adaptive_scale), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.min_2.setPixmap(QPixmap(get_path("img/" + M[1] + ".png")).scaled(int(15*adaptive_scale), int(20*adaptive_scale), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.sec_1.setPixmap(QPixmap(get_path("img/" + S[0] + ".png")).scaled(int(15*adaptive_scale), int(20*adaptive_scale), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.sec_2.setPixmap(QPixmap(get_path("img/" + S[1] + ".png")).scaled(int(15*adaptive_scale), int(20*adaptive_scale), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.scaleUI()
    
    def calcTime(self): # Time format convter
        time = count - 300
        m = int(time / 60) + time_state*4
        if(m < 0): # for 00:00 to work
            M = '00'
        elif(m < 10):
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
        self.scaleL.setGeometry(int(half_width*scale - 95*factor), int(height*scale + 40*factor), int(67.5*factor), int(20*factor))
        self.scaleM.setGeometry(int(half_width*scale - 27.5*factor), int(height*scale + 40*factor), int(67.5*factor), int(20*factor))
        self.scaleS.setGeometry(int(half_width*scale + 40*factor), int(height*scale + 40*factor), int(67.5*factor), int(20*factor))
        self.slider.setGeometry(int(half_width*scale - 50*factor), int(height*scale + 70*factor), int(100*factor), int(20*factor))
        self.figtomato.setGeometry(int(half_width*scale -75*factor), int(height*scale + 90*factor), int(67.5*factor), int(21*factor))
        self.figapple.setGeometry(int(half_width*scale + 30*factor), int(height*scale + 90*factor), int(67.5*factor), int(21*factor))
        self.calcTime()
    
    def Scale(self, new_scale):
        startpos = self.size()
        if(settings_state == 0):
            newpos = QSize(int(width*new_scale), int(height*new_scale))
            self.expand.setStartValue(startpos)
            self.expand.setEndValue(newpos)
        else:
            newpos = QSize(int(width*new_scale), int(height*new_scale + 120*factor))
            self.expand.setStartValue(startpos)
            self.expand.setEndValue(newpos)
        self.scaling.start()

    def fade_faucet(self, value):
        x = value.x()
        self.faucet.setGeometry(int(x + width*scale + 39*adaptive_scale), int(25*factor + 5*adaptive_scale + 4.5*scale), int(37.5*adaptive_scale), int(45*adaptive_scale))

    def fade_out(self):
        self.cutscene.show()
        self.cutscene.setGeometry(int(half_width*scale - 82*adaptive_scale), int(25*factor + 25*adaptive_scale + 2.5*scale), int(346*adaptive_scale), int(123*adaptive_scale))
        self.cutscene.setPixmap(QPixmap(get_path("img/fade_out_" + str(figure) +".png")).scaled(int(346*adaptive_scale), int(123*adaptive_scale), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.fade.setDuration(500)
        self.fade.setEasingCurve(QEasingCurve.OutQuad)
        self.fade.setStartValue(QRect(int(half_width*scale - 82*adaptive_scale), int(25*factor + 25*adaptive_scale + 2.5*scale), int(346*adaptive_scale), int(123*adaptive_scale)))
        self.fade.setKeyValueAt(0.2, QRect(int(half_width*scale - 72*adaptive_scale), int(25*factor + 25*adaptive_scale + 2.5*scale), int(346*adaptive_scale), int(123*adaptive_scale)))
        self.fade.setEndValue(QRect(int(-164*adaptive_scale), int(25*factor + 25*adaptive_scale + 2.5*scale), int(346*adaptive_scale), int(123*adaptive_scale)))
        self.fade.start()
    
    def fade_in(self):
        self.cutscene.show()
        self.cutscene.setGeometry(int(-164*adaptive_scale), int(25*factor + 25*adaptive_scale + 2.5*scale), int(346*adaptive_scale), int(123*adaptive_scale))
        self.cutscene.setPixmap(QPixmap(get_path("img/fade_in_" + str(figure) +".png")).scaled(int(346*adaptive_scale), int(123*adaptive_scale), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.fade.setDuration(800)
        self.fade.setEasingCurve(QEasingCurve.OutQuad)
        self.fade.setStartValue(QRect(int(-164*adaptive_scale), int(25*factor + 25*adaptive_scale + 2.5*scale), int(346*adaptive_scale), int(123*adaptive_scale)))
        self.fade.setKeyValueAt(0.8, QRect(int(half_width*scale - 72*adaptive_scale), int(25*factor + 25*adaptive_scale + 2.5*scale), int(346*adaptive_scale), int(123*adaptive_scale)))
        self.fade.setEndValue(QRect(int(half_width*scale - 82*adaptive_scale), int(25*factor + 25*adaptive_scale + 2.5*scale), int(346*adaptive_scale), int(123*adaptive_scale)))
        self.fade.start()
class Bar(QWidget):
    clickPos = None
    def __init__(self, parent):
        super().__init__(parent)
        self.setAutoFillBackground(True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addStretch()

        self.title = QLabel("")
        # if setPalette() was used above, this is not required
        self.title.hide()

        style = self.style()
        ref_size = self.fontMetrics().height()
        ref_size += style.pixelMetric(style.PM_ButtonMargin)*1.2
        ref_size = int(ref_size)
        self.setMaximumHeight(ref_size + 2)

        btn_size = QSize(ref_size, ref_size)
        for target in ('min', 'normal', 'close'):
            btn = QToolButton(self, focusPolicy=Qt.NoFocus)
            layout.addWidget(btn)
            btn.setFixedSize(btn_size)
            btn.lower()

            iconType = getattr(style, 
                'SP_TitleBar{}Button'.format(target.capitalize()))
            btn.setIcon(style.standardIcon(iconType))

            if target == 'close':
                colorNormal = bg_color
                colorHover = '#c73030'
                radius = corner_radius
            else:
                colorNormal = bg_color
                colorHover = bg_hover
                radius = 0
            btn.setStyleSheet('''
                QToolButton {{
                    background-color: {};
                    border: none;
                }}
                QToolButton:hover {{
                    background-color: {};
                    border: none;
                    border-radius: 0px;
                    border-top-right-radius: {};
                }}
            '''.format(colorNormal, colorHover, radius))
            
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

QT_SCALE_FACTOR=0
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
        time_state = -1
        window.fade_out()
    elif(count == 299):
        window.cutscene.hide()
        time_state = 1
        window.calcTime()
        aniTimer.start(42)

    elif(count == 0):
        time_state = -1
        aniTimer.stop()
        window.fade_in()
    elif(count < 0):
        timer.stop()
        window.cutscene.setGeometry(int(-164*adaptive_scale), int(10*factor + 25*adaptive_scale + 2.5*scale), int(346*adaptive_scale), int(123*adaptive_scale))
        window.cutscene.hide()
        count = 1800
        time_state = 0
        rstTimer.start(1)
    window.update()

def reset(): # Timer reset
    global count
    if(count >= 1799):
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

def animation():
    global frame
    frame += 1
    frame %= 40
    window.update()
    

window.calcTime()
timer = QTimer()
timer.timeout.connect(tic)

rstTimer = QTimer()
rstTimer.timeout.connect(reset)

sTimer = QTimer()
sTimer.timeout.connect(rotate)

aniTimer = QTimer()
aniTimer.timeout.connect(animation)

T = QThread()
T.run = timer
T.run = rstTimer
T.start()

sys.exit(app.exec_())