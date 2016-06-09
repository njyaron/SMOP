import pickle
import os
DEFAULT_PREFIX = 'data_'
UNIFORM_PREFIX = 'UNIFORM'
SAMPLE_SIZE = 4000

results_directory = "Results"
main_directory = r'F:\Clouds\Google Drive\SMOP Data'
#main_directory = r'F:\Nir\Temp\SMOPlimited'

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
    sessions = [session for directory in directories for session in load_uniform_sessions(directory)] 
    return sessions

def load_uniform_sessions(path):
    " Returns all uniform sessions in this directory "
    only_uniform_files = get_filelist(path, UNIFORM_PREFIX)
    sessions = read_pickle_files(path, only_uniform_files)
    return sessions

def split_sample_training(events, filter, is_uniform):
    """Returns (training_events, sample_events) from the given events, 
    after some basic filtering"""
    if not is_uniform:
        filtered_events = filter.filter_sample_events(events)
        length = min(len(filtered_events)//4, SAMPLE_SIZE)
        sample_start = (len(filtered_events) - length)//2
        sample_end = sample_start + length

        sample_events = filtered_events[sample_start:sample_end]
        training_events = filtered_events[:sample_start] + filtered_events[sample_end:]

        return training_events, sample_events
    else:
        pass #TODO: take the last session

def get_events(person_path, filter, is_uniform, with_sample=False):
    results_path = os.path.join(person_path, results_directory)
    events = []
    if os.path.exists(results_path):
        if is_uniform:
            sessions = [session for kind,index,session in parseFile.load_all_uniform_sessions(results_path)]
            events = [ev for session in sessions for ev in session]
        else:
            events = load_all_standard_sessions(results_path)

    if with_sample:
        return split_sample_training(events, filter, is_uniform)
    else:
        return events, list()