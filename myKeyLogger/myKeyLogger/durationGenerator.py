import matplotlib.pyplot as plt
import statistics

class Duration:
    def __init__(self, data, key):
        self.key = key
        self.count = len(data)
        if self.count:
            self.mean = statistics.median(data)
        if self.count > 1:
            self.stdev = statistics.stdev(data)

def build_key2events(events):
    key2events = dict()
    for ev in events:
        if ev.names:
            if ev.names[-1] not in key2events: #usually the last event name is more detailed: ['shift','right shift']
                key2events[ev.names[-1]] = list()
            key2events[ev.names[-1]].append(ev)
    return key2events

def build_durations_list(key_events):
    #to improve: filter away chars that were pressed for a long time (many 'down's)
    durations = list()
    for i in range(len(key_events)-1):
        #throw away chars with no partner
        if key_events[i].event_type=='down' and key_events[i+1].event_type=='up':
            durations.append(key_events[i+1].time - key_events[i].time)
    return durations

def analyze_durations(events, filter):
    key2events = build_key2events(events)
    #filter events
    key2events = {key:filter.filter_events(key_events) for key,key_events in key2events.items()}

    key2durations = {key:build_durations_list(key_events) for key,key_events in key2events.items()}
    #filter durations
    key2durations = {key:filter.filter_durations(durations) for key,durations in key2durations.items()}
    key2info = {key:Duration(durations, key) for key,durations in key2durations.items()}
    return key2info

#def plot_duration_histogram(key_events, languages=[ENGLISH], n_bins=40, graph_title="", filter=True):
#    events = filter_by_language(key_events, languages)
#    durations = build_durations_list(events)
#    if filter:
#        durations = filter_outliers(durations)
#    plt.hist(durations, n_bins) #n, bins, patches = plt.hist(durations, n_bins)
#    plt.title(graph_title)
#    plt.show()


