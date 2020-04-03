#created by Holoday
#v0.4.2 - 4/3/2020 Earth Time

import ast
import math
import os
import platform
import re
import sys
import threading
import tkinter as tk
from tkinter import messagebox
from time import sleep
from tkinter import filedialog
from tkinter.ttk import *

import praw
import requests


#sub exists checker function
def sub_exists(sub):
    exists = True
    r = praw.Reddit(
    client_id = 'yourid',
    client_secret = 'yoursecret',
    username='youruid',
    password='yourpw',
    user_agent='reddittestdownloader'
    )
    try:
        r.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        exists = False
    return exists

download_in_progress = False
#image downloader, are you blind??
def image_downloader(subred,amount,statustf):
    global download_in_progress
    download_in_progress = True
    #Reddit Script UID Setup
    r = praw.Reddit(
    client_id = 'yourid',
    client_secret = 'yoursecret',
    username='youruid',
    password='yourpw',
    user_agent='reddittestdownloader'
    )
    subreddit = r.subreddit(subred)

    #Check Sticked 'pinned' posts
    stickied_post = []
    for sticky in subreddit.hot(limit=amount):
        if sticky.stickied:
            stickied_post.append(sticky.id)
    
    #Checks if content is in [] of stickied posts
    for submission in subreddit.hot(limit=amount):
        if submission.id not in stickied_post:
            post = submission
    #if not, downloads
            url = (post.url)
            file_name = url.split("/")
            if len(file_name) == 0:
                file_name = re.findall("/(.*?)", url)
            file_name = file_name[-1]
            if "." not in file_name:
                file_name += ".jpg"
            if statustf:
                print(url)
                print(file_name)
            try:
                r = requests.get(url)
                with open(folderdest+'/'+file_name,"wb") as f:
                    f.write(r.content)
            except OSError:
                pass
            progress['value'] += 100/amount
            root.update_idletasks()
    progress['value'] = 0
    root.update_idletasks()
    download_in_progress = False

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 400, height = 450,  relief = 'raised', highlightthickness=0)
canvas1.pack()
canvas1['bg'] = '#141414'
root['bg'] = '#141414'

root.title('Reddit Image Downloader v1.3.5')

label1 = tk.Label(root, text='Reddit Image Downloader v1.3.5')
label1.config(font=('verdana', 15),bg='#141414',fg='#fffffe')

canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Please Enter Subreddit Name:')
label2.config(font=('verdana', 10),bg='#141414',fg='#fffffe')
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry (root) 
entry1.config(insertbackground='white',bg='#3e3e3d',fg='#fffffe')
canvas1.create_window(200, 140, window=entry1)

label2 = tk.Label(root, text='Please Enter amount of images to download: ')
label2.config(font=('verdana', 10))
label2['bg'] = '#141414'
label2['fg'] = '#fffffe'
canvas1.create_window(200, 190, window=label2)

entry2 = tk.Entry (root) 
entry2.config(insertbackground='white',bg='#3e3e3d',fg='#fffffe')
canvas1.create_window(200, 220, window=entry2)

def download():
    
    subreddit = entry1.get()

    amount_of_images = entry2.get()

    worked = True
    try:
        if sub_exists(subreddit) == False:
            pass
    except:
        label3 = tk.Label(root,text='             Subreddit \''+subreddit+'\' does not exist.             ')
        label3.config(font=('verdana', 10),bg='#141414',fg='#fffffe')
        canvas1.create_window(200,330, window=label3)
        worked = False
    if worked:
        if not subreddit:
            label3 = tk.Label(root,text='             Subreddit value is falsy.             ')
            label3.config(font=('verdana', 10),bg='#141414',fg='#fffffe')
            canvas1.create_window(200,330, window=label3)
            worked = False


    try:
        amount_of_images_safe = ast.literal_eval(amount_of_images)
    except:
        if not amount_of_images:
            label4 = tk.Label(root,text='              Amount of images is not valid.              ')
        else:
            label4 = tk.Label(root,text='              Amount of images \''+amount_of_images+'\' is not valid.              ')
        label4.config(font=('verdana', 10),bg='#141414',fg='#fffffe')
        canvas1.create_window(200,360, window=label4)
        worked = False
    
    if 'folderdest' not in globals():
        worked = False
        button2 = tk.Button(text='Change Folder Destination', command=changefolderdest, font=('helvecta',9,'bold'),bg = 'red')
        canvas1.create_window(85,260,window= button2)

    if worked:
        label3 = tk.Label(root,text='Subreddit \''+subreddit+'\' exists.')
        label3.config(font=('verdana', 10),bg='#141414',fg='#fffffe')
        canvas1.create_window(200,330, window=label3)
        label4 = tk.Label(root,text='              Amount of images \''+amount_of_images+'\' is valid.              ')
        label4.config(font=('verdana', 10),bg='#141414',fg='#fffffe')
        canvas1.create_window(200,360, window=label4)

        t = threading.Thread(target=image_downloader,args= (subreddit,amount_of_images_safe,False))
        t.setDaemon(True)
        t.start()
        
def changefolderdest():
    dir1 = filedialog.askdirectory(parent=root,title='Destination Folder?')
    if not dir1:
        label5 = tk.Label(root,text='                        Invalid Folder Destination                        ')
        label5.config(font=('verdana', 10),bg='#141414',fg='#ff0001')
        canvas1.create_window(200,390,window=label5)
        return

    if len(dir1)>25:
        label5 = tk.Label(root,text='              Destination Folder set to:              ')
        label5.config(font=('verdana', 10),bg='#141414',fg='#fffffe')
        canvas1.create_window(200,390,window=label5)
        split_dir = re.findall('.?'*60,dir1)

        for loop in range(math.ceil(len(dir1)/60)):
            label6 = tk.Label(root,text=split_dir[loop])
            label6.config(font=('verdana', 10),bg='#141414',fg='#fffffe')
            canvas1.create_window(200,(420+loop*15),window=label6)

    else:
        label5 = tk.Label(root,text='              Destination Folder set to:\n'+dir1+'              ')
        label5.config(font=('verdana', 10))
        label5['bg'] = '#141414'
        label5['fg'] = '#fffffe'
        canvas1.create_window(200,390,window=label5)
    
    button2 = tk.Button(text='Change Folder Destination', command=changefolderdest, font=('helvecta',9,'bold'),borderwidth=0, bg = '#242424', fg = 'white')
    canvas1.create_window(85,260,window= button2)
    global folderdest
    folderdest = dir1

settings = tk.Tk()
settings.withdraw()
settings_canvas = tk.Canvas(settings, width = 400, height = 450,  relief = 'raised', highlightthickness=0)
settings_canvas['bg'] = '#141414'
settings_canvas.pack()
settings['bg'] = '#141414'
settings.title('Application Settings (WIP)')
settings.iconbitmap('websites hide here/LL Logo Just Rocket.png')

'''
label8 = tk.Label(root,text='Minimum Upvotes')
label8.config(font=('verdana', 10),bg='#141414',fg='#fffffe')

settings_canvas.create_window(200,200,window=label8)
'''

min_votes = tk.Scale(settings,orient = 'horizontal',borderwidth=0,bg = '#242424', fg = 'white',length=360)
settings_canvas.create_window(200,100,window=min_votes)

root.title('Reddit Image Downloader v1.3.5')
def settings_toggle():
    if 'normal' == settings.state():
        settings.withdraw()
    else:
        settings.update()
        settings.deiconify()

def close_windows():
    if download_in_progress:
        if tk.messagebox.askokcancel("Quit", "Download Is Currently In Progress. Proceeding will interupt the downloading process."):
            try:
                root.destroy()
                settings.destroy()
            except:
                pass
    else:
        try:
            root.destroy()
            settings.destroy()
        except:
            pass

progress = Progressbar(root, orient = 'horizontal', length = 370, mode = 'determinate') 
canvas1.create_window(200,293, window=progress)

button1 = tk.Button(text='Download', command=download, bg='red', fg='white', font=('helvetica', 9, 'bold'), borderwidth=0,activebackground='light green')
canvas1.create_window(200, 260, window=button1)

button2 = tk.Button(text='Change Folder Destination', command=changefolderdest, font=('helvecta',9,'bold'), bg = '#242424', fg = 'white',borderwidth=0)
canvas1.create_window(85,260,window= button2)

button3 = tk.Button(text='                   Settings                 ',font=('helvecta',9,'bold'), bg = '#242424', fg = 'white', borderwidth=0, command =settings_toggle)
canvas1.create_window(319,260, window=button3)

root.iconbitmap('websites hide here/LL Logo Just Rocket.png')

root.protocol("WM_DELETE_WINDOW", close_windows)

root.mainloop()
