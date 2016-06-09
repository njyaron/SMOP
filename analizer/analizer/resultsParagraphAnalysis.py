#### Paragraph analysis ####
import trigraphArray
import matplotlib.pyplot as plt

people = trigraphArray.load_all()

# distribution of similarity in sessions from the same person, for some users
names = ['Nir Yaron', 'Adi Asher', 'Yovel Rom', 'Guy Levanon']
for name in names:
    person = [p for p in people if p.name == name][0]
    plt.hist(person.vars)
    plt.show()

# distribution of similarity in sessions from the same person, for all users
varsSimilar = [var for person in people for var in person.vars]
plt.hist(varsSimilar)
plt.show()

# distribution of similarity in sessions of different people
varsDifferent = []
for person in people:
    people2 = [p for p in people if p != person]
    sessions = [s for person1 in people2 for s in person1.sessions]
    for session1 in person.sessions:
        for session2 in sessions:
            if trigraphArray.can_compare(session1, session2):
                varsDifferent.append(trigraphArray.compare_sessions(session1, session2))

plt.hist(varsSimilar, normed=True)
plt.hist(varsDifferent, normed=True)
plt.show()

# distribution of common trigraphs for same person sessions
common_trigraphs = [c for p in people for c in p.get_common_trigraphs()]
plt.hist(common_trigraphs)
plt.show()

#sucess rates of this method
learned_people = [p for p in people if len(p.sessions) > 1]
sessions = [(person1.name,s) for person1 in learned_people for s in person1.sessions]
for name, session in sessions: 
    print(name, name==trigraphArray.best_fit(people,session))
successes = [name==trigraphArray.best_fit(people,session) for name, session in sessions]
print(sum(successes)/len(successes))

#gets 0.8837209302325582 (fails on Greenberg and Caspi because of typos)
#if i change trigraphArray.MINIMAL_COMMON_KEYS = 10:
#gets 0.9767441860465116 (fails only once with Guy=Efi)

