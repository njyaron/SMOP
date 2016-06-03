#### איסוף נתונים ####

import parseFile
import os

results_directory = "Results"
main_directory = r'F:\Clouds\Google Drive\SMOP Data'

# כמה אנשים נבדקו? 
print(len( [name for name in os.listdir(main_directory) if os.path.isdir(os.path.join(main_directory,name))]))

#1/6: 35

# כמה הקשות מקלדת נחקרו? 
#כמה מהן היו מעניינות? = לא מספרים/כפתורים הזויים 
keys = {'d', 'v', 'right alt', '[', 'right shift', 'b', 'm', 'p', 'q', 'c', 'u', 'g', 'enter', '\\', 's', "'", 'j', 'y', '.', 'f', 'k', 'i', ',', 'z', '*', 'a', 't', 'l', 'right ctrl', 'tab', 'r', 'alt', 'space', 'w', '/', 'n', '=', 'e', 'shift', ']', ';', 'o', '+', 'x', 'ctrl', '-', 'h'}
countKeyUps = 0
countGoodKeyUps = 0
#d = [] #TEMP
for name in os.listdir(main_directory):
    print("Building " + name)
    results_path = os.path.join(main_directory, name, results_directory)
    if os.path.exists(results_path):
        events = parseFile.load_all_standard_sessions(results_path)
        upEvents = [ev for ev in events if ev.event_type=='up']
        countKeyUps += len(upEvents)
        goodUpEvents = [ev for ev in upEvents if ev.names and ev.names[-1] in keys]
        countGoodKeyUps += len(goodUpEvents)
        #d.append( (name, len(upEvents), len(goodUpEvents)) ) #TEMP

print(countKeyUps)
print(countGoodKeyUps)

#1/6: 2012982, 1428796


#כמה פסקאות מולאו וכמה אנשים מילאו כל כמות פעמים
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

#print(sorted(people, reverse=True))
from collections import Counter
cnt = Counter([c for c,name in people])
for k,v in cnt.items():
    print(k,v)

