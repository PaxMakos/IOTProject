from operator import truediv
import paho.mqtt.client as mqtt
import random
from consts import *
from main2 import handle_card_read

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

    message_parsed = message_decoded.split(":")
    entrance = True

    if message_parsed.__contains__(EXIT_MESSAGE_1):
        entrance = False

    handle_card_read(message_parsed[-1], entrance)
    

def run_receiver():
    connectToBroker()
    disconnectFromBroker()


if __name__ == '__main__':
    run_receiver()
    