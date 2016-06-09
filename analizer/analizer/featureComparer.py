import parseFile
import featureGenerator

import os, math

#compare all users
results_directory = parseFile.results_directory
main_directory = parseFile.main_directory

class Sample:
    def __init__(self, name, events, filters, feature_types):
        self.name = name
        self.feature_types = feature_types
        #analyze (including filtering)
        self.features = list() #list of format: [ (key, time), (key, time), ...]
        for filter, feature_type in zip(filters, self.feature_types):
            self.features.extend(featureGenerator.analyze_sample(events, filter, feature_type))



class Person:
    def __init__(self, name, events, filters, feature_types, is_uniform):
        self.name = name
        self.feature_types = feature_types
        #analyze (including filtering)
        self.features = dict()
        for filter, feature_type in zip(filters, self.feature_types):
            self.features.update(featureGenerator.analyze(events, filter, feature_type, is_uniform))
        
    def get_feature_names(self, feature_types=featureGenerator.ALL_TYPES):
        return {key for key, feature in self.features.items() 
                if feature.is_good() and feature.feature_type in feature_types}

    def is_feature_good(self, feature_name):
        return feature_name in self.features and self.features[feature_name].is_good()

    def get_similarity(self, sample):
        weights = 0
        value = 0
        for feature_name, feature_value in sample.features:
            if self.is_feature_good(feature_name):
                feature = self.features[feature_name]
                weights += feature.trust
                if feature.probability_of(feature_value) != 0.0:
                    value += feature.trust * math.log(feature.probability_of(feature_value))
                else:
                    value += feature.trust * (-600) #math.log(math.exp(-700))
        if weights:
            return value / weights
        else:
            return -200 #Default bad number


def are_different(feature1, feature2):##TODO: maybe change criteria, to be type-dependent
    return abs(feature1.mean - feature2.mean) > (feature1.stdev + feature2.stdev)

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



def generate_people(filters, feature_types, is_uniform=False):
    default_filter = filters[0] #should all be identical
    people = []
    for name in os.listdir(main_directory):
        print("Building " + name)
        path = os.path.join(main_directory, name)
        if os.path.isdir(path):
            events, _ = parseFile.get_events(path, default_filter, is_uniform, with_sample=False)
            people.append(Person(name, events, filters, feature_types, is_uniform))
    return people

def generate_people_samples(filters, feature_types, is_uniform=False):
    default_filter = filters[0] #should all be identical
    people, samples = [], []
    for name in os.listdir(main_directory):
        print("Building " + name)
        path = os.path.join(main_directory, name)
        if os.path.isdir(path):
            events, sample_events = parseFile.get_events(path, default_filter, is_uniform, with_sample=True)
            people.append(Person(name, events, filters, feature_types, is_uniform))
            samples.append(Sample(name, sample_events, filters, feature_types))
    return people, samples


def get_all_feature_names(people, feature_types=featureGenerator.ALL_TYPES):
    return set().union(*[person.get_feature_names(feature_types) for person in people])

def print_good_features(people, minimal_frequency = 3, minimal_quality = 0.2):
    feature_names = get_all_feature_names(people)
    for feature_name in feature_names:
        feature_frequency = count_users_containing_feature(people, feature_name)
        if feature_frequency > minimal_frequency:
            possible_couples = feature_frequency * (feature_frequency - 1)/2 
            feature_quality = count_differentialbe_couples(people, feature_name) / possible_couples
            if feature_quality > minimal_quality:
                print(feature_name, feature_frequency, feature_quality)



