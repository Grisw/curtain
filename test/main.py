import app
import time

behaviors = {}

# Load behaviors
for behavior in app.behaviors:
    module = __import__(f'app.{behavior}', fromlist=True)
    for cls in dir(module):
        member = getattr(module, cls)
        if issubclass(member, app.Behavior):
            assert behavior not in behaviors, f'Duplicated behaviors: {behavior}.'
            behaviors[behavior] = member()
            break
print(f'{len(behaviors)} behaviors loaded.')

_behaviors = behaviors.values()

# Start.
for behavior in _behaviors:
    behavior.start()

# Update.
while True:
    start_time = time.time()
    for behavior in _behaviors:
        behavior.update()
        for coroutine in behavior.coroutines:
            if time.time() - coroutine.yield_start_time >= coroutine.yield_delay:
                coroutine.yield_start_time = time.time()
                try:
                    coroutine.yield_delay = next(coroutine)
                except StopIteration:
                    behavior.coroutines.remove(coroutine)
    time.sleep(1 - time.time() + start_time)
