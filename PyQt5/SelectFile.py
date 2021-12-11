import os, time, cv2, sys, auditok, traceback, subprocess, platform
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import speech_recognition as sr
from moviepy.editor import *

class Subtitle:
    def __init__(self, start, end, silent=None, content=' '):
        self.start = start
        self.end = end
        self.length = float(start) - float(end)
        self.silent = silent # silent time before this speech
        self.content = content

    def split(self):
        # yet using time library
        former_timestart = self.start
        former_timeend = self.get_mid_time(self.start, self.end)
        former_content = self.content[:len(self.content)//2] + '\n'
        latter_timestart = self.get_mid_time(self.start, self.end)
        latter_timeend = self.end
        latter_content = self.content[len(self.content)//2:]

        return Subtitle(former_timestart, former_timeend, former_content), Subtitle(latter_timestart, latter_timeend, latter_content)

    @classmethod
    def get_mid_time(cls, start, end):
        # h1, m1, s1, ms1 = start[0:2], start[3:5], start[6:8], start[9:]
        # h2, m2, s2, ms2 = end[0:2], end[3:5], end[6:8], end[9:]
        # ss1 = int(h1) * 60 * 60 + int(m1) * 60 + int(s1) 
        # ss2 = int(h2) * 60 * 60 + int(m2) * 60 + int(s2)
        # dur = (ss2 - ss1)//2
        dur = (float(end) - float(start))//2
        # rh = int(h1) + dur // 3600
        # dur %= 3600
        # rm = int(m1) + dur // 60
        # dur %= 60
        # rs = int(s1) + dur
        
        # return str(rh).zfill(2) + ':' + str(rm).zfill(2) + ':' + str(rs).zfill(2) + ',' + '000'
        return str(float(start) + dur)

class Subtitle_list:
    def __init__(self):
        self.list = []

    def Add_blank(self):
        i = 0
        while i < len(self.list) - 1:
            if self.list[i].end < self.list[i+1].start:
                start = self.list[i].end
                end = self.list[i+1].start
                self.list.insert(i+1, Subtitle(start, end))
                i += 1

            i += 1

    def Optimize_length(self):
        for index in range(len(self.list)):
            if 25 < len(self.list[index].content):
                former, latter = self.list[index].split()
                self.list[index] = former
                self.list.insert(index+1, latter)

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

# class WorkThread(QThread):
#     timer = pyqtSignal() # 每隔一秒發送一次信號
#     end = pyqtSignal()   # 技術完成後發送一次信號
#     def run(self):
#         while True:
#             self.sleep(1) # 休眠一秒
#             if sec == 100:
#                 self.end.emit() # 發送end信號
#                 break;
#             self.timer.emit()  # 發送timer信號

class Edit_videos_windows(QWidget):
    def __init__(self, parent = None):
        super(Edit_videos_windows, self).__init__(parent)
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
        self.buttonRemoveFile = QPushButton('Remove File')
        self.buttonRemoveFile.clicked.connect(self.RemovePath)
        self.buttonRemoveAll = QPushButton('Empty List')
        self.buttonRemoveAll.clicked.connect(self.DelListItem)

        # 建立選取影片列表
        self.listview = QListView()       
        self.listModel = QStringListModel()
        self.listview.setModel(self.listModel)
        self.listview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listview.setFixedHeight(200)

        # 選擇語言
        #self.combobox = QComboBox()
        #self.combobox.setItemText(3, "Tw")
        #layout.addWidget(self.combobox)

        # 按鈕編輯影片
        self.buttonClip = QPushButton('Edit Video')
        self.buttonClip.clicked.connect(self.VideoEdit_launcher)
        self.buttonSub = QPushButton('Generate Subtitle')
        self.buttonSub.clicked.connect(self.Gen_subtitle_popup)
        self.bnt2bar = QStatusBar(self)
        self.bnt2bar.addPermanentWidget(self.buttonClip, stretch=8)
        self.bnt2bar.addPermanentWidget(self.buttonSub, stretch=8)

        # 處理狀態 UI
        # self.statusLabel = QLabel()
        # self.statusLabel.setText("\nResult: None")
        # self.statusbar = QStatusBar(self)
        # self.statusbar.addWidget(self.statusLabel, stretch=8)
        
        # 處理狀態 UI
        self.rst_label = QLabel()
        self.rst_label.setText('\nResult:')
        self.rst_list = QListView()       
        self.rst_model = QStringListModel()
        self.rst_list.setModel(self.rst_model)
        # self.rst_list.setFixedHeight(100)
        self.rst_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.rst_bar = QStatusBar()
        # self.rst_bar.addPermanentWidget(self.rst_label, stretch = 1)
        # self.rst_bar.addPermanentWidget(self.rst_list, stretch=16)

        layout.addWidget(self.buttonOpenFile)
        layout.addWidget(self.buttonRemoveFile)
        layout.addWidget(self.buttonRemoveAll)
        layout.addWidget(self.listview)
        layout.addWidget(self.bnt2bar)
        layout.addWidget(self.rst_label)
        layout.addWidget(self.rst_list)
        self.setLayout(layout)
      
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

    def ExportMsg(self, model, msg, src=None, withtime = True):
        # row = model.rowCount()
        model.insertRow(0)
        index = model.index(0, 0)
        current_time = time.strftime("%H:%M:%S", time.localtime())
        if withtime:
            model.setData(index, "{:<12}{}  {}".format(current_time, msg, src)) 
        else:
            model.setData(index, "{}".format(msg))

    def SetLabel(self, progress_callback):
        row = self.listModel.rowCount()
        if row == 0:
            QMessageBox.information(self,'Message','Please selected file first', QMessageBox.Ok)
            return
        
        self.buttonClip.setDisabled(True)
        # self.ExportMsg(self.rst_model, 'Processing: ' + self.listModel.stringList()[row])
        # QMessageBox.information(self,'Message','Your file is being processed',QMessageBox.Ok)
                
    def VideoEdit_launcher(self):
        rows = self.listModel.rowCount()
        if rows == 0:
            QMessageBox.information(self,'Message','Please selected file first', QMessageBox.Ok)
            return

        self.buttonClip.setDisabled(True)
        self.buttonSub.setDisabled(True)
        for row in range(rows):
            src_path, src_name, src_format = self.GetSrcArg(self.listModel.stringList()[row])
            video_edit_wkr = Worker(self.VideoEdit, src_path, src_name, src_format)
            video_edit_wkr.setAutoDelete(True)
            self.thd_pool.start(video_edit_wkr)

        ChaneBtnState_wkr = Worker(self.ChaneBtnState_waitpool)
        ChaneBtnState_wkr.setAutoDelete(True)
        self.thd_pool.start(ChaneBtnState_wkr)

    def ChaneBtnState_waitpool(self, progress_callback):
        while 1 < self.thd_pool.activeThreadCount():
            pass

        self.buttonSub.setEnabled(True)

    def VideoEdit(self, src_path, src_name, src_format, progress_callback):
        self.ExportMsg(self.rst_model, "Loading :", src_name + src_format)
        srcfile = src_path + src_name + src_format
        wavfile = src_path + src_name + '.wav'     
        outfile = src_path + src_name + '_edited.mp4' 
        src_path += 'wav/'
        if not os.path.exists(src_path + src_name + '.wav'):
            if not os.path.exists(src_path):
                os.mkdir(src_path)
            
            os.system("ffmpeg -i " + srcfile + " " + src_path + src_name + '.wav')

        # split audio
        audio_regions = auditok.split(
            src_path + src_name + '.wav',
            min_dur=0.01,        # minimum duration of a valid audio event in seconds
            max_dur=100,        # maximum duration of an event
            max_silence=0.3,      # maximum duration of tolerated continuous silence within an event
            energy_threshold=50  # threshold of detection
        )

        # build speeching content
        speech_content = Subtitle_list()        
        for i, r in enumerate(audio_regions):
            filename = r.save(src_path + "audio_{}.wav".format(i))
            speech_content.list.append(Subtitle(r.meta.start, r.meta.end, ' '))

        # get all command position
        self.ExportMsg(self.rst_model, "Detecting :", src_name + src_format)
        instuction_list = self.DetectInstructionPosition(speech_content.list, src_path)
        if len(instuction_list) == 0:
            self.ExportMsg(self.rst_model, "[Command not found]", src_name + src_format)
            return

        # process all command
        self.ExportMsg(self.rst_model, "Processing :", src_name + src_format)
        croptime = self.ProcessInstruction(instuction_list)
        print(croptime)

        # crop the video
        self.ExportMsg(self.rst_model, "Cropping :", src_name + src_format)
        clip = VideoFileClip(srcfile)
        final_clip = self.Crop(clip, croptime)

        # export the video
        self.ExportMsg(self.rst_model, "Exporting :", src_name + "_edited" + src_format)
        final_clip.write_videofile(outfile)
        final_clip.close()
        self.ExportMsg(self.rst_model, "[Done]", src_name + "_edited" + src_format)
        self.UpdateFile(srcfile, outfile)
        self.LaunchFile(outfile)

    def UpdateFile(self, srcfile, outfile):
        for row in range(len(self.listModel.stringList())):
            if srcfile == self.listModel.stringList()[row]:
                index = self.listModel.index(row, 0)
                self.listModel.setData(index, outfile) 
                break

        return

    def tmp_graylevel_process(self):

        # # 抓影片前5秒進行辨識
        # before_ins_end = int(pre_content.end)      #指令前的結束時間
        # if (before_ins_end-5) < 0 :
        #     before_ins_start=0
        #     sec = float(before_ins_end)
        # else :
        #     before_ins_start = before_ins_end-5    #指令前的起始時間
        #     sec = 5
        
        # after_ins_start = float(content.start) # 指令後的起始時間
        # print('往前抓＿秒進行辨識:',sec)
        # 轉灰階--------------------------------------
        self.ExportMsg(self.rst_model, "Comparing :", src_name + src_format)
        for i in range(0,len(ins_loca)-1,2):
            grayclip = VideoFileClip(srcfile).subclip(round(ins_loca[i],2),round(ins_loca[i+1],2))
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
        
        # 找出fps---------------------------------------
            clip = cv2.VideoCapture(srcfile)
            fps = clip.get(cv2.CAP_PROP_FPS)
            fps = round(fps,)       
            clip.release()

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

    def Crop(self, src_clip, croptime):
        clips = []
        start_time = 0
        for crop in croptime:
            clips.append(src_clip.subclip(start_time, crop[0]))
            start_time = crop[1]
        
        clips.append(src_clip.subclip(start_time))
        return concatenate_videoclips(clips)

    def AudioToText(self, audiofile):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audiofile) as src:
            audio_data = recognizer.record(src)
            try:
                txt = recognizer.recognize_google(audio_data, language= 'zh-TW')
            except:
                txt = ' ' # None

        return txt

    def DetectInstructionPosition(self, content_list, src_path='./'):
        rst_list = []
        pre_content = Subtitle(0, 0)
        for i in range(len(content_list)):
            content = content_list[i]
            content.silent = content.start - pre_content.end

            if 1.4 < content.silent and content.length < 3.0:
                txt = self.AudioToText(src_path + "audio_{}.wav".format(i))
                if "剪接" in str(txt): 
                    pre_content.content = self.AudioToText(src_path + "audio_{}.wav".format(i-1))
                    suf_content = content_list[i+1]
                    suf_content.content = self.AudioToText(src_path + "audio_{}.wav".format(i+1))
                    rst_list.append((pre_content, suf_content))

            pre_content = content

        for data in rst_list:
            print(data[0].content, data[1].content)

        return rst_list

    def ProcessInstruction(self, instruction_list):
        croptime = self.ProcessBySpeechContent(instruction_list)
        if False in croptime:
            print("[Log] ProcessInstruction() : False found in croptime")

        return croptime

    def ProcessBySpeechContent(self, instruction_list):
        croptime = []
        for ins in instruction_list: # instruction
            pre_content, new_content = ins[0].content, ins[1].content
            word_length = 1
            succeed = False
            for i in range(0, len(new_content), word_length):
                word = new_content[i:i + word_length + 1]
                pos_wrong = pre_content.find(word)
                if -1 < pos_wrong:
                    croptime.append((float(ins[0].start) + ins[0].length * (pos_wrong / len(pre_content)), ins[1].start))
                    succeed = True
                    break
            
            if not succeed:
                croptime.append(False)

        return  croptime

    def LaunchFile(self, file):
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', file))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(file)
        else:                                   # linux variants
            subprocess.call(('xdg-open', file))

    def GetSrcArg(self, srcfile):
        slash_pos = srcfile.rfind('/')
        dot_pos = srcfile.rfind('.')
        return srcfile[:slash_pos+1], srcfile[slash_pos+1:dot_pos], srcfile[dot_pos:]

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
        self.thd_pool.setMaxThreadCount(8)
        self.src_list = src_list
        slash_pos = src_list[0].rfind('/')
        dot_pos = src_list[0].rfind('.')
        self.src_cur_path, self.src_cur_name, self.src_cur_format = src_list[0][:slash_pos+1], src_list[0][slash_pos+1:dot_pos], src_list[0][dot_pos:]
        self.setWindowTitle('Generate Subtitle')
        self.resize(700, 550)
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

        self.src_listview.setFixedHeight(25 * len(self.src_list))
        self.src_listview.setCurrentIndex(self.src_listmodel.index(0,0))
        

        # prepare subtitle & adjust box
        self.subtitle_dict = {} 
        self.adjust_table = QTableView()
        self.adjust_model_dict = {}
        for row in range(self.src_listmodel.rowCount()):
            row = str(row + 1)                
            self.adjust_model_dict[row] = QStandardItemModel(0, 3)
            self.adjust_model_dict[row].setHorizontalHeaderLabels(['Time start', 'Time end', 'Subtitle'])
            self.adjust_model_dict[row].itemChanged.connect(self.ModifyItem)

        table_wkr = Worker(self.BuildupTable)
        table_wkr.setAutoDelete(True)
        self.thd_pool.start(table_wkr)
        subtitle_wkr = Worker(self.BuildupSubtitle)
        subtitle_wkr.setAutoDelete(True)
        self.thd_pool.start(subtitle_wkr)

        self.adjust_table.horizontalHeader().setStretchLastSection(True)
        self.adjust_table.setFixedHeight(500)
        self.src_listview.selectionModel().currentChanged.connect(lambda: self.RefreshTable(None))

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

    def BuildupSubtitle(self, progress_callback):
        for row in range(self.src_listmodel.rowCount()):
            row = str(row + 1)             
            src_path, src_name, src_fmt = self.GetSrcArg(self.src_list[int(row) - 1])
            self.subtitle_dict[row] = Subtitle_list()
            if os.path.exists(src_path + src_name + '.srt'):
                file = open(src_path + src_name + '.srt', encoding='utf-8')
                sub_file = file.readlines()
                file.close()

                for line in range(0, len(sub_file), 4):
                    content = sub_file[line + 2]
                    pos = sub_file[line + 1].find('-')
                    start, end = sub_file[line + 1][:pos-1], sub_file[line+1][pos+4:]
                    self.subtitle_dict[row].list.append(Subtitle(start, end, content))
            else:
                src_path += 'wav/'
                if not os.path.exists(src_path + src_name + '.wav'):
                    if not os.path.exists(src_path):
                        os.mkdir(src_path)
                    
                    os.system("ffmpeg -i " + self.src_list[int(row) - 1] + " " + src_path + src_name + '.wav')

                audio_region = auditok.split(
                    src_path + src_name+'.wav',
                    min_dur=0.01,        # minimum duration of a valid audio event in seconds
                    max_dur=100,        # maximum duration of an event
                    max_silence=0.3,      # maximum duration of tolerated continuous silence within an event
                    energy_threshold=60  # threshold of detection
                )

                for i, r in enumerate(audio_region):
                    filename = r.save(src_path + "region_{meta.start:.3f}-{meta.end:.3f}.wav")
                    start, end = "{r.meta.start:.3f}".format(r=r), "{r.meta.end:.3f}".format(r=r)
                    self.subtitle_dict[row].list.append(Subtitle(start, end, ' '))
                    audio2txt_wkr = Worker(self.AudioToText, filename, row, len(self.subtitle_dict[row].list) - 1)
                    audio2txt_wkr.setAutoDelete(True)
                    while self.thd_pool.maxThreadCount() <= self.thd_pool.activeThreadCount(): pass
                    self.thd_pool.start(audio2txt_wkr)

            while 2 < self.thd_pool.activeThreadCount(): pass # wait for all subtitle thread finished
            self.subtitle_dict[row].Optimize_length()
            self.subtitle_dict[row].Add_blank()
            self.RefreshTable()

    def BuildupTable(self, progress_callback):
        row = str(self.GetCurrentIndex() + 1) 
        while 1 < self.thd_pool.activeThreadCount(): # if generate_subtitle thread is processing
            # print("[Log] Active Thread Count: {}".format(self.thd_pool.activeThreadCount()))
            try:
                self.RefreshTable(full = False)

            except: pass
            time.sleep(0.2)

    def RefreshTable(self, row = None, full=True):
        row = str(self.GetCurrentIndex() + 1) if row == None else str(row + 1)
        end = len(self.subtitle_dict[row].list)
        start = 0 if full or self.thd_pool.maxThreadCount()*2 >= end else end - self.thd_pool.maxThreadCount()*2
        
        for i in range(start, end):
            item1 = QStandardItem(self.subtitle_dict[row].list[i].start)
            item2 = QStandardItem(self.subtitle_dict[row].list[i].end)
            item3 = QStandardItem(self.subtitle_dict[row].list[i].content.rstrip('\n'))
            try:
                self.adjust_model_dict[row].setItem(i, 0, item1)
                self.adjust_model_dict[row].setItem(i, 1, item2)
                self.adjust_model_dict[row].setItem(i, 2, item3)
            except:
                self.adjust_model_dict[row].appendRow([item1, item2, item3])
        
        self.adjust_table.setModel(self.adjust_model_dict[row])

    def AudioToText(self, audiofile, rst_row, index, progress_callback):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audiofile) as src:
            audio_data = recognizer.record(src)
            try:
                self.subtitle_dict[rst_row].list[index].content = recognizer.recognize_google(audio_data, language= 'zh-TW')
                # print(rst)
            except sr.UnknownValueError:
                self.subtitle_dict[rst_row].list[index].content = "Recognize Error"
            except sr.RequestError as e:
                self.subtitle_dict[rst_row].list[index].content = "Request Error"
            except IOError as e:
                self.subtitle_dict[rst_row].list[index].content = "IO Error"
            except:
                self.subtitle_dict[rst_row].list[index].content = "Unexpect Error"

        return

    def ChangeBtnState(self, chkbox, btn):
        if chkbox.isChecked() == True:
            btn.setEnabled(True)
        else:
            btn.setDisabled(True)

    def GetCurrentIndex(self):
        for i in range(self.src_listmodel.rowCount()):
            if self.src_listview.currentIndex() == self.src_listmodel.index(i):
                return i

    def ModifyItem(self, item):
        try:
            src_index = str(self.GetCurrentIndex() + 1)
            if item.column() == 0:
                self.subtitle_dict[src_index].list[item.row()].start = item.text()
            elif item.column() == 1:
                self.subtitle_dict[src_index].list[item.row()].end = item.text()
            else:
                self.subtitle_dict[src_index].list[item.row()].content = item.text()
    
            print('[Log] Modifying Item: {}  {}  {}'.format(item.row(), item.column(), item.text()))
        except:
            pass

    def GetSrcArg(self, srcfile):
        slash_pos = srcfile.rfind('/')
        dot_pos = srcfile.rfind('.')
        return srcfile[:slash_pos+1], srcfile[slash_pos+1:dot_pos], srcfile[dot_pos:]

    def GenerateSubtitle_Launcher(self):
        current_row = self.GetCurrentIndex()
        setui_wkr = Worker(self.SetUI)
        setui_wkr.setAutoDelete(True)
        self.thd_pool.start(setui_wkr)

        eprt_srt_wkr = Worker(self.Export_srt_file, current_row)
        eprt_srt_wkr.setAutoDelete(True)
        self.thd_pool.start(eprt_srt_wkr)

        gen_subtitle_wkr = Worker(self.GenerateSubtitle, current_row)
        gen_subtitle_wkr.setAutoDelete(True)
        self.thd_pool.start(gen_subtitle_wkr)

    def Export_srt_file(self, row, progress_callback):
        src_path, src_name, src_format = self.GetSrcArg(self.src_list[row])
        row = str(row+1)
        subtitle_list = self.subtitle_dict[row].list

        f = open(src_path+src_name+'.srt', 'w')
        for i in range(len(subtitle_list)):
            f.write(str(i) + '\n')
            f.write(subtitle_list[i].start + ' --> ' + subtitle_list[i].end + '\n')
            f.write(subtitle_list[i].content + '\n')
            f.write('\n')

        f.close()
        self.ExportMsg(self.rst_model, src_path+src_name+'.srt')

    def ExportMsg(self, model, msg, withtime = True):
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
        self.ExportMsg(self.rst_model, "Generating subtitle...")

    def GenerateSubtitle(self, row, progress_callback):
        src_path, src_name, src_format = self.GetSrcArg(self.src_list[row])
        row = str(row+1)
        subtitle_list = self.subtitle_dict[row].list

        FONT_URL="./resources/GenJyuuGothicL-Medium.ttf"
        def annotate(clip, txt, txt_color='black', fontsize=60):
            """ Writes a text at the bottom of the clip. """
            txtclip = TextClip(txt, fontsize=fontsize, font=FONT_URL, color=txt_color)
            cvc = CompositeVideoClip([clip, txtclip.set_pos(('center', 'bottom'))])
            return cvc.set_duration(clip.duration)

        # bind subtitle file into video stream
        src_clip = VideoFileClip(src_path + src_name + src_format)
        annotated_clips = []
        for subtitle in subtitle_list:
            annotated_clips.append(annotate(src_clip.subclip(subtitle.start, subtitle.end), subtitle.content))

        final_clip = concatenate_videoclips(annotated_clips)
        final_clip.write_videofile(src_path + src_name + "_with_subtitle.mp4")
        self.ExportMsg(self.rst_model, src_path + src_name + "_with_subtitle.mp4")
        self.ExportMsg(self.rst_model, "Done.")

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./resources/icon.png'))
    win = Edit_videos_windows()
    win.show()
    sys.exit(app.exec_())