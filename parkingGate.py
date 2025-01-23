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
        client.publish(CONNECTION_CANAL, ENTRANCE_MESSAGE_1 + time + ENTRANCE_MESSAGE_2 + str(uid))
    else:
        client.publish(CONNECTION_CANAL, EXIT_MESSAGE_1 + time + EXIT_MESSAGE_2 + str(uid))



#Connects to the broker and sends a message with the current time
def connectToBroker():
    client.connect(BROKER)
    client.publish(CONNECTION_CANAL, CONNECTED_MESSAGE + datetime.now().strftime(DATETIME_FORMAT))

#Disconnects from the broker and sends a message with the current time
def disconnectFromBroker():
    client.publish(CONNECTION_CANAL, DISCONNECTED_MESSAGE + datetime.now().strftime(DATETIME_FORMAT))
    client.disconnect()

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

                    lightUp(True)

                    if entrance:
                        welcomeMessage()
                    else:
                        goodbyeMessage()

                    buzz(True)
                    lightDown()

                else:
                    #errorMessage()

                    lightUp(False)
                    buzz(False)
                    lightDown()

            debouncer = datetime.timestamp(datetime.now())


#Oled functions
#Prints welcome message on the OLED
def welcomeMessage():
    image1 = Image.new("RGB", (oled.width, oled.height), "BLACK")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype('./lib/oled/Font.ttf', 10)

    draw.text((0, 0), "Welcome!", font=font, fill=(255, 255, 255))
    draw.text((0, 10), "Have a nice", font=font, fill=(255, 255, 255))
    draw.text((0, 20), "stay!", font=font, fill=(255, 255, 255))

    oled.ShowImage(image1, 0, 0)


#Prints goodbye message on the OLED
def goodbyeMessage():
    image1 = Image.new("RGB", (oled.width, oled.height), "BLACK")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype('./lib/oled/Font.ttf', 10)

    draw.text((0, 0), "Welcome!", font=font, fill=(255, 255, 255))
    draw.text((0, 10), "Have a nice", font=font, fill=(255, 255, 255))
    draw.text((0, 20), "stay!", font=font, fill=(255, 255, 255))

    oled.ShowImage(image1, 0, 0)


#Prints message to second entrance on the OLED
def secondEntranceMessage():
    image1 = Image.new("RGB", (oled.width, oled.height), "BLACK")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype('./lib/oled/Font.ttf', 10)

    draw.text((0, 0), "Welcome!", font=font, fill=(255, 255, 255))
    draw.text((0, 10), "Have a nice", font=font, fill=(255, 255, 255))
    draw.text((0, 20), "stay!", font=font, fill=(255, 255, 255))

    oled.ShowImage(image1, 0, 0)


#Prints message to second exit on the OLED
def secondExitMessage():
    image1 = Image.new("RGB", (oled.width, oled.height), "BLACK")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype('./lib/oled/Font.ttf', 10)

    draw.text((0, 0), "Welcome!", font=font, fill=(255, 255, 255))
    draw.text((0, 10), "Have a nice", font=font, fill=(255, 255, 255))
    draw.text((0, 20), "stay!", font=font, fill=(255, 255, 255))

    oled.ShowImage(image1, 0, 0)


#Prints error message to the OLED
def errorMessage():
    image1 = Image.new("RGB", (oled.width, oled.height), "BLACK")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype('./lib/oled/Font.ttf', 10)

    draw.text((0, 0), "Welcome!", font=font, fill=(255, 255, 255))
    draw.text((0, 10), "Have a nice", font=font, fill=(255, 255, 255))
    draw.text((0, 20), "stay!", font=font, fill=(255, 255, 255))

    oled.ShowImage(image1, 0, 0)


#Setup
def setup():
    GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=redButtonPressed, bouncetime=500)
    GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=greenButtonPressed, bouncetime=500)
    connectToBroker()

    oled.clear()


#Main
def main():
    setup()
    rfidRead()
    disconnectFromBroker()
    oled.clear()
    GPIO.cleanup()


if __name__ == "__main__":
    main()