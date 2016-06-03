ORD_MINIMUM_COUNT = 40

def build_duration_key2events(events):
    keys2events = dict()
    for i in range(len(events)):
        ev1 = events[i]
        ev2 = None
        if ev1.event_type=='down':
            j = i+1
            while j < len(events) and events[j].names != ev1.names:
                j += 1
            if j < len(events) and events[j].event_type=='up':
                ev2 = events[j]
            if ev1.names and ev2 and ev2.names: #sometimes they are not 
                key = ev1.names[-1]
                if key not in keys2events:
                    keys2events[key] = list()
                keys2events[key].append((ev1, ev2))
    return keys2events

def build_durations_list(key_events):
    return [ev2.time - ev1.time for ev1, ev2 in keys_events]
