import pickle
import os
import matplotlib.pyplot as plt
import statistics
DEFAULT_PREFIX = 'data_'
HEBREW = 1037
ENGLISH = 1033

def write2csv(data, filepath):
    import csv
    writer = csv.writer(open(path, 'w+'), lineterminator='\n')
    writer.writerows([ [str(dt)] for dt in data])
    #del writer

original_events = load_data()
key2events = build_key2events(original_events)
key2durations = {key:build_durations_list(key_events) for key,key_events in key2events.items()}
key = 'n'
plot_duration_histogram(key2events[key])

for key in ['a', 'n', 's', 'm', 't']:
    plot_duration_histogram(key2events[key], graph_title="durations of " + key)



# work in progress

def get_digraphs(original_events, languages=[ENGLISH], time_threshold=1):
    #time_threshold=1 second maximal duration of digraph
    up_events = [ev for ev in original_events if ev.language in languages and ev.event_type=='up']
    #throw away chars with no partner
    cpl_durations = dict()
    for i in range(len(up_events)-1):
        if up_events[i+1].time - up_events[i].time < time_threshold:
            cpl = (up_events[i].names[-1], up_events[i+1].names[-1])
            if cpl not in cpl_durations:
                cpl_durations[cpl] = list()
            cpl_durations[cpl].append(up_events[i+1].time - up_events[i].time)
    return cpl_durations

def get_common_digraphs(original_events, language=ENGLISH):
    cpl_durations = list(get_digraphs(original_events, language).items())
    sorted_cpl_durations = sorted(cpl_durations, key=lambda k,lst: len(lst))

len(cpl_durations.keys())
cAsize = [(len(v), k, v) for k,v in cpl_durations.items()]
cAsize.sort()
cAsize.reverse()

plt.hist([t for t in cAsize[2][2] if t < 0.1], 40) #this happens to be ctrl+s
plt.show()
