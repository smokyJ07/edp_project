import speech_recognition as sr
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(4,GPIO.OUT)
GPIO.setup(14,GPIO.OUT)
GPIO.output(2,GPIO.LOW)
GPIO.output(3,GPIO.LOW)
GPIO.output(4,GPIO.LOW)
GPIO.output(14,GPIO.LOW)
GPIO.setup(15,GPIO.OUT)
GPIO.output(15,GPIO.LOW)
GPIO.setup(18,GPIO.OUT)
GPIO.output(18,GPIO.LOW)
GPIO.setup(17,GPIO.OUT)
GPIO.output(17,GPIO.LOW)
GPIO.setup(27,GPIO.OUT)
GPIO.output(27,GPIO.LOW)
GPIO.setup(22,GPIO.OUT)
GPIO.output(22,GPIO.LOW)

GPIO.setup(5,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.output(5,GPIO.LOW)
GPIO.output(6,GPIO.LOW)
GPIO.output(13,GPIO.LOW)
GPIO.output(19,GPIO.LOW)
GPIO.setup(26,GPIO.OUT)
GPIO.output(26,GPIO.LOW)
GPIO.setup(12,GPIO.OUT)
GPIO.output(12,GPIO.LOW)
GPIO.setup(16,GPIO.OUT)
GPIO.output(16,GPIO.LOW)
GPIO.setup(20,GPIO.OUT)
GPIO.output(20,GPIO.LOW)
GPIO.setup(21,GPIO.OUT)
GPIO.output(21,GPIO.LOW)
#from g2p_en import g2p



       
class Motor:
    def __init__(self, pin_in=0):
        self.pin = pin_in
        if (self.pin>0):
            GPIO.setup(self.pin,GPIO.OUT)
            GPIO.output(self.pin,GPIO.LOW)
    def low(self):
        GPIO.output(self.pin,GPIO.LOW)
    def high(self):
        GPIO.output(self.pin,GPIO.HIGH)
    def switch_on(self, duration=0.5):
        GPIO.output(self.pin,GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.pin,GPIO.LOW)

class Pad:
    def __init(self):
        self.motors = []
        
    def vibrate(self,pattern=40):
        #decide the pad
        if (pattern[1]==0):
            self.spatial(index_ls=pattern[2])
        elif(pattern[1]==1):
            self.temporal(index_ls=pattern[2])
        else:
            print("Error while choosing mode of vibration")
    
    #executes a static vibration pattern (single motor on)
    def static(self, motor_index = 0, duration = 0.5):
        self.motors[motor_index].switch_on(duration)
        
    #causes a spatial vibration pattern (multiple motors on at same time)
    def spatial(self, index_ls = [], duration = 0.5):
        for index in index_ls:
            self.motors[index].high()
        time.sleep(duration)
        for index in index_ls:
            self.motors[index].low()
            
    #causes a temporal vibration pattern (direction given by order in index_ls) 
    def temporal(self,index_ls=[],duration=0.12):
        length = len(index_ls)
        self.motors[index_ls[0]].high()
        time.sleep(duration)
        for i in range(1,length):
            self.motors[index_ls[i]].high()
            time.sleep(duration)
            self.motors[index_ls[i-1]].low()
        time.sleep(duration)
        self.motors[index_ls[len(index_ls)-1]].low()
     
    def all_off(self):
        for i in range(0,8):
            self.motors[i].low()


#transform speech to integer output (can be changed to what is needed)
#returns a list where each element represents one word
#each word is a list of several phonemes
def speech2phonemes(text):
    phonemes = g2p(text)
    print (phonemes)
    commands = [] #one command representing one phoneme
    words = []
    # values: first entry: left pad(0) right pad(1), second entry: spatial(0), temporal(1), third entry: index list
    stimuli= {',':0, '<PAD>':0, '<EOS>':0,' ':0, 'AA0':[0,1,[3,0]], 'AA1':[0,1,[3,0]], 'AA2':[0,1,[3,0]],'AE0':[0,0,[0,3]], 'AE1':[0,0,[0,3]], 'AE2':[0,0,[0,3]],
        'AH0':[0,0,[2,6]], 'AH1':[0,0,[2,6]], 'AH2':[0,0,[2,6]],'AO0':[0,0,[1,2]], 'AO1':[0,0,[1,2]], 'AO2':[0,0,[1,2]],'AW0':[0,1,[2,4,6]], 'AW1':[0,1,[2,4,6]], 'AW2':[0,1,[2,4,6]], 'AY0':[0,1,[0,4,8]],
        'AY1':[0,1,[0,4,8]], 'AY2':[0,1,[0,4,8]], 'B':[1,1,[0,4,8]],'CH':[1,0,[2,5,8]],'D':[1,0,[0,2,6,8]],'DH':[1,1,[1,2,5,8,7]],'EH0':[0,1,[8,7]], 'EH1':[0,1,[8,7]], 'EH2':[0,1,[8,7]],'ER0':[0,1,[6,4,2]], 'ER1':[0,1,[6,4,2]],
        'ER2':[0,1,[6,4,2]],'EY0':[0,1,[0,3]], 'EY1':[0,1,[0,3]], 'EY2':[0,1,[0,3]],'F':[1,0,[8]],'G':[1,0,[6]],'HH':[1,0,[2]],'IH0':[0,0,[0,8]], 'IH1':[0,0,[0,8]], 'IH2':[0,0,[0,8]],'IY0':[0,1,[7,8]], 
        'IY1':[0,1,[7,8]], 'IY2':[0,1,[7,8]],'JH':[1,1,[6,4,2]],'K':[1,1,[3,4,5]],'L':[1,1,[2,1,0,3,6]],'M':[1,0,[1,3,4,5,7]],'N':[1,1,[4,3,6,7,8,5,2,1,0]],'NG':[1,1,[4,5,8,7,6,3,0,1,2]],'OW0':[0,1,[1,2]], 'OW1':[0,1,[1,2]], 'OW2':[0,1,[1,2]],
        'OY0':[0,1,[0,1,2]], 'OY1':[0,1,[0,1,2]], 'OY2':[0,1,[0,1,2]],'P':[1,1,[0]],'R':[1,1,[2,5,8,7,6,3,0,1]],'S':[1,1,[5,4,3]],'SH':[1,0,[0,3,6]],'T':[1,1,[1,4,7]],'TH':[1,1,[1,0,3,6,7]],'UH0':[0,0,[1,3,5,7]], 'UH1':[0,0,[1,3,5,7]],
        'UH2':[0,0,[1,3,5,7]],'UW':[0,1,[5,7,3,1]], 'UW0':[0,1,[5,7,3,1]], 'UW1':[0,1,[5,7,3,1]], 'UW2':[0,1,[5,7,3,1]],'V':[1,1,[8,4,0]],'W':[1,1,[6,3,4,5,2]],'Y':[1,1,[2,1,4,7,6]],'Z':[1,1,[7,4,1]],'ZH':[1,0,[6,7,8]]}
    for phoneme in phonemes:
        if stimuli[phoneme] == 0:
            words.append(commands)
            commands = []
        else:
            commands.append(stimuli[phoneme])
    words.append(commands)
    return words 


motor_ls1 = [Motor(pin_in=2), Motor(pin_in=3), Motor(pin_in=4), Motor(pin_in=14), Motor(pin_in=15), Motor(pin_in=18), Motor(pin_in=17), Motor(pin_in=27), Motor(pin_in=22)]
motor_ls2 = [Motor(pin_in=5),Motor(pin_in=6),Motor(pin_in=13),Motor(pin_in=19),Motor(pin_in=26),Motor(pin_in=12),Motor(pin_in=16),Motor(pin_in=20),Motor(pin_in=21),]
p1 = Pad()
p2 = Pad()
p1.motors=motor_ls1
p2.motors=motor_ls2
print("Start")
time.sleep(3)
p1.temporal(index_ls=[0,1,2,3,4,5,6,7,8], duration=1)
#p1.spatial(index_ls=[8])

###execute patterns for each phoneme (no pad distinction yet)
#for word in words:
    #while(True):
        #for phoneme in word:
            #if phoneme[0] < 2:
                #p1.vibrate(pattern=phoneme)
            #else:
                #print("Error while selecting pad")
            #time.sleep(5) 
print("Finished")
p1.all_off()
time.sleep(10)
