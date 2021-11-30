import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os
import numpy as np
import auditok
from pydub import AudioSegment
import speech_recognition as sr
from moviepy.editor import *
from moviepy import editor
import cv2 as cv
import subprocess

class Subtitle:
    def __init__(self, time_start, time_end, string=' '):
        self.time_start = time_start
        self.time_end = time_end
        self.string = string

    def split(self):
        # yet using time library
        former_timestart = self.time_start
        former_timeend = self.get_mid_time(self.time_start, self.time_end)
        former_string = self.string[:len(self.string)//2] + '\n'
        latter_timestart = self.get_mid_time(self.time_start, self.time_end)
        latter_timeend = self.time_end
        latter_string = self.string[len(self.string)//2:]

        return Subtitle(former_timestart, former_timeend, former_string), Subtitle(latter_timestart, latter_timeend, latter_string)

    @classmethod
    def get_mid_time(cls, time_start, time_end):
        h1, m1, s1, ms1 = time_start[0:2], time_start[3:5], time_start[6:8], time_start[9:]
        h2, m2, s2, ms2 = time_end[0:2], time_end[3:5], time_end[6:8], time_end[9:]
        ss1 = int(h1) * 60 * 60 + int(m1) * 60 + int(s1) 
        ss2 = int(h2) * 60 * 60 + int(m2) * 60 + int(s2)
        dur = (ss2 - ss1)//2

        rh = int(h1) + dur // 3600
        dur %= 3600
        rm = int(m1) + dur // 60
        dur %= 60
        rs = int(s1) + dur
        
        return str(rh).zfill(2) + ':' + str(rm).zfill(2) + ':' + str(rs).zfill(2) + ',' + '000'


sec = 0

class WorkThread(QThread):
    timer = pyqtSignal() # 每隔一秒發送一次信號
    end = pyqtSignal()   # 技術完成後發送一次信號
    def run(self):
        while True:
            self.sleep(1) # 休眠一秒
            if sec == 100:
                self.end.emit() # 發送end信號
                break;
            self.timer.emit()  # 發送timer信號

class ListViewDemo(QWidget):
    def __init__(self, parent = None):
        super(ListViewDemo, self).__init__(parent)
        self.setWindowTitle('智慧影音接軌')
        self.resize(450,500)
        self.initUI()
       
    def initUI(self):
        layout = QVBoxLayout()
        self.listWidget = QListWidget()

        # 按鈕選擇檔案
        self.buttonOpenFile = QPushButton('Select File')
        self.buttonOpenFile.clicked.connect(self.LoadPath) 
        layout.addWidget(self.buttonOpenFile)

        # 按鈕移除檔案
        self.buttonRemoveFile = QPushButton('Remove File')
        self.buttonRemoveFile.clicked.connect(self.RemovePath)
        layout.addWidget(self.buttonRemoveFile)


        self.buttonRemoveAll = QPushButton('Empty List')

        self.buttonRemoveAll.clicked.connect(self.DelListItem)
        layout.addWidget(self.buttonRemoveAll)

        # 建立選取影片列表
        self.listview = QListView()       
        self.listModle = QStringListModel() #建立一個空的模型
        #self.list = ["列表項1", "列表項2", "列表項3"]
         #將數據放到空的模型內
        #self.listModle.setStringList(self.list)
        self.listview.setModel(self.listModle)
        layout.addWidget(self.listview)

        # 選擇語言
        #self.combobox = QComboBox()
        #self.combobox.setItemText(3, "Tw")
        #layout.addWidget(self.combobox)

        # 按鈕編輯影片
        self.buttonClip = QPushButton('Edit Video')
        self.buttonClip.clicked.connect(self.lable)

        self.buttonClip.clicked.connect(self.VideoEdit)
        layout.addWidget(self.buttonClip)


        self.buttonSub = QPushButton('Generate Subtitle')
        self.buttonSub.clicked.connect(self.GenerateSubtitle)
        self.buttonSub.clicked.connect(self.lable)
        layout.addWidget(self.buttonSub)

        self.statusLabel = QLabel()
        #self.statusLabel.setText("            ")

        self.statusbar = QStatusBar(self)
        layout.addWidget(self.statusbar)

        self.progressBar = QProgressBar()
        self.progressBar.setRange(0,100)
        #layout.addWidget(self.progressBar)
        self.statusbar.addPermanentWidget(self.statusLabel, stretch=2)
        self.statusbar.addPermanentWidget(self.progressBar, stretch=10)
        
        self.workThread = WorkThread()

        self.workThread.timer.connect(self.countTime)
        self.setLayout(layout)

    def countTime(self):
        global sec
        sec += 1
        self.statusLabel.setText(str(sec))
        self.progressBar.setValue(sec)

    def work(self):
        self.workThread.start() 
      

    def LoadPath(self):
        fname,_ = QFileDialog.getOpenFileName(self, '打開文件', '.', '文件(*.MOV *.mp4)')
        if len(fname) != 0 :
            row = self.listModle.rowCount()  # 獲得最後一行的行數       
            self.listModle.insertRow(row)  # 數據模型添加行
            index = self.listModle.index(row,0)  # 獲得數據模型的索引
            self.listModle.setData(index,fname) 
        print(self.listModle.stringList())
            
    def RemovePath(self):
        selected  = self.listview.selectedIndexes() # 根據所有獲取item
        for i in selected:
            self.listModle.removeRow(i.row())
    
    def DelListItem(self):
        row1 = self.listModle.rowCount()
        for i in range(row1):
            self.listModle.removeRow(self.listview.modelColumn())

    def lable(self):
        row = self.listModle.rowCount()
        if row == 1:
            self.statusLabel.setText('影片製作中...')
            QMessageBox.information(self,'Message','幫你製作影片',QMessageBox.Ok)
            print('影片製作中...')
        if row == 0:
            QMessageBox.information(self,'Message','請選擇影片',QMessageBox.Ok)
            #self.statusLabel.setText('選擇影片')

    

    def VideoEdit(self):
        # mp4 轉成 wav -----------------------------
        #inputfile = "media/tainanvlog.mp4"
        row = self.listModle.rowCount()
        print(row)
        for i in range(row):   
            self.buttonClip.setEnabled(False)
            self.statusLabel.setText('影片')
            source_file = self.listModle.stringList()[i]
            slash_pos = source_file.rfind('/')
            dot_pos = source_file.rfind('.')
            source_path, source_name, source_format = source_file[:slash_pos+1], source_file[slash_pos+1:dot_pos], source_file[dot_pos:]
            wavfile = source_path + source_name + '.wav'     # 執行完刪除 *wav
            outfile = source_path + source_name + '_out.mp4' # 把檔案存在自己想要的地方
            

            if not os.path.exists(wavfile):
                os.system("ffmpeg -i "+source_file+" "+source_path + source_name + '.wav')

            # 找出fps---------------------------------------
            clip = cv.VideoCapture(source_file)
            fps = clip.get(cv.CAP_PROP_FPS)
            fps = round(fps,)       
            clip.release()

            # 測試靜音 ----------------------------------
            # split returns a generator of AudioRegion objects
            sound = AudioSegment.from_file(wavfile, format="wav") 
            audio_regions = auditok.split(
                wavfile,
                min_dur=0.2,         # minimum duration of a valid audio event in seconds
                max_dur=100,         # maximum duration of an event
                max_silence=2,       # maximum duration of tolerated continuous silence within an event
                energy_threshold=50  # threshold of detection
            )

            record_start = np.zeros(1000)
            record_end = np.zeros(1000)
            silence_duration = np.zeros(1000)
            speech_duration = np.zeros(1000)
            num = 0
            ins_loca=[]
            subclip_sec=[]

            for i, r in enumerate(audio_regions):
                record_start[i] = r.meta.start
                record_end[i] = r.meta.end
                num = num+1

            for j in range(num-1):
                # evaluate silence section length
                silence_duration[j] = record_start[j+1] - record_end[j]
                print("Silence ", j, " :", round(record_end[j], 3), 's', 'to', round(record_start[j+1], 3), 's, Duration : ', round(silence_duration[j],3))

                # if there are two continuous silence sections >2.5 
                if silence_duration[j-1] > 1.4 and silence_duration[j] > 1.4 and speech_duration[j] < 5.0:
                    #print("instruction : ", round(record_start[j], 3), 's', 'to', round(record_end[j], 3), 's')

            # 辨識是否為語音指令“剪接” ---------------------------
                    r = sr.Recognizer()
                    instruction = sr.AudioFile(wavfile)
                    with instruction as source:
                        audio = r.record(source, offset = record_start[j], duration = 5)
                    try:
                        ins = r.recognize_google(audio_data=audio, key=None,language="zh-TW", show_all=True)
                        if "剪接" in str(ins):
                            print("instruction ", round(record_start[j], 3), 's to', round(record_end[j], 3), 's'," : 剪接")      

                            # 抓影片前5秒進行辨識
                            before_ins_end = int(record_end[j-1])      #指令前的結束時間
                            if (before_ins_end-5) < 0 :
                                before_ins_start=0
                                sec = float(before_ins_end)
                            else :
                                before_ins_start = before_ins_end-5    #指令前的起始時間
                                sec = 5
                            
                            after_ins_start = float(record_start[j+1]) # 指令後的起始時間
                            print('往前抓＿秒進行辨識:',sec)
                                    
                            ins_loca.append(float(before_ins_start))
                            ins_loca.append(float(after_ins_start))
                        
                        else:
                            print(ins,'pass')
                            pass
                    
                    except sr.UnknownValueError:   
                        ins = "無法翻譯"
                    except sr.RequestError as e:
                        ins = "無法翻譯{0}".format(e)
                            
            for i in range(1,len(ins_loca)-1,2):
                if ins[i]> ins[i+1]:
                    del ins[i]
                    del ins[i+1]
            print('ins:',ins_loca)

                                    
        # 轉灰階--------------------------------------
            for i in range(0,len(ins_loca)-1,2):
                grayclip = VideoFileClip(source_file).subclip(round(ins_loca[i],2),round(ins_loca[i+1],2))
                gray_scalar = []
                for frames in grayclip.iter_frames():
                    gray = cv.cvtColor(frames, cv.COLOR_BGR2GRAY)
                    #cv.imshow("gray", gray) #播放灰階影片
                    gray_scalar.append(gray)
                    key = cv.waitKey(1)
                    if key == ord("q"):
                        break;
                print('轉灰階成功clip :', round(before_ins_start,2),'s - ', round(after_ins_start,2),'s ')        
                #print(len(gray_scalar))
            
            # 偵測重複 ----------------------------------
                min = 100000000000
                
                for i in range(sec*fps):
                    before_ins = gray_scalar[i]
                    after_ins = gray_scalar[len(gray_scalar)-1]
                    
                    d = (before_ins-after_ins)**2
                    
                    if min > d.sum():
                        cutpoint = (before_ins_start*fps+i)/fps 
                        min = d.sum()
                    #print('t : ', round(before_ins_start*fps+i+j, 1)/fps,' ', d.sum())          
                #輸出最相近
                print(cutpoint, min)
                subclip_sec.append(float(cutpoint))
                subclip_sec.append(float(after_ins_start))

            subclip_sec.insert(0, 0)
            subclip_sec.append(' ')
            print('subclip[(from_t, to_t)]:',subclip_sec)

            # 剪接 -------------------------------------
            clips = []
            for i in range(0,len(subclip_sec),2):
                if i == (len(subclip_sec)-2):
                    clip = VideoFileClip(source_file).subclip(subclip_sec[i], )
                    #print("subclip(",subclip_sec[i],", )")  
                else:
                    clip = VideoFileClip(source_file).subclip(subclip_sec[i], subclip_sec[i+1])
                    #print("subclip(",subclip_sec[i],", ",subclip_sec[i+1],")")  
                clips.append(clip)
            print ('sub: ', clips)
            final_clip = concatenate_videoclips(clips)
            final_clip.write_videofile(outfile)
            final_clip.close()
            self.statusLabel.setText('影片剪接完成')
            vlc = "/Applications/VLC.app/Contents/MacOS/VLC"
            p1 =subprocess.run ([''+vlc+'', ''+outfile+'',  'vlc://quit'])
            print(p1)


    
    def GenerateSubtitle(self):
        for i in range(self.listModle.rowCount()):
            source_file = self.listModle.stringList()[i]
            slash_pos = source_file.rfind('/')
            dot_pos = source_file.rfind('.')
            source_path, source_name, source_format = source_file[:slash_pos+1], source_file[slash_pos+1:dot_pos], source_file[dot_pos:]

            source_name += '_out'
            source_file = source_path+source_name+source_format
            source_clip = editor.VideoFileClip(source_file)

            if not os.path.exists(source_path + source_name + '.srt'):
                os.system("autosub -S zh-CN -D zh-CN " + source_file)

            # read the srt file
            subtitle_file = open(source_path + source_name + '.srt')
            subtitle_line = subtitle_file.readlines()
            subtitle_file.close()

            subtitle_list = []
            for index in range(0, len(subtitle_line), 4):
                string = subtitle_line[index + 2]
                time_start = subtitle_line[index + 1][:12]
                time_end = subtitle_line[index+1][17:29]
                subtitle_list.append(Subtitle(time_start, time_end, string))

            # handling subtitle go out of screen
            for index in range(len(subtitle_list)):
                if 25 < len(subtitle_list[index].string):
                    former, latter = subtitle_list[index].split()
                    subtitle_list[index] = former
                    subtitle_list.insert(index+1, latter)


            # add clip without subtitle into subtitle_list
            i = 0
            while i < len(subtitle_list) - 1:
                if subtitle_list[i].time_end < subtitle_list[i+1].time_start:
                    time_start = subtitle_list[i].time_end
                    time_end = subtitle_list[i+1].time_start
                    subtitle_list.insert(i+1, Subtitle(time_start, time_end))
                    i += 1

                i += 1

            def export_srt_file(subtitle_list, filename=source_name+'_new', filepath=source_path):
                f = open(filepath+filename+'.srt', 'w')

                for i in range(len(subtitle_list)):
                    f.write(str(i) + '\n')
                    f.write(subtitle_list[i].time_start + ' --> ' + subtitle_list[i].time_end + '\n')
                    f.write(subtitle_list[i].string + '\n')

                f.close()

            export_srt_file(subtitle_list)
            print('Done: New srt file exported')
                
            FONT_URL="./resources/GenJyuuGothicL-Medium.ttf"
            def annotate(clip, txt, txt_color='black', fontsize=50, font='Xolonium-Bold'):
                """ Writes a text at the bottom of the clip. """
                txtclip = editor.TextClip(txt, fontsize=fontsize, font=FONT_URL, color=txt_color)
                cvc = editor.CompositeVideoClip([clip, txtclip.set_pos(('center', 'bottom'))])
                return cvc.set_duration(clip.duration)

            # bind subtitle file into video stream
            annotated_clips = []
            for subtitle in subtitle_list:
                annotated_clips.append(annotate(source_clip.subclip(subtitle.time_start, subtitle.time_end), subtitle.string))

            final_clip = editor.concatenate_videoclips(annotated_clips)
            final_clip.write_videofile(source_name + "_with_subtitle.mp4")

if __name__ == "__main__" :   
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./PyQt5/1179069.png'))
    win = ListViewDemo()
    win.show()
    
    sys.exit(app.exec_())