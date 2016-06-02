import statistics

class Trigraph:
    def __init__(self, data, keys):
        self.key1, self.key2, self.key3 = keys
        self.count = len(data)
        if self.count:
            self.mean = statistics.median(data)
        if self.count > 1:
            self.stdev = statistics.stdev(data)

def build_keys2events(events):
    keys2events = dict()
    for i in range(len(events)):
        ev1 = events[i]
        ev2 = None
        ev3 = None
        if ev1.event_type=='down':
            j = i+1
            while j < len(events) and events[j].event_type != 'down':
                j += 1
            if j < len(events):
                ev2 = events[j]
                j += 1
            while j < len(events) and events[j].event_type != 'down':
                j += 1
            if j < len(events):
                ev3 = events[j]

            if ev2 and ev3 and ev1.names and ev2.names and ev3.names: #sometimes they are not 
                keys = (ev1.names[-1], ev2.names[-1], ev3.names[-1])
                if keys not in keys2events:
                    keys2events[keys] = list()
                keys2events[keys].append((ev1, ev2, ev3))
    return keys2events

def build_list(keys_events):
    return [ev3.time - ev1.time for ev1, ev2, ev3 in keys_events]

def analyze_trigraphs(events, filter):
    key2events = build_keys2events(events)
    #filter events
    key2events = {key:filter.filter_events(key_events) for key,key_events in key2events.items()}

    key2trigraphs = {key:build_list(key_events) for key,key_events in key2events.items()}
    #filter time leaps
    key2trigraphs = {key:filter.filter_data(trigraphs) for key,trigraphs in key2trigraphs.items()}
    key2info = {key:Trigraph(trigraphs, key) for key,trigraphs in key2trigraphs.items() if trigraphs} 
    return key2info
