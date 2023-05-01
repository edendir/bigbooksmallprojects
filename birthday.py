#Birthday 'Paradox' simulation

import datetime, random


def getBirthdays(numberOfBirthdays):
    #Returns list of number random date objects for birthdays
    birthdays = []
    for i in range(numberOfBirthdays):
        startOfYear = datetime.date(2001, 1, 1)

        #get random day in year
        randomNumOfDays = datetime.timedelta(random.randint(0, 364))
        birthday = startOfYear + randomNumOfDays
        birthdays.append(birthday)
    return birthdays

def getMatch(birthdays):
    #Returns date object of birthday occurs more than once in the list
    if len(birthdays) == len(set(birthdays)):
        return None
    
    for a, birthdayA in enumerate(birthdays):
        for b, birthdayB in enumerate(birthdays[a + 1 :]):
            if birthdayA == birthdayB:
                return birthdayA
            
print('The Birthday Paradox shows us that in a group of N people, the odds that two of them have matching birthdays is surprisingly large.')

MONTHS = ('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC')

while True:
    print('How many birthdays should I generate? (Max 100)')
    response = input('> ')
    if response.isdecimal() and (0 < int(response) <= 100):
        numBDays = int(response)
        break

print('Here are ', numBDays, 'birthdays:')
birthdays = getBirthdays(numBDays)
for i, birthday in enumerate(birthdays):
    if i != 0:
        print(', ', end='')
    monthName = MONTHS[birthday.month - 1]
    dateText = '{} {}'.format(monthName, birthday.day)
    print(dateText, end='')
print()
print()

match = getMatch(birthdays)

print('In this simulation, ', end='')
if match != None:
    monthName = MONTHS[match.month - 1]
    dateText = '{} {}'.format(monthName, match.day)
    print('multiple people have a birthday on:', dateText)
else:
    print('there are no matching birthdays.')
print()

#Run through 100k simulations
print('Generating {} random birthdays 100,000 times'.format(numBDays))
input('Press Enter to begin.')

simMatch = 0 #simulations with matching bdays
for i in range(100_000):
    #report on progress every 10k
    if i % 10_000 == 0:
        print('{} simulations run.'.format(i))
    birthdays = getBirthdays(numBDays)
    if getMatch(birthdays) != None:
        simMatch += 1
print('100,000 simulations run.')

#Display results
probability = round(simMatch / 100_000 * 100, 2)
print('Out of 100,000 simulations of', numBDays, 'people, there was a matching birthday in that group', simMatch, 'times. This means that', numBDays, 'people have a', probability, '% chance of having a matching birthday in their group.')
