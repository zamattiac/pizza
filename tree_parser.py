from memory import *


class Parser(object):
    def __init__(self):
        self.commands = []
        self.body = None

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
            line = line.rstrip(';').split(';')
            for spot in line:
                spot = spot.strip().strip('!')
                if in_block and spot.startswith('!'):
                    block.commands.append(LineParser(spot))
                    continue
                else:
                    in_block = False
                    self.commands.append(LineParser(spot))


class MainFileParser(Parser):
    def __init__(self, filename):
        super(MainFileParser, self).__init__()
        with open(filename) as f:
            self.body = f.read().split('comeinwereopen')[1].split('sorrywereclosed')[0]
            self.body = self.body.replace('\n\n', '\n')
        self.parse_outer_scope()

    def __repr__(self):
        return "\n".join([str(command) for command in self.commands])

    def run(self):
        for command in self.commands:
            command.run()


class KneadFileParser(Parser):
    def __init__(self, fname):
        super(KneadFileParser, self).__init__()
        with open(fname) as f:
            pass


class LineParser:
    def __init__(self, statement):
        self.statement = statement.split(' ')
        self.statement = [self.parse_delivery(x) for x in self.statement]
        self.keyword = self.statement[0]

    def __repr__(self):
        return self.keyword + ":" + ", ".join(self.statement[1:])

    def parse_delivery(self, word):
        if 'delivery' in word:
            if not word.replace('-delivery', ''):
                return arrays.get(word.replace('-delivery', '')).deliver()
            return arrays.get('cheese').deliver()
        return word

    def deliver(self):
        return

    def handle_toppings(self):
        for topping in self.statement:
            arrays[topping] = MemoryArray()

    def ooze(self):
        print(" ".join(self.statement[1:]))

    def run(self):
        if len(self.statement) == 1:
            quick_keys = {
                'extra': arrays.get('cheese').increment(),
                'holdthe': arrays.get('cheese').reset(),
            }
            quick_keys.get(self.keyword)
            return
        self.keywords = {
            'toppings': self.handle_toppings(),
            'delivery': self.deliver(),
            'ooze': self.ooze(),
            'extra': arrays.get(self.statement[1]).increment(),
            'holdthe': arrays.get(self.statement[1]).reset()
        }
        if self.keyword in self.keywords:
            self.keywords.get(self.keyword)


class ConditionNode:
    def __init__(self, statement):
        # self.type
    #     self.evaluate()
        self.commands = []

    def evaluate(self):
        pass

    def run(self):
        for command in self.commands:
            command.run()