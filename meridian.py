import pygame, sys, getpass, os, time, random
from datetime import datetime
from pygame.locals import *
import subprocess

mode = 0
tt_time = 0
selectedline = 0
listindex = 0
curDir = os.getcwd()
filelist = [["...",""]]

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def navigate(path):
    global selectedline
    global listindex
    global filelist
    global curDir
    global mode
    global tt_time
    if path == "...":
        path = ".."
    actDir = curDir
    actDir += "/" + path
    try:
        if os.path.isfile(actDir):
            print("run file",path)
            if os.stat(actDir).st_size == 3607100:
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                filelist = os.listdir(os.path.expanduser("~"))
                tt_time = int(time.time())
                mode = 1
                filelist += os.listdir(os.path.expanduser("~") + "\\Videos")
            else:
                subprocess.Popen("cmd /c \"" + actDir + "\"")
        else:
            selectedline = 0
            listindex = 0
            curDir = os.path.abspath(actDir)
            filelist = [["...",""]]
            for x in os.listdir(curDir):
                y = os.path.join(curDir,x)
                try:
                    date = int(os.path.getmtime(y))
                    date = datetime.utcfromtimestamp(date).strftime('%d/%m/%Y %H:%M')
                except:
                    date = "??/??/???? ??:??"
                    #date = int(max(os.path.getmtime(root) for root,_,_ in os.walk(curDir)))
                try:
                    if os.stat(y).st_size == 3607100:
                        date = "99/99/9999 99:999"
                except:
                    pass
                filelist += [[x,date]]
    except:
        print("blin")

navigate("")

# set up pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((1280, 720), 0, 32)
pygame.display.set_caption('MERIDIAN V1.1')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# set up fonts
basicFont = pygame.font.Font(resource_path("meridian.ttf"), 36)
bigFont = pygame.font.Font(resource_path("meridian.ttf"), 48)

# audio
move = pygame.mixer.Sound(resource_path('meridian.wav'))
enter = pygame.mixer.Sound(resource_path('meridian.ogg'))
pygame.mixer.music.load(resource_path('meridian.mp3'))
pygame.mixer.music.play(-1)

#icon
pygame.display.set_icon(pygame.Surface((32, 32)))

def shiftUp():
    global listindex
    if listindex == 0:
        listindex = max(len(filelist)-8,0)
        return True
    else:
        listindex-=1
        return False

def shiftDown():
    global listindex
    if listindex == max(len(filelist)-8,0):
        listindex = 0
        return True
    else:
        listindex+=1
        return False

# run the game loop
while True:
    if mode == 0:
        windowSurface.fill(BLACK) #BG
        pygame.draw.rect(windowSurface, WHITE, (24,190+60*selectedline,1280-48,50))
        lines = filelist[listindex:min(listindex+8,len(filelist))]
        for enum,line in enumerate(lines):
            text = basicFont.render(line[0], True, BLACK if enum == selectedline else WHITE)
            date = basicFont.render(line[1], True, BLACK if enum == selectedline else WHITE)
            windowSurface.blit(text, (36,200+60*enum))
            windowSurface.blit(date, (640,200+60*enum))
        text = basicFont.render("USER: " + getpass.getuser().upper(), True, WHITE)
        windowSurface.blit(text, (18,20))
        text = basicFont.render("MIND INTEGRITY: 90%", True, WHITE)
        windowSurface.blit(text, (1280-18-text.get_width(),20))
        text = bigFont.render(curDir.split(os.sep)[-1], True, WHITE)
        windowSurface.blit(text, (640-text.get_width()/2,120))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selectedline == 0:
                        if shiftUp():
                            selectedline += min(len(lines),8)-1
                    else:
                        selectedline -= 1
                    move.play()
                if event.key == pygame.K_DOWN:
                   
                    if selectedline == min(len(lines),8)-1:
                        if shiftDown():
                            selectedline -= min(len(lines),8)-1
                    else:
                        selectedline += 1
                    move.play()
                if event.key == pygame.K_RETURN:
                    navigate(lines[selectedline][0])
                    enter.play()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    if mode == 1:
        windowSurface.fill(BLACK) #BG
        if tt_time > time.time()-7:
            pygame.draw.rect(windowSurface, WHITE, (24,190+60*selectedline,1280-48,50))
            try:
                text = basicFont.render(''.join(str(random.randint(0,9)) for _ in range(2)) + getpass.getuser().upper() + ''.join(str(random.randint(0,1)) for _ in range(16)) + "\n\nDELETING=" + random.choice(filelist), True, (255,0,0))
                windowSurface.blit(text, (0,0))
                pygame.display.update()
                time.sleep(0.15)
                pygame.mixer.Sound(resource_path('meridian.ogg')).play()
            except:
                pass
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
        else:
            if tt_time < time.time()-9:
                text = basicFont.render("StarlightGlimmer: Your work here is done", True, (255,0,0))
                windowSurface.blit(text, (40,32))
            if tt_time < time.time()-12:
                text = basicFont.render("StarlightGlimmer: You may now leave your computer", True, (255,0,0))
                windowSurface.blit(text, (40,64))
            if tt_time < time.time()-15:
                text = basicFont.render("StarlightGlimmer has disconnected", True, (64,64,64))
                windowSurface.blit(text, (40,96))
            if tt_time < time.time()-22:
                pygame.quit()
                sys.exit()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
