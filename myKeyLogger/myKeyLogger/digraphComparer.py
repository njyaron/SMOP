import parseFile
import digraphGenerator
import digraphFilter

import os

#compare all users
results_directory = "Results"
main_directory = r'F:\Clouds\Google Drive\SMOP Data'

class Person:
    ORD_MINIMUM_COUNT = 30
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
        self.digraphs = digraphGenerator.analyze_digraphs(events, filter)
        
    def get_key_couples(self):
        return {key_couple for key_couple, dig in self.digraphs.items() if dig.count > self.MINIMUM_COUNT}

    def is_digraph_good(self, key_couple):
        return key_couple in self.digraphs and self.digraphs[key_couple].count > self.MINIMUM_COUNT

def are_different(digraph1, digraph2):##TODO: maybe change criteria
    return abs(digraph1.mean - digraph2.mean) > (digraph1.stdev + digraph2.stdev) / 2 

def can_feature_differentiate(person1, person2, key_couple):
    return person1.is_digraph_good(key_couple) and person2.is_digraph_good(key_couple) and are_different(person1.digraphs[key_couple], person2.digraphs[key_couple])

def count_differentialbe_couples(people, key_couple):
    " returns how many pairs of people can be differentiated with this key "
    can_differentaite = 0
    for person1 in people:
        for person2 in people:
            if person1 != person2 and can_feature_differentiate(person1, person2, key_couple):
                can_differentaite += 1
    return can_differentaite

def count_users_containing_key_couple(people, key_couple):
    "Returns how many users has this feature"
    return len([1 for user in people if user.is_digraph_good(key_couple)])
                

#main
#if __name__ == '__main__':
filter = digraphFilter.Filter(languages=[digraphFilter.HEBREW], 
                                stdev_factor=2.5, keywords=[])

people = []
for name in os.listdir(main_directory):
    print("Building " + name)
    path = os.path.join(main_directory, name)
    if os.path.isdir(path):
        people.append(Person(name, path, filter, is_uniform=False))

#generate list of key_couples
key_couples = set().union(*[person.get_key_couples() for person in people])

for key_couple in key_couples:
    feature_frequency = count_users_containing_key_couple(people, key_couple)
    if feature_frequency > 3:
        possible_couples = feature_frequency * (feature_frequency - 1) #no division by 2, cuz counts couples twice 
        feature_quality = count_differentialbe_couples(people, key_couple) / possible_couples
        if feature_quality > 0.2:
            print(key_couple, feature_frequency, feature_quality)

