import paho.mqtt.client as mqtt
import random

broker = "localhost"
client = mqtt.Client()

def connectToBroker():
    client.connect(broker)
    client.on_message = processMessage
    client.subscribe("parking/entrace")
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

        client.publish("parking/info", str(option))


def run_receiver():
    connectToBroker()
    disconnectFromBroker()


if __name__ == '__main__':
    run_receiver()