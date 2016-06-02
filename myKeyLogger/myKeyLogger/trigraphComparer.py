import parseFile
import trigraphGenerator
import trigraphFilter

import os

#compare all users
results_directory = "Results"
main_directory = r'F:\Clouds\Google Drive\SMOP Data'

class Person:
    ORD_MINIMUM_COUNT = 20
    UNIFORM_MINIMUM_COUNT = 0
    def __init__(self, name, path, filter, is_uniform = False):
        self.name = name
        self.path = path
        #load events
        results_path = os.path.join(path, results_directory)
        events = [] #made this temp value
        if os.path.exists(results_path):
            if is_uniform:
                sessions = [session for kind,index,session in parseFile.load_all_uniform_sessions(results_path)]
                events = [ev for session in sessions for ev in session]
                self.MINIMUM_COUNT = Person.UNIFORM_MINIMUM_COUNT
            else:
                events = parseFile.load_all_standard_sessions(results_path)
                self.MINIMUM_COUNT = Person.ORD_MINIMUM_COUNT
        #analyze (including filtering)
        self.trigraphs = trigraphGenerator.analyze_trigraphs(events, filter)
        
    def get_keys(self):
        return {key for key, tri in self.trigraphs.items() if tri.count > self.MINIMUM_COUNT}

    def is_key_good(self, key):
        return key in self.trigraphs and self.trigraphs[key].count > self.MINIMUM_COUNT

def are_different(trigraphs1, trigraphs2):##TODO: maybe change criteria
    return abs(trigraphs1.mean - trigraphs2.mean) > (trigraphs1.stdev + trigraphs2.stdev) / 2 

def compare_two_people(person1, person2):
    common_keys = person1.get_keys().intersection(person2.get_keys())
    good_keys = [key for key in common_keys if can_feature_differentiate(perosn1, person2, key)]
    return len(good_keys), len(common_keys)

def can_feature_differentiate(person1, person2, key):
    return person1.is_key_good(key) and person2.is_key_good(key) and are_different(person1.trigraphs[key], person2.trigraphs[key])

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
    filter = trigraphFilter.Filter(languages=[trigraphFilter.HEBREW], 
                                stdev_factor=2.5, keywords=[])

people = []
for name in os.listdir(main_directory):
    print("Building " + name)
    path = os.path.join(main_directory, name)
    if os.path.isdir(path):
        people.append(Person(name, path, filter, is_uniform=False))

#generate list of keys
keys = set().union(*[person.get_keys() for person in people])

for key in list(keys):
    feature_frequency = count_users_containing_key(people, key)
    if feature_frequency > 4:
        possible_couples = feature_frequency * (feature_frequency - 1) #no division by 2, cuz counts couples twice 
        feature_quality = count_differentialbe_couples(people, key) / possible_couples
        if feature_quality > 0.2:
            print(key, feature_frequency, feature_quality)

