import parseFile
import durationGenerator

import os

#compare all users
results_directory = "Results"
main_directory = r'F:\Clouds\Google Drive\SMOP Data'

class Person:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        results_path = os.path.join(path, results_directory)
        events = [] #made this temp value
        if os.path.exists(results_path):
            events = parseFile.load_all_standard_sessions(results_path)
        self.durations = durationGenerator.analyze_durations(events)
        
    def get_duration_keys(self):
        MINIMUM_COUNT = 100
        return {key for key, dur in self.durations.items() if dur.count > MINIMUM_COUNT}

    def is_key_good(self, key):
        MINIMUM_COUNT = 100
        return self.durations[key].count > MINIMUM_COUNT

def are_different(duration1, duration2):
    return abs(durations1.mean - durations2.mean) > (durations1.stev + durations2[key].stev)

def compare_two_people(person1, person2):
    common_keys = person1.get_duration_keys().intersection(person2.get_duration_keys())
    good_keys = [key for key in common_keys if can_feature_differentiate(perosn1, person2, key)]
    return len(good_keys), len(common_keys)

def can_feature_differentiate(person1, person2, key):
    return person1.is_key_good(key) and person2.is_key_good(key) and are_different(person1.durations[key], person2.durations[key])

def get_feature_quality(people, key):
    " returns how many pairs of people can be differentiated with this key "
    can_differentaite = 0
    for person1 in people:
        for person2 in people:
            if person1 != person2 and can_feature_differentiate(person1, person2, key):
                can_differentaite += 1
    return can_differentaite

def get_feature_frequency(people, key):
    "Returns in how many users has this feature"
    return len([1 for user in people if user.is_key_good(key)])
                

people = []
for name in os.listdir(main_directory):
    print("Starting with " + name)
    path = os.path.join(main_directory,name)
    if os.path.isdir(path):
        people.append(Person(name, path))


##temporary
#path1 = r'C:\Nir\SMOP\Results\testNir3' #nir yaron
#path2 = r'F:\Clouds\Google Drive\SMOP Data\Guy Levanon\Results\testT81901911' #guy levanon

#events1 = parseFile.load_standard_session(path1)
#events2 = parseFile.load_standard_session(path2)

#durations1 = durationGenerator.analyze_durations(events1)
#durations2 = durationGenerator.analyze_durations(events2)

##common keys
#keys1 = {key for key, dur in durations1.items() if dur.count > MINIMUM_COUNT}
#keys2 = {key for key, dur in durations2.items() if dur.count > MINIMUM_COUNT}

#keys = keys1.intersection(keys2)

##can differentiate?
#for key in keys:
#    s = "%.4f %.4f %.4f %.4f" %(durations1[key].mean, durations2[key].mean, durations1[key].stev, durations2[key].stev)
#    print(s)
