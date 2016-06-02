import statistics

HEBREW = 1037
ENGLISH = 1033
ALL_LANGUAGES = [HEBREW, ENGLISH]

class Filter:
    def __init__(self, languages=ALL_LANGUAGES, stdev_factor=2.5, keywords=[], long_time=2.0):
        self.languages = languages
        self.stdev_factor = stdev_factor
        self.keywords = keywords
        self.long_time = long_time

    def filter_events(self, events):
        events = filter_by_language(events, self.languages)
        events = filter_by_program(events, self.keywords)
        return events

    def filter_data(self,times):
        times = filter_long_times(times, self.long_time)
        times = filter_outliers(times, self.stdev_factor)
        return times

def filter_long_times(data, long_time=2.0):
    return [x for x in data if x < long_time]

def filter_outliers(data, stdev_factor=2.5):
    #stdev_factor - how many stdevs from the median is still legit
    if not (data and stdev_factor): #empty
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

def filter_by_language(event_couples, languages=ALL_LANGUAGES):
    filtered = list()
    for ev1,ev2,ev3 in event_couples:
        if ev1.language == ev2.language and ev2.language == ev3.language and ev1.language in languages:
            filtered.append( (ev1,ev2,ev3) )
    return filtered

def contains_some_words(test, keywords):
    return sum([(word in text) for word in keywords]) > 0

def filter_by_program(event_triples, keywords):
    filtered = list()
    for ev1,ev2,ev3 in event_triples:
        if ev1.window_name == ev2.window_name and ev2.window_name == ev3.window_name:
            filtered.append( (ev1,ev2,ev3) )
    if keywords:
        filtered = [triple for triple in filtered if contains_some_words(triple[0].window_name, keywords)]
    return filtered
