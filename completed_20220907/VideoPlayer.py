import sys
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QFileDialog, QLabel,QPushButton,
                             QHBoxLayout, QVBoxLayout,
                             QSizePolicy, QSlider, QStyle,  
                             QMainWindow,QAction)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (Qt,
                          QUrl,QDir) 
#__________________________________________________________________________________
class VideoPlayer(QMainWindow):
    def __init__(self,fname):
        super().__init__()
        self.setWindowTitle("PyQt5 Video Player")  
        self.fname = fname
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()  
        
        #--------[button]play
        self.playButton = QPushButton()
        self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(self.fname)))
        self.playButton.setEnabled(True)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.playButton.clicked.connect(self.play)
        self.play()#changed to automatically play 
        #-------[slider]position
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        #------[lb]err
        self.error = QLabel()
        self.error.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        """
        #------[button]open
        openButton = QPushButton("Open Video")   
        openButton.setToolTip("Open Video File")
        openButton.setStatusTip("Open Video File")
        openButton.setFixedHeight(24)
        openButton.clicked.connect(self.openFile)
        """
 
        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)
 
        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
 
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.error)
        #layout.addWidget(openButton)
 
        # Set widget to contain window contents
        wid.setLayout(layout)
 
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
 
    def exitCall(self):
        sys.exit(app.exec_())
 
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
 
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))
 
    def positionChanged(self, position):
        self.positionSlider.setValue(position)
 
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
 
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
 
    def handleError(self):
        self.playButton.setEnabled(False)
        self.error.setText("Error: " + self.mediaPlayer.errorString())
 
    """
app = QApplication(sys.argv)
videoplayer = VideoPlayer()
videoplayer.resize(640, 480)
videoplayer.show()
sys.exit(app.exec_())
    """
