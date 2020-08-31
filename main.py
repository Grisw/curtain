import app
import time
import settings
import machine

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
    start_time = time.ticks_ms()
    for behavior in _behaviors:
        behavior.update()
        for coroutine in behavior.coroutines:
            if time.ticks_diff(time.ticks_ms(), coroutine.yield_start_time) >= coroutine.yield_delay:
                coroutine.yield_start_time = time.ticks_ms()
                try:
                    coroutine.yield_delay = next(coroutine)
                except StopIteration:
                    behavior.coroutines.remove(coroutine)
    machine.lightsleep(settings.FPS - time.ticks_diff(time.ticks_ms(), start_time))
