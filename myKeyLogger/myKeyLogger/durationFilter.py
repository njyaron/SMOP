import statistics

HEBREW = 1037
ENGLISH = 1033
ALL_LANGUAGES = [HEBREW, ENGLISH]

class Filter:
    def __init__(self, languages=ALL_LANGUAGES, stdev_factor=2.5, keywords=[]):
        self.languages = languages
        self.stdev_factor = stdev_factor
        self.keywords = keywords

    def filter_events(self, events):
        events = filter_by_language(events, self.languages)
        events = filter_by_program(events, self.keywords)
        return events

    def filter_durations(self,duration_times):
        data = filter_outliers(duration_times, self.stdev_factor)
        return data

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
    return [ev for ev in events if ev.language in languages]

def filter_by_program(events, keywords):
    if keywords:
        return [ev for ev in events if sum([(word in ev.window_name) for word in keywords])]
    else: #dont filter
        return events 