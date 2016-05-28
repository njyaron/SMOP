import statistics

HEBREW = 1037
ENGLISH = 1033
ALL_LANGUAGES = [HEBREW, ENGLISH]

def filter_outliers(data, stdev_factor=2.5):
    #stdev_factor - how many stdevs from the median is still legit
    med = statistics.median(data)
    #filter extreme outliers
    error = [abs(x-med) for x in data]
    max_error = statistics.median(error)*5 #5 seems like enough
    data = [x for x in data if abs(x-med) > max_error]
    #filter outliers
    stdev = statistics.stdev(data)
    return [v for v in data if abs(med-v) < stdev_factor*stdev]

def filter_by_language(events, languages=ALL_LANGUAGES):
    return [ev for ev in events if ev.language in languages]

def filter(duration_times, languages=ALL_LANGUAGES, stdev_factor=2.5):
    data = filter_by_language(duration_times,languages)
    data = filter_outliers(data,stdev_factor)
    return data