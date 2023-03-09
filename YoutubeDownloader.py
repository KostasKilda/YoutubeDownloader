from pytube import YouTube 
from pytube import Playlist
from pathlib import Path
from tkinter import *
from tkinter import ttk
import urllib.request
from PIL import ImageTk, Image
import io


defaultImgUrl = 'https://mir-s3-cdn-cf.behance.net/projects/404/305eeb62042495.Y3JvcCwxMzg0LDEwODMsMjcwLDA.jpg'
# downloadPath = str(Path.home() / "Downloads")
# print(downloadPath)

# Video
# url = 'https://www.youtube.com/watch?v=lSsvzBV0tyI'

# Playlist
# url = 'https://www.youtube.com/playlist?list=PLeNVp42ZDPZpqNq06kF9qZQYadQ-Ji1nt'

# Stream
# url = 'https://www.youtube.com/watch?v=jfKfPfyJRdk'


root = Tk()

# Method that attempts to check the link again after a failed attempt
# This was made due to Pytube's high failure chance, around 5%-10%
def tryLink(i, link):
    if i < 10:
        try:
            return YouTube(link).title
        except:
            return tryLink(i+1, link)
        

# Check the source of the link
# Determines if it's a playlist, stream, video or invalid link
def viewSource():
    # Checking if the link is playlist
    if(url.get().find('playlist?')!=-1):
        playlist = Playlist(url.get())
        if(len(playlist)!=0):
            for video in playlist:
                print(tryLink(0, video))
        else:
            print('The youtube link is not valid')
    else:
        # Checking if the link is valid and leads to a video
        youtubeLink = tryLink(0, url.get())
        if(youtubeLink!=None):
            changeImage(YouTube(url.get()).thumbnail_url)
            print(youtubeLink)
        else:
            print('The youtube link is not valid')


# Method that acts as a trigger event for "Search" button
def sendInfo():
    # Checking if the link is valid
    if(len(url.get())>5 and (url.get().lower().find('yout')!=-1)):
        viewSource()
    else:
        print('The youtube link is not valid')


# Method that is called to change the placeholder or current image
def changeImage(imageUrl):
    with urllib.request.urlopen(imageUrl) as url_image:
        image_bytes = url_image.read()
        image = Image.open(io.BytesIO(image_bytes))
    image = image.resize((180, 160))
    photo_image = ImageTk.PhotoImage(image)
    label.configure(image=photo_image)
    label.image = photo_image
        

# Method that is called when starting the application, that loads the default image as a placeholder.
def loadDefaultImage(imageUrl):
    with urllib.request.urlopen(imageUrl) as url_image:
        image_bytes = url_image.read()
        return(Image.open(io.BytesIO(image_bytes)))
    



# Setting the window size and open location to the middle of the screen
root.geometry('450x300+%d+%d' % ( root.winfo_screenwidth()/2.6,root.winfo_screenheight()/3.6))
root.grid()


ttk.Label(root, text="Enter a link to a youtube video, stream or playlist", font=('Arial', 14), padding=(20)).grid(column=0, row=0, columnspan=2)
url = Entry(root ,width='46')
ttk.Button(root, text="Search", command=sendInfo).grid(column=1, row=1)


# Setting the label for later image use
label = Label(root)


# Setting grid layout for things
url.grid(column=0, row=1)
label.grid(column=0, row=3, sticky='w', padx=20, pady=20)

# load the default image
changeImage(defaultImgUrl)


root.pack_slaves()
root.mainloop()












# youtube = 'https://mir-s3-cdn-cf.behance.net/projects/404/305eeb62042495.Y3JvcCwxMzg0LDEwODMsMjcwLDA.jpg'
# # youtube = YouTube('https://www.youtube.com/watch?v=lSsvzBV0tyI')

# thumbnail_url = youtube.thumbnail_url
# with urllib.request.urlopen(thumbnail_url) as url_image:
#     image_bytes = url_image.read()
#     image = Image.open(io.BytesIO(image_bytes))

# image = image.resize((160, 160))
# photo_image = ImageTk.PhotoImage(image)
# label = Label(root, image=photo_image)