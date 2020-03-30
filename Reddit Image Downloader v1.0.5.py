#created by Nathan Myers
#v1.0.5 - 2/22/2020 Earth Time

import praw,requests,re,os,platform,sys
from time import sleep

dir_path = os.path.dirname(os.path.realpath(__file__))

#Console Clearing Function
if platform.system() == 'Windows':
    clear = lambda: os.system('cls') #WINDOWS
elif platform.system() == 'Linux':
    clear = lambda: os.system('clear') #LINUX
else: #up yours mac kernel
    sys.exit("Please use either Windows or Linux to run this program.")

clear()
print('Reddit Image Downloader\nCreated by **FILE CORRUPTED*\nv1.0.5\nIntended to download memes from subreddit(s) to set as screensavers for viewing pleasure.')
print('More Features like upvote mins soon!')
input('\nPress \'Ctrl + C\' at any time to force quit. Continue? ')

#Create directory
def dirctory_creator(name):
    try:
    #Create target Directory
        os.mkdir(name)
        print("Directory (folder) " , name ,  " Created at "+dir_path) 
    except FileExistsError:
        print("Directory " , name ,  " already exists at "+dir_path)
clear()
dirName = input('Directory (Folder) Name? ')
dirctory_creator(dirName)

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
                with open(dir_path+'/'+dirName+'/'+file_name,"wb") as f:
                    f.write(r.content)
            except OSError:
                if statustf:
                    print('Image Downloader Error')

#downloader menu
def sub_selection_menu(debugger):
    print('Prepping Download...')
    sub = input('What subreddit? ')
    if sub_exists(sub):
        amo = int(input('How many images from this subreddit? '))
        if amo > 100:
            input('Hold up cowboy, that\'s a lot! Are you sure?')
        print('Size Estimate = '+str(amo*.53)+'mb')
        image_downloader(sub,amo,debugger)
    else:
        print('Sorry, that subreddit does not exist.')
        sleep(2)

#main menu
sleep(1.5)
while True:
    clear()
    print('1 : Start\n2 : Debug\n3 : Destination Folder\n4 : Exit')
    menu_select = input('')
    if menu_select != '1' and menu_select != '2' and menu_select != '3' and menu_select != '4':
        print('Invalid Entry.')
    if menu_select == '1':
        clear()
        sub_selection_menu(False)
    elif menu_select == '2':
        print('debug mode activated for one loop')
        sleep(2)
        clear()
        sub_selection_menu(True)
    elif menu_select == '3':
        clear()
        print('Current Directory Is located at : '+ dir_path+'\\'+dirName)
        dirNameTemp = input('What would you like to change this too? ')
        if dirNameTemp:
            dirName = dirNameTemp
        else:
            print('Unexpected Falsy Value.')
            sleep(1.5)
        dirctory_creator(dirName)
    elif menu_select == '4':
        print('Thank you for using [placeholder!]')
        break