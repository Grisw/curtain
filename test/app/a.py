from app import Behavior


class BB(Behavior):

    def start(self):
        print('start')
        self.start_coroutine(self.e())

    def e(self):
        yield 1
        print('a')
        yield 2
        print('b')
