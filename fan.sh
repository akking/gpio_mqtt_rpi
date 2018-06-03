#!/bin/bash

docker build . -t switch_mqtt
docker run --name='fan' -d --restart always --privileged -e 'INVERT_LOGIC=True' -e 'GPIO_PIN=8' -e 'SWITCH_NAME=livingroom_fan' switch_mqtt
docker run --name='ac' -d --restart always --privileged -e 'INVERT_LOGIC=True' -e 'GPIO_PIN=12' -e 'SWITCH_NAME=livingroom_ac' switch_mqtt
docker run --name='heat' -d --restart always --privileged -e 'INVERT_LOGIC=True' -e 'GPIO_PIN=10' -e 'SWITCH_NAME=livingroom_heat' switch_mqtt

