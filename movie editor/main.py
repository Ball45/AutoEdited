import os
import numpy as np
import auditok
from pydub import AudioSegment
import speech_recognition as sr
from moviepy.editor import *
import cv2 as cv

# mp4 轉成 wav -----------------------------
#inputfile = "media/tainanvlog.mp4"
source_file = "media/tetest.mp4"
slash_pos = source_file.rfind('/')
dot_pos = source_file.rfind('.')
source_path, source_name, source_format = source_file[:slash_pos+1], source_file[slash_pos+1:dot_pos], source_file[dot_pos:]
wavfile = source_path + source_name + '.wav'
outfile = source_path + source_name + '_out.mp4'

if not os.path.exists(wavfile):
    os.system("ffmpeg -i "+source_file+" "+source_path + source_name + '.wav')
    print('音檔輸出')


# 找出fps---------------------------------------
clip = cv.VideoCapture(source_file)
fps = clip.get(cv.CAP_PROP_FPS)
fps = round(fps,)   
print('FPS :', fps)    
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

# 偵測重複 ----------------------------------
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

                          
#轉灰階--------------------------------------
for i in range(1,len(ins_loca)-1,2):
    grayclip = VideoFileClip(source_file).subclip(round(before_ins_start,2),round(after_ins_start,2))
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

