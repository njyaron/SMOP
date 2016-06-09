import parseFile
import featureFilter
import featureGenerator
import featureComparer
import duration, digraph, trigraph, digraphRatio

import pickle, os, math
import matplotlib.pyplot as plt

results_directory = parseFile.results_directory
main_directory = parseFile.main_directory

#load general
loc = r"F:\Clouds\Dropbox\SMOP\AnalysisCompressed\people_general.p"
people = pickle.load( open( loc, "rb" ) )
loc = r"F:\Clouds\Dropbox\SMOP\AnalysisCompressed\samples_general.p"
samples = pickle.load( open( loc, "rb" ) )

#get top keys
list_keys = []
for feature_type in featureGenerator.ALL_TYPES:
    keys = []
    for key in featureComparer.get_all_feature_names(people, [feature_type]):
        keyCount = sum( [person.features[key].count for person in people if key in person.features])
        keys.append( (keyCount, key) )
    list_keys.append(sorted(keys, reverse=True))

for li in list_keys:
    print(li[:15])

chosen_keys = [('space', 0), ('e', 0) ,
               ('i', 'n', 1), ('f', 'i', 1),
               ('t', 'h', 'e', 2), ('i', 'n', 'g', 2),
               ('t', 'h', 'e', 3), ('i', 'n', 'g', 3)
               ]


#features distribution for two people
filters = [featureFilter.Filter(long_time=duration.LONG_TIME),
            featureFilter.Filter(long_time=digraph.LONG_TIME),
            featureFilter.Filter(long_time=trigraph.LONG_TIME),
            featureFilter.Filter(long_time=digraphRatio.LONG_TIME),
            ] 
feature_types = featureGenerator.ALL_TYPES
names = ["Nir Yaron", "Guy Levanon", "Noam Greenberg"]
people = dict()
for name in names:
    print("Building " + name)
    path = os.path.join(main_directory, name)
    events, _ = parseFile.get_events(path, filter, is_uniform=False, with_sample=False)
    people[name] = dict()
    for filter, feature_type in zip(filters, feature_types):
        keys2data = featureGenerator.create_data(events,filter,feature_type)
        people[name].update( keys2data )#{key:data for key,data in keys2data.items() if key in chosen_keys})

for key in chosen_keys:
    for name in names:
        plt.hist(people[name][key], 20, normed=True)
    if key[-1] != 3:
        plt.xlabel('Time [ms]')
    else:
        plt.xlabel('Ratio')
    plt.ylabel('Occurances')
    plt.title('Histogram of ' + "".join(key[:-1]))
    p = os.path.join(r'F:\Clouds\Dropbox\SMOP\Presentation',"general_"+"".join([str(s) for s in key]))
    plt.savefig(p)
    plt.cla()
    #plt.show()

#Median and error of features

#loc = r"F:\Clouds\Dropbox\SMOP\AnalysisCompressed\people_general.p"
#people = pickle.load( open( loc, "rb" ) )
#ppl = [people[i] for i in [5,9,18,21]]
#for person in ppl:
#    x = [person.features[key].mean for key in chosen_keys]
#    xerr = [person.features[key].stdev for key in chosen_keys]
#    y = list(range(len(chosen_keys)))
#    plt.errorbar(x, y, xerr=xerr,fmt='.')
#plt.show()

for key in chosen_keys:
    x = [person.features[key].mean for person in people if person.is_feature_good(key)]
    xerr = [person.features[key].stdev for person in people if person.is_feature_good(key)]
    y = list(range(len(x)))
    plt.errorbar(x, y, xerr=xerr,fmt='.')
    plt.show()

