__author__ = 'Hexa'

import json
import Modifier
import random

def getRandomMod(modList=[]):
	if len(modList) != 0:
		return modList.pop(random.randint(0, len(modList)-1))

tHead = 0
tGloves = 1
tBelt = 2
tPants = 3
tShoes = 4
tNecklace = 5
tRing = 6
tWeapon = 7
tChest = 8

typeDict = {
	0: "Headpiece",
	1: "pair of Gloves",
	2: "Belt",
	3: "pair of Pants",
	4: "pair of Shoes",
	5: "Necklace",
	6: "Ring",
	7: "Weapon",
	8: "Chest"
}

magicItemModNumber = 2
rareItemModNumber = 3

def decideTier(level=1):
	if level<5:
		return 1
	elif level<10:
		return 2
	elif level<15:
		return 3
	else:
		return 4

def generateXFixes(rareItem=True):
	#Magic items have one affix and one prefix, can have 2 of one type if the other is 0
	#rare items have between 1 and 3 of each with a minimum total of 3, changing this to 2 - 3
	modList = []
	if rareItem:
		modList.append(random.randint(2,3))
		modList.append(random.randint(2,3))
	else:
		modList.append(random.randint(0,2))
		if modList[0]==2:
			modList.append(0)
		elif modList[0]==0:
			modList.append(random.randint(0,2))
		else:
			modList.append(random.randint(0,1))
	return modList

#TODO: Break down the function into more managable components
#TODO: Add influences (making it so that some mods are more likely), this will play into delve crafting
#TODO: Add essences (Predetermined mod)
#TODO: Make item reusable (so that item changing can be done through script)
def makeItem(preffixes = 0, suffixes=0, itemType=0, tier=1):
	with open('datafile', 'r') as infile:
		jsonData = json.load(infile)
		accumulateList = []
		prefixList = []
		affixList = []
		for key, value in jsonData.items():
			if isinstance(value[0], dict):
				accumulateList.append(value)
				if value[0]['ISPREFIX']:
					prefixList.append(value)
				else:
					affixList.append(value)
		if len(accumulateList)!= (len(prefixList)+len(affixList)):
			print("Loading did not go well, please debug")
		else:
			accumulateList = None #Clearing unused variables
			modDescriptions = "A " + typeDict[itemType] + " that grants: \n"
			for prefixes in range(preffixes):
				dictionary = {}
				while True:
					tempList = getRandomMod(prefixList)
					tempDict = tempList[tier-1]
					if itemType in tempDict['POSSIBLE_ITEMS']:
						dictionary = tempDict
						break
				modDescriptions += dictionary['DESC'].format(random.randint(dictionary['MIN'], dictionary['MAX'])) + '\n'
			for affixes in range(suffixes):
				dictionary = {}
				while True:
					tempList = getRandomMod(affixList)
					tempDict = tempList[tier-1]
					if itemType in tempDict['POSSIBLE_ITEMS']:
						dictionary = tempDict
						break
				randomNumber=random.randint(dictionary['MIN'], dictionary['MAX'])
				modDescriptions += dictionary['DESC'].format(randomNumber) + '\n'

			return modDescriptions


def main():
	equipment = open('equipmentFile', 'w')
	modNumberList = generateXFixes(True)#first entry [0] is for preffixes, second entry [1] is for affixes/suffixes
	equipment.write(makeItem(preffixes=modNumberList[0], suffixes=modNumberList[1], itemType=tWeapon, tier=decideTier(level=3)))

if __name__ == "__main__":
	main()
