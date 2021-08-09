# 0713

## Getting frame from Video File Clip
- using MoviePy 
    - get_frame 可以取得一個幀。[reference](https://www.geeksforgeeks.org/moviepy-getting-frame-from-video-file-clip/?ref=rp)
    - iter_frames 可以取得所有幀。[reference](https://www.geeksforgeeks.org/moviepy-iterating-frames-of-video-file-clip/)
- 了解frame


# 0720

## Converting RGB to GRAYSCALE
- using OpenCV
    - cv2.IMREAD_GRAYSCALE 以灰階的格式來讀取圖片。
    - [reference1](https://blog.gtwang.org/programming/opencv-basic-image-read-and-write-tutorial/)
- [reference2](https://www.geeksforgeeks.org/converting-color-video-to-grayscale-using-opencv-in-python/)

# 0727

## revise overlap.py
- rename comparemp4.py to overlap.py
- 測得比較準了，因為之前忘記秒數要＊fps
- 希望下禮拜可以慢慢把程式碼統整

# 0806

- 完成剪接模組 videomodule.py
- BUG : 測出來不準，秒數會有小數點（但目前都是一秒為一單位，可能要0.1秒為一單位？）
- 還要加強overlap.py 

# 0809
- 將overlap.py改成0.5秒為一單位，但測出來結果一樣