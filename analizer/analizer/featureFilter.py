import statistics

HEBREW = 1037
ENGLISH = 1033
ALL_LANGUAGES = [HEBREW, ENGLISH]

class Filter:
    def __init__(self, languages=ALL_LANGUAGES, stdev_factor=2.5, keywords=[], long_time=1.0):
        self.languages = languages
        self.stdev_factor = stdev_factor
        self.keywords = keywords
        self.long_time = long_time

    def filter_events(self, events):
        events = filter_by_language(events, self.languages)
        events = filter_by_program(events, self.keywords)
        return events

    def filter_data(self, times):
        times = filter_long_times(times, self.long_time)
        times = filter_outliers(times, self.stdev_factor)
        return times

def filter_long_times(data, long_time=1.0):
    return [x for x in data if x < long_time]

def filter_outliers(data, stdev_factor=2.5):
    #stdev_factor - how many stdevs from the median is still legit
    if not data: #empty
        return data 
    med = statistics.median(data)
    #filter extreme outliers
    error = [abs(x-med) for x in data]
    max_error = statistics.median(error)*5 #5 seems like enough
    data = [x for x in data if abs(x-med) < max_error]
    #filter outliers
    if len(data) > 1: #statistics.stdev only works for two or more elements
        stdev = statistics.stdev(data)
        return [v for v in data if abs(med-v) < stdev_factor*stdev]
    else:
        return data

def filter_by_language(events, languages=ALL_LANGUAGES):
    #events can be [(ev1, ev2), (ev3, ev4),...] or [ev1, ev2, ev3,...]
    filtered = list()
    for evs in events:
        should_filter = True
        for i in range(len(evs)-1):
            if evs[i].language != evs[i+1].language:
                should_filter = False
        if should_filter and evs[0].language in languages:
            filtered.append( evs )
    return filtered

def contains_some_words(test, keywords):
    return sum([(word in text) for word in keywords]) > 0

def filter_by_program(event_couples, keywords):
    filtered = list()
    for evs in events:
        should_filter = True
        for i in range(len(evs)-1):
            if evs[i].window_name != evs[i+1].window_name:
                should_filter = False
        if should_filter:
            filtered.append( evs )
    if keywords:
        filtered2 = list()
        for evs in filtered:
            if contains_some_words(evs[0].window_name, keywords):
                filtered2.append( evs )
        filtered = filtered2
    return filtered
