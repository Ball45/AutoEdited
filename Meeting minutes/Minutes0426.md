# Install ffmpeg & Convert mp4 to mp3

## Install ffmpeg in anaconda prompt in [windows](https://pypi.org/project/ffmpeg-python/)
```
pip install ffmpeg-python
```

## Install ffmpeg in anaconda in macos
Installing ffmpeg from the conda-forge channel can be achieved by adding conda-forge to your channels with:
```
conda config --add channels conda-forge
```
Once the conda-forge channel has been enabled, ffmpeg can be installed with:
```
conda install ffmpeg
```
```
pip install ffmpeg-python
```
It is possible to list all of the versions of ffmpeg available on your platform with:
```
conda search ffmpeg --channel conda-forge
```

## Test 
```
import os
mp4file = "video.mp4"
mp3file = "audio.mp3"
os.system("ffmpeg -i "+mp4file+" "+mp3file)
```

## Questions
1. 剪接影片變成雜訊
2. MOV沒辦法轉成音檔 (解決）

