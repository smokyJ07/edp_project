import speech_recognition as sr
import time
from g2p_en import g2p

# Just disables a warning regarding Jonas CPU (just ignore)
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#transform speech to integer output (can be changed to what is needed)
def speech2phonemes(text):
    phonemes = g2p(text)
    print (phonemes)
    stimuli= {'<PAD>':0, '<EOS>':0,' ':0, 'AA0':1, 'AA1':1, 'AA2':1,'AE0':2, 'AE1':2, 'AE2':2,'AH0':3, 'AH1':3,
    'AH2':3,'AO0':4, 'AO1':4, 'AO2':4,'AW0':5, 'AW1':5, 'AW2':5, 'AY0':6, 'AY1':6, 'AY2':6, 'B':7,'CH':8,
    'D':9,'DH':10,'EH0':11, 'EH1':11, 'EH2':11,'ER0':12, 'ER1':12, 'ER2':12,'EY0':13, 'EY1':13, 'EY2':13,
    'F':14,'G':15,'HH':16,'IH0':17, 'IH1':17, 'IH2':17,'IY0':18, 'IY1':18, 'IY2':18,'JH':19,'K':20,'L':21,
    'M':22,'N':23,'NG':24,'OW0':25, 'OW1':25, 'OW2':25,'OY0':26, 'OY1':26, 'OY2':26,'P':27,'R':28,'S':29,
    'SH':30,'T':31,'TH':32,'UH0':33, 'UH1':33, 'UH2':33,'UW':34, 'UW0':34, 'UW1':34, 'UW2':34,'V':35,'W':36,
    'Y':37,'Z':38,'ZH':39}
    for phoneme in phonemes:
        print (stimuli[phoneme])

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source) #adapt to noise

    elapsed = 0;
    print("Say something!")
    start = time.time()
    while elapsed < 5:

            audio = r.listen(source)
            # recognize speech using Sphinx
            elapsed = time.time() - start

print("Please stop !")
try:
    text = r.recognize_google(audio)
    print(text)
    speech2phonemes(text)

except:
    print(" Google couldn't understand.")
