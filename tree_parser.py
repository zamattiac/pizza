import sys
filename = sys.argv[1]
# Output file
o = 'o' in sys.argv or '-o' in sys.argv

current = None

class MemoryArray(object):
    def __init__(self):
        self.array = []
        self.index = 0

    def increment(self):
        self.index += 1

    def reset(self):
        self.index = 0

    def deliver(self):
        return self.array[self.index]

arrays = {'cheese': MemoryArray()}


class Parser(object):
    def __init__(self):
        self.commands = []
        self.body = None

    def parse_outer_scope(self):
        in_block = False
        for line in self.body.split('\n'):
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
    def __init__(self):
        super(MainFileParser, self).__init__()
        with open(filename) as f:
            self.body = f.read().split('comeinwereopen')[1].split('sorrywereclosed')[0]
            self.body = self.body.replace('\n\n', '')
            f.close()
        self.parse_outer_scope()

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
        self.keyword = self.statement[0]
        if len(self.statement) == 1:
            quick_keys = {
                'extra': arrays.get('cheese').increment(),
                'holdthe': arrays.get('cheese').reset(),
            }
            quick_keys.get(self.keyword)
        keywords = {
            'toppings': self.handle_toppings(),
            'deliver': self.deliver(),
            'ooze': self.ooze(),
        }
        if self.keyword in keywords:
            keywords.get(self.keyword)

    def deliver(self):
        return
    def handle_toppings(self):
        return


    def run(self):
        print(self.statement)


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


if __name__ == '__main__':
    m = MainFileParser()
    m.run()