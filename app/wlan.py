from app import Behavior
import network
import settings


class WLANBehavior(Behavior):
    disconnected_events = []
    connected_events = []
    _wlan = None
    state = False
    _reconnect_coroutine = None

    def start(self):
        self._wlan = network.WLAN(network.STA_IF)
        self._wlan.active(True)
        self._wlan.connect(settings.SSID, settings.PASSWORD)

    def update(self):
        if self.state != self._wlan.isconnected():
            self.state = self._wlan.isconnected()
            if self._wlan.isconnected():
                for e in self.connected_events:
                    e(*self._wlan.ifconfig())
            else:
                for e in self.disconnected_events:
                    e(self._wlan.status())

        if self._reconnect_coroutine is None and \
            (self._wlan.status() == network.STAT_NO_AP_FOUND or
             self._wlan.status() == network.STAT_CONNECT_FAIL or
             self._wlan.status() == network.STAT_IDLE):
            self._reconnect_coroutine = self.start_coroutine(self._reconnect())

    def _reconnect(self):
        yield 30 * 1000
        self._wlan.connect(settings.SSID, settings.PASSWORD)
        self._reconnect_coroutine = None
