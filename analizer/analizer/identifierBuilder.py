import parseFile
import featureFilter
import featureGenerator
import featureComparer

import pickle, os, math, statistics

results_directory = parseFile.results_directory
main_directory = parseFile.main_directory

MINIMUM_FEATURE_OCCURANCES = 25

#choose the names of people i want to test
names = ['Adi Asher', 'Dor Aharonson', 'Elad Kliger', 'Elisha Modelevsky', 'Gal Oz-Ari', 'Gallil Maimon', 'Gil Boazi', 'Gilad Samuels', 'Guy Levanon', 'Matan Levine', 'Nir Yaron', 'Noam Greenberg', 'Ohad Ben-Or', 'Or Johnson Ezra', 'Shaked Rosenstein', 'Yonathan Schwammenthal', 'Yovel Rom', 'Yuval Itkin']

#find best features (most common of each type)
def best_keys2(people, feature_type):
    #for people from featureGenerator.create_data
    keys = dict()
    for p in people.values():
        for k,li in p.items():
            if k[-1] == feature_type:
                if k not in keys:
                    keys[k] = 0
                keys[k] += len(li)
    keys = sorted(list(keys.items()), key=lambda x:-x[1])
    return keys

loc = "F:\Clouds\Dropbox\SMOP\AnalysisCompressed\general_people2key2data.p"  #r"F:\Clouds\Dropbox\SMOP\AnalysisCompressed\eclipse_english_people2key2data.p"
people = pickle.load( open( loc, "rb" ) )
people = {name:person for (name,person) in people.items() if name in names}
options_best_keys_digraph = best_keys2(people, featureGenerator.DIGRAPH_TYPE)
possible_keys = [k for k,v in options_best_keys_digraph if not 
                 sum( [not (k in key2data and len(key2data[k])>MINIMUM_FEATURE_OCCURANCES) 
                       for key2data in people.values()]) ]

#build database of averages
keys_digraph = possible_keys
trainings = people
trainings_avg = {name:{key:statistics.mean(data) for key,data in person.items()} 
                     for name,person in trainings.items()}

def get_avg_key_time(trainings):
    key2times = dict()
    for person in trainings.values() 


#now we'll try to make a bigger sample-base
def get_estimates_single_sample(trainings_avg, sample, keys_digraph,debug=False):
    sample_avg = {key:statistics.mean(data) for key,data in sample.items()} 

    d = [0 for p in trainings_avg]
    for key in keys_digraph:
        for i,person_avg in enumerate(trainings_avg.values()):
            d[i] += abs(sample_avg[key] - person_avg[key])
    d = sorted(list(zip(d,trainings_avg.keys())))
    return d #[ (score,name), (score,name),...]

