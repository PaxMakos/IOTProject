#Imports
from tests.config import *
from consts import *

import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

from mfrc522 import MFRC522
import neopixel
import board
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import tests.lib.oled.SSD1331 as SSD1331

#globals
pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0/32, auto_write=False)
RFID = MFRC522()
execute = True
entrance = True
client = mqtt.Client()
oled = SSD1331.SSD1331()
oled.Init()

#Connection functions
#Sends a message to the broker with the current time and the UID read
def sendToBroker(time, uid):
    global entrance

    if entrance:
        client.publish(GATE_TO_BASE_CANAL, ENTRANCE_MESSAGE_1 + time + ENTRANCE_MESSAGE_2 + str(uid))
    else:
        client.publish(GATE_TO_BASE_CANAL, EXIT_MESSAGE_1 + time + EXIT_MESSAGE_2 + str(uid))



#Connects to the broker and sends a message with the current time
def connectToBroker():
    client.connect(BROKER)
    client.publish(GATE_TO_BASE_CANAL, CONNECTED_MESSAGE + datetime.now().strftime(DATETIME_FORMAT))

    client.subscribe(BASE_TO_GATE_CANAL)
    client.on_message = processMessage

#Disconnects from the broker and sends a message with the current time
def disconnectFromBroker():
    client.publish(GATE_TO_BASE_CANAL, DISCONNECTED_MESSAGE + datetime.now().strftime(DATETIME_FORMAT))
    client.disconnect()

#Processes the message from the broker
def processMessage(client, userdata, message):
    message_decoded = str(message.payload.decode("utf-8"))
    print(message_decoded)

    if (message_decoded == WELCOME_CODE):
        welcomeMessage()
        lightUp(True)
        buzz(True)
        lightDown()

    elif (message_decoded == GOODBYE_CODE):
        goodbyeMessage()
        lightUp(True)
        buzz(True)
        lightDown()

    elif (message_decoded == SECOND_ENTRY_CODE):
        secondEntranceMessage()
        lightUp(False)
        buzz(False)
        lightDown()

    elif (message_decoded == SECOND_EXIT_CODE):
        secondExitMessage()
        lightUp(False)
        buzz(False)
        lightDown()

    elif (message_decoded == ERROR_CODE):
        errorMessage()
        lightUp(False)
        buzz(False)
        lightDown()

    elif (message_decoded == PAYMENT_CODE):
        paymentMessage()
        lightUp(False)
        buzz(False)
        lightDown()


#Buttons functions
#Red button - turns off the system
def redButtonPressed(channel):
    global execute

    lightDown()

    execute = False


#Green button - changes the entrance/exit mode
def greenButtonPressed(channel):
    global entrance

    if entrance:
        entrance = False
    else:
        entrance = True

    pixels.show()


#Buzzer functions
#Buzzes the buzzer, if readOk is True, buzzes for 0.1s, else for 0.5s
def buzz(readOk):
    GPIO.output(buzzerPin, 0)

    if readOk:
        time.sleep(0.1)
    else:
        time.sleep(0.5)

    GPIO.output(buzzerPin, 1)


#LED functions
#Turns on the LEDs, if readOk is True, turns them green, else red
def lightUp(readOk):
    if readOk:
        pixels.fill((0, 255, 0))
    else:
        pixels.fill((255, 0, 0))

    pixels.show()


#Turns off the LEDs
def lightDown():
    pixels.fill((0, 0, 0))
    pixels.show()


#RFID functions
#Reads the RFID card and returns the UID
def rfidRead():
    global execute
    global entrance
    debouncer = datetime.timestamp(datetime.now()) - DEBOUNCE_TIME

    while execute:
        (status, TagType) = RFID.MFRC522_Request(RFID.PICC_REQIDL)

        if status == RFID.MI_OK:
            if(datetime.timestamp(datetime.now()) - debouncer > DEBOUNCE_TIME):
                (status, uid) = RFID.MFRC522_Anticoll()

                if status == RFID.MI_OK:
                    timeStamp = datetime.now().strftime(DATETIME_FORMAT)
                    num = 0
                    for i in range(0, len(uid)):
                        num += uid[i] << (i*8)

                    sendToBroker(timeStamp, num)

            debouncer = datetime.timestamp(datetime.now())


#Oled functions
#Prints welcome message on the OLED
def welcomeMessage():
    image = Image.new("RGB", (oled.width, oled.height), "GREEN")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('.t/ests/lib/oled/Font.ttf', 12)

    draw.text((20, 8), "Welcome!", font=font, fill=(255, 255, 255))
    draw.text((16, 20), "Have a nice", font=font, fill=(255, 255, 255))
    draw.text((34, 32), "stay!", font=font, fill=(255, 255, 255))

    oled.ShowImage(image, 0, 0)


#Prints goodbye message on the OLED
def goodbyeMessage():
    image = Image.new("RGB", (oled.width, oled.height), "GREEN")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('./tests/lib/oled/Font.ttf', 12)

    draw.text((15, 8), "Parking Paid", font=font, fill=(255, 255, 255))
    draw.text((16, 20), "Have a nice", font=font, fill=(255, 255, 255))
    draw.text((34, 32), "day!", font=font, fill=(255, 255, 255))

    oled.ShowImage(image, 0, 0)


#Prints message to second entrance on the OLED
def secondEntranceMessage():
    image = Image.new("RGB", (oled.width, oled.height), "YELLOW")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('./tests/lib/oled/Font.ttf', 12)

    draw.text((14, 8), "Car already", font=font, fill=(0, 0, 0))
    draw.text((17, 20), "parked on", font=font, fill=(0, 0, 0))
    draw.text((22, 32), "this card", font=font, fill=(0, 0, 0))

    oled.ShowImage(image, 0, 0)


#Prints message to second exit on the OLED
def secondExitMessage():
    image = Image.new("RGB", (oled.width, oled.height), "YELLOW")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('./tests/lib/oled/Font.ttf', 12)

    draw.text((24, 8), "No car", font=font, fill=(0, 0, 0))
    draw.text((17, 20), "parked on", font=font, fill=(0, 0, 0))
    draw.text((22, 32), "this card", font=font, fill=(0, 0, 0))

    oled.ShowImage(image, 0, 0)


#Prints error message to the OLED
def errorMessage():
    image = Image.new("RGB", (oled.width, oled.height), "RED")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('./tests/lib/oled/Font.ttf', 10)

    draw.text((26, 8), "ERROR!", font=font, fill=(0, 0, 0))
    draw.text((0, 20), "Contact service", font=font, fill=(0, 0, 0))
    draw.text((18, 32), "or try again", font=font, fill=(0, 0, 0))

    oled.ShowImage(image, 0, 0)

#Prints the message on the OLED
def paymentMessage():
    image = Image.new("RGB", (oled.width, oled.height), "YELLOW")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('./tests/lib/oled/Font.ttf', 12)

    draw.text((10, 8), "Parking ticket", font=font, fill=(0, 0, 0))
    draw.text((26, 20), "unpaid!", font=font, fill=(0, 0, 0))
    draw.text((8, 32), "Go to counter!", font=font, fill=(0, 0, 0))

    oled.ShowImage(image, 0, 0)

#Setup
def setup():
    GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=redButtonPressed, bouncetime=500)
    GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=greenButtonPressed, bouncetime=500)
    connectToBroker()

    oled.clear()


#Main
def main():
    setup()
    client.loop_start()
    rfidRead()
    client.loop_stop()
    disconnectFromBroker()
    oled.clear()
    GPIO.cleanup()


if __name__ == "__main__":
    main()