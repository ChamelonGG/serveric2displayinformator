# -*- coding: utf-8 -*-
"""
Gets system information like CPU temperature, RAM, and more and display it on I2C backpack controlled 20x4 display, comes with bunch of prebuilt settings, still WIP
Made avanaiable under GNU GENERAL PUBLIC LICENSE
# Needed items to let this work: I2C backpack with 20x4 dipslay; w1thermsensor; two buttons; 5k ohm resistor 
# Recomended items to let this work: aprox. 14 female to male jumper wires; breadboard;
# Tested on Raspberry Pi 2B rev. 2 with Python 3.7 and I2C backpack 20x4 blue LED display and with two microswitches
# By chamelongg (ChamelonGG)¨
# 2021-06-27, ver 0.8
"""
#
#
#imports (modules, files)
import i2cdriver as I2C_LCD_driver
import time, psutil, speedtest
from datetime import datetime
from gpiozero import Button, CPUTemperature
from w1thermsensor import W1ThermSensor
#language setting (WIP)
#- import language_EN.json
#gpio settups
lcd = I2C_LCD_driver.lcd()
btn_next = Button(17)
btn_previous = Button(27)
sen_temp = W1ThermSensor()
#library setups
network =  speedtest.Speedtest() #defines the internet measuring service 
cpu = CPUTemperature() #defines main CPU temperature measuring service
#fonts
fonts = [ #sets primary used fonts/symbols
    [0x04,0x0A,0x0A,0x0A,0x0A,0x11,0x11,0x0E], #temp     0
    [0x04,0x04,0x04,0x15,0x0E,0x04,0x00,0x1F], #download 1
    [0x04,0x0E,0x15,0x04,0x04,0x04,0x00,0x1F], #upload   2
    [0x00,0x00,0x18,0x04,0x03,0x00,0x00,0x00], #ping     3
    [0x1C,0x14,0x1C,0x00,0x00,0x00,0x00,0x1C], #celsious 4
    [0x00,0x04,0x12,0x09,0x12,0x04,0x00,0x00], #load     5
    [0x00,0x02,0x02,0x02,0x15,0x08,0x08,0x00]  #frequency6
]
fonts_misc = [ # sets secondary/misc fonts/symbols
    [0x00,0x1F,0x11,0x17,0x17,0x11,0x1F,0x00], #cpu      1
    [0x00,0x1F,0x11,0x15,0x13,0x15,0x1F,0x00], #ram      2
    [0x00,0x1F,0x15,0x1B,0x1B,0x15,0x1F,0x00], #box      3
]
#defined settings
global pressed, interrput, dis_type, page, debug, pages, safety_space, animation_duration, animation_state, onofftimer
page = 1 #home page, the page the program will start on (default: 1)
interrput = False #controlling the loop (default: False)
onofftimer = True #controlling the backlight within current time, turns off backlight on display, not this program (default: True)
debug = False #controlls additional writing to console (default: False)
pages = [1, 2, 3, 4] #pages which are getting automatically updated by certain amount of time which is defined by time need to get values from sensors (default: [1, 2, 3, 4])
animation_duration = 2 #time for which are animatio/title pages shown (default: 2)
animation_state = True #controlls the animation function (default: True)
safety_space = " " #solves the next symbol problem i n measuring services (default: " ")(one space)



def page_counter(number):
    #makes sure to on click would be a different page
    if number == 1:
        if debug == True:
            print("returned 1")
        page = 1
        return 1
    elif number == 2:
        if debug == True:
            print("returned 2")
        page = 2
        return 2
    elif number == 3:
        if debug == True:
            print("returned 3")
        page = 3
        return 3
    elif number == 4:
        if debug == True:
            print("returned 4")
        page = 4
        return 4
    elif number == 5:
        if debug == True:
            print("returned 5")
        page = 5
        return 5
    elif number == 6:
        if debug == True:
            print("returned 1")
        page = 1
        return 1
    elif number == 0:
        if debug == True:
            print("returned 5")
        page = 5
        return 5
    else:
        return 1
def animation(page_numb, state):
    if state == True:
        #defines every animation used for between specific pages
        if page_numb == 1:
            lcd.lcd_display_string("####################", 1)
            lcd.lcd_display_string("#   Temperatures   #", 2)
            lcd.lcd_display_string("#     CPU, Case    #", 3)
            lcd.lcd_display_string("####################", 4)
            time.sleep(animation_duration) #sleeps just to show user the animation other time the animation will be too fast for human's eye to regognise the animation
            lcd.lcd_clear()
        elif page_numb == 2:
            lcd.lcd_display_string("####################", 1)
            lcd.lcd_display_string("#      Loads       #", 2)
            lcd.lcd_display_string("#       CPU        #", 3)
            lcd.lcd_display_string("####################", 4)
            time.sleep(animation_duration) #sleeps just to show user the animation other time the animation will be too fast for human's eye to regognise the animation
            lcd.lcd_clear()
        elif page_numb == 3:
            lcd.lcd_display_string("####################", 1)
            lcd.lcd_display_string("#      Loads       #", 2)
            lcd.lcd_display_string("#       RAM        #", 3)
            lcd.lcd_display_string("####################", 4)
            time.sleep(animation_duration) #sleeps just to show user the animation other time the animation will be too fast for human's eye to regognise the animation
            lcd.lcd_clear()
        elif page_numb == 4:
            lcd.lcd_display_string("####################", 1)
            lcd.lcd_display_string("#      Loads       #", 2)
            lcd.lcd_display_string("#    SWAP memory   #", 3)
            lcd.lcd_display_string("####################", 4)
            time.sleep(animation_duration) #sleeps just to show user the animation other time the animation will be too fast for human's eye to regognise the animation
            lcd.lcd_clear()
        elif page_numb == 5:
            lcd.lcd_display_string("####################", 1)
            lcd.lcd_display_string("#     Internet     #", 2)
            lcd.lcd_display_string("#  up, down, lat   #", 3)
            lcd.lcd_display_string("####################", 4)
            time.sleep(animation_duration) #sleeps just to show user the animation other time the animation will be too fast for human's eye to regognise the animation
            lcd.lcd_clear()
        else:
            lcd.lcd_display_string("####################", 1)
            lcd.lcd_display_string("#    No defined    #", 2)
            lcd.lcd_display_string("#    animation     #", 3)
            lcd.lcd_display_string("####################", 4)
            print("Something went wrong")
            time.sleep(animation_duration) #sleeps just to show user the animation other time the animation will be too fast for human's eye to regognise the animation 
            lcd.lcd_clear()

def page_select(page_num):
    if page_num == 1:
        #temperatures
        lcd.lcd_load_custom_chars(fonts)
        if (debug == False or debug == ""):
            #shows on display information about temperatures
            lcd.lcd_display_string("%s"%"CPU"+chr(0)+": "+str(round(cpu.temperature, 1))+"C"+chr(7)+"  ", 1)
            lcd.lcd_display_string("%s"%"Case"+chr(0)+": "+str(round(sen_temp.get_temperature(W1ThermSensor.DEGREES_C), 2))+"C"+chr(7)+safety_space, 2)
        elif (debug == True):
            lcd.lcd_display_string("1", 1)
    elif page_num == 2:
        #loads - CPU
        lcd.lcd_load_custom_chars(fonts)
        if (debug == False or debug == ""):
            #shows on display information about CPU
            lcd.lcd_display_string("%s"%"CPU"+chr(5)+": "+str(psutil.cpu_percent())+"%"+safety_space, 1)
            lcd.lcd_display_string("%s"%"CPU"+chr(6)+": "+str(round(psutil.cpu_freq(percpu=False).current, 2))+"MHz"+safety_space, 2)
            time.sleep(0.5)
        elif (debug == True):
            lcd.lcd_display_string("2", 2)
    elif page_num == 3: 
        #loads - RAM
        lcd.lcd_load_custom_chars(fonts)
        if (debug == False or debug == ""):
            #shows on display information about RAM
            lcd.lcd_display_string("%s"%"RAM"+"-total"+": "+str(round(psutil.virtual_memory().total / 1048576, 2))+"MB"+safety_space, 1)
            lcd.lcd_display_string("%s"%"RAM"+"-used "+": "+str(round(psutil.virtual_memory().used / 1048576, 2 ))+"MB"+safety_space, 2)
            lcd.lcd_display_string("%s"%"RAM"+"-avai "+": "+str(round(psutil.virtual_memory().available / 1048576, 2))+"MB"+safety_space, 3)
            lcd.lcd_display_string("%s"%"RAM"+"-free "+": "+str(round(psutil.virtual_memory().free / 1048576, 2))+"MB"+safety_space, 4)
        elif (debug == True):
            lcd.lcd_display_string("3", 3)
    elif page_num == 4:
        #loads - SWAP
        lcd.lcd_load_custom_chars(fonts)
        if (debug == False or debug == ""):
            #shows on display information about SWAP memory
            lcd.lcd_display_string("%s"%"SWAP"+"-total"+": "+str(round(psutil.swap_memory().total / 1048576, 2))+"MB"+safety_space, 1)
            lcd.lcd_display_string("%s"%"SWAP"+"-used "+": "+str(round(psutil.swap_memory().used / 1048576, 2 ))+"MB"+safety_space, 2)
            lcd.lcd_display_string("%s"%"SWAP"+"-free "+": "+str(round(psutil.swap_memory().free / 1048576, 2))+"MB"+safety_space, 3)
        elif (debug == True):
            lcd.lcd_display_string("4", 4)
    elif page_num == 5:
        #network
        lcd.lcd_load_custom_chars(fonts)
        if (debug == False or debug == ""):
            #creates dummy text, just to show user that something is happening
            lcd.lcd_display_string("%s"%"Net"+chr(1)+": ? Mb/s"+safety_space, 1)
            lcd.lcd_display_string("%s"%"Net"+chr(2)+": ? Mb/s"+safety_space, 2)
            lcd.lcd_display_string("%s"%"Net"+chr(3)+": ? ms"+safety_space, 3)
            #actualy, slowly measures download, upload and ping(to speedtest's random server)
            lcd.lcd_display_string("%s"%"Net"+chr(1)+": "+str(round(network.download() / 1048576, 2))+"Mb/s"+safety_space, 1)
            lcd.lcd_display_string("%s"%"Net"+chr(2)+": "+str(round(network.upload() / 1048576, 2))+"Mb/s"+safety_space, 2)
            network.get_servers([]) #settups the ping servers to speedtest test on
            lcd.lcd_display_string("%s"%"Net"+chr(3)+": "+str(network.results.ping)+"ms"+safety_space, 3)
            lcd.lcd_display_string("Press < or > to exit", 4) #waits till user switch to different page (because automatic testing is not neat)
        elif (debug == True):
            lcd.lcd_display_string("5", 1)
    else:
        lcd.lcd_display_string("Error, wrong input", 1)

if __name__ == "__main__":
    while interrput == False: 
        if debug == True:
            print(str("Looping"+interrput))
        if (btn_next.is_pressed):
            lcd.lcd_clear() #clears the screen from previos display data
            page += 1 #select the next page
            page = page_counter(page)#updates page number
            animation(page, animation_state) #shows a title for currently displayed data for sertain amount of time defined by animation_duration
            page_select(page_counter(page)) #selects and show the page and its information to user
            if (debug == True):
                print("p"+str(page)) #shows which page is being showed (in console)
        elif (btn_previous.is_pressed):
            lcd.lcd_clear() #clears the screen from previos display data
            page -= 1 #select the previous page
            page = page_counter(page) #updates page number
            animation(page, animation_state) #shows a title for currently displayed data for sertain amount of time defined by animation_duration
            page_select(page_counter(page)) #selects and show the page and its information to user
            if (debug == True):
                print("p"+str(page)) #shows which page is being showed (in console)
        elif (pages.__contains__(page)):
            page = page_counter(page) #updates page number
            page_select(page_counter(page)) #selects and show the page and its information to user
            if (debug == True):
                print("p"+str(page)) #shows which page is being showed (in console)
            
        
        
                
