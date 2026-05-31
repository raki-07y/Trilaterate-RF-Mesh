#!/usr/bin/python
# -*- coding:utf-8 -*-

import SH1106
import time
import config
import traceback

from PIL import Image,ImageDraw,ImageFont

try:
    disp = SH1106.SH1106()

    print("\r\1.3inch OLED")
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()

    # Create blank image for drawing.
    image1 = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype('Font.ttf', 20)
    font10 = ImageFont.truetype('Font.ttf',13)
    print ("***draw line")
    draw.line([(0,0),(127,0)], fill = 0)
    draw.line([(0,0),(0,63)], fill = 0)
    draw.line([(0,63),(127,63)], fill = 0)
    draw.line([(127,0),(127,63)], fill = 0)
    print ("***draw rectangle")

    print ("***draw text")
    draw.text((30,0), ' LoRa', font = font, fill = 0)
    draw.text((10,25), u'welcome tourist', font = font10, fill = 0)

    # image1=image1.rotate(180) 
    disp.ShowImage(disp.getbuffer(image1))
    time.sleep(2)
    
    print ("***draw image")
    Himage2 = Image.new('1', (disp.width, disp.height), 255)  # 255: clear the frame
    bmp = Image.open('SA.jpg')
    Himage2.paste(bmp, (0,5))
    # Himage2=Himage2.rotate(180) 	
    disp.ShowImage(disp.getbuffer(Himage2))
    time.sleep(2)
    disp.reset()
except IOError as e:
    print(e)
    
except KeyboardInterrupt:    
    print("ctrl + c:")
    disp.RPI.module_exit()
    exit()
