import statistics

import duration, digraph, trigraph, digraphRatio

DURATION_TYPE = 0
DIGRAPH_TYPE = 1
TRIGRAPH_TYPE = 2
DIGRAPH_RATIO_TYPE = 3

TYPE2MINIMUM_COUNT = {DURATION_TYPE:duration.ORD_MINIMUM_COUNT, 
                      DIGRAPH_TYPE:digraph.ORD_MINIMUM_COUNT,
                      TRIGRAPH_TYPE:digraph.ORD_MINIMUM_COUNT,
                      DIGRAPH_RATIO_TYPE:digraphRatio.ORD_MINIMUM_COUNT}

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

    def get_minimum_count(self):
        if self.is_uniform:
            return 1
        else:
            return TYPE2MINIMUM_COUNT[self.feature_type]

    def is_good(self):
        return self.count >= self.get_minimum_count()

#need to implement: 
def build_keys2events(events, feature_type):
    if feature_type == DURATION_TYPE:
        return duration.build_duration_key2events(events)
    elif feature_type == DIGRAPH_TYPE:
        return digraph.build_digraph_keys2events(events)
    elif feature_type == TRIGRAPH_TYPE:
        return trigraph.build_trigraph_keys2events(events)
    elif feature_type == DIGRAPH_RATIO_TYPE:
        return digraphRatio.build_digraph_ratio_keys2events(events)
    else:
        return []

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

def analyze(events, filter, feature_type):
    keys2events = build_keys2events(events, feature_type)
    #filter events
    keys2events = {key:filter.filter_events(key_events) for key,key_events in keys2events.items()}

    keys2data = {key:build_list(key_events, feature_type) for key,key_events in keys2events.items()}
    #filter time leaps
    keys2data = {key:filter.filter_data(data) for key,data in keys2data.items()}
    keys2info = {key:Feature(data, key, feature_type) for key,data in keys2data.items()}
    return keys2info
