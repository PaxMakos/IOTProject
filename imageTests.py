from PIL import Image, ImageDraw, ImageFont

width = 96
height = 64

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

if __name__ == '__main__':
    welcomeMessage()
    goodbyeMessage()
    secondEntranceMessage()
    secondExitMessage()
    errorMessage()
    payMessage()