import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os
import numpy as np
import auditok
from pydub import AudioSegment
import speech_recognition as sr
from moviepy import editor
import cv2 as cv

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



class ListViewDemo(QWidget):
    def __init__(self, parent = None):
        super(ListViewDemo, self).__init__(parent)
        self.setWindowTitle('智慧影音接軌')
        self.resize(450,500)
        self.initUI()
       
    def initUI(self):
        layout = QVBoxLayout()
        self.listWidget = QListWidget()

        self.buttonOpenFile = QPushButton('Select File')
        self.buttonOpenFile.clicked.connect(self.LoadPath) 
        layout.addWidget(self.buttonOpenFile)

        self.buttonRemoveFile = QPushButton('Remove File')
        self.buttonRemoveFile.clicked.connect(self.RemovePath)
        layout.addWidget(self.buttonRemoveFile)

        self.buttonRemoveAll = QPushButton('Remove All')
        self.buttonRemoveAll.clicked.connect(self.DelListItem)
        layout.addWidget(self.buttonRemoveAll)

        self.listview = QListView()
        #建立一個空的模型
        self.listModle = QStringListModel()
        #self.list = ["列表項1", "列表項2", "列表項3"]
         #將數據放到空的模型內
        #self.listModle.setStringList(self.list)
        self.listview.setModel(self.listModle)
        layout.addWidget(self.listview)

        self.combobox = QComboBox()
        self.combobox.setItemText(3, "Tw")
        layout.addWidget(self.combobox)

        self.buttonClip = QPushButton('Edit Video')
        self.buttonClip.clicked.connect(self.VideoEdit)
        layout.addWidget(self.buttonClip)

        self.buttonClip = QPushButton('Generate Subtitle')
        self.buttonClip.clicked.connect(self.GenerateSubtitle)
        layout.addWidget(self.buttonClip)


        self.setLayout(layout)
    

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

    def VideoEdit(self):
        # mp4 轉成 wav -----------------------------
        #inputfile = "media/tainanvlog.mp4"
        row = self.listModle.rowCount()
        for i in range(row):
            source_file = self.listModle.stringList()[i]
            slash_pos = source_file.rfind('/')
            dot_pos = source_file.rfind('.')
            source_path, source_name, source_format = source_file[:slash_pos+1], source_file[slash_pos+1:dot_pos], source_file[dot_pos:]
            wavfile = source_path + source_name + '.wav'
            outfile = source_path + source_name + '_out.mp4'


            if not os.path.exists(wavfile):
                os.system("ffmpeg -i "+source_file+" "+source_path + source_name + '.wav')


            #轉灰階--------------------------------------
            clip = editor.VideoFileClip(source_file)
            gray_scalar = []
            for frames in clip.iter_frames():
                gray = cv.cvtColor(frames, cv.COLOR_BGR2GRAY)
                # cv.imshow("gray", gray) #播放灰階影片
                gray_scalar.append(gray)
                key = cv.waitKey(1)
                if key == ord("q"):
                    break

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
            cut=1

            for i, r in enumerate(audio_regions):
                record_start[i] = r.meta.start
                record_end[i] = r.meta.end
                num = num+1

            for j in range(num-1):
                # evaluate silence section length
                silence_duration[j] = record_start[j+1] - record_end[j]
                print("Silence ", j, " :", round(record_end[j], 3), 's', 'to', round(record_start[j+1], 3), 's, Duration : ', silence_duration[j])

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
                            print("Instruction : 剪接")                
            # 偵測重複 ----------------------------------
                            min = 100000000000
                            
                            # 抓影片前5秒進行辨識
                            before_ins_end = int(record_end[j-1])      #指令前的結束時間
                            if (before_ins_end-5) < 0 :
                                before_ins_start=0
                            else :
                                before_ins_start = before_ins_end-5    #指令前的起始時間
                            
                            after_ins_start = float(record_start[j+1]) # 指令後的起始時間
                            
                            for i in range(5*fps):
                                before_ins = gray_scalar[before_ins_start*fps+i]
                                after_ins = gray_scalar[round(after_ins_start*fps)]
                                
                                d = (before_ins-after_ins)**2
                                
                                if min > d.sum():
                                    cutpoint = (before_ins_start*fps+i)/fps 
                                    min = d.sum()
                                #print('t : ', round(before_ins_start*fps+i+j, 1)/fps,' ', d.sum())          
                            #輸出最相近
                            print(cutpoint, min)
            # 剪接 -------------------------------------
                            if cut != 1 :
                                file = final_clip
                            else :
                                file = source_file
                                cut+=1

                            clip1 = editor.VideoFileClip(file).subclip(0, cutpoint)
                            clip2 = editor.VideoFileClip(file).subclip(after_ins_start, )
                            final_clip = editor.concatenate_videoclips([clip1, clip2])
                        else:
                            print(ins,'pass')
                            pass

                    except sr.UnknownValueError:   
                        ins = "無法翻譯"
                    except sr.RequestError as e:
                        ins = "無法翻譯{0}".format(e)

            final_clip.write_videofile(outfile)
            final_clip.close()

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
    app.setWindowIcon(QIcon('./resources/firefox-icon-02.png'))
    win = ListViewDemo()
    win.show()
    sys.exit(app.exec_())