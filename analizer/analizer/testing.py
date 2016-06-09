import parseFile
import featureFilter
import featureGenerator
import featureComparer
import duration, digraph, trigraph, digraphRatio

import pickle, os, math
import matplotlib.pyplot as plt

results_directory = parseFile.results_directory
main_directory = parseFile.main_directory


def build_database(filename, keywords=[], languages=featureFilter.ALL_LANGUAGES,update=False):
    filters = [featureFilter.Filter(long_time=duration.LONG_TIME,keywords=keywords, languages=languages),
               featureFilter.Filter(long_time=digraph.LONG_TIME,keywords=keywords, languages=languages),
               featureFilter.Filter(long_time=trigraph.LONG_TIME,keywords=keywords, languages=languages),
               featureFilter.Filter(long_time=digraphRatio.LONG_TIME,keywords=keywords, languages=languages),
               ] 

    feature_types = featureGenerator.ALL_TYPES
    people, samples = featureComparer.generate_people_samples(filters,feature_types,is_uniform=False)

    if update:
        import pickle
        loc = r"F:\Clouds\Dropbox\SMOP\AnalysisCompressed\people_"+filename+".p"
        pickle.dump( people, open( loc, "wb+" ) )
        loc = r"F:\Clouds\Dropbox\SMOP\AnalysisCompressed\samples_"+filename+".p"
        pickle.dump( samples, open( loc, "wb+" ) )

    return people, samples 
    

people, samples = build_database("eclipse",keywords=('java', 'Java', 'Eclipse', 'IntelliJ', 'IDEA'),languages=[featureFilter.ENGLISH],update=True)

for sample in samples:
    fit = [(person.get_similarity(sample),person.name) for person in people]
    fit = sorted(fit,reverse=True)
    idx = [n for v,n in fit].index(sample.name)
    print(sample.name, idx, fit[:5])




#choose the names of people i want to test
names = ['Gal Oz-Ari', 'Gil Boazi', 'Nir Yaron', 'Guy Levanon', 'Yonathan Schwammenthal', 'Matan Levine', 'Ohad Ben-Or', 'Dor Aharonson', 'Yuval Itkin', 'Yonatan Caspi', 'Noam Greenberg', 'Adi Asher', 'Yovel Rom']

#filter and get feature arrays for them
keywords = ('java', 'Java', 'Eclipse', 'IntelliJ', 'IDEA')
languages = [featureFilter.ENGLISH]
filters = [featureFilter.Filter(long_time=duration.LONG_TIME,keywords=keywords),
            featureFilter.Filter(long_time=digraph.LONG_TIME,keywords=keywords),
            featureFilter.Filter(long_time=trigraph.LONG_TIME,keywords=keywords),
            featureFilter.Filter(long_time=digraphRatio.LONG_TIME,keywords=keywords),
            ] 
feature_types = featureGenerator.ALL_TYPES
people = dict() #name:[time1, time2, time3...]
for name in names:
    print("Building " + name)
    path = os.path.join(main_directory, name)
    events, _ = parseFile.get_events(path, filters[0], is_uniform=False, with_sample=False)
    people[name] = dict()
    for filter, feature_type in zip(filters, feature_types):
        keys2data = featureGenerator.create_data(events,filter,feature_type)
        people[name].update( keys2data )#{key:data for key,data in keys2data.items() if key in chosen_keys})

loc = r"F:\Clouds\Dropbox\SMOP\AnalysisCompressed\eclipse_english_people2key2data.p"
pickle.dump( people, open( loc, "wb+" ) )

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

options_best_keys_digraph = best_keys2(people, featureGenerator.DIGRAPH_TYPE)

def key_occurances_in_people(people, key):
    #for people from build_key2data
    return [(name,len(key2data[key])) for name,key2data in people.items()]

#after using this
for key,v in options_best_keys_digraph[:8]:
    print(key_occurances_in_people(people, key))

keys_digraph = [('e', 'r', 1), ('f', 'i', 1), ('i', 'n', 1), ('t', 'h', 1)]

#for one person:
name = "Gal Oz-Ari"
person = people[name]
#split for training+sample(last 10% of array)
training = {key:li[:-len(li)//10] for key,li in person.items()}
sample = {key:li[-len(li)//10:] for key,li in person.items()}

#draw both historgrams and hope to see similar things
for key in keys_digraph:
    plt.hist(training[key], bins=10,normed=True)
    plt.hist(sample[key], bins=10,normed=True)
    plt.show()

#if works, do the same for a few people and hope to see differences
temp_names = ['Gal Oz-Ari', 'Gil Boazi', 'Nir Yaron', 'Guy Levanon', 'Yonathan Schwammenthal']
temp_people = [people[name] for name in temp_names]
for key in keys_digraph:
    for person in temp_people:
        plt.hist(person[key], bins=10,normed=True,alpha=0.6)
    plt.show()

name1,name2 = 'Nir Yaron', 'Yonatan Caspi'
training = {key:li[:-len(li)//10] for key,li in people[name1].items()}
imposture = people[name2]
sample = {key:li[-len(li)//10:] for key,li in people[name1].items()}
temp_people = [training, imposture, sample]
for key in keys_digraph:
    for person in temp_people:
        plt.hist(person[key], bins=10,normed=True,alpha=0.6)
    plt.show()


#if works: try to define parameters that distinguish people
import statistics
temp_names = ['Gal Oz-Ari', 'Gil Boazi', 'Nir Yaron', 'Guy Levanon', 'Yonathan Schwammenthal', 'Matan Levine', 'Ohad Ben-Or', 'Dor Aharonson', 'Yuval Itkin', 'Yonatan Caspi', 'Noam Greenberg', 'Adi Asher', 'Yovel Rom']
temp_people = [people[name] for name in temp_names]+[sample]

for key in keys_digraph:
    print(key)
    for person in temp_people:
        print(statistics.mean(person[key]), statistics.stdev(person[key]))
        #print(statistics.stdev(person[key]))

#now try to estimate how close each person is to the sample
temp_names = ['Gal Oz-Ari', 'Gil Boazi', 'Nir Yaron', 'Guy Levanon', 'Yonathan Schwammenthal', 'Matan Levine', 'Ohad Ben-Or', 'Dor Aharonson', 'Yuval Itkin', 'Yonatan Caspi', 'Noam Greenberg', 'Adi Asher', 'Yovel Rom']
temp_people = [people[name] for name in temp_names]
d = [0 for p in temp_people]
for key in keys_digraph:
    for i,person in enumerate(temp_people):
        d[i] += abs(statistics.mean(sample[key]) - statistics.mean(person[key]))
print(sorted([(v,i) for i,v in enumerate(d)]))

#do this for each sample
trainings = {name:{key:li[:-len(li)//10] for key,li in key2data.items()} for name, key2data in people.items()}
samples = {name:{key:li[-len(li)//10:] for key,li in key2data.items()} for name, key2data in people.items()}
for j,sample in enumerate(samples.values()):
    d = [0 for p in trainings]
    for key in keys_digraph:
        for i,person in enumerate(trainings.values()):
            d[i] += abs(statistics.mean(sample[key]) - statistics.mean(person[key]))
    print(j)
    print(sorted([(v,i) for i,v in enumerate(d)]))

#now try with more features and hope for better accuracy
keys_digraph = [k for k,v in options_best_keys_digraph[:30] if not sum( [k not in key2data for key2data in people.values()]) ]
trainings = {name:{key:li[3:] for key,li in key2data.items()} for name, key2data in people.items()}
samples = {name:{key:li[:3] for key,li in key2data.items()} for name, key2data in people.items()}
for j,sample in enumerate(samples.values()):
    d = [0 for p in trainings]
    for key in keys_digraph:
        for i,person in enumerate(trainings.values()):
            d[i] += abs(statistics.mean(sample[key]) - statistics.mean(person[key]))
    print(j)
    print(sorted([(v,i) for i,v in enumerate(d)]))


#understand why Caspi and Nir are similar - because the last data on Caspi is bad
name1,name2 = 'Yonatan Caspi', 'Nir Yaron'
training = {key:li[30:] for key,li in people[name1].items()}
imposture = people[name2]
sample = {key:li[:30] for key,li in people[name1].items()}
temp_people = [training, imposture, sample]
for key in keys_digraph:
    for person in temp_people:
        plt.hist(person[key], bins=10,normed=True,alpha=0.6)
    plt.show()


for key in keys_digraph:
    print(key)
    for person in temp_people:
        print(statistics.mean(person[key]), statistics.stdev(person[key]))

for key in keys_digraph:
    print(key)
    for person in [training, imposture]:
        abs(statistics.mean(sample[key]) - statistics.mean(person[key]))

    d = [0 for p in trainings]
    for key in keys_digraph:
        for i,person in enumerate(trainings.values()):
            d[i] += abs(statistics.mean(sample[key]) - statistics.mean(person[key]))
    print(j)
    print(sorted([(v,i) for i,v in enumerate(d)]))


#now we'll try to make a bigger sample-base
def get_samples_idxs(li, sample_count, sample_size):
    if len(li) > sample_count * sample_size:
        return [(len(li)//sample_count*j,len(li)//sample_count*j+sample_size+1)
                for j in range(sample_count)]
    else:
        raise Exception("List too short")

keys_digraph = [k for k,v in options_best_keys_digraph[:30] if not sum( [not (k in key2data and len(key2data[k])>30) for key2data in people.values()]) ]
sample_count, sample_size = 4,5
trainings = dict() #{name: {key:li, key:...}, name:...}
samples = dict() #{name: {key:[li, li,..], key:...}, name:...}
for name, key2data in people.items():
    trainings[name] = dict()
    samples[name] = [dict() for i in range(sample_count)]
    for key in keys_digraph:
        li = key2data[key]
        trainings[name][key] = list()
        idxs = get_samples_idxs(li,sample_count,sample_size)+[(len(li),len(li))]
        for i in range(len(idxs)-1):
            samples[name][i][key] = li[idxs[i][0]:idxs[i][1]]
            trainings[name][key].extend(li[idxs[i][1]:idxs[i+1][0]])

#now run on all:
for name, many_samples in samples.items():
    print(name)
    for sample in many_samples:
        d = [0 for p in trainings]
        for key in keys_digraph:
            for i,person in enumerate(trainings.values()):
                d[i] += abs(statistics.mean(sample[key]) - statistics.mean(person[key]))
        d = sorted(list(zip(d,trainings.keys())))
        if name != d[0][1]:
            print(d)
#still 100%