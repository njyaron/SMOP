#import DataAnalyzer.parseFile as parseFile
#import DataAnalyzer.durationGenerator as durationGenerator
#import DataAnalyzer.durationFilter as durationFilter

import parseFile
import durationGenerator
import durationFilter
import os

#compare all users
results_directory = "Results"
main_directory = r'F:\Clouds\Google Drive\SMOP Data'

class Person:
    MINIMUM_COUNT = 100
    def __init__(self, name, path, filter):
        self.name = name
        self.path = path
        #load events
        results_path = os.path.join(path, results_directory)
        events = [] #made this temp value
        if os.path.exists(results_path):
            events = parseFile.load_all_standard_sessions(results_path)
        #analyze (including filtering)
        self.durations = durationGenerator.analyze_durations(events, filter)
        
    def get_duration_keys(self):
        return {key for key, dur in self.durations.items() if dur.count > Person.MINIMUM_COUNT}

    def is_key_good(self, key):
        return key in self.durations and self.durations[key].count > Person.MINIMUM_COUNT

def are_different(durations1, durations2):
    return abs(durations1.mean - durations2.mean) > (durations1.stdev + durations2.stdev)

def compare_two_people(person1, person2):
    common_keys = person1.get_duration_keys().intersection(person2.get_duration_keys())
    good_keys = [key for key in common_keys if can_feature_differentiate(perosn1, person2, key)]
    return len(good_keys), len(common_keys)

def can_feature_differentiate(person1, person2, key):
    return person1.is_key_good(key) and person2.is_key_good(key) and are_different(person1.durations[key], person2.durations[key])

def count_differentialbe_couples(people, key):
    " returns how many pairs of people can be differentiated with this key "
    can_differentaite = 0
    for person1 in people:
        for person2 in people:
            if person1 != person2 and can_feature_differentiate(person1, person2, key):
                can_differentaite += 1
    return can_differentaite

def count_users_containing_key(people, key):
    "Returns how many users has this feature"
    return len([1 for user in people if user.is_key_good(key)])
                

#main
#if __name__ == '__main__':
filter = durationFilter.Filter(languages=durationFilter.ALL_LANGUAGES, stdev_factor=2.5)

people = []
for name in os.listdir(main_directory):
    print("Building " + name)
    path = os.path.join(main_directory, name)
    if os.path.isdir(path):
        people.append(Person(name, path, filter))

#generate list of keys
keys = set().union(*[person.get_duration_keys() for person in people])

for key in keys:
    feature_frequency = count_users_containing_key(people, key)
    possible_couples = feature_frequency * (feature_frequency + 1) // 2
    feature_quality = count_differentialbe_couples(people, key) / possible_couples
    print(key, feature_frequency, feature_quality)

