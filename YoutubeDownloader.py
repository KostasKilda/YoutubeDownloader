from pytube import YouTube 
from pytube import Playlist
from pathlib import Path
from tkinter import *
from tkinter import ttk
import urllib.request
from PIL import ImageTk, Image
import io
import time
import re
import os
import threading


defaultImgUrl = 'https://mir-s3-cdn-cf.behance.net/projects/404/305eeb62042495.Y3JvcCwxMzg0LDEwODMsMjcwLDA.jpg'
youtubePlaylistImg = 'https://static.wikia.nocookie.net/youtube/images/8/8e/Youtubeplaylist.png/revision/latest?cb=20150311191950'


# downloadPath = str(Path.home() / "Downloads")
# print(downloadPath)

# Video
# url = 'https://www.youtube.com/watch?v=lSsvzBV0tyI'
# https://www.youtube.com/watch?v=lSsvzBV0tyI

# Playlist
# url = 'https://www.youtube.com/playlist?list=PLeNVp42ZDPZpqNq06kF9qZQYadQ-Ji1nt'

root = Tk()

# Method that attempts to check the link again after a failed attempt
# This was made due to Pytube's high failure chance, around 5%-10%
def tryLink(i, link):
    if i < 3:
        try:
            return YouTube(link)
        except:
            return tryLink(i+1, link)
        
def retrieveInformation(i, youtubeLink):
    if i < 3:
        try:
            changeImage(youtubeLink.thumbnail_url)
            changeVideoTitle(youtubeLink.title)
        except:
            # Calls the original method to redetermine if the link is valid
            # Solves an error of youtube link property not having a title element
            viewSource(i+1)
    else:
        changeImage(defaultImgUrl)
        changeVideoTitle('None')

def changePlaylistTitle(playlistUrl):
    # Send a GET request to the playlist URL and read the HTML content
    with urllib.request.urlopen(playlistUrl) as response:
        html_content = response.read().decode()

    # Use regular expressions to extract the playlist title and thumbnail URL from the HTML content
    title_match = re.search('<title>(.*?) - YouTube</title>', html_content)

    # Retrieve the playlist title and thumbnail URL from the regular expression matches
    playlist_title = title_match.group(1)

    changeVideoTitle(playlist_title)

# Check the source of the link
# Determines if it's a playlist, stream, video or invalid link
def viewSource(i):
    # Checking if the link is playlist
    if(url.get().find('playlist?')!=-1):
        playlist = Playlist(url.get())
        if(len(playlist)!=0):
            changePlaylistTitle(url.get())   
            try:
                changeImage(YouTube(playlist[0]).thumbnail_url)
            except:
                changeImage(youtubePlaylistImg)
        else:
            changeImage(defaultImgUrl)
            changeVideoTitle('None')
    else:
        # Checking if the link is valid and leads to a video
        youtubeLink = tryLink(0, url.get())
        if(youtubeLink!=None):
            retrieveInformation(i, youtubeLink)
        else:
            changeImage(defaultImgUrl)
            changeVideoTitle('None')


# Method that acts as a trigger event for "Search" button
def sendInfo(option):
    # Checking if the link is valid
    if(len(url.get())>5 and (url.get().lower().find('yout')!=-1)):
        if(option==1):
            thread = threading.Thread(target=startDownload)
            thread.start()
        viewSource(0)
    else:
        changeImage(defaultImgUrl)
        changeVideoTitle('None')


# Method that is called to change the placeholder or current image
def changeImage(imageUrl):
    with urllib.request.urlopen(imageUrl) as url_image:
        image_bytes = url_image.read()
        image = Image.open(io.BytesIO(image_bytes))
    image = image.resize((140, 140))
    photo_image = ImageTk.PhotoImage(image)
    placeHolderImg.configure(image=photo_image)
    placeHolderImg.image = photo_image

def findTitleNewLine(title):
    matches = [m.start() for m in re.finditer(' ', title)]
    if matches != [] and matches[0]<18:
        i = len(matches)-1
        while i!=0:
            if(matches[i]<=18):
                return matches[i]+1
            i-=1
    else:
        return 18
        
# Method that will change video title
def changeVideoTitle(videoTitle):
    if(len(videoTitle)>18):
        breakPoint = findTitleNewLine(videoTitle)
        if(len(videoTitle)>=62):
            videoName.configure(text="Video name: %s\n %s..." % (videoTitle[:breakPoint],videoTitle[breakPoint:61]))
        else:
            videoName.configure(text="Video name: %s\n%s" % (videoTitle[:breakPoint], videoTitle[breakPoint:]))
    else:
        videoName.configure(text="Video name: %s" % videoTitle)


def createFolder():
    downloadPath = str(Path.home() / "Downloads")
    folderName = 'Youtube downloads'
    if not os.path.exists(os.path.join(downloadPath, folderName)):
        os.mkdir(os.path.join(downloadPath, folderName))
    return os.path.join(downloadPath, folderName)

def startDownload():
    downloadPath = createFolder()
    if(url.get().find('playlist?')!=-1):
            playlistUrl = Playlist(url.get())

            for video_url in playlistUrl.video_urls:
                # download video
                try:
                    yt = YouTube(video_url)
                    stream = yt.streams.get_highest_resolution()
                    stream.download(output_path=downloadPath)
                except: 
                    try:
                        yt = YouTube(video_url)
                        stream = yt.streams.get_highest_resolution()
                        stream.download(output_path=downloadPath)
                    except: 
                        try:
                            yt = YouTube(video_url)
                            stream = yt.streams.get_highest_resolution()
                            stream.download(output_path=downloadPath)
                        except:        
                            print('Not a valid playlist')
    else:
        try:
            yt = YouTube(url.get())
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            stream.download(output_path=downloadPath)
        except:
            print('Not a valid video')



def downLoad():
    sendInfo(1)

def search():
    sendInfo(0)

# Setting the window size and open location to the middle of the screen
root.geometry('380x380+%d+%d' % ( root.winfo_screenwidth()/2.6,root.winfo_screenheight()/3.6))
root.grid()

style = ttk.Style()



ttk.Label(root, text="Enter a link to a youtube video or playlist", font=('Arial', 14), padding=(20), background='white').grid(column=0, row=0, columnspan=2)
url = Entry(root ,width='46')
ttk.Button(root, text="Search", command=search).grid(column=1, row=1)
videoName = Label(root, text="Video name: None", font=('Arial', 10), anchor='w', justify='left')

style.theme_create('downloadstyle', parent='alt', settings={"Download.TButton": {"configure": {"foreground": "#ffffff", "background": "#4CAF50", "font": ('Arial', 10),
        "padding": (8, 5), "borderwidth": 0, "bordercolor": "#4CAF50", "borderradius": "50%"}, "map": {"background": [("active", "#4CAF50"), ("pressed", "#4CAF50")]}}})
style.theme_use('downloadstyle')
ttk.Button(root, text="Download", command=downLoad, style='Download.TButton').grid(column=0, row=4, columnspan=2, sticky='s')


# Setting the label for later image use
placeHolderImg = Label(root)


# Setting grid layout for things
url.grid(column=0, row=1)
placeHolderImg.grid(column=0, row=3, sticky='w', padx=20, pady=20)
videoName.grid(column=0, row=3,sticky='w', padx=(170,0), pady=(30,140), columnspan=2)

# load the default image
changeImage(defaultImgUrl)

root.pack_slaves()
root.mainloop()