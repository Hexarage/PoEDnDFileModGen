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
	"""
	print("Hey there, the types of items are as follows:")
	print("Headwear: ", tHead)
	print("Gloves: ", tGloves)
	print("Belts: ",tBelt)
	print("Pants: ", tPants)
	print("Shoes: ", tShoes)
	print("Necklaces: ", tNecklace)
	print("Rings: ", tRing)
	print("Weapons: ", tWeapon)
	print("\n\nPlease enter the rarity(1 for curruption, 2 for magic and 3 for rare), the item type and finally the level of the character.")
	rarity = int(input("Rarity?"))
	itemType = int(input("What's the item type?"))
	if itemType>7 or itemType<0:
		itemType = tWeapon
	level = int(input("What level is the character?"))
	tier = decideTier(level)
	"""
	equipment = open('equipmentFile', 'w')
	equipment.write(makeItem(3, 3, tRing, 1))

if __name__ == "__main__":
	main()
