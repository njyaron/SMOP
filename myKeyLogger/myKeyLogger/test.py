#from ctypes import windll, c_ulong, byref, sizeof, Structure
#user32 = windll.user32

#class RECT(Structure):
#    _fields_ = [
#        ("left", c_ulong),
#        ("top", c_ulong),
#        ("right", c_ulong),
#        ("bottom", c_ulong)];

#class GUITHREADINFO(Structure):
#    _fields_ = [
#    ("cbSize", c_ulong),
#    ("flags", c_ulong),
#    ("hwndActive", c_ulong),
#    ("hwndFocus", c_ulong),
#    ("hwndCapture", c_ulong),
#    ("hwndMenuOwner", c_ulong),
#    ("hwndMoveSize", c_ulong),
#    ("hwndCaret", c_ulong),
#    ("rcCaret", RECT)
#    ]

#def get_layout():
#    guiThreadInfo = GUITHREADINFO(cbSize=sizeof(GUITHREADINFO))
#    user32.GetGUIThreadInfo(0, byref(guiThreadInfo))
#    dwThread = user32.GetWindowThreadProcessId(guiThreadInfo.hwndCaret, 0)
#    return user32.GetKeyboardLayout(dwThread)


#this one really works
def get_layout():
    window_number = win32gui.GetForegroundWindow()
    dwThread = user32.GetWindowThreadProcessId(window_number, 0)
    return user32.GetKeyboardLayout(dwThread)






import win32api
import win32console
import win32gui
import pythoncom, pyHook

def OnKeyboardEvent(event):
    print('MessageName:',event.MessageName)
    print('Message:',event.Message)
    print('Time:',event.Time)
    print('Window:',event.Window)
    print('WindowName:',event.WindowName)
    print('Ascii:', event.Ascii, chr(event.Ascii))
    print('Key:', event.Key)
    print('KeyID:', event.KeyID)
    print('ScanCode:', event.ScanCode)
    print('Extended:', event.Extended)
    print('Injected:', event.Injected)
    print('Alt', event.Alt)
    print('Transition', event.Transition)
    print('Layout', get_layout())
    print('---')
    # return True to pass the event to other handlers
    return True

# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse events
hm.KeyDown = OnKeyboardEvent
hm.KeyUp = OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()