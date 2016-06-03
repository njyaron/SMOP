import statistics

class Digraph:
    def __init__(self, data, keys):
        self.key1, self.key2 = keys
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
        if ev1.event_type=='down':
            j = i+1
            while j < len(events) and events[j].event_type != 'down':
                j += 1
            if j < len(events):
                ev2 = events[j]
            if ev1.names and ev2 and ev2.names: #sometimes they are not 
                keys = (ev1.names[-1], ev2.names[-1])
                if keys not in keys2events:
                    keys2events[keys] = list()
                keys2events[keys].append((ev1, ev2))
    return keys2events

def build_digraphs_list(keys_events):
    return [ev2.time - ev1.time for ev1, ev2 in keys_events]

def analyze_digraphs(events, filter):
    keys2events = build_keys2events(events)
    #filter events
    keys2events = {key:filter.filter_event_couples(key_events) for key,key_events in keys2events.items()}

    keys2digraphs = {key:build_digraphs_list(key_events) for key,key_events in keys2events.items()}
    #filter time leaps
    keys2digraphs = {key:filter.filter_digraphs(digraphs) for key,digraphs in keys2digraphs.items()}
    keys2info = {key:Digraph(digraphs, key) for key,digraphs in keys2digraphs.items()}
    return keys2info
