import sys
import webbrowser

w = 'w' in sys.argv or '-w' in sys.argv


class Error(object):
    def __init__(self, message):
        if w: print(message)


class BurntPizzaError(Error):
    def __init__(self, message):
        super(BurntPizzaError, self).__init__("UNRESOLVABLE (burnt pizza): " + message)
        if w: webbrowser.open('http://www.techrepublic.com/blog/software-engineer/10-tips-to-go-from-a-beginner-to-an-intermediate-developer/')
        sys.exit(1)


class ColdPizzaError(Error):
    def __init__(self, message):
        if message == 'dereference a null pointer' and w:
            webbrowser.open('https://youtu.be/bLHL75H_VEM')
        super(ColdPizzaError, self).__init__("RESOLVABLE (cold pizza): " + message)

    def random(self):
        pizza = 'pizza'
        return pizza