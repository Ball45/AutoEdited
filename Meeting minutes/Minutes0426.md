# Install ffmpeg & Convert mp4 to mp3
## Install ffmpeg in [windows](https://pypi.org/project/ffmpeg-python/)
```
pip install ffmpeg-python
```
## Test 
```
import os
mp4file = "video.mp4"
mp3file = "audio.mp3"
"ffmpeg -i "+mp4file+" "+mp3file
```

## Questions
1. 剪接影片變成雜訊
2. MOV沒辦法轉成音檔 

