# bron: Youtube, ChatGPT, Stackoverflow





from machine import Pin, I2C, PWM
from os import listdir
from ssd1306 import SSD1306_I2C
from time import sleep
import _thread
import neopixel
import urequests
import network
import socket
import random
import json
import framebuf

# wifi settings
# ssid = 'NothingRick'
# password = 'Welkom01'
#


# Wifi HBO LAB
ssid = "hbo-ict-lab-2.4GHz"
password = "hboictlab2018"

# IP Laptop LAB
pc_ip = "http://192.168.3.174:5000"
# HOME TESTING WIFI
# ssid = 'BlackMirror'

# # password = 'Interstell@r2014'
# pc_ip = "http://192.168.66.9:5000"


# PC ip for flask connection
# pc_ip = "http://192.168.77.9:5000"

# Neopixel
np = neopixel.NeoPixel(machine.Pin(13), 8)

# RGB
Led_R = PWM(Pin(22))
Led_G = PWM(Pin(27))
Led_B = PWM(Pin(28))
# Define the frequency
Led_R.freq(2000)
Led_G.freq(2000)
Led_B.freq(2000)

# I2C variables
id = 0
sda = Pin(0)
scl = Pin(1)
i2c = I2C(id=id, scl=scl, sda=sda)

# I2C variables Second Display
i2c2 = I2C(id=1, scl=Pin(11), sda=Pin(10))

# Screen Variables
width = 128
height = 64
line = 1
highlight = 1
shift = 0
list_length = 0
total_lines = 6

# create the display
oled = SSD1306_I2C(width=width, height=height, i2c=i2c)
oled.init_display()

# create the second display
oled2 = SSD1306_I2C(width=width, height=height, i2c=i2c2)
oled2.init_display()

# Setup the Rotary Encoder
button_pin = Pin(16, Pin.IN, Pin.PULL_UP)
direction_pin = Pin(17, Pin.IN, Pin.PULL_UP)
step_pin = Pin(18, Pin.IN, Pin.PULL_UP)

# setup abort button
abort_pin = Pin(14, Pin.IN, Pin.PULL_UP)

# for tracking the direction and button state
previous_value = True
button_down = False

abort = False

# Turn off leds
R = int(0)
Led_R.duty_u16(R)
G = int(0)
Led_G.duty_u16(G)
B = int(0)
Led_B.duty_u16(B)
np[0] = [0, 0, 0]
np[1] = [0, 0, 0]
np[2] = [0, 0, 0]
np[3] = [0, 0, 0]
np[4] = [0, 0, 0]
np[5] = [0, 0, 0]
np[6] = [0, 0, 0]
np[7] = [0, 0, 0]
np.write()

# create Steam Logo
# Image data (converted from Arduino-style bitmap)
image_data = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1f, 0xf8, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x01, 0xff, 0xff, 0x80, 0x00, 0x00, 0x00, 0x00, 0x0f, 0xff, 0xff, 0xf0, 0x00, 0x00,
    0x00, 0x00, 0x3f, 0xe0, 0x07, 0xfc, 0x00, 0x00, 0x00, 0x00, 0xfe, 0x00, 0x00, 0x7f, 0x00, 0x00,
    0x00, 0x01, 0xf8, 0x00, 0x00, 0x1f, 0xc0, 0x00, 0x00, 0x07, 0xe0, 0x00, 0x00, 0x07, 0xe0, 0x00,
    0x00, 0x0f, 0x80, 0x00, 0x00, 0x01, 0xf0, 0x00, 0x00, 0x1e, 0x00, 0x00, 0x00, 0x00, 0x78, 0x00,
    0x00, 0x3c, 0x00, 0x00, 0x00, 0x00, 0x3c, 0x00, 0x00, 0x78, 0x00, 0x00, 0x00, 0x00, 0x1e, 0x00,
    0x00, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x0f, 0x00, 0x01, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x07, 0x80,
    0x01, 0xc0, 0x00, 0x1f, 0xf8, 0x00, 0x03, 0xc0, 0x03, 0x80, 0x00, 0xff, 0xff, 0x00, 0x01, 0xc0,
    0x07, 0x80, 0x03, 0xff, 0xff, 0xc0, 0x01, 0xe0, 0x07, 0x00, 0x07, 0xff, 0xff, 0xe0, 0x00, 0xe0,
    0x0f, 0x00, 0x0f, 0xff, 0xff, 0xf0, 0x00, 0xf0, 0x0e, 0x00, 0x1f, 0xff, 0xff, 0xf8, 0x00, 0x70,
    0x1e, 0x00, 0x3f, 0xff, 0xf9, 0xfc, 0x00, 0x78, 0x1c, 0x00, 0x7f, 0xff, 0xc0, 0x3e, 0x00, 0x38,
    0x1c, 0x00, 0xff, 0xff, 0x80, 0x1f, 0x00, 0x38, 0x38, 0x00, 0xff, 0xff, 0x1f, 0x8f, 0x00, 0x1c,
    0x38, 0x01, 0xff, 0xff, 0x30, 0xcf, 0x80, 0x1c, 0x38, 0x01, 0xff, 0xfe, 0x20, 0x47, 0x80, 0x1c,
    0x38, 0x01, 0xff, 0xfe, 0x60, 0x67, 0x80, 0x1c, 0x70, 0x03, 0xff, 0xfe, 0x60, 0x67, 0xc0, 0x0e,
    0x70, 0x03, 0xff, 0xfc, 0x20, 0x67, 0xc0, 0x0e, 0x70, 0x03, 0xff, 0xfc, 0x30, 0x47, 0xc0, 0x0e,
    0x70, 0x03, 0xff, 0xf8, 0x19, 0x8f, 0xc0, 0x0e, 0x70, 0x00, 0xff, 0xf0, 0x0f, 0x1f, 0xc0, 0x0e,
    0x70, 0x00, 0x1f, 0xf0, 0x00, 0x1f, 0xc0, 0x0e, 0x70, 0x00, 0x07, 0xe0, 0x00, 0x7f, 0xc0, 0x0e,
    0x70, 0x00, 0x00, 0x00, 0x07, 0xff, 0xc0, 0x0e, 0x70, 0x00, 0x00, 0x30, 0x0f, 0xff, 0xc0, 0x0e,
    0x70, 0x00, 0x00, 0x0c, 0x1f, 0xff, 0xc0, 0x0e, 0x38, 0x01, 0x00, 0x04, 0x7f, 0xff, 0x80, 0x1c,
    0x38, 0x01, 0xc0, 0x04, 0xff, 0xff, 0x80, 0x1c, 0x38, 0x01, 0xf0, 0x04, 0xff, 0xff, 0x80, 0x1c,
    0x38, 0x00, 0xfc, 0x05, 0xff, 0xff, 0x00, 0x1c, 0x1c, 0x00, 0xfc, 0xd9, 0xff, 0xff, 0x00, 0x38,
    0x1c, 0x00, 0x7e, 0x73, 0xff, 0xfe, 0x00, 0x38, 0x1e, 0x00, 0x3f, 0x07, 0xff, 0xfc, 0x00, 0x78,
    0x0e, 0x00, 0x1f, 0xff, 0xff, 0xf8, 0x00, 0x70, 0x0f, 0x00, 0x0f, 0xff, 0xff, 0xf0, 0x00, 0xf0,
    0x07, 0x00, 0x07, 0xff, 0xff, 0xe0, 0x00, 0xe0, 0x07, 0x80, 0x03, 0xff, 0xff, 0xc0, 0x01, 0xe0,
    0x03, 0x80, 0x00, 0xff, 0xff, 0x00, 0x01, 0xc0, 0x01, 0xc0, 0x00, 0x1f, 0xf8, 0x00, 0x03, 0x80,
    0x01, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x07, 0x80, 0x00, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x0f, 0x00,
    0x00, 0x78, 0x00, 0x00, 0x00, 0x00, 0x1e, 0x00, 0x00, 0x3c, 0x00, 0x00, 0x00, 0x00, 0x3c, 0x00,
    0x00, 0x1e, 0x00, 0x00, 0x00, 0x00, 0x78, 0x00, 0x00, 0x0f, 0x80, 0x00, 0x00, 0x01, 0xf0, 0x00,
    0x00, 0x07, 0xe0, 0x00, 0x00, 0x07, 0xe0, 0x00, 0x00, 0x01, 0xf8, 0x00, 0x00, 0x1f, 0x80, 0x00,
    0x00, 0x00, 0xfe, 0x00, 0x00, 0x7f, 0x00, 0x00, 0x00, 0x00, 0x3f, 0xe0, 0x07, 0xfc, 0x00, 0x00,
    0x00, 0x00, 0x0f, 0xff, 0xff, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x01, 0xff, 0xff, 0x80, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x1f, 0xf8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
]

# define screen size
image_width = 64
image_height = 64

# Calculate the starting position to center the image
start_x = (width - image_width) // 2
start_y = (height - image_height) // 2

# Create a frame buffer with the image dimensions
fbuf = framebuf.FrameBuffer(bytearray(image_data), image_width, image_height, framebuf.MONO_HLSB)

# Clear the display before blitting the image
oled2.fill(0)

# Blit the image onto the display at the calculated starting position
oled2.blit(fbuf, start_x, start_y)

# Center the text
text = "STEAMPROJECT"
text_width = len(text) * 8  # Assuming 8 pixels width for each character
text_x = (width - text_width) // 2
oled.text(text, text_x, 0)
text2 = "PuntKomma"
text2_width = len(text2) * 8  # Assuming 8 pixels width for each character
text2_x = (width - text2_width) // 2
oled.text(text2, text2_x, 20)

# Update the display
oled.show()
oled2.show()
sleep(3)
oled2.fill_rect(0, 0, 128, 64, 0)
oled2.show()
oled.fill_rect(0, 0, 128, 64, 0)
oled.show()


# Connect to the internet
def connect():
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        oled.fill_rect(0, 0, 128, 64, 0)
        oled.show()
        oled.text("Waiting for", 0, 20)
        oled.text("connection.", 0, 30)
        oled.show()
        print('Waiting for connection...')
        sleep(1)
        oled.fill_rect(0, 0, 128, 64, 0)
        oled.show()
        oled.text("Waiting for", 0, 20)
        oled.text("connection..", 0, 30)
        oled.show()
        print('Waiting for connection...')
        sleep(1)
        oled.fill_rect(0, 0, 128, 64, 0)
        oled.show()
        oled.text("Waiting for", 0, 20)
        oled.text("connection...", 0, 30)
        oled.show()
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}     =====WELCOME TO THE INTERNET=====')
    oled.fill_rect(0, 0, 128, 64, 0)
    oled.show()
    oled.text("Welcome to the", 0, 20)
    oled.text("internet!", 0, 30)
    oled.show()
    sleep(1.5)
    return ip


try:
    ip = connect()
except KeyboardInterrupt:
    machine.reset()


# Programs as functions


def ApiRequestTest():
    try:
        res = urequests.post(f"{pc_ip}/test_profile/B129420016573EE260056E21D4218C90/76561198072948436").json()[0]
        print(res)
        print(res["personaname"])
    except Exception as e:
        print(f"Exception during API request: {e}")


def Rick_Mageddon():
    try:
        res = urequests.post(f"{pc_ip}/test_profile/B129420016573EE260056E21D4218C90/76561198072948436").json()[0]
        print(res)
        print(res["personaname"])
    except Exception as e:
        print(f"Exception during API request: {e}")


def CaveJohnson():
    oled2.text("If i punch those", 0, 0)
    oled2.text("numbers into my", 0, 10)
    oled2.text("calcualtor, it", 0, 20)
    oled2.text("makes an", 0, 30)
    oled2.text("happy face :D", 0, 40)
    oled2.show()


def StatusLEDTest():
    while True:
        # range of random numbers
        R = random.randint(0, 65535)
        G = random.randint(0, 65535)
        B = random.randint(0, 65535)
        print(R, G, B)
        Led_R.duty_u16(R)
        Led_G.duty_u16(G)
        Led_B.duty_u16(B)
        utime.sleep_ms(100)


def PixelTestRGB():
    global abort
    np[0] = [255, 0, 0]
    np[1] = [0, 255, 0]
    np[2] = [0, 0, 255]
    np.write()

    while not abort:
        pass

    np[0] = [0, 0, 0]
    np[1] = [0, 0, 0]
    np[2] = [0, 0, 0]
    np.write()


def loop_neopixel():
    global abort
    while not abort:
        np[7] = [255, 0, 0]
        sleep(0.1)
        np.write()
        np[6] = [255, 0, 0]
        sleep(0.1)
        np.write()
        np[5] = [255, 0, 0]
        sleep(0.1)
        np.write()
        np[4] = [255, 0, 0]
        sleep(0.1)
        np.write()
        np[3] = [255, 0, 0]
        sleep(0.1)
        np.write()
        np[2] = [255, 0, 0]
        sleep(0.1)
        np.write()
        np[1] = [255, 0, 0]
        sleep(0.1)
        np.write()
        np[0] = [255, 0, 0]
        sleep(0.1)
        np.write()
        np[0] = [0, 0, 0]
        np[1] = [0, 0, 0]
        np[2] = [0, 0, 0]
        np[3] = [0, 0, 0]
        np[4] = [0, 0, 0]
        np[5] = [0, 0, 0]
        np[6] = [0, 0, 0]
        np[7] = [0, 0, 0]

        sleep(0.1)
        np.write()

    abort = False


# Abort running process
def abort_running():
    global abort
    abort = True
    sleep(3)
    abort = False


# LAunch program
def launch(item):
    global file_list
    global abort
    global functions

    # clear the screen
    oled.fill_rect(0, 0, width, height, 0)
    oled.text("Searching", 1, 0)
    oled.text(item["name"], 1, 20)
    oled.show()

    abort_running()
    _thread.start_new_thread(item["function"], [])
    oled.fill_rect(0, 0, width, height, 0)
    oled.text("Showing", 1, 0)
    oled.text(item["name"], 1, 20)
    oled.show()


# Show Menu
def show_menuu(functions):
    # bring in the global variables
    global line, highlight, shift, list_length

    # menu variables
    item = 1
    line = 1
    line_height = 10

    # clear the display
    oled.fill_rect(0, 0, width, height, 0)

    # print(type(functions))

    for item in functions:
        if highlight == line:
            oled.fill_rect(0, (line - 1) * line_height, width, line_height, 1)
            oled.text(">", 0, (line - 1) * line_height, 0)
            oled.text(item["name"], 10, (line - 1) * line_height, 0)
            oled.show()
        else:
            oled.text(item["name"], 10, (line - 1) * line_height, 1)
            oled.show()
        line += 1
    oled.show()


# ENTER FUNTIONS HERE FOR MENU
functions = [{"name": "ApiRequestTest", "function": ApiRequestTest},
             {"name": "Rick_Mageddon", "function": Rick_Mageddon}, {"name": "PixelTestRGB", "function": PixelTestRGB},
             {"name": "CaveJohnson", "function": CaveJohnson},
             {"name": "StatusLEDTest", "function": StatusLEDTest}, {"name": "Neopixel", "function": loop_neopixel}]

# Get the list of Python files and display the menu
# file_list = get_files()
# show_menu(file_list)


show_menuu(functions)

# Rotary Encoder settings
# Repeat forever
while True:

    if previous_value != step_pin.value():
        if step_pin.value() == False:

            # Turned Left
            if direction_pin.value() == False:
                if highlight > 1:
                    highlight -= 1
                else:
                    if shift > 0:
                        shift -= 1

                        # Turned Right
            else:
                if highlight < total_lines:
                    highlight += 1
                else:
                    if shift + total_lines < list_length:
                        shift += 1

            show_menuu(functions)
        previous_value = step_pin.value()

        # Check for button pressed of encoder
    if button_pin.value() == False and not button_down:
        button_down = True

        print("Launching", functions[highlight - 1 + shift]["name"])

        # execute script
        launch(functions[highlight - 1 + shift])

        print("Running", functions[highlight - 1 + shift]["name"])

    # Decbounce button
    if button_pin.value() == True and button_down:
        button_down = False
    # Abort Button
    if not abort_pin.value():
        abort = True

        oled2.fill_rect(0, 0, 128, 64, 0)
        oled2.show()
        print("Returned from launch")
        show_menuu(functions)

#         Led_R.freq(0)
#         Led_G.freq(0)
#         Led_B.freq(0)




