import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pytube
import os
from pathlib import Path
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context

url = "https://www.youtube.com/watch?v=Mn535_yHJ9I"
save_path = "/Users/jyoon/Local/Projects/YoutubeDownloader"

def get_download_path():
    download_path = str(Path.home() / "Downloads")
    if os.path.exists(download_path):
        return download_path
    else:
        print(os.getcwd())
        return str(os.getcwd())
    
def select_directory():
    directory = filedialog.askdirectory(initialdir=Path.home(), title="영상을 다운로드 할 위치를 선택해 주세요.")
    if directory:
        save_path.set(directory)

def download_video():
    video_url = url.get()
    path = save_path.get()

    if video_url and path:
        try:
            youtube = pytube.YouTube(video_url)
            stream = youtube.streams.filter(res="720p", file_extension="mp4").first()
            stream.download(output_path=path)
            result_msg.set("다운로드 완료!")
        except Exception as e:
            print(str(e))
            result_msg.set("에러: " + str(e))
    else:
        result_msg.set("영상의 주소가 잘못 되었거나 영상 저장 위치가 잘못되었습니다. 다시 설정해 주세요.")

# Tkinter Settings
window = tk.Tk()
save_path = tk.StringVar()
save_path.set(get_download_path())
url = tk.StringVar()
result_msg = tk.StringVar()

width = 720
height = 480
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)

window.title("유튜브 영상 다운로드")
window.geometry('%dx%d+%d+%d' % (width, height, x, y))
window.resizable(False, False)

# Frame Settings
directory_frame = ttk.Frame(master = window)
content_frame = ttk.Frame(master = window)
result_frame = ttk.Frame(master = window)

# Title Label
title_label = ttk.Label(master = window, text = "유튜브 영상 다운로드", font = ("Calibri 24 bold"))
title_label.pack(pady=30)

# Directory Label
directory_label = ttk.Label(master = directory_frame, text = "다운로드 할 위치:", font = ("Calibri 14"))
directory_label.pack(side = 'left', padx = 10)

# Directory Path Label
directory_path_label = ttk.Label(master = directory_frame, textvariable = save_path)
directory_path_label.pack(side = 'left', padx = 20)

# Directory Select Button
directory_select_btn = ttk.Button(master = directory_frame, text = "폴더 변경", command = select_directory)
directory_select_btn.pack(side = 'left')

directory_frame.pack(pady=10)

# URL Input
url_input = ttk.Entry(master = content_frame, textvariable=url)
url_input.pack(side = 'left', padx = 10)

# Donwload Button
download_btn = ttk.Button(master = content_frame, text = "Download", command = download_video)
download_btn.pack(side = 'left')

content_frame.pack()

# Result Label
result_label = ttk.Label(master = result_frame, textvariable = result_msg)
result_label.pack(pady = 10)

result_frame.pack()

window.mainloop()
