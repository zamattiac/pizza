from error import *


class MemoryArray(object):
    def __init__(self):
        self.array = [('None', '')]
        self.index = 0

    def __repr__(self):
        return "Index {}".format(self.index) + str(self.array)

    def increment(self):
        self.index += 1
        if self.index == len(self.array):
            self.array.append(('None', ''))

    def reset(self):
        self.index = 0

    def deliver(self):
        if self.array[self.index][1]:
            return self.array[self.index]
        else:
            return 'WrongOrder', NullPizza('dereference a null pointer').random()

    def set(self, type, string):
        self.array[self.index] = (type, string)

arrays = {'cheese': MemoryArray()}