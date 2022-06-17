__author__ = 'Hexa'


class Mod:
    def __init__(self, min=0, max=0, desc="Default description.", possible_items=None, prefix=True):
        self._min = min
        self._max = max
        self._description = desc
        self._possibleItems = possible_items
        self._isPrefix = prefix
        self._tier = 1

    @property
    def mid(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def description(self):
        return self._description

    @property
    def possibleItems(self):
        return self._possibleItems

    @property
    def prefix(self):
        return self._isPrefix

    @property
    def tier(self):
        return self._tier

    def getObjForJson(self):
        data = {
            'MIN': self._min,
            'MAX': self._max,
            'DESC': self._description,
            'POSSIBLE_ITEMS': self._possibleItems,
            'ISPREFIX': self._isPrefix}
        return data
