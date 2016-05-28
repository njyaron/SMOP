import win32gui
from ctypes import windll
user32 = windll.user32
import pickle
import os
import time
import keyboard
import threading

#MAIN_DIRECTORY_PATH = r'F:\Clouds\Dropbox\SMOP\Results'
MAIN_DIRECTORY_PATH = r'..\Results'
DIRECTORY_PREFIX = 'test'+os.getlogin().lower()
DEFAULT_PREFIX = 'data_'
MAX_FILE_SIZE = 1000000 #megabye maximum
WAITING_DURATION = 50 #in seconds
SPECIAL_CODES = ["UNIFORM", "INDIVIDUAL"]
AUTORIZED_CODES = " or ".join(SPECIAL_CODES)
SPECIAL_MSG = "To start recording special text, write: " + AUTORIZED_CODES + ", or EXIT to exit: \n"
STARTED_RECORDING_SPECIAL = "To finish recording, press 'esc' twice and expect a message \n"
UNAUTORIZED_CODE_MSG = "This is not an authorized code, the codes are: " + AUTORIZED_CODES
DEBUG = False

#recording functions
def get_layout():
    window_number = win32gui.GetForegroundWindow()
    dwThread = user32.GetWindowThreadProcessId(window_number, 0)
    return user32.GetKeyboardLayout(dwThread)

def get_language():
    return get_layout()%(2**16)

def get_window_name():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())

#os functions
def get_max_name(namelist, prefix):
    newlist = [f[len(prefix):] for f in namelist]
    numbers_list = [int(f) for f in newlist if f.isdecimal()]
    if numbers_list:
        return max(numbers_list)
    else:
        return 0

def get_dir_number(dir_path=MAIN_DIRECTORY_PATH, prefix=DIRECTORY_PREFIX):
    onlydirectories = [f for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f)) and f.startswith(prefix)]
    return get_max_name(onlydirectories,prefix)+1

#initialize DIRECTORY_PATH
DIRECTORY_PATH = os.path.join(MAIN_DIRECTORY_PATH,DIRECTORY_PREFIX+str(get_dir_number()))
os.makedirs(DIRECTORY_PATH)

#more os functions
def get_current_file_number(dir_path=DIRECTORY_PATH, prefix=DEFAULT_PREFIX):
    onlyfiles = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and f.startswith(prefix)]
    return get_max_name(onlyfiles, prefix)
        
def get_current_filename(dir_path=DIRECTORY_PATH, prefix=DEFAULT_PREFIX):
    return os.path.join(dir_path,prefix+str(get_current_file_number(dir_path, prefix)))

def get_next_filename(dir_path=DIRECTORY_PATH, prefix=DEFAULT_PREFIX):
    return os.path.join(dir_path,prefix+str(get_current_file_number(dir_path, prefix)+1))

#logging functions
def get_event_adder(recording_list):
    def add_event(event):
        event.language = get_language()
        event.window_name = get_window_name()
        recording_list.append(event)
        if DEBUG:
            print("recorded " + str(event))
    return add_event

@keyboard.listener.wrap 
def start_record(event_handler):
    keyboard.listener.add_handler(event_handler)

@keyboard.listener.wrap
def end_record(event_handler):
    keyboard.listener.remove_handler(event_handler)


class SaverThread(threading.Thread):
    def __init__(self, recording_list):
        super(SaverThread, self).__init__()
        self.recorded = recording_list

    def save_data(self): #this clears 'self.recorded' if it is too large
        #if needs to write to new file
        if os.path.exists(get_current_filename(prefix=DEFAULT_PREFIX)) and \
                os.path.getsize(get_current_filename(prefix=DEFAULT_PREFIX)) > MAX_FILE_SIZE:
            filename = get_next_filename(prefix=DEFAULT_PREFIX)
            pickle.dump(self.recorded, open(filename, 'wb+'))
            self.recorded.clear()
        else: 
            filename = get_current_filename(prefix=DEFAULT_PREFIX)
            pickle.dump(self.recorded, open(filename, 'wb+'))

    def run(self):
        while (True):
            time.sleep(WAITING_DURATION)
            self.save_data()

if __name__ == "__main__":
    try:
        #inititalize 
        recorded = []
        recorded_special = []
        add_event = get_event_adder(recorded)
        add_event_special = get_event_adder(recorded_special)
        
        #start recording and set schedualed thread
        print("starting to record in " + DIRECTORY_PATH)
        start_record(add_event)
        saver = SaverThread(recorded)
        saver.daemon = True
        saver.start()
        #wait for special recording instruction
        while True: 
            code_name = input(SPECIAL_MSG)
            if code_name in SPECIAL_CODES:
                # get text index (the index of the text, since there are 
                # many of same cartegory (UNIFORM, INDIVIDUAL)
                text_index = input("Enter the text index: ")
                print(STARTED_RECORDING_SPECIAL)
                #record special until two escape presses are pressed
                start_record(add_event_special)
                keyboard.wait('esc, esc')
                end_record(add_event_special)
                #store the needed data in a file and clear recorded_special
                data = (code_name, text_index, recorded_special)
                filename = get_next_filename(prefix=code_name)
                pickle.dump(data, open(filename, 'wb+'))
                recorded_special.clear()
            elif code_name == "EXIT":
                break
            else:
                print(UNAUTORIZED_CODE_MSG)
    except KeyboardInterrupt:
        print("Finishing to record")
    finally:
		#save data and finish
        saver.save_data()
        end_record(add_event)
        print("The program is closing")
