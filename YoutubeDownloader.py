import customtkinter
import threading
from pytube import YouTube 
from pytube import Playlist
import requests
from pathlib import Path
from PIL import ImageTk, Image
import io
import os

def processUrl():

    url = entry.get()

    # Brief URL validation
    if(not (('youtu.be/' in url) or ('youtube.com/playlist' in url) or ('youtube.com/watch' in url))):
        return
    
    # Acquiring the URL to a global variable for later use
    global videoUrl

    if ('youtube.com/playlist' in url):
        videoUrl = ['Playlist', url]
        
        updateSearchVideo(Playlist(url)[0], 'Playlist: ' + Playlist(url).title)
        # changeVideoTitle('Playlist: ' + Playlist(url).title)

    else:
        videoUrl = ['Video', url]
        updateSearchVideo(url, YouTube(url).title)
        # changeVideoTitle(YouTube(url).title)
    

# Adding the thumbnail of the video, title and download button after the URL has been found
def updateSearchVideo(url, title):
    thumbnail_image = Image.open(io.BytesIO(requests.get(YouTube(url).thumbnail_url).content))
    thumbnail_image.thumbnail((200, 140))
    thumbnail_photo = ImageTk.PhotoImage(thumbnail_image)
    image_label = customtkinter.CTkLabel(master=frame, image=thumbnail_photo, text='')
    image_label.grid(row=2, column=0, pady=12, padx=10, sticky='W', rowspan=2 , columnspan=2)

    if(len(title)>100):
        title = title[:99] + '...'

    videoTitle.configure(text=title)

    downloadButton = customtkinter.CTkButton(master=frame, text='Download', width=100, command=createDownloadThread)
    downloadButton.grid(row=3, column=2, pady=(12, 26), padx=12, sticky="S", columnspan=2)



def fetchDownloadUrl():
    # Validating that videoUrl variable exists
    try:
        videoUrl[0]
        videoUrl[1]
    except:
        return
    
    global downloadPath
    downloadPath = createFolder()

    if(videoUrl[0] == 'Playlist'):
        playlist = Playlist(videoUrl[1])
        for url in playlist:
            download(url, 0)

    elif(videoUrl[0] == 'Video'):
        download(videoUrl[1], 0)


def createFolder():
    downloadPath = str(Path.home() / "Downloads")
    folderName = 'Youtube downloads'
    if not os.path.exists(os.path.join(downloadPath, folderName)):
        os.mkdir(os.path.join(downloadPath, folderName))
    return os.path.join(downloadPath, folderName)


def download(url, itteration):
    if(itteration < 10):
        print(itteration)
        try:
            YouTube(url).streams.get_highest_resolution().download(output_path=downloadPath)
        except:
            download(url, itteration+1)
        return True

def createDownloadThread():
    thread = threading.Thread(target=fetchDownloadUrl, daemon=True)
    thread.start()

def createSearcgThread():
    thread = threading.Thread(target=processUrl, daemon=True)
    thread.start()




customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("500x300")
root.title("Youtube downloader")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=10, padx=10, fill='both', expand=True)

label = customtkinter.CTkLabel(master=frame, text='Enter a youtube video/playlist link', font=("Roboto", 24, 'bold'))
label.grid(row=0, column=0, pady=12, padx=10, columnspan=4, sticky='NSEW')

entry = customtkinter.CTkEntry(master=frame, placeholder_text='Link', width=330)
entry.grid(row=1, column=0, pady=12, padx=10, columnspan=3)

button = customtkinter.CTkButton(master=frame, text='Search', width=100, command=createSearcgThread)
button.grid(row=1, column=3, pady=12, padx=10)

videoTitle = customtkinter.CTkLabel(master=frame, text='', font=("Roboto", 16,), wraplength=240)
videoTitle.grid(row=2, column=2, pady=(18,0), padx=(0,10), sticky='W', columnspan=2)

placeholder_image = ImageTk.PhotoImage(Image.new(mode='RGB', size=(200, 140), color=(43,43,43)))
image_label = customtkinter.CTkLabel(master=frame, image=placeholder_image, text='')
image_label.grid(row=2, column=0, pady=12, padx=10, sticky='W', rowspan=2, columnspan=2)

root.mainloop()