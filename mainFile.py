__author__ = 'Hexa'

import json
import Modifier
import random

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

#TODO: Break down the function into more managable components
#TODO: Add influences (making it so that some mods are more likely), this will play into delve crafting
#TODO: Add essences (Predetermined mod)
#TODO: Make item reusable (so that item changing can be done through script)
#TODO: Add spell gem slots, 3 types (possibly color coded) with some random number of sockets, possibly between 3 and 6 (maybe copy the way it is in game)

def getRandomMod(modList=[]):
	if len(modList) != 0:
		return modList.pop(random.randint(0, len(modList)-1))

def decideTier(level=1):
	if level<5:
		return 1
	elif level<10:
		return 2
	elif level<15:
		return 3
	else:
		return 4

def generateXFixNumbers(rareItem=True):
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

def makeItem(preffixes = 0, suffixes=0, itemType=0, tier=1, strItemType = 'SWORDS'):
	[prefixList, affixList] = loadXFixes(itemType)
	modDescriptions = getName(strItemType.upper())+ "\nA " + typeDict[itemType] + " that grants: \n"
	modDescriptions += generateDescription(prefixList, tier, preffixes)
	modDescriptions += generateDescription(affixList, tier, suffixes)
	
	return modDescriptions

def getName(strItemType = 'SWORDS'):
    with open('names.json') as json_file:
        data = json.load(json_file)
        genericList = data['NAMES']['GENERIC']
        specificList = data['NAMES'][strItemType]
        fullName = generateName(genericList)+" "+ generateName(specificList)
    return fullName

def generateName(NameList):
    return NameList[random.randint(0,len(NameList)-1)]

def loadXFixes(itemType):
	with open('modifiers.json', 'r') as infile:
		data = json.load(infile)
		prefixDict = data['PREFFIXES']
		affixDict = data['AFFIXES']
	return [filterTypeAndConvertToList(itemType,prefixDict), filterTypeAndConvertToList(itemType,affixDict)]

def generateDescription(xfixList, tier, Range):
	"""
	Generates the description from the given xfix list, tier and number of modifiers
	"""
	modDescriptions = ""
	for _xfix in range(Range):
		dictionary = getRandomMod(xfixList)[tier-1]
		modDescriptions += dictionary['DESC'].format(random.randint(dictionary['MIN'], dictionary['MAX'])) + '\n'
	return modDescriptions
	
def filterTypeAndConvertToList(itemType, modifierDict):
	"""
	Converts the read dict into a list, removing the keys and filtering out the modifiers that do not apply
	"""
	returnList = []
	for _key, value in modifierDict.items() :
		if isinstance(value[0], dict) and itemType in value[0]['POSSIBLE_ITEMS']:
			returnList.append(value)
	return returnList

# strItemType can be
# Armors: BODYS, BOOTS, GLOVES, HELMETS, PANTS, OTHER_SHIELDS
# Weapons: AXES, BOWS, CLAWS, DAGGERS, MACES, SCEPTRES, STAVES, SWORDS, WANDS
# Misc: AMULETS,BELTS, QUIVERS, RINGS, SPIRIT_SHIELDS
def main():
	equipment = open('equipmentFile', 'w')
	modNumberList = generateXFixNumbers(True) #first entry [0] is for preffixes, second entry [1] is for affixes/suffixes

	equipment.write(makeItem(preffixes=modNumberList[0], suffixes=modNumberList[1], itemType=tWeapon, tier=decideTier(level=5),strItemType = 'SWORDS'))

if __name__ == "__main__":
	main()