import win32gui
from ctypes import windll
user32 = windll.user32
import pickle
import os
import time
import keyboard
import threading
import digraph, featureGenerator

TIME_BETWEEN_UPDATES = 60 #seconds
MAIN_DIRECTORY_PATH = ''
DEFAULT_PREFIX = 'data_'

#loading stuff
filter = featureFilter.Filter(long_time=digraph.LONG_TIME)
feature_type = featureGenerator.DIGRAPH_TYPE
loc = "allYouNeed.p" 
all_you_need = pickle.load( open( loc, "rb" ) )
trainings_avg = all_you_need['trainings_avg']
keys_digraph = all_you_need['keys_digraph']
names = all_you_need['names']

me = {key:[] for key in keys_digraph} # {key:[data...], key:[data],...}

#parsing functions
def get_estimates_single_sample(sample, debug=False):
    sample_avg = {key:statistics.mean(data) for key,data in sample.items() if data} 
    d = [0 for p in trainings_avg]
    for key in sample_avg.keys():
        for i,person_avg in enumerate(trainings_avg.values()):
            d[i] += abs(sample_avg[key] - person_avg[key])
    d = sorted(list(zip(d,trainings_avg.keys())))
    return d #[ (score,name), (score,name),...]

#os functions
def get_max_name(namelist, prefix):
    newlist = [f[len(prefix):] for f in namelist]
    numbers_list = [int(f) for f in newlist if f.isdecimal()]
    if numbers_list:
        return max(numbers_list)
    else:
        return 0

#more os functions
def get_current_file_number(dir_path, prefix=DEFAULT_PREFIX):
    onlyfiles = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and f.startswith(prefix)]
    return get_max_name(onlyfiles, prefix)
        
def get_next_filename(dir_path, prefix=DEFAULT_PREFIX):
    return os.path.join(dir_path,prefix+str(get_current_file_number(dir_path, prefix)+1))

FILENAME = get_next_filename(MAIN_DIRECTORY_PATH,DEFAULT_PREFIX)

#recording functions
def get_layout():
    window_number = win32gui.GetForegroundWindow()
    dwThread = user32.GetWindowThreadProcessId(window_number, 0)
    return user32.GetKeyboardLayout(dwThread)

def get_language():
    return get_layout()%(2**16)

def get_window_name():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())

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
        self.c = 0

    def save_data(self):
        pickle.dump(me, open(FILENAME, 'wb+'))
        
    def update_data(self): #this clears 'self.recorded' if it is too large
        #if needs to write to new file
            keys2data = featureGenerator.create_data(self.recorded,filter,feature_type)
            self.recorded.clear()
            for key in me.keys():
                me[key].extend(keys2data[key])
            last_update = time.time()
            c += 1
            if c % 10 == 0:
                self.save_data()

            #estimate and print
            d = get_estimates_single_sample(me)
            print("\n"*4)
            print(d[:3])

    def run(self):
        while (True):
            time.sleep(TIME_BETWEEN_UPDATES)
            self.update_data()

if __name__ == "__main__":
    try:
        #inititalize 
        recorded = []
        add_event = get_event_adder(recorded)
        
        #start recording and set schedualed thread
        start_record(add_event)
        saver = SaverThread(recorded)
        saver.daemon = True
        saver.start()
        #wait for special recording instruction
        while True: 
            code_name = input()
            if code_name == "EXIT":
                break
    except KeyboardInterrupt:
        print("Finishing to record")
    finally:
		#save data and finish
        saver.save_data()
        end_record(add_event)
        print("The program is closing")
