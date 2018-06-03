import logging
import json
import os

import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import RPi.GPIO as gpio

switch_name = os.getenv('SWITCH_NAME', 'test01')
host = os.getenv('MQTT_HOST', 'nas.home')
pin = int(os.getenv('GPIO_PIN', '40'))
invert_logic = False if os.getenv('INVERT_LOGIC', 'False') == 'False' else True

entity_topic = 'home/switch/' + switch_name
command_topic = entity_topic + '/command'
config_topic = entity_topic + '/config'
state_topic = entity_topic + '/state'

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)
logger.info('entity topic: %s', entity_topic)


def setup_rpi_gpio():
    logger.info('seting up rpi gpio for pin: %s', str(pin))
    gpio.setmode(gpio.BOARD)
    gpio.setup(pin, gpio.OUT)


def turn_on():
    logger.info('turning %s on', switch_name)
    gpio.output(pin, True if not invert_logic else False)
    report_state()


def turn_off():
    logger.info('turning %s off', switch_name)
    gpio.output(pin, False if not invert_logic else True)
    report_state()


def report_state():
    pin_state = True if gpio.input(pin) else False
    if invert_logic:
        rst = not pin_state
    else:
        rst = pin_state
    on_off = 'on' if rst else 'off'
    logger.info('state: %s', on_off)
    publish.single(state_topic, payload=on_off,
                   hostname=host, retain=True)


def turn_switch(cmd):
    if cmd == 'on':
        turn_on()
    else:
        turn_off()


def on_new_command(client, userdata, msg):
    cmd = msg.payload.decode('utf-8')
    logger.info('get new command: %s from topic: %s', cmd, msg.topic)
    turn_switch(cmd)


if __name__ == '__main__':
    setup_rpi_gpio()
    conf = {"name": switch_name, "command_topic": command_topic,
            "payload_on": "on", "payload_off": "off", "optimistic": False,
            "retain": True}
    publish.single(config_topic, payload=json.dumps(conf), hostname=host,
                   retain=True)
    subscribe.callback(on_new_command, command_topic, hostname=host)

