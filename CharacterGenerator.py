# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 15:12:27 2023

@author: Nathan
"""
import json
import random

raceDict = {'Dwarf': 5, 'Gnome': 20, 'Half-Elf': 10, 'Human': 50}
occupationDict = {'guard': 3, 'hunter': 6, 'lord': 1, 'farmer':8, 'artisan': 4}
names = ['name: ' for x in range(63)]
healthMap = {'Dwarf': 2, 'Gnome': 0, 'Half-Elf': 0, 'Human': 1}
speedMap = {'Dwarf': 25, 'Gnome': 25, 'Half-Elf': 30, 'Human': 30}


weapon1Map = {'guard'   : ['pike','shortsword'], 
              'hunter'  : ['short bow','sling','torch'], 
              'artisan' : ['pin roller','light hammer','soup ladle'],
              'farmer'  : ['hand axe','club','sickle','torch'],
             }

weapon2Map = {'guard': ['','dagger'],
             'hunter': ['','dagger'],
             }
weaponStats = { 
    #                   damage |    type        | range
    'club'          : ( '1d4',   'bludgeoning'  ,      5),
    'dagger'        : ( '1d4',   'piercing'     ,      5),
    'hand axe'      : ( '1d6',   'slashing'     ,      5),
    'light hammer'  : ( '1d4',   'bludgeoning'  ,      5),
    'sickle'        : ( '1d4',   'slashing'     ,      5),
    'pike'          : ('1d10',   'piercing'     ,      5),
    'shortsword'    : ( '1d6',   'piercing'     ,      5),
    'short bow'     : ( '1d6',   'piercing'     ,      '80/320'),
    'sling'         : ( '1d4',   'bludgeoning'  ,      '30/120')
    }

def isClub(weapon):
    return weapon in [ 'pin roller', 'soup ladle', 'torch', 'club']

def getWeaponStats(weapon):
    t = weapon
    if isClub(weapon):
        t = 'club'
    return weaponStats[t]

armorType = {'guard': {'chain shirt': 2,'breast plate':1},
             'hunter': {'leather': 3, 'hide': 1, 'no armor': 5},
             'farmer': {'no armor': 4, 'leather': 1}
                 }
armorStats = {
    'chain shirt'   : 13,
    'breast plate'  : 14,
    'leather'       : 11, 
    'hide'          : 12, 
    'no armor'      : 10,
    }

def normalizeDict(d):
    n = sum(d.values())
    x = {}
    for k in d.keys():
        x[k] = d[k]/n
    return x

def countOccupations(arr):
    d = {}
    for a in arr:
        if a.occupation in d:
            d[a.occupation] = d[a.occupation] + 1
        else:
            d[a.occupation] = 1
    print('Occupation Demographics:')
    for key in list(d.keys()): 
        print("\t",key, ":", d[key])  
        
def countRace(arr):
    d = {}
    for a in arr:
        if a.race in d:
            d[a.race] = d[a.race] + 1
        else:
            d[a.race] = 1
    print('Racial Demographics:')
    for key in list(d.keys()): 
        print("\t",key, ":", d[key])  
        
occupationDict = normalizeDict(occupationDict)
raceDict = normalizeDict(raceDict)
    
class character():
    def __init__(self, n=''):
        self.name = n
        self.occupation = 'peasant'
        self.ac = -1
        self.speed = 30
        self.armor = 'no armor'
        self.weapon1 = {}
        self.weapon2 = {}
        self.race = 'human'
        self.hp = 7
        self.level = 1 
        self.proficiency = 2
        
    def setLevel(self):
        self.level = random.choices([1,2],weights=[8,1], k=1)[0]
    def setSpeed(self):
        self.speed = speedMap[self.race]
    def setAC(self):
        self.ac = armorStats[self.armor]
        
    def drawHealth(self):
        self.hp = self.hp + healthMap[self.race] + random.randrange(-1,3) + self.level
    def drawProficiency(self):
        self.proficiency = self.proficiency + random.randrange(-1,2)

    def drawOccupation(self):
       self.occupation = random.choices(list(occupationDict.keys()),
                                        weights=list(occupationDict.values()),
                                        k=1)[0]
    def drawRace(self):
       self.race = random.choices(list(raceDict.keys()),
                                        weights=list(raceDict.values()),
                                        k=1)[0]
    
    def drawArmor(self):
        if self.occupation in list(armorType.keys()):
            armorAvailable = armorType[self.occupation]
            self.armor = random.choices(list(armorAvailable.keys()),
                                             weights=list(armorAvailable.values()),
                                             k=1)[0]
    
    def setWeapon(self):
        if self.occupation in list(weapon1Map.keys()):
            self.weapon1['name'] = random.choice(weapon1Map[self.occupation])
            if self.weapon1['name'] != '':
                self.weapon1['damage'],self.weapon1['type'],self.weapon1['range (ft)'] = getWeaponStats(self.weapon1['name'])
        if self.occupation in list(weapon2Map.keys()):
            self.weapon2['name'] = random.choice(weapon2Map[self.occupation])
            if self.weapon2['name'] != '':
                self.weapon2['damage'],self.weapon2['type'],self.weapon2['range (ft)'] = getWeaponStats(self.weapon2['name'])
            
    def reprWeapon(self):
        if self.weapon2:
            w2Name = self.weapon2['name']
            s1 = f', {w2Name}'
        else:
            s1 = ''
        s2 = f', {self.armor}' if self.armor else ''
        w1Name = self.weapon1['name']
        return f'\n\tWeapons: {w1Name}' +s1 +s2
    
    def reprCharacteristics(self):
        return f'\n\tCharacteristics: {self.race} - {self.occupation}'
    
    def reprStats(self):
        s1 = f'\t\tLevel: {self.level}'
        s2 = f'\t\tHP: {self.hitpoints}'
        return '\n'+'\n'.join([s1,s2])
    
    def __repr__(self):
        #f'{self.name} ({self.race})\n\tHP: {self.hitpoints}\n\tArmor: {self.armor}\n\tLevel: {self.level}\n\tOccupation: {self.occupation}'
        
        s1 = f'{self.name}'
        s1 += self.reprCharacteristics()
        s1 += self.reprWeapon()
        s1 += self.reprStats()
        return s1 + '\n'
        
characters = []
for name in names:
    newCharacter = character(name)
    newCharacter.drawOccupation()
    newCharacter.drawRace()
    newCharacter.setLevel()
    newCharacter.setSpeed()
    newCharacter.drawHealth()
    newCharacter.drawArmor()
    newCharacter.setAC()
    newCharacter.setWeapon()
    characters.append(newCharacter)
    
tim = character('name: ')
tim.occupation = 'druid'
tim.race = 'Boar'
tim.level = 2
tim.speed = 40
tim.hp = 11
tim.ac = 11
tim.proficiency = 3
tim.weapon1 = {'name': 'tusk', 'range': 5, 'damage': '1d6+1', 'type': 'slashing'}
tim.weapon2 = {'name': 'attributes', 'charge': 'see PHB', 'relentless': 'see PHB'}
characters.append(tim)



#x = [print(c) for c in characters]
charactersWithWeapons = [c for c in characters if c.weapon1 != {}]
charactersWithArmor = [c for c in characters if c.armor != 'no armor']
print(f'Total number of Characters: {len(characters)}')
print(f'Characters with Weapons: {len(charactersWithWeapons)}')
print(f'Characters with Armor: {len(charactersWithArmor)}')
countOccupations(characters)
countRace(characters)

f = open('.\Characters.json','w')
f.write('{\n\t"characters": [')
for i,c in enumerate(characters):
    f.write('\t\t')
    f.write(json.dumps(c.__dict__))
    if i != len(characters)-1:
        f.write(',')
    f.write('\n')
    
f.write('\t]\n}')
f.close()


