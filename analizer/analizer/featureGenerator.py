import statistics
import math
#import scipy.stats
import duration, digraph, trigraph, digraphRatio

DURATION_TYPE = 0
DIGRAPH_TYPE = 1
TRIGRAPH_TYPE = 2
DIGRAPH_RATIO_TYPE = 3

ALL_TYPES = [DURATION_TYPE, DIGRAPH_TYPE, TRIGRAPH_TYPE, DIGRAPH_RATIO_TYPE]

TYPE2MINIMUM_COUNT = {DURATION_TYPE:duration.ORD_MINIMUM_COUNT, 
                      DIGRAPH_TYPE:digraph.ORD_MINIMUM_COUNT,
                      TRIGRAPH_TYPE:digraph.ORD_MINIMUM_COUNT,
                      DIGRAPH_RATIO_TYPE:digraphRatio.ORD_MINIMUM_COUNT}

TYPE2TRUST = {DURATION_TYPE:1, 
                DIGRAPH_TYPE:3,
                TRIGRAPH_TYPE:0.4,
                DIGRAPH_RATIO_TYPE:0.4}

#ALLOWED_KEYS = {'d', 'v', 'right alt', '[', 'right shift', 'b', 'm', 'p', 'q', 'c', 'u', 'g', 'enter', '\\', 's', "'", 'j', 'y', '.', 'f', 'k', 'i', ',', 'z', '*', 'a', 't', 'l', 'right ctrl', 'tab', 'r', 'alt', 'space', 'w', '/', 'n', '=', 'e', 'shift', ']', ';', 'o', '+', 'x', 'ctrl', '-', 'h'}
ALLOWED_KEYS = {'d', 'v', '[', 'b', 'm', 'p', 'q', 'c', 'u', 'g', 'enter', '\\', 's', "'", 'j', 'y', '.', 'f', 'k', 'i', ',', 'z', '*', 'a', 't', 'l', 'r', 'space', 'w', '/', 'n', '=', 'e', ']', ';', 'o', '+', 'x', '-', 'h'}

class Feature:
    def __init__(self, data, keys, feature_type, is_uniform):
        self.keys = keys
        self.count = len(data)
        self.feature_type = feature_type
        self.is_uniform = is_uniform
        if self.count:
            self.mean = statistics.median(data)
        if self.count > 1:
            self.stdev = statistics.stdev(data)
            #self.norm = scipy.stats.norm(self.mean, self.stdev)

    def get_minimum_count(self):
        if self.is_uniform:
            return 1
        else:
            return TYPE2MINIMUM_COUNT[self.feature_type]

    def is_good(self):
        return self.count >= self.get_minimum_count()

    def probability_of(self, value):
        var = self.stdev**2 #float(self.stdev)**2
        denom = math.sqrt(2*math.pi*var)
        num = math.exp(-(value-self.mean)**2/(2*var))
        return num/denom
        #return self.norm.pdf(value)

    def update_trust(self, avg_count):
        self.trust = self.count * TYPE2TRUST[self.feature_type] / avg_count

def build_keys2events(events, feature_type):
    keys2events = build_keys2events_helper(events, feature_type)
    return { keys+(feature_type,):events for keys, events in keys2events.items() }

def build_keys2events_helper(events, feature_type):
    events = [ev for ev in events if ev.names and ev.names[-1] in ALLOWED_KEYS]
    if feature_type == DURATION_TYPE:
        return duration.build_duration_key2events(events)
    elif feature_type == DIGRAPH_TYPE:
        return digraph.build_digraph_keys2events(events)
    elif feature_type == TRIGRAPH_TYPE:
        return trigraph.build_trigraph_keys2events(events)
    elif feature_type == DIGRAPH_RATIO_TYPE:
        return digraphRatio.build_digraph_ratio_keys2events(events)
    else:
        return dict()

def build_list(keys_events, feature_type):
    if feature_type == DURATION_TYPE:
        return duration.build_durations_list(keys_events)
    elif feature_type == DIGRAPH_TYPE:
        return digraph.build_digraphs_list(keys_events)
    elif feature_type == TRIGRAPH_TYPE:
        return trigraph.build_trigraph_list(keys_events)
    elif feature_type == DIGRAPH_RATIO_TYPE:
        return digraphRatio.build_digraph_ratio_list(keys_events)
    else:
        return []


def create_data(events, filter, feature_type):
    keys2events = build_keys2events(events, feature_type)
    #filter events
    keys2events = {key:filter.filter_events(key_events) for key,key_events in keys2events.items()}

    keys2data = {key:build_list(key_events, feature_type) for key,key_events in keys2events.items()}
    #filter time leaps
    keys2data = {key:filter.filter_data(data) for key,data in keys2data.items()}
    keys2data = {key:data for key,data in keys2data.items() if data}
    return keys2data 

def analyze(events, filter, feature_type, is_uniform):
    keys2data = create_data(events, filter, feature_type)
    if keys2data:
        avg_count = sum([len(data) for data in keys2data.values()]) / len(keys2data)
    keys2info = {key:Feature(data, key, feature_type, is_uniform) for key,data 
                 in keys2data.items() if data} #remember to remove empty
    if keys2data:
        for feature in keys2info.values():
            feature.update_trust(avg_count)
    return keys2info


def analyze_sample(events, filter, feature_type):
    keys2events = build_keys2events(events, feature_type)
    #filter events
    keys2events = {key:filter.filter_events(key_events) for key,key_events in keys2events.items()}

    keys2data = {key:build_list(key_events, feature_type) for key,key_events in keys2events.items()}

    key_time = [(feature_name,time) for feature_name,time_list in keys2data.items() 
                for time in time_list if filter.is_good_time(time)]

    return key_time
