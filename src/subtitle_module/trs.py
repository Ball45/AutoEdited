'''
Please place video file into 'resources' directory.
'''
from moviepy import editor
import os, speech_recognition
if os.path.exists('./resources/wt024.ttf'):
    FONT_URL='./resources/wt024.ttf'




os.system("echo pwd=%cd%")

# handling with video source
source_file = input('Enter your video stream and file name:')
slash_pos = source_file.rfind('/')
dot_pos = source_file.rfind('.')
source_path, source_name, source_format = source_file[:slash_pos+1], source_file[slash_pos+1:dot_pos], source_file[dot_pos:]
source_clip = editor.VideoFileClip(source_file)


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

    # def get_prev_timeslice(self): # get time_start - 1 ms
    #     start_time_ms = int(self.time_start[9:])
    #     if start_time_ms != 0:
    #         return self.time_start[:9] + str(start_time_ms - 1).zfill(3)
    #     else:
    #         return self.time_start[:6] + \
    #          str(int(self.time_start[6:8]) - 1).zfill(2) + ",999"

    # def get_next_timeslice(self): # get time_end + 1 ms
    #     end_time_ms = int(self.time_end[9:])
    #     if end_time_ms != 999:
    #         return self.time_end[:9] + str(end_time_ms + 1).zfill(3)
    #     else:
    #         return self.time_end[:6] + \
    #          str(int(self.time_end[6:8]) + 1).zfill(2) + ",000"

# handling with subtitle file
if not os.path.exists(source_path + source_name + '.srt'):
    os.system("autosub -S zh-CN -D zh-CN " + source_file)

# read the srt file
subtitle_file = open(source_path + source_name + '.srt', encoding='utf-8')
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


'''
# using google speech_recognition to generate subtitle
import speech_recognition as sr
import auditok


class Segment:
    def __init__(self, start, end, text, filename):
        self.time_start = start
        self.time_end = end
        self.text = text
        self.filename = filename


def audioToText(audiofile):
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
'''
'''
audiofile = source_path+source_name+'.wav'
audio_regions = auditok.split(
    audiofile,
    min_dur=0.01,        # minimum duration of a valid audio event in seconds
    max_dur=100,        # maximum duration of an event
    max_silence=0.3,      # maximum duration of tolerated continuous silence within an event
    energy_threshold=60  # threshold of detection
)

segment_list = []
for i, r in enumerate(audio_regions):
    print("Region {i}: {r.meta.start:.3f}s -- {r.meta.end:.3f}s".format(i=i, r=r))
    filename = r.save("region_{meta.start:.3f}-{meta.end:.3f}.wav")
    start, end = "{r.meta.start:.3f}".format(r=r), "{r.meta.end:.3f}".format(r=r)
    text = audioToText(filename)
    segment_list.append(Segment(start, end, text, filename))

for i in segment_list:
    print(i.filename)
    print(i.time_start, i.time_end)
    print(i.text)
    print()

source_clip = editor.VideoFileClip("movie_2.mp4")
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

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