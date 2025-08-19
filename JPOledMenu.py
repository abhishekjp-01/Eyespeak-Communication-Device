from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
import time
import subprocess
from gpiozero import OutputDevice

relay = OutputDevice(17, active_high=True,initial_value=False)
relay2 = OutputDevice(27, active_high=True,initial_value=False)

# OLED Setup
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)
image = Image.new("1", (device.width, device.height))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("/home/abhishekjp/tflite1/myenv/lib64/python3.11/site-packages/BIG JOHN.otf", 16)

# Actions
def idle():
    global menu_select
    menu_select = False
    draw.rectangle((0, 0, device.width, device.height), outline=0, fill=0)
    draw.rectangle((0, 0, 124, 63), outline=255, fill=0)
    draw.text((16, 21), "idle mode", font=font, fill=255)
    device.display(image)
def Light_ON_OFF():relay.toggle()
def Fan_ON_OFF():relay2.toggle()
def Need_Water(): speak("I want some water")
def Need_Food(): speak("i am hungry")
def Washroom(): speak("washroom please")
def Go_Out(): speak("I wanna go out")
def Back (): print("back")

def speak(text):
    subprocess.run(['espeak','-v','en+f2',text])

# Menus
menu = {
    "Main": {
        "Devices": {
            "1 LIGHT": Light_ON_OFF,
            "2 FAN": Fan_ON_OFF,
            "Back": Back
        },
        "Comm": {
            "Water": Need_Water,
            "Food": Need_Food,
            "Washroom": Washroom,
            "Go Out": Go_Out,
            "Back": Back
        },
        "Idle": idle,
        "Back": Back
    }
}

path = ["Main"]

def boot_logo():
    draw.rectangle((0, 0, device.width, device.height), outline=0, fill=0)
    draw.rectangle((0, 0, 124, 63), outline=255, fill=0)
    draw.text((16, 21), "eyespeak", font=font, fill=255)
    time.sleep(1)
    device.display(image)
    draw.rectangle((0, 0, device.width, device.height), outline=0, fill=0)
    draw.text((16, 21), "loading...", font=font, fill=255)
    time.sleep(2)
    device.display(image)
    
def get_current_menu():
    m = menu
    for p in path:
        m = m[p]
    return m

def draw_menu():
    global keys
    current_menu = get_current_menu()
    if isinstance(current_menu, dict):
        
        keys = list((current_menu.keys()))
        draw.rectangle((0, 0, device.width, device.height), outline=0, fill=0)
        draw.rectangle((0, 18, 124, 38), outline=255, fill=0)
        for i, j in zip(keys, range(0, 100, 21)):
            
            draw.text((4, j), i, font=font, fill=255)
        device.display(image)
        speak(keys[1])
      
            
    elif callable(current_menu):
        current_menu()


# Menu navigation state

def scroll_up():
    global keys
    temp = keys
    
    
    for k in range(0,28,7):
        draw.rectangle((0, 0, device.width, device.height), outline=0, fill=0)
        draw.rectangle((0, 18, 124, 38), outline=255, fill=0)

        for i, j in zip(temp, range(0, 100, 21)):
            
            if (j==0):
                j = (len(temp))*21
                j = j-k
                draw.text((4, j-((len(temp))*21)), i, font=font, fill=255)
                draw.text((4, j), i, font=font, fill=255)
            else:
                j = j-k
                draw.text((4, j), i, font=font, fill=255)
        time.sleep(0.024)
        device.display(image)
  
    keys = keys[1:] + keys[:1]
    speak(keys[1])
def scroll_down():
    global keys
    temp = keys
    
    for k in range(0,28,7):
        draw.rectangle((0, 0, device.width, device.height), outline=0, fill=0)
        draw.rectangle((0, 18, 124, 38), outline=255, fill=0)

        for i, j in zip(temp, range(0, 100, 21)):
            
            if j==((len(temp)-1)*21):
                j = -21
                j = j+k
                draw.text((4, j+66), i, font=font, fill=255)
                draw.text((4, j), i, font=font, fill=255)
            else:
                j = j+k
                draw.text((4, j), i, font=font, fill=255)
        time.sleep(0.024)
        device.display(image)
  
    keys = keys[-1:] + keys[:-1]
    speak(keys[1])
    
def select():
    global path
    current_menu = get_current_menu()
    selected = keys[1]

    if selected == "Back":
        if len(path) > 1:
            path.pop()  # go back one level
            draw_menu()
    elif isinstance(current_menu[selected], dict):
        path.append(selected)
        draw_menu()
    elif callable(current_menu[selected]):
        current_menu[selected]()
    
boot_logo()
