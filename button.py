import RPi.GPIO as GPIO
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# Raspberry Pi pin configuration:
RST = 24

GPIO.setmode(GPIO.BCM)

button_pin = 7
button_pin2 = 12

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Get display width and height.
width = disp.width
height = disp.height

# Clear display.
disp.clear()
disp.display()

# Create image buffer.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (width, height))

# Load default font.
font = ImageFont.load_default()

# Create drawing object.
draw = ImageDraw.Draw(image)

# Define text and get total width.
text = 'Taking over this text!!'
maxwidth, unused = draw.textsize(text, font=font)

counter = 0
loop = 0
loop_running = True

#risk global variables
risk_player_state = True

def button_callback(channel):
    global counter
    global loop_running
    #loop_running = False
    print(counter)
    counter += 1

#def play_chess():

#def risk_button_callback():

def get_risk_first_player():
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text(((width/3)+3, height/4), "First", font=font, fill=255)
    draw.text((width/3, height/2), "Player?", font=font, fill=255)
    draw.text((width/3, 3*(height/4)), "<    >", font=font, fill=255)
    disp.image(image)
    disp.display()
    return_player = -1
    
    while True:
        if GPIO.input(button_pin) == 0:
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            return_player = 1
            break
        if GPIO.input(button_pin2) == 0:
            return_player = 2
            break
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    if return_player == 1:
        draw.text((width/3, height/4), "Player 1", font=font, fill=255)
        draw.text((width/3, height/2), "Selected", font=font, fill=255)
    elif return_player == 2:
        draw.text((width/3, height/4), "Player 2", font=font, fill=255)
        draw.text((width/3, height/2), "Selected", font=font, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(2)
    disp.clear()
    disp.display()
    time.sleep(.5)
    
    return return_player
    

def play_risk():
    # Clear image buffer by drawing a black filled box.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((width/3, height/4), "loading", font=font, fill=255)
    draw.text((width/3, height/2), "Risk...", font=font, fill=255)
    # Draw the image buffer.
    disp.image(image)
    disp.display()
    
    GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=500)
    time.sleep(2)
    GPIO.add_event_detect(button_pin2, GPIO.FALLING, callback=button_callback, bouncetime=500)
    time.sleep(.5)
    first_player = get_risk_first_player()
    

def play_chess():
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((width/3, height/4), "Chess Not", font=font, fill=255)
    #draw.text((width/3, height/2), "Not", font=font, fill=255)
    draw.text((width/4, (height/2)), "Available :(", font=font, fill=255)
    # Draw the image buffer.
    disp.image(image)
    disp.display()
    time.sleep(2)
    return 0

try:
    # Clear image buffer by drawing a black filled box.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((width/3, height/3), "loading...", font=font, fill=255)
    # Draw the image buffer.
    disp.image(image)
    disp.display()
    
    while True:
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((width/3, height/4), "< Risk", font=font, fill=255)
        draw.text((width/3, 2*(height/4)), "Chess >", font=font, fill=255)
        disp.image(image)
        disp.display()
        while True:
            if GPIO.input(button_pin) == 0:
                print("button_pin clicked")
                play_chess()
            if GPIO.input(button_pin2) == 0:
                print("button_pin2 clicked")
                play_risk()
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            draw.text((width/3, height/4), "< Risk", font=font, fill=255)
            draw.text((width/3, 2*(height/4)), "Chess >", font=font, fill=255)
            disp.image(image)
            disp.display()
        print("menu screen button clicked")
        
        time.sleep(60)
        
    
except KeyboardInterrupt:
    GPIO.cleanup()

disp.clear()
disp.display()
GPIO.cleanup()
