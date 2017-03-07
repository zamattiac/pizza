from copy import copy

from memory import *
from error import *


def parse_replacements(word):
    if type(word) != str: return word
    if 'takeorder' in word:
        return input(word.replace('takeorder-', '') + '- ')

    if 'delivery' in word:
        pair = arrays.get(word.replace('-delivery', ''), arrays.get('cheese')).deliver()
        if pair[0] == 'thincrust':
            return int(pair[1])
        elif pair[0] == 'thickcrust':
            return float(pair[1])
        return str(pair[1])
    return word


class Parser(object):
    def __init__(self):
        self.commands = []
        self.body = None

    def verify_kosher(self):
        treif_words = ['peppero', 'ham', 'mushr']
        [BurntPizzaError('this program is not kosher.') for word in treif_words if word in self.body]

    def parse_outer_scope(self):
        in_block = False
        for line in self.body.split('\n'):
            if line == '':
                continue
            if line.startswith('|>') or line.startswith('#'):
                continue
            if '?' in line:
                block = ConditionNode(line)
                self.commands.append(block)
                in_block = True
                continue
            elif ':' in line:
                block = LoopNode(line)
                self.commands.append(block)
                in_block = True
                continue
            line = line.rstrip(';').split(';')
            for spot in line:
                spot = spot.strip()
                if in_block and spot.startswith('!'):
                    block.commands.append(LineParser(spot.strip('!')))
                    continue
                else:
                    in_block = False
                    self.commands.append(LineParser(spot))

    def run(self):
        for command in self.commands:
            command.run()


class MainFileParser(Parser):
    def __init__(self, filename):
        super(MainFileParser, self).__init__()
        with open(filename) as f:
            self.body = f.read().split('comeinwereopen')[1].split('sorrywereclosed')[0]
            if not self.body:
                k = KneadFileParser(filename)
                k.run()
                return
            self.body = self.body.replace('\n\n', '\n').replace('digiornos ', '')
            self.verify_kosher()
        self.parse_outer_scope()

    def __repr__(self):
        return "\n".join([str(command) for command in self.commands])


class KneadFileParser(Parser):
    def __init__(self, fname):
        self.fname = fname
        super(KneadFileParser, self).__init__()
        with open(fname) as f:
            self.body = f.read().split('sorrywereclosed')[1]
            self.body = self.body.replace('\n\n', '\n').replace('digiornos ', '')
        self.verify_kosher()
        self.parse_outer_scope()

    def __repr__(self):
        return "KNEAD {}:\n\t".format(self.fname) + "\n\t".join([str(command) for command in self.commands])


class LineParser:
    def __init__(self, statement):
        self.statement = statement.split(' ')
        self.keyword = self.statement[0]
        if self.keyword == 'knead':
            self.kneaded = KneadFileParser(self.statement[1] + '.pz')

    def __repr__(self):
        if self.keyword == 'knead':
            return str(self.kneaded)
        return self.keyword + ":" + ", ".join(str(x) for x in self.statement[1:])

    def deliver(self):
        pass

    def handle_toppings(self):
        for topping in self.statement[1:]:
            arrays[topping] = MemoryArray()

    def ooze(self):
        print(" ".join([str(x) for x in self.statement[1:]]))

    def array_increment(self):
        arrays.get(self.statement[1], NullArray(self.statement[1])).increment()

    def array_reset(self):
        arrays.get(self.statement[1], NullArray(self.statement[1])).reset()

    def set_var(self):
        memory_array = 'cheese'
        var_type = self.statement[1].split('-')
        if len(var_type) > 1:
            memory_array = var_type[0]
            var_type = var_type[1]
        else:
            var_type = var_type[0]
        arrays.get(memory_array, NullArray(memory_array)).set(var_type, " ".join(self.statement[2:]))

    def knead(self):
        self.kneaded.run()

    def default(self):
        ColdPizzaError('Keyword `{}` not found'.format(self.keyword))

    def run(self):
        self.statement = [parse_replacements(x) for x in self.statement]

        if len(self.statement) == 1:
            quick_keys = {
                'extra': arrays.get('cheese').increment(),
                'holdthe': arrays.get('cheese').reset(),
            }
            quick_keys.get(self.keyword)
            return

        keywords = {
            'toppings': self.handle_toppings,
            'delivery': self.deliver,
            'ooze': self.ooze,
            'extra': self.array_increment,
            'holdthe': self.array_reset,
            'lemmegeta': self.set_var,
            'knead': self.knead,
        }
        keywords.get(self.keyword, self.default)()


class ConditionNode:
    def __init__(self, statement):
        self.statement = statement.lstrip('yougotta ').rstrip('?').split(' ')
        self.commands = []

    def __repr__(self):
        return '?: {}\n\t'.format(' '.join(self.statement)) + '\n\t'.join([str(x) for x in self.commands])

    def evaluate(self):
        if len(self.statement) == 1:
            return self.statement[0] != 'pizza'

        if self.statement[1] == 'cheaperthan':
            return self.statement[0] < self.statement[2]

        if self.statement[1] == 'samepriceas':
            return self.statement[0] == self.statement[2]

    def run(self):
        self.statement = [parse_replacements(x) for x in self.statement]
        self.acceptable = self.evaluate()
        if self.acceptable:
            for command in self.commands:
                command.run()


class LoopNode:
    def __init__(self, statement):
        self.statement = statement.lstrip('gimme ').rstrip(':')
        self.commands = []

    def __repr__(self):
        return 'loop: {}\n\t'.format(self.statement) + '\n\t'.join([str(x) for x in self.commands])

    def iterable(self):
        self.statement = parse_replacements(self.statement)
        if type(self.statement) != tuple:
            return arrays.get(self.statement, self.statement)
        if type(self.statement) == int:
            return range(self.statement)
        elif type(self.statement) == str:
            return str(self.statement[0][1])
        else:
            ColdPizzaError('`{}` non-iterable'.format(self.statement))
            return 'PIZZA'

    def run(self):
        iterable = self.iterable()
        length = len(iterable)
        commands = [[copy(command) for x in range(length)] for command in self.commands]
        n = 0
        for i in iterable:
            if n < length:
                for command in commands:
                    # runs out of index
                    command[n].run()
                    n += 1