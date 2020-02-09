import csv
import copy 

maleNames = {}
femaleNames = {}

males = {}
females = {}
with open('test.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if row['gender'].strip().lower() == "male":
            males[row['number']] = [ row['first'], row['second'], row['third'] ]
            maleNames[row['number']] = row['name']
        elif row['gender'].strip().lower() == "female":
            females[row['number']] = [ row['first'], row['second'], row['third'] ]
            femaleNames[row['number']] = row['name']

print(males)
print(females)

def prefers(man, former_woman, new_woman):
    preference = False
    if (man[0] == new_woman):
        preference = True
    elif (man[1] == new_woman and (man[0] != former_woman)):
        preference = True
    elif (man[2] == new_woman and man[0] != former_woman and man[1] != former_woman):
        preference = True
    return preference

def matchmaker():
    girlsfree = list(females)
    engaged  = {}
    guyprefers = copy.deepcopy(males)
    girlprefers = copy.deepcopy(females)
    while girlsfree:
        girl = girlsfree.pop(0)
        girlslist = girlprefers[girl]
        guy = girlslist.pop(0)
        fiance = engaged.get(guy)
        if not fiance:
            # He's free
            engaged[guy] = girl
            print("  %s and %s" % (girl, guy))
        else:
            # The bounder proposes to an engaged guy!
            guyslist = guyprefers[guy]
            if prefers(guyslist, fiance, girl):
                # He prefers new girl
                engaged[guy] = girl
                print("  %s dumped %s for %s" % (guy, fiance, girl))
                if girlprefers[fiance]:
                    # Ex has more girls to try
                    girlsfree.append(fiance)
            else:
                # She is faithful to old fiance
                if girlslist:
                    # Look again
                    girlsfree.append(girl)
    print()
    return engaged
 
print('\nEngagements:')
engaged = matchmaker()

all_taken_guys = []
all_taken_girls = []

remaining_guys = []
remaining_girls = []

for couple in sorted(engaged.items()):
    all_taken_guys.append(couple[0])
    all_taken_girls.append(couple[1])

for guy in list(males):
    if guy not in all_taken_guys:
        remaining_guys.append(guy)

for girl in list(females):
    if girl not in all_taken_girls:
        remaining_girls.append(girl)

print(remaining_girls)
print(remaining_guys)

for guy in remaining_guys:
    if (males[guy][0] not in all_taken_girls):
        engaged[guy] = males[guy][0]
        remaining_guys.remove(guy)
        remaining_girls.remove(males[guy][0])
    elif (males[guy][1] not in all_taken_girls):
        remaining_guys.remove(guy)
        engaged[guy] = males[guy][1]
        remaining_girls.remove(males[guy][1])
    elif (males[guy][2] not in all_taken_girls):
        engaged[guy] = males[guy][2]
        remaining_guys.remove(guy)
        remaining_girls.remove(males[guy][2])

for index, guy in enumerate(remaining_guys):
    engaged[guy] = remaining_girls[index]

print('\nCouples:')
print('  ' + ',\n  '.join('{} is matched to {}'.format(maleNames[couple[0]], femaleNames[couple[1]]) for couple in sorted(engaged.items())))