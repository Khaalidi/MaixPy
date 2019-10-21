import os, sys, time


sys.path.append('')
sys.path.append('.')

# chdir to "/sd" or "/flash"
devices = os.listdir("/")
if "sd" in devices:
    os.chdir("/sd")
    sys.path.append('/sd')
else:
    os.chdir("/flash")
sys.path.append('/flash')

print("[MaixPy] init end") # for IDE
for i in range(200):
    time.sleep_ms(1) # wait for key interrupt(for maixpy ide)

# check IDE mode
ide_mode_conf = "/flash/ide_mode.conf"
ide = True
try:
    f = open(ide_mode_conf)
    f.close()
except Exception:
    ide = False

if ide:
    os.remove(ide_mode_conf)
    import lcd
    from machine import UART
    from board import board_info
    from fpioa_manager import fm
    from Maix import FPIOA, GPIO
    import time
    lcd.init(color=lcd.PINK)
    fm.register(board_info.PIN17,fm.fpioa.GPIO0)
    led=GPIO(GPIO.GPIO0,GPIO.OUT)
    led.value(1)
    lcd.rotation(2)
    lcd.clear((255,0,0))
    lcd.draw_string(lcd.width()//2-68,lcd.height()//2-4, "Welcome to MaixPy", lcd.WHITE, lcd.RED)
    repl = UART.repl_uart()
    repl.init(1500000, 8, None, 1, read_buf_len=2048, ide=True, from_ide=False)
    sys.exit()    

import gc
import machine
from board import board_info
from fpioa_manager import fm
from pye_mp import pye
from Maix import FPIOA, GPIO


# detect boot.py
boot_py = '''
from fpioa_manager import *
import os, Maix, lcd, image
from Maix import FPIOA, GPIO

test_pin=16
fpioa = FPIOA()
fpioa.set_function(test_pin,FPIOA.GPIO7)
test_gpio=GPIO(GPIO.GPIO7,GPIO.IN)
lcd.init(color=(255,0,0))
fm.register(board_info.PIN17,fm.fpioa.GPIO0)
led=GPIO(GPIO.GPIO0,GPIO.OUT)
led.value(1)
lcd.rotation(2)
lcd.clear((255,0,0))
lcd.draw_string(lcd.width()//2-68,lcd.height()//2-4, "Welcome to MaixPy", lcd.WHITE, lcd.RED)
if test_gpio.value() == 0:
    print('PIN 16 pulled down, enter test mode')
    import sensor
    import image
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.run(1)
    lcd.freq(16000000)
    while True:
        img=sensor.snapshot()
        lcd.display(img)
'''

flash_ls = os.listdir()
if (not "boot.py" in flash_ls) :
    f = open("boot.py", "wb")
    f.write(boot_py)
    f.close()

banner = '''
 __  __              _____  __   __  _____   __     __
|  \/  |     /\     |_   _| \ \ / / |  __ \  \ \   / /
| \  / |    /  \      | |    \ V /  | |__) |  \ \_/ /
| |\/| |   / /\ \     | |     > <   |  ___/    \   /
| |  | |  / ____ \   _| |_   / . \  | |         | |
|_|  |_| /_/    \_\ |_____| /_/ \_\ |_|         |_|

Official Site : https://www.sipeed.com
Wiki          : https://maixpy.sipeed.com
'''
print(banner)

# run boot.py
with open("boot.py") as f:
    exec(f.read())

