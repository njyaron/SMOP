import pickle
import os
DEFAULT_PREFIX = 'data_'
UNIFORM_PREFIX = 'UNIFORM'


def get_filelist(path, prefix):
    " Returns list of all files starting with the given prefrix"
    files = [f for f in os.listdir(path) if 
             os.path.isfile(os.path.join(path, f)) and f.startswith(prefix)]

    return sorted(files, key=lambda s: int(s[len(prefix):]))

def read_pickle_files(path, filelist):
    " returns parsed pickle files from the filelist, located in the 'path' directory"
    try:
        return [pickle.load(open(os.path.join(path,f),"rb")) for f in filelist]
    except EOFError: #in case the file is empty
        return []

def load_all_standard_sessions(path):
    " Returns all event in a single session "
    directories = [os.path.join(path,o) for o in os.listdir(path) 
                   if os.path.isdir(os.path.join(path,o))]
    events = [ev for directory in directories for ev in load_standard_session(directory)] 
    return events

def load_standard_session(path):
    " Returns all event in this directory "
    only_data_files = get_filelist(path, DEFAULT_PREFIX) 
    sessions = read_pickle_files(path, only_data_files)
    #merge sessions to one
    events = [ev for session in sessions for ev in session]
    return events
 
def load_all_uniform_sessions(path):
    " Returns all uniform sessions "
    directories = [os.path.join(path,o) for o in os.listdir(path) 
                   if os.path.isdir(os.path.join(path,o))]
    events = [sessions for directory in directories for sessions in load_uniform_sessions(directory)] 
    return events

def load_uniform_sessions(path):
    " Returns all uniform sessions in this directory "
    only_uniform_files = get_filelist(path, UNIFORM_PREFIX)
    sessions = read_pickle_files(path, only_uniform_files)
    return sessions
