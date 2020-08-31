from machine import I2C, Pin, lightsleep
from pca9685 import Servos
import settings
from umqtt import MQTTClient
import json


def main(led_pin):
    i2c = I2C(-1, scl=Pin(5), sda=Pin(4))
    pca = Servos(i2c, min_us=500, max_us=2500)

    def domoticz_out(topic, msg):
        data = json.loads(msg)
        if data['idx'] == settings.CURTAIN_IDX:
            if data['nvalue'] == 1:
                pca.position(0, us=500)
            else:
                pca.position(0, us=1500)

    mqtt = MQTTClient(settings.CLIENT_ID, settings.MQTT_SERVER, user=settings.MQTT_USER, password=settings.MQTT_PASSWD)
    mqtt.set_callback(domoticz_out)
    mqtt.connect()
    mqtt.subscribe(settings.SUB_TOPIC)
    print('Connected to {}, subscribed to {} topic'.format(settings.MQTT_SERVER, settings.SUB_TOPIC))

    while True:
        led_pin.value(0)
        mqtt.check_msg()
        lightsleep(100)
        led_pin.value(1)
        lightsleep(1000)
