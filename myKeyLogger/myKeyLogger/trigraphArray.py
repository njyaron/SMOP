import parseFile
import trigraphFilter
import trigraphGenerator

import os
import statistics

MAX_STDEV = 2.5
GOOD_SIMILARITY = 0.43
MINIMAL_COMMON_KEYS = 250 #maybe 180 is enought

#compare all users
results_directory = "Results"
main_directory = r'F:\Clouds\Google Drive\SMOP Data'

class Person:
    def __init__(self, name, path, filter):
        self.name = name
        self.path = path
        #load events
        results_path = os.path.join(path, results_directory)
        event_sessions = [] 
        if os.path.exists(results_path):
            event_sessions = [session for kind,index,session in parseFile.load_all_uniform_sessions(results_path)]
        #analyze (including filtering)
        self.sessions = list()
        for event_session in event_sessions:
            session = trigraphGenerator.analyze_trigraphs(event_session, filter)
            self.sessions.append(sort_session(session))
        self.calc_variances()

    def compare_session(self, new_session):
        #watch out - if i'm already in, it's not fair...
        comparisons = [compare_sessions(new_session, session) for session in self.sessions 
                       if can_compare(new_session, session)]
        if comparisons:
            return sum(comparisons) / len(comparisons)
        else:
            return 1000

    def get_common_trigraphs(self):
        common_trigraphs = list()
        for i in range(len(self.sessions)):
            for j in range(i+1,len(self.sessions)):
                common_keys = set(self.sessions[i]).intersection(self.sessions[j])
                common_trigraphs.append(len(common_keys))
        return common_trigraphs

    def calc_variances(self):
        self.vars = []
        for i in range(len(self.sessions)):
            for j in range(i+1,len(self.sessions)):
                comparison = compare_sessions(self.sessions[i], self.sessions[j])
                if comparison:
                    self.vars.append(comparison)
        if self.vars:
            self.avg_var = sum(self.vars)/len(self.vars)
        if len(self.vars) > 1:
            self.std_var = statistics.stdev(self.vars)

    def get_worse_variance(self):
        return max(self.vars)

    def can_be_me(self, session):
        return can_be_me1()

    def can_be_me1(self, session):
        #with stdev
        similarity = self.compare_session(session)
        return similarity < self.avg_var + MAX_STDEV * self.std_var

    def can_be_me2(self, session):
        #better than worse attemp
        similarity = self.compare_session(session)
        return similarity < get_worse_variance()

    def can_be_me3(self, session):
        #better than worse attemp
        similarity = self.compare_session(session)
        return similarity < GOOD_SIMILARITY

#session is a list of key triples
def sort_session(session):
    sorted_items = sorted(session.items(), key=lambda x: x[1].mean)
    return [key for key,trigraph in sorted_items]

def can_compare(session1, session2):
    common_keys = set(session1).intersection(session2)
    return len(common_keys) > MINIMAL_COMMON_KEYS and session1 != session2

def compare_sessions(session1, session2):
    bad_factor = 0
    common_keys = set(session1).intersection(session2)
    if len(common_keys) > MINIMAL_COMMON_KEYS:
        session1_trimmed = [k for k in session1 if k in common_keys]
        session2_trimmed = [k for k in session2 if k in common_keys]
        session12idx = {k:idx for idx,k in enumerate(session1_trimmed)}
        for idx,k in enumerate(session2_trimmed):
            bad_factor += abs(idx-session12idx[k])
        counter = len(common_keys)
        return bad_factor / (counter*counter/2)
    else:
        return 1000

def get_fits(people, session):
    matches = [ ( person.compare_session(session), person.name ) for person in people]
    return sorted(matches)

def best_fit(people, session):
    return min(get_fits(people,session))[1]

def load_all():
    filter = trigraphFilter.Filter(languages=trigraphFilter.ALL_LANGUAGES, 
                                stdev_factor=0, keywords=[], long_time=0.8)
    people = []
    for name in os.listdir(main_directory):
        print("Building " + name)
        path = os.path.join(main_directory, name)
        if os.path.isdir(path):
            people.append(Person(name, path, filter))

    return [p for p in people if p.sessions]



#main
if __name__ == '__main__':
    #Load all:
    people = load_all()


    name = "Nir Yaron"
    path = os.path.join(main_directory, name)
    per = Person(name, path, filter)

    for i1,s1 in enumerate(per.sessions):
        for i2,s2 in enumerate(per.sessions):
            print(i1,i2,compare_sessions(s1,s2))


    def min_max_dist(person, people):
        people2 = [p for p in people if p != person]
        matches = [person.compare_session(s1) for person1 in people2 for s1 in person1.sessions]
        return min(matches), max(matches)

    for person in people:
        print(person.name, min_max_dist(person, people))

    for person in people:
        if person.get_variances():
            print(person.name, max(person.get_variances()))

    for person in people:
        if person.get_variances():
            print(person.name,  min_max_dist(person, people)[0] - max(person.get_variances()))


    ##generate list of key_couples
    #key_couples = set().union(*[person.get_key_couples() for person in people])

    #for key_couple in key_couples:
    #    feature_frequency = count_users_containing_key_couple(people, key_couple)
    #    if feature_frequency > 3:
    #        possible_couples = feature_frequency * (feature_frequency - 1) #no division by 2, cuz counts couples twice 
    #        feature_quality = count_differentialbe_couples(people, key_couple) / possible_couples
    #        if feature_quality > 0.2:
    #            print(key_couple, feature_frequency, feature_quality)

