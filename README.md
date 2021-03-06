# 智慧影音接軌

> Design a video editing software, focusing on making remote teaching videos easily.
 
## Function
在錄影過程中，如果不小心口誤，可 以暫時安靜一小段時間，然後說明一段 語音指令，接著再靜默一小段時間後， 再重新錄製那段話以及之後的內容，最後應用程式就可以自己分析 語音指令，並自動為影片進行剪接工作。
- 語音指令
- 自動影片剪接
- 字幕
- 分段標題

## 研究方法及步驟
1. 軟體需求的訂定：
    - 編修指令：剪接、重覆、分段標題、字幕。
    - 語音指令：前後用空白隔開。透過程式抓到語音指令，再用辨識引摯找出指令文字。最後透過指令的內容對影片做處理 。
    - 各段影片能透過語音指令自動剪接、重覆片段、下標題。
    - 字幕：將語音轉成文字，加上時間點做成字幕檔案。播放器可以直接抓影片和字幕檔，同步播放。
    - 設計理想的使用者界面。

2. 相關軟體的學習與使用：
    - Anaconda：設定 Python 的工作環境，在開發時建立專屬的虛擬環境。
    - MoviePY的基本使用：影片編輯的Python庫，能進行剪切、重複，可用來做影片處理和創建自定義的效果。
    - FFMPEG的使用：執行音訊和視訊多種格式的錄影、轉檔、串流功能。
    - PyQt5的基本使用：採用 Qt 的 GUI 架構。在圖形使用者介面中，電腦畫面上顯示視窗、圖示、按鈕等圖形，表示不同目的之動作，使用者通過滑鼠等指標裝置進行選擇。
    - 使用Git進行軟體專案的建立與管理。

3. 計畫應用程式的開發 :
    - 主要的軟體模組開發：語音辨識模組、影片剪接模組、分段標題、字幕模組。
    - 語音指令的模組開發：先抓到影片中的語音指令(前後空白)，再透過語音辨視模組辨識其中的指令，接著使用指令內容進行影片的處理。
    - 影片剪接模組：接收到語音指令後，在指令前後的影片中找出相似處，並進行影片剪接。
    - 分段標題模組：接到語音指令後，使用分段標題剪接模組，使其能自動在影片中建立分段標題頁及影片串接。
    - 字幕模組：開發字幕模組，播放器會直接抓影片和字幕檔，同步播放。

4. 應用的測試與除錯：
    - 先建立測試影片。
    - 使用測試影片進行測式。
    - 除錯。

5. 計畫文件撰寫：
    - 軟體模組使用說明。
    - 應用程式的說明。
    - 計畫結案報告 。


## Reference
- [sololearn](https://www.sololearn.com/learning/1073)
- [anaconda](https://docs.anaconda.com/)
- [MoviePY](https://pypi.org/project/moviepy/)
- [pyqt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [terminal command](https://gitbook.tw/chapters/command-line/command-line.html)
