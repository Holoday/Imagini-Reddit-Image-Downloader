#created by Nathan Myers
#v1.0.5 - 2/22/2020 Earth Time

import praw,requests,re,os,platform,sys
from time import sleep

#dir_path = os.path.dirname(os.path.realpath(__file__))

#Console Clearing Function
if platform.system() == 'Windows':
    clear = lambda: os.system('cls') #WINDOWS


elif platform.system() == 'Linux':
    clear = lambda: os.system('clear') #LINUX
else: #up yours mac kernel
    sys.exit("Please use either Windows or Linux to run this program.")

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

#image downloader, are you blind??
def image_downloader(subred,amount,statustf):     
    #Reddit Script UID Setup
    r = praw.Reddit(
    client_id = 'yourid',
    client_secret = 'yoursecret',
    username='youruid',
    password='yourpw',
    user_agent='reddittestdownloader'
    )
    #Subreddit of your choice
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
            #POI: updates 'progress' value and then the update bar so you get a nice little bar in theory, but instead it doesn't work. I've tried Global progress, to no avail.
            progress['value'] += 100/amount
            root.update_idletasks()
    progress['value'] = 0
    root.update_idletasks()

#root.geometry("700x500")
import tkinter as tk
import ast
from tkinter import filedialog
import re
import math
from tkinter.ttk import *
import threading

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 400, height = 450,  relief = 'raised')
canvas1.pack()
#root.wm_attributes("-topmost", True)
#root.wm_attributes("-transparentcolor", "light grey")
#root.wm_attributes('-alpha',0.3)

label1 = tk.Label(root, text='Reddit Image Downloader v1.3.1')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Please Enter Subreddit Name:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

root.title('Reddit Image Downloader')

entry1 = tk.Entry (root) 
canvas1.create_window(200, 140, window=entry1)

label2 = tk.Label(root, text='Please Enter amount of images to download: ')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 180, window=label2)

entry2 = tk.Entry (root) 
canvas1.create_window(200, 220, window=entry2)



def download():
    
    subreddit = entry1.get()
    #print(subreddit)
    amount_of_images = entry2.get()
    #print(amount_of_images)

    worked = True
    try:
        if sub_exists(subreddit) == False:
            print('This should not show up, uh oh.')
    except:
        label3 = tk.Label(root,text='Subreddit \''+subreddit+'\' does not exist.')
        canvas1.create_window(200,330, window=label3)
        worked = False
    
    try:
        amount_of_images_safe = ast.literal_eval(amount_of_images)
    except:
        label4 = tk.Label(root,text='              Amount of images \''+amount_of_images+'\' is not valid.              ')
        canvas1.create_window(200,360, window=label4)
        worked = False
    
    if 'folderdest' not in globals():
        worked = False
        button2 = tk.Button(text='Change Folder Destination', command=changefolderdest, font=('helvecta',9,'bold'),bg = 'red')
        canvas1.create_window(85,260,window= button2)

    if worked:
        label3 = tk.Label(root,text='Subreddit \''+subreddit+'\' exists.')
        canvas1.create_window(200,330, window=label3)
        label4 = tk.Label(root,text='              Amount of images \''+amount_of_images+'\' is valid.              ')
        canvas1.create_window(200,360, window=label4)
        sleep(1)

        #current code, as multithreading did not work. Instead, it just does the same thing this \/ does. How can I keep root.mainloop() running while running the other thread?
        #image_downloader(subreddit,amount_of_images_safe,False)

        #threading below
        t = threading.Thread(target=image_downloader,args= (subreddit,amount_of_images_safe,False))
        t.start()
        
        #root.mainloop()
        
def changefolderdest():
    dir1 = filedialog.askdirectory(parent=root,title='Destination Folder?')
    if len(dir1)>25:
        label5 = tk.Label(root,text='              Destination Folder set to:              ')
        canvas1.create_window(200,390,window=label5)
        split_dir = re.findall('.?'*60,dir1)

        for loop in range(math.ceil(len(dir1)/60)):
            canvas1.create_window(200,(420+loop*15),window=tk.Label(root,text=split_dir[loop]))

    else:
        label5 = tk.Label(root,text='              Destination Folder set to:\n'+dir1+'              ')
        canvas1.create_window(200,390,window=label5)
    
    button2 = tk.Button(text='Change Folder Destination', command=changefolderdest, font=('helvecta',9,'bold'))
    canvas1.create_window(85,260,window= button2)
    global folderdest
    folderdest = dir1

progress = Progressbar(root, orient = 'horizontal', length = 370, mode = 'determinate') 
canvas1.create_window(200,293, window=progress)
#progress['value'] = 20.5
#root.update_idletasks() 

button1 = tk.Button(text='Download', command=download, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 260, window=button1)

button2 = tk.Button(text='Change Folder Destination', command=changefolderdest, font=('helvecta',9,'bold'))
canvas1.create_window(85,260,window= button2)

button3 = tk.Button(text='                   Settings                 ',font=('helvecta',9,'bold'))
canvas1.create_window(319,260, window=button3)

root.iconbitmap('websites hide here/LL Logo Just Rocket.png')

root.mainloop()