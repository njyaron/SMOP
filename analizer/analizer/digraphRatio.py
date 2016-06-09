import trigraph
ORD_MINIMUM_COUNT = trigraph.ORD_MINIMUM_COUNT
LONG_TIME = 4 #this is not really a time but a ration
LONG_PERIOD = 0.95 #this should have actually been callec "long time"...

def build_digraph_ratio_keys2events(events):
    return trigraph.build_trigraph_keys2events(events) #exactly the same

def build_digraph_ratio_list(keys_events):
    return [ (ev3.time - ev2.time) / (ev2.time - ev1.time) for ev1, ev2, ev3 in keys_events 
            if ev2.time != ev1.time and ev3.time - ev1.time < LONG_PERIOD]
