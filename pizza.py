import sys

vars = [None]
inc = 0

current = None


def globalize():
    global begun, ended, inc


def inc_change(up=True):
    global inc
    if up:
        inc += 1
    else:
        inc = 0


def set_current():
    global current
    current = vars[inc]


class Command:
    def __init__(self, command, args):
        self.args = args[1:]
        self.command = command
        self.commands = {
            # 'extra': self.inc_change(),
            # 'holdthe': self.inc_change(False),
            # 'lemegeta': self.vars_set(),
            'ooze': self.ooze(),
            '': None,
            # 'delivery': self.set_current(),
            # 'openforbusiness': None,
            # 'sorrywereclosed': None,
        }


    # def vars_set(self):
    #     type = self.args[0]
    #     value = self.args[1]
    #     vars[inc] = value
    #     vars.append(None)

    def ooze(self):
        print(" ".join(self.args))

    def execute(self):
        self.commands[self.command]


class Block:
    def __init__(self, condition):
        self.commands = []
        self.condition = condition
        # self.commands = {
        #     # 'extra': self.inc_change(),
        #     # 'holdthe': self.inc_change(False),
        #     # 'lemegeta': self.vars_set(),
        #     'ooze': self.ooze(),
        #     # 'delivery': self.set_current(),
        #     # 'openforbusiness': None,
        #     # 'sorrywereclosed': None,
        # }


    # def vars_set(self):
    #     type = self.args[0]
    #     value = self.args[1]
    #     vars[inc] = value
    #     vars.append(None)

    # def ooze(self):
    #     print(" ".join(self.args))

    def execute(self):
        for command in self.commands:
            command.execute()



def parse_file(file):
    loop_executed = True
    f = open(file)
    main = f.read().split('comeinwereopen')[1]
    main = main.split('sorrywereclosed')[0].replace('?', ';').replace(':', ';').replace('\n', '').split(';')
    for line in main:
        if line.startswith('|>'):
            continue
        if line == '':
            continue
        keys = line.split(' ')
        if keys[0] in ['yougotta', 'theworks']:
            loop = Block(keys[1:])
            loop_executed = False
            continue
        if keys[0].startswith('\t'):
            keys[0] = keys[0].replace('\t', '')
            try:
                loop.commands.append(Command(keys[0], keys))
            except:
                print('Out of block {}'.format(line))
        elif not loop_executed:
            loop.execute()
            loop_executed = True
        parsed.append(Command(keys[0], keys))
    f.close()

if __name__ == '__main__':
    parsed = []
    parse_file(sys.argv[1])
    for parsed_line in parsed:
        parsed_line.execute()