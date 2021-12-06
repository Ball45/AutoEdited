import os, time, cv2, sys, auditok, traceback
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import speech_recognition as sr
from moviepy.editor import *
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

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done
    

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
        self.thd_pool = QThreadPool()
        self.setWindowTitle('智慧影音接軌')
        self.resize(600,500)
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

        #self.bntbar = QStatusBar(self)
        #self.bntbar.addPermanentWidget(self.buttonOpenFile, stretch=4)
        #self.bntbar.addPermanentWidget(self.buttonRemoveFile, stretch=4)
        #self.bntbar.addPermanentWidget(self.buttonRemoveAll, stretch=4)
        #layout.addWidget(self.bntbar)

        # 建立選取影片列表
        self.listview = QListView()       
        self.listModel = QStringListModel()
        #self.list = ["列表項1", "列表項2", "列表項3"]
         #將數據放到空的模型內
        #self.listModel.setStringList(self.list)
        self.listview.setModel(self.listModel)
        self.listview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.listview)

        # 選擇語言
        #self.combobox = QComboBox()
        #self.combobox.setItemText(3, "Tw")
        #layout.addWidget(self.combobox)

        # 按鈕編輯影片
        self.buttonClip = QPushButton('Edit Video')
        self.buttonClip.clicked.connect(self.VideoEdit_launcher)
        #layout.addWidget(self.buttonClip)


        self.buttonSub = QPushButton('Generate Subtitle')
        self.buttonSub.clicked.connect(self.Gen_subtitle_popup)
        #layout.addWidget(self.buttonSub)

        self.bnt2bar = QStatusBar(self)
        self.bnt2bar.addPermanentWidget(self.buttonClip, stretch=8)
        self.bnt2bar.addPermanentWidget(self.buttonSub, stretch=8)
        layout.addWidget(self.bnt2bar)

        self.statusLabel = QLabel()
        self.statusLabel.setText("\nResult: None")

        self.statusbar = QStatusBar(self)
        layout.addWidget(self.statusbar)

        self.progressBar = QProgressBar()
        self.progressBar.setRange(0,100)
        #layout.addWidget(self.progressBar)
        self.statusbar.addWidget(self.statusLabel, stretch=8)
        #self.statusbar.addPermanentWidget(self.progressBar, stretch=10)
        
        # self.rst_list = QListView()       
        # self.rst_model = QStringListModel()
        # self.rst_list.setModel(self.rst_model)
        # self.rst_list.setFixedHeight(100)
        # layout.addWidget(self.rst_list)

        # resulttext = QPlainTextEdit()
        # resulttext.setReadOnly(True)
        # layout.addWidget(resulttext)

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
            row = self.listModel.rowCount()  # 獲得最後一行的行數       
            self.listModel.insertRow(row)  # 數據模型添加行
            index = self.listModel.index(row,0)  # 獲得數據模型的索引
            self.listModel.setData(index,fname) 
            self.listview.setCurrentIndex(self.listModel.index(0,0))
            self.buttonClip.setEnabled(True)
        print(self.listModel.stringList())
            
    def RemovePath(self):
        selected  = self.listview.selectedIndexes() # 根據所有獲取item
        for i in selected:
            self.listModel.removeRow(i.row())
    
    def DelListItem(self):
        row1 = self.listModel.rowCount()
        for i in range(row1):
            self.listModel.removeRow(self.listview.modelColumn())

    def SetLabel(self, progress_callback):
        row = self.listModel.rowCount()
        if row == 0:
            QMessageBox.information(self,'Message','Please selected file first', QMessageBox.Ok)
            return
        
        self.statusLabel.setText('\nResult: processing your file...')
        QMessageBox.information(self,'Message','Your file is being processed',QMessageBox.Ok)
        self.buttonClip.setDisabled(True)
                
    def VideoEdit_launcher(self):
        video_edit_wkr = Worker(self.VideoEdit)
        video_edit_wkr.setAutoDelete(True)
        self.thd_pool.start(video_edit_wkr)
        

        set_label_wkr = Worker(self.SetLabel)
        set_label_wkr.setAutoDelete(True)
        self.thd_pool.start(set_label_wkr)

    def VideoEdit(self, progress_callback):
        # mp4 轉成 wav -----------------------------
        #inputfile = "media/tainanvlog.mp4"
        rowCount = self.listModel.rowCount()
        for row in range(rowCount):   
            self.statusLabel.setText('\nResult: loading your file...')
            source_file = self.listModel.stringList()[row]
            slash_pos = source_file.rfind('/')
            dot_pos = source_file.rfind('.')
            source_path, source_name, source_format = source_file[:slash_pos+1], source_file[slash_pos+1:dot_pos], source_file[dot_pos:]
            wavfile = source_path + source_name + '.wav'     # 執行完刪除 *wav
            outfile = source_path + source_name + '_edited.mp4' # 把檔案存在自己想要的地方
            

            if not os.path.exists(wavfile):
                os.system("ffmpeg -i "+source_file+" "+source_path + source_name + '.wav')

            # 找出fps---------------------------------------
            clip = cv2.VideoCapture(source_file)
            fps = clip.get(cv2.CAP_PROP_FPS)
            fps = round(fps,)       
            clip.release()

            # 測試靜音 ----------------------------------
            self.statusLabel.setText('\nResult: detecting voice instructions...')
            # split returns a generator of AudioRegion objects
            # sound = AudioSegment.from_file(wavfile, format="wav") 
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
            self.statusLabel.setText('\nResult: cropping the video...')

            for i in range(0,len(ins_loca)-1,2):
                grayclip = VideoFileClip(source_file).subclip(round(ins_loca[i],2),round(ins_loca[i+1],2))
                gray_scalar = []
                for frames in grayclip.iter_frames():
                    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
                    #cv2.imshow("gray", gray) #播放灰階影片
                    gray_scalar.append(gray)
                    key = cv2.waitKey(1)
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

            index = self.listModel.index(row, 0)
            self.listModel.setData(index, outfile) 
            self.statusLabel.setText('\nResult: File exported done')
            '''
            vlc = "/Applications/VLC.app/Contents/MacOS/VLC"
            p1 =subprocess.run ([''+vlc+'', ''+outfile+'',  'vlc://quit'])
            print(p1)

            
            ListViewDemo.DelListItem(self)
            self.buttonClip.setEnabled(True)
            '''
    def Gen_subtitle_popup(self):
        if self.listModel.rowCount() <= 0:
            QMessageBox.information(self,'Message','Please selected file first', QMessageBox.Ok)
            return 

        popup = Gen_subtitle_popup(self.listModel.stringList())
        try:
            rtn_val = popup.exec_()
        except:
            rtn_val = 1
        
        print(rtn_val)
            

class Gen_subtitle_popup(QDialog):
    def __init__(self, src_list):
        super().__init__()
        self.thd_pool = QThreadPool()
        self.src_list = src_list
        slash_pos = src_list[0].rfind('/')
        dot_pos = src_list[0].rfind('.')
        self.src_cur_path, self.src_cur_name, self.src_cur_format = src_list[0][:slash_pos+1], src_list[0][slash_pos+1:dot_pos], src_list[0][dot_pos:]
        self.setWindowTitle('Generate Subtitle')
        self.resize(700, 550)
        # self.rst_list = []
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.listWidget = QListWidget()

        self.src_list_label = QLabel()
        self.src_list_label.setText("Your selected file:")
        self.adjust_label = QLabel()
        self.adjust_label.setText("\nSubtitle Preview:")

        # selectd source list
        self.src_listview = QListView()
        self.src_listmodel = QStringListModel()
        self.src_listview.setModel(self.src_listmodel)
        for src in self.src_list:
            row = self.src_listmodel.rowCount()       
            self.src_listmodel.insertRow(row)
            index = self.src_listmodel.index(row,0)  
            self.src_listmodel.setData(index, src) 

        self.src_listview.setFixedHeight(20 * len(self.src_list))
        self.src_listview.setCurrentIndex(self.src_listmodel.index(0,0))
        

        # prepare subtitle
        self.subtitle_dict = {} 

        # adjust box
        self.adjust_table = QTableView()
        self.adjust_model_dict = {}
        self.adjust_model_dict['1'] = QStandardItemModel(0, 3)
        self.adjust_model_dict['1'].setHorizontalHeaderLabels(['Time start', 'Time end', 'Subtitle'])
        self.adjust_table.setModel(self.adjust_model_dict['1'])
        setup_table_launcher = Worker(self.SetupSubtitleAndTable_launcher)
        setup_table_launcher.setAutoDelete(True)
        self.thd_pool.start(setup_table_launcher)

        self.adjust_model_dict['1'].itemChanged.connect(self.ModifyItem)
        self.adjust_table.horizontalHeader().setStretchLastSection(True)
        self.adjust_table.setFixedHeight(300)
        self.src_listview.selectionModel().currentChanged.connect(self.AdjustSubtitle)

        # Accept checkbox
        self.AcceptSubtitle_chkbox = QCheckBox('Accept subtitle preview')
        self.AcceptSubtitle_chkbox.stateChanged.connect(lambda:self.ChangeBtnState(self.AcceptSubtitle_chkbox, self.gen_subtitle_btn))
        # Generate butten
        self.gen_subtitle_btn = QPushButton('Generate')
        self.gen_subtitle_btn.clicked.connect(self.GenerateSubtitle_Launcher)
        self.gen_subtitle_btn.setDisabled(True)

        self.gen_bar = QStatusBar()
        self.gen_bar.addPermanentWidget(self.AcceptSubtitle_chkbox, stretch=8)
        self.gen_bar.addPermanentWidget(self.gen_subtitle_btn, stretch=8)

        self.rst_label = QLabel()
        self.rst_label.setText('Experted:')
        self.rst_list = QListView()       
        self.rst_model = QStringListModel()
        self.rst_list.setModel(self.rst_model)
        self.rst_list.setFixedHeight(100)
        self.rst_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.rst_bar = QStatusBar()
        self.rst_bar.addPermanentWidget(self.rst_label, stretch = 1)
        self.rst_bar.addPermanentWidget(self.rst_list, stretch=16)


        layout.addWidget(self.src_list_label)
        layout.addWidget(self.src_listview)
        layout.addWidget(self.adjust_label)
        layout.addWidget(self.adjust_table)
        layout.addWidget(self.gen_bar)
        layout.addWidget(self.rst_bar)
        self.setLayout(layout)

    def SetupSubtitleAndTable_launcher(self, progress_callback):
        for row in range(self.src_listmodel.rowCount()):
            self.SetupSubtitleAndTable(modelIndex=row)

    def SetupSubtitleAndTable(self, modelIndex):
        if not type(modelIndex) == str:
            modelIndex = str(modelIndex + 1)

        self.subtitle_dict[modelIndex] = self.GetSubtitle(self.src_list[int(modelIndex) - 1])
        if modelIndex not in self.adjust_model_dict:
            self.adjust_model_dict[modelIndex] = QStandardItemModel(0, 3)
            self.adjust_model_dict[modelIndex].setHorizontalHeaderLabels(['Time start', 'Time end', 'Subtitle'])

        for row in range(len(self.subtitle_dict[modelIndex])):
            item1 = QStandardItem("{}".format(self.subtitle_dict[modelIndex][row].time_start))
            item2 = QStandardItem("{}".format(self.subtitle_dict[modelIndex][row].time_end))
            item3 = QStandardItem("{}".format(self.subtitle_dict[modelIndex][row].string.rstrip('\n')))
                
            self.adjust_model_dict[modelIndex].appendRow([item1, item2, item3])

    def ChangeBtnState(self, chkbox, btn):
        if chkbox.isChecked() == True:
            btn.setEnabled(True)
        else:
            btn.setDisabled(True)

    def AdjustSubtitle(self, current):
        current_row = str(current.row() + 1)
        if current_row not in self.adjust_model_dict:
            return
        #     self.SetupSubtitleAndTable(current_row)

        self.adjust_table.setModel(self.adjust_model_dict[current_row])

    def GetCurrentIndex(self):
        for i in range(self.src_listmodel.rowCount()):
            if self.src_listview.currentIndex() == self.src_listmodel.index(i):
                return i

    def ModifyItem(self, item):
        # print(item.row(), item.column(), item.text())
        src_index = str(self.GetCurrentIndex() + 1)

        if item.column() == 0:
            self.subtitle_dict[src_index][item.row()].time_start = item.text()
        elif item.column() == 1:
            self.subtitle_dict[src_index][item.row()].time_end = item.text()
        else:
            self.subtitle_dict[src_index][item.row()].string = item.text()
                    
        for i in self.subtitle_dict[src_index]:
            print(i.time_start, i.time_end)
            print(i.string)
            print()

    def GetSubtitle(self, srcfile, blank=True):
        slash_pos = srcfile.rfind('/')
        dot_pos = srcfile.rfind('.')
        src_path, src_name, src_format = srcfile[:slash_pos+1], srcfile[slash_pos+1:dot_pos], srcfile[dot_pos:]

        if not os.path.exists(src_path + 'wav/'):
            os.mkdir(src_path + 'wav/')

        src_path += 'wav/'
        if not os.path.exists(src_path + src_name + '.wav'):
            os.system("ffmpeg -i "+srcfile+" "+src_path + src_name + '.wav')

        audiofile = src_path + src_name+'.wav'
        audio_regions = auditok.split(
            audiofile,
            min_dur=0.01,        # minimum duration of a valid audio event in seconds
            max_dur=100,        # maximum duration of an event
            max_silence=0.3,      # maximum duration of tolerated continuous silence within an event
            energy_threshold=60  # threshold of detection
        )

        subtitle_list = []
        for i, r in enumerate(audio_regions):
            print("Region {i}: {r.meta.start:.3f}s -- {r.meta.end:.3f}s".format(i=i, r=r))
            filename = r.save(src_path + "region_{meta.start:.3f}-{meta.end:.3f}.wav")
            start, end = "{r.meta.start:.3f}".format(r=r), "{r.meta.end:.3f}".format(r=r)
            text = self.AudioToText(filename)
            subtitle_list.append(Subtitle(start, end, text))

        i = 0
        while i < len(subtitle_list) - 1:
            if subtitle_list[i].time_end < subtitle_list[i+1].time_start:
                time_start = subtitle_list[i].time_end
                time_end = subtitle_list[i+1].time_start
                subtitle_list.insert(i+1, Subtitle(time_start, time_end))
                i += 1

            i += 1

        if blank:
            # handling subtitle go out of screen
            for index in range(len(subtitle_list)):
                if 25 < len(subtitle_list[index].string):
                    former, latter = subtitle_list[index].split()
                    subtitle_list[index] = former
                    subtitle_list.insert(index+1, latter)

        return subtitle_list

    def AudioToText(self, audiofile):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audiofile) as src:
            audio_data = recognizer.record(src)
            try:
                text = recognizer.recognize_google(audio_data, language= 'zh-TW')
                return text
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from google Speech Recognition service; {0}".format(e))
            except IOError as e:
                print("IOError; {0}".format(e))

            return ' '

    def GenerateSubtitle_Launcher(self):
        setui_wkr = Worker(self.SetUI)
        setui_wkr.setAutoDelete(True)
        self.thd_pool.start(setui_wkr)

        eprt_srt_wkr = Worker(self.Export_srt_file)
        eprt_srt_wkr.setAutoDelete(True)
        self.thd_pool.start(eprt_srt_wkr)

        gen_subtitle_wkr = Worker(self.GenerateSubtitle)
        gen_subtitle_wkr.setAutoDelete(True)
        self.thd_pool.start(gen_subtitle_wkr)

    def Export_srt_file(self, progress_callback):
        subtitle_list = self.subtitle_dict[str(self.GetCurrentIndex() + 1)]

        f = open(self.src_cur_path+self.src_cur_name+'.srt', 'w')
        for i in range(len(subtitle_list)):
            f.write(str(i) + '\n')
            f.write(subtitle_list[i].time_start + ' --> ' + subtitle_list[i].time_end + '\n')
            f.write(subtitle_list[i].string + '\n')

        f.close()
        self.Export_msg_to_mdl(self.rst_model, self.src_cur_path + self.src_cur_name + ".srt")

    def Export_msg_to_mdl(self, model, msg, withtime = True):
        row = model.rowCount()
        model.insertRow(row)
        index = model.index(row, 0)
        current_time = time.strftime("%H:%M:%S", time.localtime())
        if withtime:
            model.setData(index, "{:<12}{}".format(current_time, msg)) 
        else:
            model.setData(index, "{}".format(msg))

    def SetUI(self, progress_callback):
        self.gen_subtitle_btn.setDisabled(True)
        self.AcceptSubtitle_chkbox.setChecked(False)
        self.Export_msg_to_mdl(self.rst_model, "Generating subtitle...")

    def GenerateSubtitle(self, progress_callback):
        subtitle_list = self.subtitle_dict[str(self.GetCurrentIndex() + 1)]
        FONT_URL="./resources/GenJyuuGothicL-Medium.ttf"
        def annotate(clip, txt, txt_color='black', fontsize=60):
            """ Writes a text at the bottom of the clip. """
            txtclip = TextClip(txt, fontsize=fontsize, font=FONT_URL, color=txt_color)
            cvc = CompositeVideoClip([clip, txtclip.set_pos(('center', 'bottom'))])
            return cvc.set_duration(clip.duration)

        # bind subtitle file into video stream
        src_clip = VideoFileClip(self.src_cur_path + self.src_cur_name + self.src_cur_format)
        annotated_clips = []
        for subtitle in subtitle_list:
            annotated_clips.append(annotate(src_clip.subclip(subtitle.time_start, subtitle.time_end), subtitle.string))

        final_clip = concatenate_videoclips(annotated_clips)
        final_clip.write_videofile(self.src_cur_path + self.src_cur_name + "_with_subtitle.mp4")
        self.Export_msg_to_mdl(self.rst_model, self.src_cur_path + self.src_cur_name + "_with_subtitle.mp4")
        self.Export_msg_to_mdl(self.rst_model, "Done.")

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./resources/firefox-icon-02.png'))
    win = ListViewDemo()
    win.show()
    sys.exit(app.exec_())
