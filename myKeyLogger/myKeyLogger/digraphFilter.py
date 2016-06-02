import statistics

HEBREW = 1037
ENGLISH = 1033
ALL_LANGUAGES = [HEBREW, ENGLISH]

class Filter:
    def __init__(self, languages=ALL_LANGUAGES, stdev_factor=2.5, keywords=[]):
        self.languages = languages
        self.stdev_factor = stdev_factor
        self.keywords = keywords

    def filter_event_couples(self, event_couples):
        event_couples = filter_by_language(event_couples, self.languages)
        event_couples = filter_by_program(event_couples, self.keywords)
        return event_couples

    def filter_digraphs(self,digraph_times):
        data = filter_outliers(digraph_times, self.stdev_factor)
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

def filter_by_language(event_couples, languages=ALL_LANGUAGES):
    filtered = list()
    for ev1,ev2 in event_couples:
        if ev1.language == ev2.language and ev1.language in languages:
            filtered.append( (ev1,ev2) )
    return filtered

def contains_some_words(test, keywords):
    return sum([(word in text) for word in keywords]) > 0

def filter_by_program(event_couples, keywords):
    filtered = list()
    for ev1,ev2 in event_couples:
        if ev1.window_name == ev2.window_name:
            filtered.append( (ev1,ev2) )
    if keywords:
        filtered2 = list()
        for ev1,ev2 in filtered:
            if contains_some_words(ev1.window_name, keywords):
                filtered2.append( (ev1,ev2) )
        filtered = filtered2
    return filtered
