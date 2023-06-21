###################
# labelling using pyqt5 hyoyeon version
# open : select mp4 file -> setText on line_open 
# next : next file       -> setText on line_open
# prev : prev file       -> setText on line_open
# play : whenever line_open changed
###################
import csv
import numpy as np
from datetime import datetime
import sys
import io
import glob
from VideoPlayer import *
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, 
                             QPushButton,  QCheckBox, QButtonGroup, 
                             QLineEdit, QTextEdit, 
                             QFileDialog, QMessageBox,
                             QHBoxLayout, QVBoxLayout,
                             QSpinBox, QComboBox,
                             QFormLayout,
                             QGridLayout)
from PyQt5.QtGui  import QFont
from PyQt5.QtCore import *

status = ["주행", "정지", "모름"]
_status = ["Driving", "Stop", "DontKnow"]



category_normal = "정상"
categories = [  "고개돌림", "길게폰응시",   "꾸벅거림",   "눈감음",
                "담배",    "뒤돌아봄",     "멍때림",     "시야돌림",  
                "양손이탈", "웃음",        "위를봄",     "음식섭취",  
                "졸림",     "좌석이탈",    "주차",       "짧게폰응시",    
                "폰사용",   "하품",        "한손운전",   "해당없음" ]
_category_normal = "normal"
_categories = ["FaceOffFront","SeePhoneLong", "FaceDown", "Sleep",
               "Smoking",     "SeeBack",      "MicSleep", "EyeOffFront",
               "NoHand",      "Smile",        "SeeUp",    "Eating", 
               "Drowsy",      "NoDriver",     "SeeRCam",  "SeePhoneShort",  
               "UsePhone",    "Yawning",      "OneHand",  "Unknown" ]
#________________________________________________________________
class Test(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()
    def initializeUI(self):
        self.setGeometry(200,200,500,500)
        self.setWindowTitle("File")
        self.displayWidgets()
        self.fnames = []
        self.fidx = None
        self.fname = None
        self.fname_csv=None
        self.fpoint = None
        self.opts = []
        self.normal = "True"
        self.status = None
    def displayWidgets(self):
        #------file select
        #   csv
        self.lb_csv = QLabel("[CSV]")
        self.bt_open_csv = QPushButton("Open",self)
        self.bt_open_csv.clicked.connect(self.setFileCSV)
        self.bt_create_csv = QPushButton("Create",self)
        self.bt_create_csv.clicked.connect(self.setFileCSV)
        self.line_open_csv = QLineEdit()
        boxH_open_csv = QHBoxLayout()
        boxH_open_csv.setSpacing(30)
        boxH_open_csv.addWidget(self.lb_csv)
        boxH_open_csv.addWidget(self.bt_create_csv)
        boxH_open_csv.addWidget(self.bt_open_csv)
        boxH_open_csv.addWidget(self.line_open_csv)
        #   mp4
        self.lb_mp4 = QLabel("[MP4]")
        self.bt_open = QPushButton("Open",self)
        self.bt_open.clicked.connect(self.setFileNames)
        self.line_open = QLineEdit()
        boxH_open = QHBoxLayout()
        boxH_open.setSpacing(30)
        boxH_open.addWidget(self.lb_mp4)
        boxH_open.addWidget(self.bt_open)
        boxH_open.addWidget(self.line_open)
        #-------Driving Status
        boxH_status = QHBoxLayout()
        boxH_status.addStretch()
        btG_status = QButtonGroup(self)
        btG_status.setExclusive(True)
        self.reset_status = btG_status
        for i in range (0,len(status)):
            bt_name = status[i]
            self.bt_op = QPushButton(bt_name)
            self.bt_op.setStyleSheet("background-color:white")
            self.bt_op.setFixedSize(QSize(100, 40))
            self.bt_op.setFont(QFont('Arial', 11))
            boxH_status.addWidget(self.bt_op)
            btG_status.addButton(self.bt_op)
            btG_status.setId(self.bt_op,i)
        boxH_status.addStretch()
        btG_status.buttonClicked.connect(self.buttonClicked_status)
        
        
        #------options
        boxV_opts = QVBoxLayout()
        btG_opts = QButtonGroup(self)
        self.reset = btG_opts
        for i in range (0,5):
            boxH_temp = QHBoxLayout()
            boxH_temp.addStretch()
            for j in range(0,4):
                idx=i*4+j
                bt_name = categories[idx]
                self.bt_op = QPushButton(bt_name)
                self.bt_op.setStyleSheet("background-color:white")
                self.bt_op.setFixedSize(QSize(100, 40))
                self.bt_op.setFont(QFont('Arial', 11))
                boxH_temp.addWidget(self.bt_op)
                btG_opts.addButton(self.bt_op)
                btG_opts.setId(self.bt_op,idx)
            boxH_temp.addStretch()
            boxV_opts.addLayout(boxH_temp)
        btG_opts.buttonClicked.connect(self.buttonClicked_opts)
        #------file next/prev
        self.bt_prev = QPushButton("이전",self)
        self.bt_prev.setFixedSize(QSize(100, 40))
        self.bt_prev.setFont(QFont('Arial', 14))
        self.bt_submit      = QPushButton("제출",self)
        self.bt_submit.setFixedSize(QSize(100, 40))
        self.bt_submit.setFont(QFont('Arial', 14))
        self.bt_next      = QPushButton("다음",self)
        self.bt_next.setFixedSize(QSize(100, 40))
        self.bt_next.setFont(QFont('Arial', 14))
        
        
        boxH_prevnext = QHBoxLayout()
        boxH_prevnext.addStretch()
        #boxH_prevnext.setSpacing(100)
        btG_prevnext  = QButtonGroup(self)
        #boxH_prevnext.addStretch()
        boxH_prevnext.addWidget(self.bt_prev)
        btG_prevnext.addButton(self.bt_prev)
        #boxH_prevnext.addStretch()
        boxH_prevnext.addWidget(self.bt_submit)
        btG_prevnext.addButton(self.bt_submit)
        #boxH_prevnext.addStretch()
        boxH_prevnext.addWidget(self.bt_next)
        btG_prevnext.addButton(self.bt_next)
        boxH_prevnext.addStretch()
        btG_prevnext.buttonClicked.connect(self.buttonClicked)
        ###################################################################
        boxV_main = QVBoxLayout()       
        boxV_main.addLayout(boxH_open_csv)
        boxV_main.addStretch(1)
        boxV_main.addLayout(boxH_open)
        boxV_main.addStretch(1)
        boxV_main.addLayout(boxH_status)
        boxV_main.addStretch(1)
        boxV_main.addLayout(boxV_opts)
        boxV_main.addStretch(2)
        boxV_main.addLayout(boxH_prevnext)
        boxV_main.addStretch(1)
        ###################################################################
        self.setLayout(boxV_main)
        
    def setFileCSV(self):
        sender = self.sender()
        txt = sender.text()
        if txt == "Open":
            f, _ = QFileDialog.getOpenFileName(self,'Open File',"",
                                          "CSV Files(*.csv)",
                                          options = QFileDialog.Options())
        elif txt == "Create":
            f, _ = QFileDialog.getSaveFileName(self,'Create File',"",
                                              "CSV Files(*.csv)")
            if not f:
                return
            with open(f,'w') as file_csv:
                header ="file name, Driving Status, " + _category_normal + ", " + ", ".join(_categories) + "\n"
                file_csv.write(header)
                
        self.fname_csv = f
        self.line_open_csv.setText(f)
        if txt=="Open":
            with open(f,'r') as file_csv:
                fn = file_csv.readlines()[-1].split(',')[0]
            temp = fn.split('/')
            temp = temp[0:len(temp)-1]
            folder =""
            for i in temp:
                folder = folder+i+'/'
            lists = glob.glob(folder+'*')
            final = []
            for i in lists:
                word = i.split('.')[-1] 
                if word== 'mp4':
                    final.append(i.replace("\\",'/'))  ## windows only
            final.sort()
            self.fnames = final
            self.fidx = final.index(fn)+1
            if self.fidx>len(final)-1:
                msg_ferr = QMessageBox.question(self,"no more file","최근 작업파일이 마지막입니다.\nClose?",
                                               QMessageBox.No|QMessageBox.Yes,
                                               QMessageBox.Yes)
                if msg_ferr == QMessageBox.Yes:
                    if self.fname is not None:
                        self.videoplayer.close()
                    self.close()
                    return
                else: 
                    return
            self.fname = self.fnames[self.fidx]
            self.line_open.setText(self.fname)
            self.play_video()
            
    def setFileNames(self):
        f, _ = QFileDialog.getOpenFileName(self,'Open File',"",
                                         "Video Files(*.mp4)",
                                           options=QFileDialog.Options())
        temp = f.split('/')
        temp = temp[0:len(temp)-1]
        folder =""
        for i in temp:
            folder = folder+i+'/'
        lists = glob.glob(folder+'*')
        final = []
        for i in lists:
            word = i.split('.')[-1] 
            if word== 'mp4':
                final.append(i.replace("\\",'/'))  ## windows only
        final.sort()
        self.fnames = final
        self.fidx = final.index(f)
        self.fname = self.fnames[self.fidx]
        self.line_open.setText(self.fname)
        self.play_video()
        
        
        
    def buttonClicked(self,btG_prevnext):
        t = btG_prevnext.text()
        if t=="제출":
            if self.status is None or self.fname is None or self.fname_csv is None:
                messages = ""
                if self.fname_csv is None:
                    messages = messages+"[에러] csv파일 미선택\n"
                if self.fname is None:
                    messages = messages+"[에러] 영상 미선택\n"      
                if self.status is None:
                    messages = messages+"[에러] 주행상태 미선택.\n"
                msg_ferr = QMessageBox.question(self,"Error",messages+"Close?",
                                               QMessageBox.No|QMessageBox.Yes,
                                               QMessageBox.Yes)
                if msg_ferr == QMessageBox.Yes:
                    if self.fname is not None:
                        self.videoplayer.close()
                    self.close()
                    return
                else: 
                    return
            #--------------find the right row in csv file to write the result    
            for i in range(0,len(status)):
                self.reset_status.button(i).setStyleSheet("background-color:white")
            for i in range(0,len(categories)):
                self.reset.button(i).setStyleSheet("background-color:white")
            
            if len(self.opts)==0:
                self.normal = "True"
            else:
                self.normal = "False"
            output = [self.fname,_status[status.index(self.status)],self.normal]
            for i in range(0,len(categories)):
                if categories[i] in self.opts:
                    output.append("True")
                else:
                    output.append("False")
            print(output)
            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            lines=[]
            fs = []
            search=self.fname
            with open(self.fname_csv,'r') as file_csv:
                reader = csv.reader(file_csv)
                for line in reader:
                    lines.append(line)
                    fs.append(line[0])
            #print(idx)
            if search in fs:
                idx = fs.index(search)
                lines[idx] = output
            else:
                idx = len(fs)
                lines.append(output)
            print ("history",idx)
            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            
            content=""
            for i in lines:
                content =content+','.join(i)+"\n"
            
            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            with open(self.fname_csv,'w') as file_csv:
                file_csv.write(content)                
            self.opts = []
            self.normal = "True"
            self.status = None
            print("Submitted!!!")
            ################
            msg_ferr = QMessageBox.question(self,"다음으로 넘어갈까요?","[ Y ] 엔터",
                                               QMessageBox.No|QMessageBox.Yes,
                                               QMessageBox.Yes)
            if msg_ferr == QMessageBox.Yes:
                t = "다음"
            else: 
                return
        ################################################################
        increment = {"이전":-1, "다음":1}
        message= {"이전":"이전파일 없음","다음":"다음파일 없음"}
        #t = btG_prevnext.text()
        if self.fidx+increment[t] <0 or self.fidx+increment[t]>=len(self.fnames):
            msg_ferr = QMessageBox.question(self,message[t],"Close?",
                                               QMessageBox.No|QMessageBox.Yes,
                                               QMessageBox.Yes)
            if msg_ferr == QMessageBox.Yes:
                self.videoplayer.close()
                self.close()
            else: 
                pass
        else:
            self.fidx = self.fidx + increment[t]
            self.fname = self.fnames[self.fidx]
            self.line_open.setText(self.fname)
            self.play_video()
    def buttonClicked_opts(self,btG_opts):
        t = btG_opts.text()
        if t not in self.opts:
            btG_opts.setStyleSheet("background-color:yellow")
            self.opts.append(t)
        else:
            btG_opts.setStyleSheet("background-color:white")
            self.opts.remove(t)
    def buttonClicked_status(self,btG_status):
        for i in range(0,len(status)):
            self.reset_status.button(i).setStyleSheet("background-color:white")           
        t = btG_status.text()
        if t != self.status:
            btG_status.setStyleSheet("background-color:red")
            self.status = t
        else:
            btG_status.setStyleSheet("background-color:white")
            self.status = None
    def play_video(self):
        self.videoplayer = VideoPlayer(self.fname)
        self.videoplayer.resize(640, 480)
        self.videoplayer.show()
     