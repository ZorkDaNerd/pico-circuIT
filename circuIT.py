from machine import Pin, ADC, PWM, Timer #This imports the pin library
from time import sleep #This imports the sleep function
from utime import sleep
import utime, math, machine, time, random, sys

#This code was writen by ZorkDaNerd and other contributers!

#Figure out timer and make a fail win condition
#Make it so you can actualy restart the game and keep the high score
#Fix the potentiomiter game and possily thr light meter game
def main(): #this is the main class that contains all the deffenitions
    circuIt()


#I should go through and make each of the areas a deffinition area
playflag = True
therm = ADC(Pin(26))

#begin deffenitions
greenLed = Pin(10, Pin.OUT, Pin.PULL_UP)
redLed = Pin(9, Pin.OUT, Pin.PULL_UP)
buzzer = PWM(Pin(15))
score = 0
tim = Timer(-1)

def buzz(): #this defines the buzzer beep cycle
    buzzer.freq(500)
    buzzer.duty_u16(1000)
    sleep(1)
    buzzer.duty_u16(0)

def readLight(photoGP):#This was origionally for the light sensor calculation
    photoRes = ADC(Pin(26))
    light = photoRes.read_u16()
    light = round(light/65535*100,2)
    return int(light)

def convert_temp(reading): #This was used for the thermistor
    c1 = 1.009249522e-03
    c2 = 2.378405444e-04
    c3 = 2.019202697e-07
    R1 = 1000 * (65535 / reading - 1.0)
    logR1 = math.log(R1)
    T = (1.0 / (c1 + c2*logR1 + c3*logR1*logR1*logR1)) #this all calculates celsius
    celsius = T - 273.15;
    return(celsius)
#end deffenitions



#start main function
def circuIt(): #This is the main game deffenition
    global playflag
    score = 0
    print("Hello there would you like to play CircuIt? y/n")
    inp = (input())
    if inp == "y":
        print("Here we go!")
        playFlag = True
    else:
        print("I am now sad :(")
        redLed.toggle()
        playsong(song) #Plays sad song
        redLed.toggle()
        sys.exit()
        #Put a sad sound here
    print("Time for first game!")  
    print("Starting in 3...")
    sleep(1)
    print("2...")
    sleep(1)
    print("1...")
    sleep(1)
    print("GO!!!")
    
    while playflag == True:
        #generates random numbers
        gamenum = random.randint(0,3)
        #gamenum = 0
        #makes a timer for the games
        #add red light to run on fail and sound
#--------------------------------------------
        if gamenum == 0:
            #this game is covering the light resistor
            #timerstat = true
            gamestat = True
            tim.init(period=5000, mode=Timer.ONE_SHOT, callback=endgame)
            #n = random.randint(0,5) #this might be used to have a random percentage of light or something
            #Posibly make it so a timer adds a number each seccond and if it goes above 5 it ends the game
            while gamestat == True:
                thermval = convert_temp(therm.read_u16())#stores light val
                print("Temp: " + str(thermval))
                if thermval > 21:
                    #run green light here and sound
                    gamestat = False

                else:
                    sleep(0.4) #set a delay between readings
            score += 1 #adds score
            tim.init(period=20000, mode=Timer.ONE_SHOT, callback=endgame)
#---------------------------------------------            
        elif gamenum == 1:
            #this game is straightening the ball switch a number of times
            lightON = Pin(12, Pin.IN)
            rnnum = random.randint(4,10)
            tim.init(period=(1000*rnnum), mode=Timer.ONE_SHOT, callback=endgame) #starts fail timer
            swnum = 0 #switch count
            lock = False #allows game to work by protecting against instant win
            print("Turn on and off the switch " + str(rnnum))
            sleep(2.5)
            
            while swnum != rnnum: #This is where the switch is actualy detected
                state = lightON.value()
                
                if state:
                    print("Switch Off")
                    lock = False
                else:
                    print("Switch On")
                    if lock == False:
                        swnum += 1
                    lock = True
                print("Switch number is at " + str(swnum)) #tells how mny are left
                sleep(0.7)
            score += 1
            tim.init(period=20000, mode=Timer.ONE_SHOT, callback=endgame) #This timer allows for the timer to stop
#----------------------------------------------
        elif gamenum == 2:
            #this game is pressing the button when propted a number of times
            sw = Pin(11, Pin.IN, Pin.PULL_UP)
            rnnum = random.randint(2,4)
            tim.init(period=(1000*rnnum), mode=Timer.ONE_SHOT, callback=endgame)
            sc = 0
            print("Press the button " + str(rnnum) +" times with random wait")
            sleep(3)
            
            while sc != rnnum:
                time = 0
                act = True
                rntime = random.randint(1,3)
                while time != rntime: #waits random amount of time
                    time += 1
                    print("Wait")
                    sleep(1)
                    
                while act == True: #Tells player to press button
                    state = sw.value()
                    if state:
                        print("PRESS BUTTON!!!")
                    else:
                        print("Button pressed")
                        sc += 1
                        act = False
                    sleep(0.2)
            score += 1
            tim.init(period=20000, mode=Timer.ONE_SHOT, callback=endgame) #this resets the timer from ending the game before the next one starts
#----------------------------------------------   
        elif gamenum == 3:
            #this game is adjusting the potentiomiter to around a cirtian number
            potentiomiter = machine.ADC(28)
            rnnum = random.randint(1,55)
            rnnum = rnnum * 1000
            updwn = random.randint(0,1)
            value = potentiomiter.read_u16()
            tim.init(period=5000, mode=Timer.ONE_SHOT, callback=endgame)
            print("Turn the potentiomiter to above or below the given value.")
            if updwn == 0:
                print("Turn the potentiomiter below " + str(rnnum)) #Not really random or working
                sleep(4)
                while value <= rnnum:
                    value = potentiomiter.read_u16()
                    print("Value is: ", value)
                    sleep(0.2)
            else:
                print("Turn the potentiomiter above " + str(rnnum)) #randomly choses having the number above or below 
                sleep(4)
                while value >= rnnum:
                    value = potentiomiter.read_u16()
                    print("Value is: ", value)
                    sleep(0.2)
            score += 1
            tim.init(period=20000, mode=Timer.ONE_SHOT, callback=endgame) 
#----------------------------------------------            
        else: #This is for if the rng fails
            print("ERROR: rng didnt make a number")
            
        greenLed.on() #turns on green led
        print("Current score is: ", score)
        buzz()
        sleep(4)
        greenLed.off()
        print("Next game starting!")
#-----------------------------------------------        


def endgame(t): #This ends and restarts the game
    print("Sorry you ran out of time :(")
    print("You got a score of " + str(score) + "!")
    circuIt()

tones = { #this holds a bunch of tones to make a song
"B0": 31,
"C1": 33,
"CS1": 35,
"D1": 37,
"DS1": 39,
"E1": 41,
"F1": 44,
"FS1": 46,
"G1": 49,
"GS1": 52,
"A1": 55,
"AS1": 58,
"B1": 62,
"C2": 65,
"CS2": 69,
"D2": 73,
"DS2": 78,
"E2": 82,
"F2": 87,
"FS2": 93,
"G2": 98,
"GS2": 104,
"A2": 110,
"AS2": 117,
"B2": 123,
"C3": 131,
"CS3": 139,
"D3": 147,
"DS3": 156,
"E3": 165,
"F3": 175,
"FS3": 185,
"G3": 196,
"GS3": 208,
"A3": 220,
"AS3": 233,
"B3": 247,
"C4": 262,
"CS4": 277,
"D4": 294,
"DS4": 311,
"E4": 330,
"F4": 349,
"FS4": 370,
"G4": 392,
"GS4": 415,
"A4": 440,
"AS4": 466,
"B4": 494,
"C5": 523,
"CS5": 554,
"D5": 587,
"DS5": 622,
"E5": 659,
"F5": 698,
"FS5": 740,
"G5": 784,
"GS5": 831,
"A5": 880,
"AS5": 932,
"B5": 988,
"C6": 1047,
"CS6": 1109,
"D6": 1175,
"DS6": 1245,
"E6": 1319,
"F6": 1397,
"FS6": 1480,
"G6": 1568,
"GS6": 1661,
"A6": 1760,
"AS6": 1865,
"B6": 1976,
"C7": 2093,
"CS7": 2217,
"D7": 2349,
"DS7": 2489,
"E7": 2637,
"F7": 2794,
"FS7": 2960,
"G7": 3136,
"GS7": 3322,
"A7": 3520,
"AS7": 3729,
"B7": 3951,
"C8": 4186,
"CS8": 4435,
"D8": 4699,
"DS8": 4978
}

song = ["E5","G5","A5","P","E5","G5","B5","A5","P","E5","G5","A5","P","G5","E5"] #This is the song

def playtone(frequency): #defines the frequency
    buzzer.duty_u16(1000)
    buzzer.freq(frequency)

def bequiet(): #turns the buzzer off
    buzzer.duty_u16(0)

def playsong(mysong): #plays the song
    for i in range(len(mysong)):
        if (mysong[i] == "P"):
            bequiet()
        else:
            playtone(tones[mysong[i]])
        sleep(0.3)
    bequiet()
#playsong(song)

if __name__ == '__main__': #defines main
    main()