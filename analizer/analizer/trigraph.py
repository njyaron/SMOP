ORD_MINIMUM_COUNT = 8
LONG_TIME = 0.95

def build_trigraph_keys2events(events):
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

def build_trigraph_list(keys_events):
    return [ev3.time - ev1.time for ev1, ev2, ev3 in keys_events]
