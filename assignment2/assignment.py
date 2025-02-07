import threading
import time
from pynq.overlays.base import BaseOverlay
base = BaseOverlay("base.bit")
eatDurationCounter = 40 #10sec
eatFrequency = 0.25 #faster blinking lets assume 250ms

napDurationCounter = 20 # 10sec
napFrequency = 0.5 #slower blinking  lets assume 500ms

def blink(t, d, n):
    for i in range(t):
        base.leds[n].toggle()
        time.sleep(d)
        
    base.leds[n].off()

def starve(n):
    base.leds[n].off()
    
#_l is the list of forks & num is the led to blink or professor Id
def philosopher_t(forkList, num):
    
    fork1AvailableStatus = False
    fork2AvailableStatus = False
    firstAcquiredFork = None
    
    btns = base.btns_gpio

    while btns[0].read() == 0: # this will be while loop until button is press

        # iterate through the list and find forks which are available and try to acquire them
        # if one is available and others are not, release the one you have & go in starve mode
        # if both are available acquire them one by one and go to eat mode for certain duration followed by napp mode
        # note the moment 2 forks are found, we can exit the search process and go into eat mode
        # if none are available then also go to starve mode
        # (how long to wait while in starve mode?)
        for fork in forkList:
            if fork1AvailableStatus == False:
                fork1AvailableStatus = fork.acquire(False)
                if fork1AvailableStatus:
                    #saving the fork for future use to release
                    firstAcquiredFork = fork
                else:
                    print("Philosopher {} didn't get 1st fork, hence starving".format(num))
                    starve(num)
                    time.sleep(0.01)                    
            #if fork1 was acquired in last run, try for fork2 now
            else:
                fork2AvailableStatus = fork.acquire(False)
                if fork2AvailableStatus:
                    #fork2 is also acquired, go to eat and once come out, release locks & go to nap
                    print("Philosopher {} has the forks, going to eat".format(num))
                    blink(eatDurationCounter,eatFrequency,num)
                    #release fork1 & fork2
                    fork.release
                    firstAcquiredFork.release
                    time.sleep(0.01)
                    print("Philosopher {} released forks, going to nap".format(num))
                    #blink(nap)
                    blink(napDurationCounter,napFrequency,num)
                    time.sleep(0.01)
                else:
                    #fork1 was acquired but not fork2, hence release fork1 & go in starve mode
                    #release fork1
                    #blink(starve)
                    firstAcquiredFork.release
                    print("Philosopher {} didn't get 2nd fork, hence starving".format(num))
                    starve(num)
                    time.sleep(0.01)
                    #how long to starve?
    print("interrupt received")

# Initialize and launch the threads
philosopherCount = 4
forkCount = 4

threads = []
forks = []

print("press button 0 to stop the program")

for i in range(philosopherCount):
    fork = threading.Lock()
    forks.append(fork)
# create threads based on philosopher count and create 1 fork for each
for i in range(philosopherCount):
    #fork = threading.Lock()
    #forks.append(fork)
    t = threading.Thread(target=philosopher_t, args=(forks, i))
    threads.append(t)
    t.start()

for t in threads:
    name = t.getName()
    t.join()
    print('{} joined'.format(name))
    for i in range(philosopherCount):
        starve(i) #shutting down all LEDs
