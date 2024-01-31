 
Inhoud
Documentatie Code	2
Main.py	2
Bronnen	8


 
Documentatie Code
De code van het TI gedeelte van het Steam Project is compleet geschreven in Python/MicroPython. De componenten die ik heb gebruikt zijn het volgende: 1x RaspberryPi Pico W, 1x Rotary Encoder, 1x Button, 1x Neopixel, 2x OLED 128x64 I2C SSD1306, 2x prototype boards, 1x RGB led, kabels en custom made behuizing. Alle componenten zijn eerst getest op een breadboard en aan elkaar verbonden voordat alles aan elkaar gesoldeerd werd.
Main.py
Geimporteerde libraries: framebuf, json, random, socket, network, urequests, neopixel, _thread, time, ssd1306, os, machine.
Als eerst word alles aangeroepen en krijgt alles zn instellingen. Als voorbeeld:
#LAB TESTING WIFI
ssid = "hbo-ict-lab-2.4GHz"
password = "***********"

De Neopixel en de RGB krijgen hun pins die nodig zijn, en voor de RGB led de frequentie:

# Neopixel
np = neopixel.NeoPixel(machine.Pin(13), 8)

#RGB
Led_R = PWM(Pin(22))
Led_G = PWM(Pin(27))
Led_B = PWM(Pin(28))
# Define the frequency
Led_R.freq(2000)
Led_G.freq(2000)
Led_B.freq(2000)

Wifi word als eerst aangeroepen en krijgt zo de instellingen die later nodig zijn. Vervolgens krijgen de displays de instellingen welke pins, ID en instellingen ze moeten gebruiken. Daarna worden ze geinitialized:


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

De instellingen van de Rotary encoder:

# Setup the Rotary Encoder
button_pin = Pin(16, Pin.IN, Pin.PULL_UP)
direction_pin = Pin(17, Pin.IN, Pin.PULL_UP)
step_pin  = Pin(18, Pin.IN, Pin.PULL_UP)

abort_pin = Pin(14, Pin.IN, Pin.PULL_UP)

# for tracking the direction and button state
previous_value = True
button_down = False

abort = False

Vervolgens komen de instellingen van de afbeelding, die zal ik alleen niet compleet in het document beschrijven ivm dat het erg groot is. De afbeelding is in binairy. Omdat de afbeelding in het midden van het scherm moet komen zeg je eerst hoe groot de afbeelding is en vervolgens zeg je waar de coordinaten van de afbeelding beginnen en deel je die door 2. De fbuf is voor dat de binaire code word omgezet naar code voor het scherm. Vervolgens maak ik eerst het scherm leeg want als de code eindigt gaat niet vanzelf het vorige wat op het scherm stond weg. Nadat het scherm geleegd is komt de afbeelding op het 2e oled schermpje (rechter schermpje):

image_data = [
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1f, 0xf8, 0x00, 0x00, 0x00,
0x00, 0x00………. ]

image_width = 64
image_height = 64

# Calculate the starting position to center the image
start_x = (width - image_width) // 2
start_y = (height - image_height) // 2

# Create a frame buffer with the image dimensions
fbuf = framebuf.FrameBuffer(bytearray(image_data), image_width, image_height, framebuf.MONO_HLSB)

# Clear the display before the image
oled2.fill(0)

# Blit the image onto the display at the calculated starting position
oled2.blit(fbuf, start_x, start_y)


Op het linker schermpje word text aangemaakt en in het midden gezet. Nadat dat gedaan is word het getoond op het schermpje. Na 3 seconden worden de schermpjes geleegd:

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

Nu komen we aan bij de eerste functie, Connect(). Functie connect zorgt ervoor dat we verbinding maken met het internet en gebruik maken van de wifi instellingen die eerder benoemt zijn in dit document. Op het linker schermpje krijg je een laadschermpje te zien totdat hij verbonden is met het internet. In de console krijg je het zelfde te zien. Zodra hij verbonden is geeft hij dat aan:

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        oled.fill_rect(0, 0, 128, 64, 0)
        oled.show()
        oled.text("Waiting for",0,20)
        oled.text("connection.",0,30)
        oled.show()
        print('Waiting for connection...')
        sleep(1)
        oled.fill_rect(0, 0, 128, 64, 0)
        oled.show()
        oled.text("Waiting for",0,20)
        oled.text("connection..",0,30)
        oled.show()
        print('Waiting for connection...')
        sleep(1)
        oled.fill_rect(0, 0, 128, 64, 0)
        oled.show()
        oled.text("Waiting for",0,20)
        oled.text("connection...",0,30)
        oled.show()
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}     =====WELCOME TO THE INTERNET=====')
    oled.fill_rect(0, 0, 128, 64, 0)
    oled.show()
    oled.text("Welcome to the",0,20)
    oled.text("internet!",0,30)
    oled.show()
    sleep(1.5)
    return ip

try:
    ip = connect()
except KeyboardInterrupt:
    machine.reset()


De volgende functies zijn alle programmas die gekozen kunnen worden in het menu. Meeste van deze functies zijn testen om alle hardware te kunnen testen. Een van de functies “Rick_Mageddon” is een voorbeeld wie je kan zoeken met de steam API:
#Programs
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

    oled2.text("If i punch those",0,0)
    oled2.text("numbers into my",0,10)
    oled2.text("calcualtor, it",0,20)
    oled2.text("makes an",0,30)
    oled2.text("happy face :D",0,40)
    oled2.show()


def StatusLEDTest():
    while True:
        # range of random numbers
        R=random.randint(0,65535)
        G=random.randint(0,65535)
        B=random.randint(0,65535)
        print(R,G,B)
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


De meest belangrijke functies zijn de volgende, die worden gebruikt om programmas te kunnen sluiten, op te starten en het menu te laten zien:
def abort_running():
    global abort
    abort = True
    sleep(3)
    abort = False

def launch(item):
    global file_list
    global abort
    global functions

    # clear the screen
    oled.fill_rect(0,0,width,height,0)
    oled.text("Searching", 1, 0)
    oled.text(item["name"],1, 20)
    oled.show()

    abort_running()
    _thread.start_new_thread(item["function"], [])
    oled.fill_rect(0,0,width,height,0)
    oled.text("Showing", 1, 0)
    oled.text(item["name"],1, 20)
    oled.show()


def show_menuu(functions ):
    # bring in the global variables
    global line, highlight, shift, list_length

    # menu variables
    item = 1
    line = 1
    line_height = 10

    # clear the display
    oled.fill_rect(0,0,width,height,0)

    #print(type(functions))
    for item in functions:
        if highlight == line:
            oled.fill_rect(0,(line-1)*line_height, width,line_height,1)
            oled.text(">",0, (line-1)*line_height,0)
            oled.text(item["name"], 10, (line-1)*line_height,0)
            oled.show()
        else:
            oled.text(item["name"], 10, (line-1)*line_height,1)
            oled.show()
        line += 1
    oled.show()

functions = [{"name": "ApiRequestTest", "function": ApiRequestTest}, {"name": "Rick_Mageddon", "function": Rick_Mageddon}, {"name": "PixelTestRGB", "function": PixelTestRGB}, {"name": "CaveJohnson", "function": CaveJohnson},
             {"name": "StatusLEDTest", "function": StatusLEDTest},{"name": "Neopixel", "function": loop_neopixel} ]

# Get the list of Python files and display the menu
# file_list = get_files()
#show_menu(file_list)
show_menuu(functions)

Als laatste word er gekeken of er aan de rotary encoder naar links of naar rechts word gedraaid of ingedrukt word. De word de button ge-debounced en als laatst word er gekeken of de Abort button word ingedrukt en dan terug word gestuurd naar het menu:
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
                    if shift+total_lines < list_length:
                        shift += 1

            show_menuu(functions)
        previous_value = step_pin.value()

    # Check for button pressed
    if button_pin.value() == False and not button_down:
        button_down = True

        print("Launching", functions[highlight-1+shift]["name"])


        # execute script
        launch(functions[highlight-1+shift])

        print("Running", functions[highlight-1+shift]["name"])

    # Decbounce button
    if button_pin.value() == True and button_down:
        button_down = False
    #Abort Button
    if not abort_pin.value():
        abort = True

        oled2.fill_rect(0, 0, 128, 64, 0)
        oled2.show()
        print("Returned from launch")
        show_menuu(functions)








Rick van der Voort
31-01-24
1855264






 
Bronnen
https://javl.github.io/image2cpp/
https://www.youtube.com/watch?v=62nABfbjDqg&t=250s
https://www.youtube.com/watch?v=tFclMtAIFF8&t=59s
https://www.youtube.com/watch?v=tFclMtAIFF8&t=59s
https://www.youtube.com/watch?v=kgjmw6SsKMc&t=60s
https://www.youtube.com/watch?v=ILELVP0kFl8
https://chat.openai.com
https://www.youtube.com/watch?v=vVS4gFI5gjM&t=75s

