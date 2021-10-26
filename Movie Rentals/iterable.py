
class Iterable:
    class Iterator():
        def __init__(self,data):
            self._data = data
            self._pos = 0

        def __next__(self):
            if self._pos == len(self._data._list):
                raise StopIteration()
            self._pos += 1
            return self._data._list[self._pos - 1]

    def __init__(self):
        self._list = []

    def __iter__(self):
        return self.Iterator(self)


    def __delitem__(self, item):
        self._list.remove(item)

    def append(self,item):
        self._list.append(item)

    def __len__(self):
        return len(self._list)

    def __setitem__(self, key, value):
       self._list[key] = value

    def __getitem__(self, item):
        return self._list[item]


def combSort(list, sort_type):
    '''
    Comb Sort is mainly an improvement over Bubble Sort. Bubble sort always compares adjacent values.
    So all inversions are removed one by one. Comb Sort improves on Bubble Sort by using gap of size more than 1.
    The gap starts with a large value and shrinks by a factor of 1.3 in every iteration until it reaches the value 1.
    Thus Comb Sort removes more than one inversion counts with one swap and performs better than Bubble Sort.
    '''

    n = len(list)
    gap = n
    swapped = True

    while gap != 1 or swapped == 1:

        gap = int(gap / 1.3)
        if gap <= 1:
            gap = 1
        swapped = False

        for i in range(0, n - gap):
            if sort_type(list[i],list[i + gap]):
                list[i], list[i + gap] = list[i + gap], list[i]
                swapped = True
    return list

def filter(list, filter_type):
    filtered_list = []
    for item in list:
        if filter_type(item):
            filtered_list.append(item)

    return filtered_list
