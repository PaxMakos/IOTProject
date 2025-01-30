import paho.mqtt.client as mqtt
import random
from consts import *

broker = "localhost"
client = mqtt.Client()

def connectToBroker():
    client.connect(broker)
    client.on_message = processMessage
    client.subscribe(GATE_TO_BASE_CANAL)
    while client.loop() == 0:
        pass


def disconnectFromBroker():
    client.loop_stop()
    client.disconnect()


def processMessage(client, userdata, message):
    message_decoded = str(message.payload.decode("utf-8"))

    if len(message_decoded) > 1:
        print(message_decoded)
        option = random.randint(1, 6)

        client.publish(BASE_TO_GATE_CANAL, str(option))


def run_receiver():
    connectToBroker()
    disconnectFromBroker()


if __name__ == '__main__':
    run_receiver()