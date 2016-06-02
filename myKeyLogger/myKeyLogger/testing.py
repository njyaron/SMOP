import parseFile
import durationGenerator
import durationFilter
import durationComparer 

import os

results_directory = "Results"
main_directory = r'F:\Clouds\Google Drive\SMOP Data'

#get which programs are common
programs = dict()

for name in os.listdir(main_directory):
    print("Building " + name)
    results_path = os.path.join(main_directory, name, results_directory)
    if os.path.exists(results_path):
        events = parseFile.load_all_standard_sessions(results_path)
        for ev in events:
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

special_keywords = [ ["WhatsApp"],
                    ["Eclipse", "IntelliJ"],
                    ["Word", "PowerPoint"],
                    ["README"],
                    ["py", "PyCharm"],
                    ]
for keywords in special_keywords:
    user_with = get_users_with(keywords)
    print("keystrokes for users with " + str(keywords))
    print(str(len(user_with)) + " users: " + str(user_with))

#temp
keywords = ["WhatsApp"]#["Word", "PowerPoint"]
user_with = get_users_with(keywords)
print("keystrokes for users with " + str(keywords))
print(str(len(user_with)) + " users: " + str(user_with))


user_with = dict()
for name in os.listdir(main_directory):
    print("Building " + name)
    results_path = os.path.join(main_directory, name, results_directory)
    if os.path.exists(results_path):
        events = parseFile.load_all_standard_sessions(results_path)
        events = [ev for ev in events if ("Google" in ev.window_name and "Chrome" not in ev.window_name)]
        if events:
            user_with[name] = len(events)



#total keystrokes: 1822664  -   sum([v for p,v in programs.items()])

#keystrokes for users with ["WhatsApp"]:
#7(6) users: {'Yotam Sali': 462, 'Shachar Baron': 493, 'Dor Aharonson': 7939, 'Nir Yaron': 14290, 'Omer Deutsch': 2466, 'Adi Asher': 2622, 'Ohad Ben-Or': 134}

#keystrokes for users with ["Eclipse", "IntelliJ"]:
#6 users: {'Yovel Rom': 50986, 'Guy Levanon': 103889, 'Dor Aharonson': 86460, 'Nir Yaron': 149578, 'Adi Asher': 27565, 'Matan Levine': 162313}

#keystrokes for users with ['Word', 'PowerPoint']
#17 users: {'Efi Sapir': 1410, 'Yotam Sali': 17768, 'Shachar Baron': 2480, 'Harel Gelfand': 1996, 'Alon Gal': 11826, 'Omer Deutsch': 27946, 'Adi Asher': 9231, 'Ohad Ben-Or': 1459, 'Nimrod Rind': 1379, 'Yovel Rom': 3321, 'Guy Levanon': 2587, 'Dor Aharonson': 16578, 'Nir Yaron': 64673, 'Matan Seri': 7098, 'Itay Efraim': 2031, 'Matan Levine': 15274, 'Noam Shapira': 1442}

#keystrokes for users with ["PowerPoint"]:
#9 users: {'Yovel Rom': 340, 'Shachar Baron': 981, 'Harel Gelfand': 629, 'Alon Gal': 6474, 'Nir Yaron': 1036, 'Matan Seri': 795, 'Adi Asher': 1695, 'Matan Levine': 10752}

#keystrokes for users with ["README"]:
#6(4) users: {'Yovel Rom': 21598, 'Guy Levanon': 28774, 'Dor Aharonson': 10801, 'Alon Gal': 4, 'Nir Yaron': 34859, 'Matan Levine': 4}


#java 527500 Eclipse 449259 Java 429352 IDEA 131454 IntelliJ 131454
#README 96040
#Google 435000 Chrome 377849 (Almost always both, so take on "Chrome")
#Word 136194 docx 75392 #PowerPoint 22149 [decided to merge them]
#gmail 96322 Inbox 63828 Gmail 32600
#py 80265 PyCharm 68960 PycharmProjects 33709 [4 ppl, but hopefully will grow]
#WhatsApp 25940 Web 26156


#OOP 337467 Ex5 327405 - contained in "java"
#Dropbox 164892 - nothing to do with
#Microsoft 161396 - almost just Word and PowerPoint
#Visual 82851 Studio 82847 - only me 

#count uniforms
people = []
for name in os.listdir(main_directory):
    c = 0
    path = os.path.join(main_directory, name)
    results_path = os.path.join(path, results_directory)
    if os.path.isdir(results_path):
        for d in os.listdir(results_path):
            if os.path.isdir(os.path.join(results_path,d)):
                for f in os.listdir(os.path.join(results_path,d)):
                    if "UNIFORM" in f:
                           c += 1

    people.append( (c,name) )

print(sorted(people, reverse=True))



#all keys in keyboard
keys = set()
for name in os.listdir(main_directory):
    print("Building " + name)
    results_path = os.path.join(main_directory, name, results_directory)
    if os.path.exists(results_path):
        events = parseFile.load_all_standard_sessions(results_path)
        keys = keys.union({nm for ev in events for nm in ev.names })

#keys = {'end', 'd', 'v', '7', 'right alt', 'home', 'esc', 'f5', '`', 'page down', '[', 'f11', 'right shift', 'b', 'm', 'p', 'q', 'ץ', '3', 'c', '8', 'u', 'g', 'enter', '\\', '9', 's', 'down', 'f1', "'", 'j', 'f9', 'y', 'f3', '.', 'f', 'insert', '4', 'f2', 'delete', 'break', 'f4', 'k', 'application', 'i', ',', 'f10', 'page up', 'ף', 'z', '*', 'f8', 'a', '5', 'print screen', 'sys req', '2', 't', '0', 'l', 'left windows', 'ת', 'right ctrl', 'windows', 'tab', 'f12', 'r', 'alt', 'space', 'w', '/', 'n', 'scroll lock', '=', '6', 'e', '1', 'shift', 'right windows', 'f7', 'left', ']', ';', 'o', 'right', '<00>', '+', 'backspace', 'up', 'x', 'ctrl', 'f6', 'caps lock', '-', 'del', 'h'}
#then i chose keys = {'d', 'v', 'right alt', '[', 'right shift', 'b', 'm', 'p', 'q', 'c', 'u', 'g', 'enter', '\\', 's', "'", 'j', 'y', '.', 'f', 'k', 'i', ',', 'z', '*', 'a', 't', 'l', 'right ctrl', 'tab', 'r', 'alt', 'space', 'w', '/', 'n', '=', 'e', 'shift', ']', ';', 'o', '+', 'x', 'ctrl', '-', 'h'}