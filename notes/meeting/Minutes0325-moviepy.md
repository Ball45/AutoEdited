# 0325--Install MoviePy and try out

- [x] Learn how to use conda
- [x] Learn how to use pip
- [ ] Learn [moviepy](https://zulko.github.io/moviepy/) 

## install anaconda in windows
1. download anaconda
2. create a new environment,type this in a terminal
```
conda create -n name pthon=version
```
3. enter the new environment,type this in a terminal
```
conda activate name #windows
```

## install moviepy in windows
1.  type this in a terminal
 ```
 pip install moviepy
 ```
2. to check whether imagemagick exists  
- [windows](https://pypi.org/project/moviepy/) 
We need to edit **moviepy/config_defaults.py** to provide the path to the ImageMagick binary, which is called convert. It should look like this:
```
IMAGEMAGICK_BINARY = "C:\\Program Files\\ImageMagick_VERSION\\convert.exe"
```

## install anaconda in macOS
1. [download anaconda](https://www.anaconda.com/products/individual)
2. installl the first one

## install moviepy in conda in macOS
1.open conda terminal

 ![open conda terminal](https://miro.medium.com/max/4800/1*v3Z3aKuWmZSny590SStldw.png)
 
 2.type this in a terminal to install moviepy
 ```
 pip install moviepy
 ```
 3.type this in a terminal to install imagemagick (ImageMagick is not strictly required, only if you want to write texts. )
 ```
 conda install -c conda-forge imagemagick
 ```

 ## Try out moviepy 
 ### Example -- add a title at the center of the screen
 In this example we open a video file, select the subclip between t=50s and t=60s, add a title at the center of the screen, and write the result to a new file:
 ```python
 from moviepy import *
 import os  

video = VideoFileClip("media/IMG_8315.mov").subclip(0,5)

# Make the text. Many more options are available.
txt_clip = ( TextClip("2021.04.15",fontsize=70,color='white')
             .with_position('center')
             .with_duration(4) )

result = CompositeVideoClip([video, txt_clip]) # Overlay text on video
result.write_videofile("media/myHolidays_edited.webm",fps=25) # Many options...
```
> video have to save in the same file as the project.

### Example -- put clips together
```python
from moviepy.editor 
import VideoFileClip, concatenate_videoclips

clip1 = VideoFileClip("media/airplane.mp4")
clip2 = VideoFileClip("media/thunder.mp4")
final_clip = concatenate_videoclips([clip1, clip2])

final_clip.write_videofile("media/test2.mp4")
```

### use conda moviepy termianl to run 
1. type this in a terminal (cd:切換目錄)
```
cd program/video
```
2. type this in a terminal (run the code)
```
python test/p03.py
```
