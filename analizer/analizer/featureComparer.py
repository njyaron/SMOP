import parseFile
import featureGenerator

import os

#compare all users
results_directory = "Results"
main_directory = r'F:\Clouds\Google Drive\SMOP Data'

class Person:
    def __init__(self, name, path, filter, feature_type, is_uniform = False):
        self.name = name
        self.path = path
        self.feature_type = feature_type
        #load events
        results_path = os.path.join(path, results_directory)
        events = [] #made this temp value
        if os.path.exists(results_path):
            if is_uniform:
                sessions = [session for kind,index,session in parseFile.load_all_uniform_sessions(results_path)]
                events = [ev for session in sessions for ev in session]
            else:
                events = parseFile.load_all_standard_sessions(results_path)
        #analyze (including filtering)
        self.features = featureGenerator.analyze(events, filter, feature_type)
        
    def get_feature_names(self):
        return {key for key, feature in self.features.items() if feature.is_good()}

    def is_feature_good(self, feature_name):
        return feature_name in self.features and self.features[feature_name].is_good()

def are_different(feature1, feature2):##TODO: maybe change criteria, to be type-dependent
    return abs(feature1.mean - feature2.mean) > (feature1.stdev + feature2.stdev) / 2 

def compare_two_people(person1, person2):
    common_features_names = person1.get_feature_names().intersection(person2.get_feature_names())
    good_features_names = [feature for feature in common_features_names if can_feature_differentiate(perosn1, person2, feature)]
    return len(good_features_names), len(common_features_names)

def can_feature_differentiate(person1, person2, feature_name):
    return person1.is_feature_good(feature_name) and person2.is_feature_good(feature_name) \
        and are_different(person1.features[feature_name], person2.features[feature_name])

def count_differentialbe_couples(people, feature_name):
    " returns how many pairs of people can be differentiated with this key "
    can_differentaite = 0
    for i in range(len(people)):
        for j in range(i+1, len(people)):
            if can_feature_differentiate(people[i], people[j], feature_name):
                can_differentaite += 1
    return can_differentaite

def count_users_containing_feature(people, feature_name):
    "Returns how many users has this feature"
    return len([1 for user in people if user.is_feature_good(feature_name)])



def generate_people(filter):
    people = []
    for name in os.listdir(main_directory):
        print("Building " + name)
        path = os.path.join(main_directory, name)
        if os.path.isdir(path):
            people.append(Person(name, path, filter, is_uniform=False))
    return people

def get_all_feature_names(people):
    return set().union(*[person.get_feature_names() for person in people])

def print_good_features(people, minimal_frequency = 3, minimal_quality = 0.2):
    feature_names = get_all_feature_names(people)
    for feature_name in feature_names:
        feature_frequency = count_users_containing_feature(people, feature_name)
        if feature_frequency > minimal_frequency:
            possible_couples = feature_frequency * (feature_frequency - 1)/2 
            feature_quality = count_differentialbe_couples(people, feature_name) / possible_couples
            if feature_quality > minimal_quality:
                print(feature_name, feature_frequency, feature_quality)
