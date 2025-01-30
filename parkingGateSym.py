"""
Test gate

Used only to test communication 
"""
from consts import *

import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

import paho.mqtt.client as mqtt

execute = True
entrance = True
client = mqtt.Client()

width = 96
height = 64

#Connection functions
#Sends a message to the broker with the current time and the UID read
def sendToBroker(time, uid):
    global entrance

    if entrance:
        client.publish(CONNECTION_CANAL, ENTRANCE_MESSAGE_1 + time + ENTRANCE_MESSAGE_2 + str(uid))
    else:
        client.publish(CONNECTION_CANAL, EXIT_MESSAGE_1 + time + EXIT_MESSAGE_2 + str(uid))



#Connects to the broker and sends a message with the current time
def connectToBroker():
    client.connect(BROKER)
    client.publish(CONNECTION_CANAL, CONNECTED_MESSAGE + datetime.now().strftime(DATETIME_FORMAT))

    client.subscribe("parking/info")
    client.on_message = processMessage


#Disconnects from the broker and sends a message with the current time
def disconnectFromBroker():
    client.publish(CONNECTION_CANAL, DISCONNECTED_MESSAGE + datetime.now().strftime(DATETIME_FORMAT))
    client.disconnect()

def processMessage(client, userdata, message):
    message_decoded = str(message.payload.decode("utf-8"))
    print(message_decoded)

    if(message_decoded == "1"):
        welcomeMessage()
    elif(message_decoded == "2"):
        goodbyeMessage()
    elif(message_decoded == "3"):
        secondEntranceMessage()
    elif(message_decoded == "4"):
        secondExitMessage()
    elif(message_decoded == "5"):
        errorMessage()
    elif(message_decoded == "6"):
        payMessage()

def welcomeMessage():
    image1 = Image.new("RGB", (width, height), "GREEN")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype('.venv/lib/oled/Font.ttf', 12)

    draw.text((20, 8), "Welcome!", font=font, fill=(255, 255, 255))
    draw.text((16, 20), "Have a nice", font=font, fill=(255, 255, 255))
    draw.text((34, 32), "stay!", font=font, fill=(255, 255, 255))

    image1.show()


#Prints goodbye message on the OLED
def goodbyeMessage():
    image1 = Image.new("RGB", (width, height), "GREEN")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype('.venv/lib/oled/Font.ttf', 12)

    draw.text((15, 8), "Parking Paid", font=font, fill=(255, 255, 255))
    draw.text((16, 20), "Have a nice", font=font, fill=(255, 255, 255))
    draw.text((34, 32), "day!", font=font, fill=(255, 255, 255))

    image1.show()


#Prints message to second entrance on the OLED
def secondEntranceMessage():
    image1 = Image.new("RGB", (width, height), "YELLOW")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype('.venv/lib/oled/Font.ttf', 12)

    draw.text((14, 8), "Car already", font=font, fill=(0, 0, 0))
    draw.text((17, 20), "parked on", font=font, fill=(0, 0, 0))
    draw.text((22, 32), "this card", font=font, fill=(0, 0, 0))

    image1.show()


#Prints message to second exit on the OLED
def secondExitMessage():
    image1 = Image.new("RGB", (width, height), "YELLOW")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype('.venv/lib/oled/Font.ttf', 12)

    draw.text((24, 8), "No car", font=font, fill=(0, 0, 0))
    draw.text((17, 20), "parked on", font=font, fill=(0, 0, 0))
    draw.text((22, 32), "this card", font=font, fill=(0, 0, 0))

    image1.show()


#Prints error message to the OLED
def errorMessage():
    image1 = Image.new("RGB", (width, height), "RED")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype('.venv/lib/oled/Font.ttf', 12)

    draw.text((26, 8), "ERROR!", font=font, fill=(0, 0, 0))
    draw.text((0, 20), "Contact service", font=font, fill=(0, 0, 0))
    draw.text((18, 32), "or try again", font=font, fill=(0, 0, 0))

    image1.show()

def payMessage():
    image1 = Image.new("RGB", (width, height), "YELLOW")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype('.venv/lib/oled/Font.ttf', 12)

    draw.text((10, 8), "Parking ticket", font=font, fill=(0, 0, 0))
    draw.text((26, 20), "unpaid!", font=font, fill=(0, 0, 0))
    draw.text((8, 32), "Go to counter!", font=font, fill=(0, 0, 0))

    image1.show()

def main():
    connectToBroker()
    client.loop_start()
    while execute:
        time.sleep(60)
        sendToBroker(datetime.now().strftime(DATETIME_FORMAT), 123456789)
    client.loop_stop()
    disconnectFromBroker()

if __name__ == '__main__':
    main()