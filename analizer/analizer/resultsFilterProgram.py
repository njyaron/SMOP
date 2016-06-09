import parseFile
import featureFilter
import featureGenerator
import featureComparer
import duration, digraph, trigraph, digraphRatio

import pickle, os, math
import matplotlib.pyplot as plt

results_directory = parseFile.results_directory
main_directory = parseFile.main_directory

def get_main_keywords():
    #get which programs are common
    programs = dict()

    for name in os.listdir(main_directory):
        print("Building " + name)
        results_path = os.path.join(main_directory, name, results_directory)
        if os.path.exists(results_path):
            events = parseFile.load_all_standard_sessions(results_path)
            for ev in events:
                if ev.event_type == 'up':
                    if ev.window_name not in programs:
                        programs[ev.window_name] = 0
                    programs[ev.window_name] += 1

    #get most common words in the window names
    import re
    def get_words(text):
        return re.compile('\w+').findall(text)

    main_keywords = dict()
    for p,v in programs.items():
        for word in get_words(p):
            if word not in main_keywords:
                main_keywords[word] = 0
            main_keywords[word] += v

    k = sorted(main_keywords.items(), key=lambda it: -it[1])
    return k

#k[:50] after some manual filttering:
#JAVA: ('java', 707352), ('Java', 448336), ('Eclipse', 465351), ('IntelliJ', 312560), ('IDEA', 312560), 
#OOP: ('ex5', 671628), ('Ex5', 584791), ('OOP', 342203), ('README', 157674), ('oop', 68520)
#web: ('Google', 564382), ('Chrome', 468451), ('gmail', 125640), ('Gmail', 85097), 
#text editors: ('Microsoft', 163368), ('docx', 129479), ('Word', 257566), ('Notepad', 103818),('PowerPoint', 82768), 
#MATLAB:('MATLAB', 87674),('R2014b', 69634), 
#Python: ('Studio', 80440), ('Visual', 80408), 
#most famous: ('src', 807663), 

#[('java', 707352), ('ex5', 671628), ('Chrome', 468451), ('Eclipse', 465351), ('IntelliJ', 312560), ('Word', 257566), ('gmail', 125640), ('MATLAB', 87674), ('PowerPoint', 82768), ]

single_keywords = [('java','Java',), ('ex5','Ex5'), ('Chrome',), ('Eclipse',), ('IntelliJ',), ('Word',), ('gmail','Gmail'), ('MATLAB',), ('PowerPoint',), ('README',)]

group_keywords = [ ('java', 'Java', 'Eclipse', 'IntelliJ', 'IDEA'), #Java
                    ('Chrome',), #Web
                    ( 'gmail', 'Gmail', 'Inbox'), #mail
                    ('Microsoft', 'docx', 'Word', 'Notepad', 'PowerPoint', 'README'), #text editors
                    ('MATLAB', 'R2014b'), #Matlab
                    ("py", "PyCharm"), #python
                    ]

#check for specially famous programs
def filter_by_program(events, keywords):
    return [ev for ev in events if sum([(word in ev.window_name) for word in keywords])]

def get_users_with(keywords):
    user_with = dict()
    for name in os.listdir(main_directory):
        print("Building " + name)
        results_path = os.path.join(main_directory, name, results_directory)
        if os.path.exists(results_path):
            events = parseFile.load_all_standard_sessions(results_path)
            #events = durationFilter.filter_by_program(events, keywords)
            events = filter_by_program(events, keywords)
            if events:
                user_with[name] = len(events)
    return user_with

def get_keywords_counter(keywords):
    counter = [0 for kwrds in keywords]
    for name in os.listdir(main_directory):
        print("Building " + name)
        results_path = os.path.join(main_directory, name, results_directory)
        if os.path.exists(results_path):
            events = parseFile.load_all_standard_sessions(results_path)
            for ev in [ev for ev in events if ev.event_type == 'up']:
                for i,kwrds in enumerate(keywords):
                    counter[i] += featureFilter.contains_some_words(ev.window_name, kwrds)
    return counter

groups_counter = get_keywords_counter(group_keywords) 
#[(('java', 'Java', 'Eclipse', 'IntelliJ', 'IDEA'), 795674), ('Chrome', 2091376), (('gmail', 'Gmail', 'Inbox'), 127650), (('Microsoft', 'docx', 'Word', 'Notepad', 'PowerPoint', 'README'), 604745), (('MATLAB', 'R2014b'), 87514), (('py', 'PyCharm'), 62340)]
single_counter = get_keywords_counter(single_keywords)
#[(('java',), 707599), (('ex5',), 488615), (('Chrome',), 494179), (('Eclipse',), 465393), (('IntelliJ',), 312564), (('Word',), 257704), (('gmail',), 125202), (('MATLAB',), 87514), (('PowerPoint',), 82724), (('README',), 157674)]

def best_people(keywords=[], languages=featureFilter.ALL_LANGUAGES):
    "Returns the people who typed the most under this restriction"
    filters = [featureFilter.Filter(long_time=duration.LONG_TIME,keywords=keywords, languages=languages),
            featureFilter.Filter(long_time=digraph.LONG_TIME,keywords=keywords, languages=languages),
            featureFilter.Filter(long_time=trigraph.LONG_TIME,keywords=keywords, languages=languages),
            featureFilter.Filter(long_time=digraphRatio.LONG_TIME,keywords=keywords, languages=languages),
            ] 
    feature_types = featureGenerator.ALL_TYPES

    people = featureComparer.generate_people(filters,feature_types,is_uniform=False)
    arr = sorted([(sum([feature.count for feature in p.features.values()]),p.name) for p in people], reverse=True)
    for v,name in arr:
        print(v,name)
    return people

def best_keys1(people, feature_type):
    #for people from generate_people
    keys = dict()
    for p in people:
        for k,ftr in p.features.items():
            if ftr.feature_type == feature_type:
                if k not in keys:
                    keys[k] = 0
                keys[k] += ftr.count
    keys = sorted(list(keys.items()), key=lambda x:-x[1])
    return keys

def best_keys2(people, feature_type):
    #for people from build_key2data
    keys = dict()
    for p in people.values():
        for k,li in p.items():
            if k[-1] == feature_type:
                if k not in keys:
                    keys[k] = 0
                keys[k] += len(li)
    keys = sorted(list(keys.items()), key=lambda x:-x[1])
    return keys


### Now same as Background General

#features distribution for two people

def build_key2data(keywords, names):
    filters = [featureFilter.Filter(long_time=duration.LONG_TIME,keywords=keywords),
                featureFilter.Filter(long_time=digraph.LONG_TIME,keywords=keywords),
                featureFilter.Filter(long_time=trigraph.LONG_TIME,keywords=keywords),
                featureFilter.Filter(long_time=digraphRatio.LONG_TIME,keywords=keywords),
                ] 
    feature_types = featureGenerator.ALL_TYPES
    people = dict()
    for name in names:
        print("Building " + name)
        path = os.path.join(main_directory, name)
        events, _ = parseFile.get_events(path, filters[0], is_uniform=False, with_sample=False)
        people[name] = dict()
        for filter, feature_type in zip(filters, feature_types):
            keys2data = featureGenerator.create_data(events,filter,feature_type)
            people[name].update( keys2data )#{key:data for key,data in keys2data.items() if key in chosen_keys})
    return people

chosen_keys = [('space', 0), ('e', 0) ,
               ('i', 'n', 1), ('f', 'i', 1),
               ('t', 'h', 'e', 2), ('i', 'n', 'g', 2),
               ('t', 'h', 'e', 3), ('i', 'n', 'g', 3)
               ]

#Chrome - failed
keywords = ('Chrome',)
names = ["Nir Yaron", "Noam Greenberg", "Shaked Rosenstein", "Matan Levine"]
people_chrome = build_key2data(keywords,names)


#Java
chosen_keys = [('space', 0), ('i', 0) ,
               ('i', 'n', 1), ('e', 'r', 1),
               ('f', 'o', 'r', 2), ('f', 'i', 'l', 2),
               ('f', 'o', 'r', 3), ('f', 'i', 'l', 3)
               ]
keywords = ('java', 'Java', 'Eclipse', 'IntelliJ', 'IDEA')
names = ['Gal Oz-Ari', 'Gil Boazi', 'Nir Yaron', 'Guy Levanon', 'Yonathan Schwammenthal', 'Matan Levine', 'Ohad Ben-Or', 'Dor Aharonson', 'Yuval Itkin', 'Yonatan Caspi', 'Noam Greenberg', 'Adi Asher', 'Yovel Rom']
people_java = build_key2data(keywords,names)
for key in chosen_keys:
    for name in names:
        plt.hist(people_java[name][key], 20, normed=True)
    if key[-1] != 3:
        plt.xlabel('Time [ms]')
    else:
        plt.xlabel('Ratio')
    plt.ylabel('Occurances')
    plt.title('Histogram of ' + "".join(key[:-1]))
    p = os.path.join(r'F:\Clouds\Dropbox\SMOP\Presentation',"java_"+"".join([str(s) for s in key]))
    plt.savefig(p)
    plt.cla()


#feature_type = featureGenerator.DIGRAPH_TYPE
#keys = dict()
#for p in people_chrome.values():
#    for k,li in p.items():
#        if k[-1] == featureGenerator.DIGRAPH_TYPE:
#            if k not in keys:
#                keys[k] = 0
#            keys[k] += len(li)
#keys = sorted(list(keys.items()), key=lambda x:-x[1])

for key in chosen_keys:
    for name in names:
        plt.hist(people_chrome[name][key], 20, normed=True)
    print(key)
    plt.show()

    
#Median and error of features

for key in chosen_keys:
    x = [person.features[key].mean for person in people if person.is_feature_good(key)]
    xerr = [person.features[key].stdev for person in people if person.is_feature_good(key)]
    y = list(range(len(x)))
    plt.errorbar(x, y, xerr=xerr,fmt='.')
    plt.show()
