import parseFile
import featureFilter
import featureGenerator
import featureComparer
import duration, digraph, trigraph, digraphRatio

import pickle, os, math, statistics
import matplotlib.pyplot as plt

results_directory = parseFile.results_directory
main_directory = parseFile.main_directory

#choose the names of people i want to test
#names = ['Gal Oz-Ari', 'Gil Boazi', 'Nir Yaron', 'Guy Levanon', 'Yonathan Schwammenthal', 'Matan Levine', 'Ohad Ben-Or', 'Dor Aharonson', 'Yuval Itkin', 'Yonatan Caspi', 'Noam Greenberg', 'Adi Asher', 'Yovel Rom']
names1 = ['Adi Asher', 'Alon Gal', 'Amitai Nevo', 'Dor Aharonson', 'Efi Sapir', 'Elad Kliger', 'Elisha Modelevsky', 'Gal Oz-Ari', 'Gallil Maimon', 'Gil Boazi', 'Gilad Samuels', 'Guy Levanon', 'Ido Zemach', 'Itay Efraim', 'Matan Levine', 'Matan Seri', 'Nir Yaron', 'Noam Greenberg', 'Ohad Ben-Or', 'Omer Deutsch', 'Or Johnson Ezra', 'Or Sagy', 'Shaked Rosenstein', 'Yonatan Caspi', 'Yonathan Schwammenthal', 'Yotam Sali', 'Yovel Rom', 'Yuval Itkin']
names2 = ['Adi Asher', 'Amitai Nevo', 'Dor Aharonson', 'Elad Kliger', 'Elisha Modelevsky', 'Gal Oz-Ari', 'Gallil Maimon', 'Gil Boazi', 'Gilad Samuels', 'Guy Levanon', 'Ido Zemach', 'Matan Levine', 'Nir Yaron', 'Noam Greenberg', 'Ohad Ben-Or', 'Omer Deutsch', 'Or Johnson Ezra', 'Or Sagy', 'Shaked Rosenstein', 'Yonatan Caspi', 'Yonathan Schwammenthal', 'Yovel Rom', 'Yuval Itkin']
names3 = ['Adi Asher', 'Dor Aharonson', 'Elad Kliger', 'Elisha Modelevsky', 'Gal Oz-Ari', 'Gallil Maimon', 'Gil Boazi', 'Gilad Samuels', 'Guy Levanon', 'Matan Levine', 'Nir Yaron', 'Noam Greenberg', 'Ohad Ben-Or', 'Or Johnson Ezra', 'Shaked Rosenstein', 'Yonathan Schwammenthal', 'Yovel Rom', 'Yuval Itkin']
names = names3

#filter and get feature arrays for them
keywords = tuple() #('java', 'Java', 'Eclipse', 'IntelliJ', 'IDEA')
languages = featureFilter.ALL_LANGUAGES #[featureFilter.ENGLISH]
filters = [featureFilter.Filter(long_time=duration.LONG_TIME,keywords=keywords,languages=languages),
            featureFilter.Filter(long_time=digraph.LONG_TIME,keywords=keywords,languages=languages),
            featureFilter.Filter(long_time=trigraph.LONG_TIME,keywords=keywords,languages=languages),
            featureFilter.Filter(long_time=digraphRatio.LONG_TIME,keywords=keywords,languages=languages),
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

loc = "F:\Clouds\Dropbox\SMOP\AnalysisCompressed\general_people2key2data.p"  #r"F:\Clouds\Dropbox\SMOP\AnalysisCompressed\eclipse_english_people2key2data.p"
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

loc = "F:\Clouds\Dropbox\SMOP\AnalysisCompressed\general_people2key2data.p"  #r"F:\Clouds\Dropbox\SMOP\AnalysisCompressed\eclipse_english_people2key2data.p"
people = pickle.load( open( loc, "rb" ) )
people = {key:person for (key,person) in people.items() if key in names}
options_best_keys_digraph = best_keys2(people, featureGenerator.DIGRAPH_TYPE)

keys_digraph = [k for k,v in options_best_keys_digraph[:30] if not sum( [not (k in key2data and len(key2data[k])>30) for key2data in people.values()]) ]

#for one person:
name = "Gal Oz-Ari"
person = people[name]
#split for training+sample(last 10% of array)
training = {key:li[:-60] for key,li in person.items()}
sample = {key:li[-60:] for key,li in person.items()}

#draw both historgrams and hope to see similar things
for key in keys_digraph:
    trn = plt.hist(training[key], bins=10,normed=True,alpha=0.6,label=['Training'])
    slp = plt.hist(sample[key], bins=10,normed=True,alpha=0.6,label=['Sample'])
    plt.legend()
    plt.xlabel('Time [s]')
    plt.ylabel('Occurances (Normalized)')
    plt.title('Histogram of ' + "_".join(key[:-1]))
    dir = r'F:\Clouds\Dropbox\SMOP\Presentation\Graphs\General\SamePerson'
    if not os.path.isdir(dir):
        os.mkdir(dir)
    p = os.path.join(dir,"OzAri_"+"".join([str(s) for s in key]))
    plt.savefig(p)
    plt.cla()
    #plt.show()

#if works, do the same for a few people and hope to see differences
temp_names = ['Gal Oz-Ari', 'Nir Yaron', 'Guy Levanon', 'Yonathan Schwammenthal']
display_names = ['Gal Oz-Ari', 'Nir Yaron', 'Guy Levanon', 'Schwammi']
temp_people = [people[name] for name in temp_names]
for key in keys_digraph:
    for name, person in zip(display_names,temp_people):
        res = plt.hist(person[key], bins=10,normed=True,alpha=0.6,label=[name])
    plt.legend()
    plt.xlabel('Time [s]')
    plt.ylabel('Occurances (Normalized)')
    plt.title('Histogram of ' + "_".join(key[:-1]))
    dir = r'F:\Clouds\Dropbox\SMOP\Presentation\Graphs\General\SameFeatureDifferentPeople'
    if not os.path.isdir(dir):
        os.mkdir(dir)
    p = os.path.join(dir,"tst1_"+"".join([str(s) for s in key]))
    plt.savefig(p)
    plt.cla()
    #plt.show()

#plot mean in std to visually see clusters
def get_samples_idxs(li, sample_count, sample_size):
    if len(li) > sample_count * sample_size:
        return [(len(li)//sample_count*j,len(li)//sample_count*j+sample_size+1)
                for j in range(sample_count)]
    else:
        raise Exception("List too short")

def get_training_samples(people, keys_digraph, sample_count, sample_size):
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
    return trainings, samples

trainings, samples = get_training_samples(people,keys_digraph,3,10)
cmap = plt.get_cmap('Set1')
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
for key in keys_digraph[:5]:
    for i,name in enumerate(names[:6]):
        #color = cmap(i/len(people))
        color = colors[i%len(colors)]
        x = [statistics.mean(sample[key]) for sample in samples[name]]
        y = [statistics.stdev(sample[key]) for sample in samples[name]]
        #y = [i for sample in samples[name]]
        plt.plot(x,y,"o",color=color,alpha=0.6)
        data = people[name][key]
        plt.plot([statistics.mean(data)],[statistics.stdev(data)],"o",color=color)
        #plt.plot([statistics.mean(data)],[i],"o",color=color)
    
    plt.xlabel('Mean [s]')
    plt.ylabel('StDev [s]')
    plt.title('Mean vs. StDev of ' + "_".join(key[:-1]))
    dir = r'F:\Clouds\Dropbox\SMOP\Presentation\Graphs\General\MeanStDevPlot'
    if not os.path.isdir(dir):
        os.mkdir(dir)
    p = os.path.join(dir,"both_"+"".join([str(s) for s in key]))
    plt.savefig(p)
    plt.cla()
    #plt.show()

#just means
temp_keys = keys_digraph[:5]
temp_names = names[:6]
for key in temp_keys:
    for i,name in enumerate(temp_names):
        color = colors[i%len(colors)]
        x = [statistics.mean(sample[key]) for sample in samples[name]]
        y = [i for sample in samples[name]]
        plt.plot(x,y,"o",color=color,alpha=0.6)
        data = people[name][key]
        plt.plot([statistics.mean(data)],[i],"o",color=color)
    
    plt.xlabel('Mean [s]')
    plt.ylabel("User's Index")
    plt.title('Mean of samples ' + "_".join(key[:-1]))
    dir = r'F:\Clouds\Dropbox\SMOP\Presentation\Graphs\General\MeanStDevPlot'
    if not os.path.isdir(dir):
        os.mkdir(dir)
    p = os.path.join(dir,"mean_"+"".join([str(s) for s in key]))
    plt.ylim(-0.5,len(temp_names)-0.5)
    plt.savefig(p)
    plt.cla()

#just std
for key in temp_keys:
    for i,name in enumerate(temp_names):
        color = colors[i%len(colors)]
        x = [i for sample in samples[name]]
        y = [statistics.stdev(sample[key]) for sample in samples[name]]
        plt.plot(x,y,"o",color=color,alpha=0.6)
        data = people[name][key]
        plt.plot([i],[statistics.stdev(data)],"o",color=color)
    
    plt.xlabel("User's Index")
    plt.ylabel("StDev [s]")
    plt.title('StDev of samples ' + "_".join(key[:-1]))
    dir = r'F:\Clouds\Dropbox\SMOP\Presentation\Graphs\General\MeanStDevPlot'
    if not os.path.isdir(dir):
        os.mkdir(dir)
    p = os.path.join(dir,"std_"+"".join([str(s) for s in key]))
    plt.xlim(-0.5,len(temp_names)-0.5)
    plt.savefig(p)
    plt.cla()


#now we'll try to make a bigger sample-base
def eval(trainings_avg, samples_avg, keys_digraph,debug=False):
    c = 0
    tot = 0
    for name, many_samples in samples_avg.items():
        for sample_avg in many_samples:
            d = [0 for p in trainings_avg]
            for key in keys_digraph:
                for i,person_avg in enumerate(trainings_avg.values()):
                    d[i] += abs(sample_avg[key] - person_avg[key])
            d = sorted(list(zip(d,trainings_avg.keys())))
            if name != d[0][1]:
                if debug:
                    print(name, d)
                c += 1
            tot += 1
    return 1-c/tot

MINIMUM_FEATURE_COUNT = 45
possible_keys = [k for k,v in options_best_keys_digraph if 
                 not sum( [not (k in key2data and len(key2data[k])>MINIMUM_FEATURE_COUNT) 
                           for key2data in people.values()]) ]

def run_all(sample_count, sample_size, key_count):
    keys_digraph = possible_keys[:key_count]
    trainings, samples = get_training_samples(people,keys_digraph,sample_count,sample_size)
    trainings_avg = {name:{key:statistics.mean(data) for key,data in person.items()} 
                     for name,person in trainings.items()}
    samples_avg = {name:[{key:statistics.mean(data) for key,data in sample.items()} 
                     for sample in many_samples]
                     for name,many_samples in samples.items() }
    return eval(trainings_avg, samples_avg, keys_digraph)

#now run on all:
#success on sample_count = 3, sample_size = 7, key_count = 24
sample_count = 3

for sample_size in range(2,25):
    for key_count in range(3,25):
        acc = run_all(sample_count, sample_size, key_count)
        if acc > 0.85:
            print(sample_size, key_count, acc)
            break

############ now again with java only


names = ['Gal Oz-Ari', 'Gil Boazi', 'Nir Yaron', 'Guy Levanon', 'Yonathan Schwammenthal', 'Matan Levine', 'Ohad Ben-Or', 'Dor Aharonson', 'Yuval Itkin', 'Yonatan Caspi', 'Noam Greenberg', 'Adi Asher', 'Yovel Rom']

#filter and get feature arrays for them
keywords = ('java', 'Java', 'Eclipse', 'IntelliJ', 'IDEA')
languages = [featureFilter.ENGLISH]
filters = [featureFilter.Filter(long_time=duration.LONG_TIME,keywords=keywords,languages=languages),
            featureFilter.Filter(long_time=digraph.LONG_TIME,keywords=keywords,languages=languages),
            featureFilter.Filter(long_time=trigraph.LONG_TIME,keywords=keywords,languages=languages),
            featureFilter.Filter(long_time=digraphRatio.LONG_TIME,keywords=keywords,languages=languages),
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
loc = r"F:\Clouds\Dropbox\SMOP\AnalysisCompressed\eclipse_english_people2key2data.p"
people = pickle.load( open( loc, "rb" ) )
options_best_keys_digraph = best_keys2(people, featureGenerator.DIGRAPH_TYPE)
names = ['Gal Oz-Ari', 'Gil Boazi', 'Nir Yaron', 'Guy Levanon', 'Yonathan Schwammenthal', 'Matan Levine', 'Ohad Ben-Or', 'Dor Aharonson', 'Yuval Itkin', 'Yonatan Caspi', 'Noam Greenberg', 'Adi Asher', 'Yovel Rom']

trainings, samples = get_training_samples(people,keys_digraph,3,10)
cmap = plt.get_cmap('Set1')
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
for key in keys_digraph[:5]:
    for i,name in enumerate(names[:6]):
        #color = cmap(i/len(people))
        color = colors[i%len(colors)]
        x = [statistics.mean(sample[key]) for sample in samples[name]]
        y = [statistics.stdev(sample[key]) for sample in samples[name]]
        #y = [i for sample in samples[name]]
        plt.plot(x,y,"o",color=color,alpha=0.6)
        data = people[name][key]
        plt.plot([statistics.mean(data)],[statistics.stdev(data)],"o",color=color)
        #plt.plot([statistics.mean(data)],[i],"o",color=color)
    
    plt.xlabel('Mean [s]')
    plt.ylabel('StDev [s]')
    plt.title('Mean vs. StDev of ' + "_".join(key[:-1]))
    dir = r'F:\Clouds\Dropbox\SMOP\Presentation\Graphs\Java\MeanStDevPlot'
    if not os.path.isdir(dir):
        os.mkdir(dir)
    p = os.path.join(dir,"both_"+"".join([str(s) for s in key]))
    plt.savefig(p)
    plt.cla()
    #plt.show()


#now we'll try to make a bigger sample-base
MINIMUM_FEATURE_COUNT = 45
possible_keys = [k for k,v in options_best_keys_digraph if not 
                 sum( [not (k in key2data and len(key2data[k])>MINIMUM_FEATURE_COUNT) 
                       for key2data in people.values()]) ]

#now run on all:
#success on sample_count = 3, sample_size = 7, key_count = 24
sample_count = 3

for sample_size in range(2,25):
    for key_count in range(3,28):
        acc = run_all(sample_count, sample_size, key_count)
        if acc > 0.85:
            print(sample_size, key_count, acc)
            break
