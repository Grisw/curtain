behaviors = ['wlan', 'b']


class Behavior:

    coroutines = []

    def start(self):
        pass

    def update(self):
        pass

    def start_coroutine(self, enumerator):
        coroutine = Coroutine(enumerator)
        self.coroutines.append(coroutine)
        return coroutine


class Coroutine:

    yield_start_time = 0
    yield_delay = 0

    def __init__(self, enumerator):
        self.enumerator = enumerator

    def __next__(self):
        return next(self.enumerator)
