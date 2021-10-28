import RPi.GPIO as GPIO
import time
from time import sleep
import smbus

GPIO.setmode(GPIO.BCM)

pins = [18,21,22,23]
for pin in pins:
  GPIO.setup(pin, GPIO.OUT, initial=0)

# Define the pin sequence for counter-clockwise motion, noting that
# two adjacent phases must be actuated together before stepping to
# a new phase so that the rotor is pulled in the right direction:
sequence = [ [1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0], [0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1] ]


def delay_us(tus): # use microseconds to improve time resolution
  endTime = time.time() + float(tus)/ float(1E6)
  while time.time() < endTime:
    pass
# current posiiton in stator sequence
state = 0
class PCF8591:

  def __init__(self,address):
    self.bus = smbus.SMBus(1)
    self.address = address

  def read(self,chn): #channel
      try:
          self.bus.write_byte(self.address, 0x40 | chn)  # 01000000
          self.bus.read_byte(self.address) # dummy read to start conversion
      except Exception as e:
          print ("Address: %s \n%s" % (self.address,e))
      return self.bus.read_byte(self.address)



class Stepper:
  pins = [18,21,22,23]
  
  sequence = [ [1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0], [0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1] ]

  state = 0
  
  ADC = PCF8591(0x48)

  pho = ADC.read(0)

  def __init__(self):
    pass
  
  def __Halfstep(self, dir):
  #dir = +/- ccw / cw
    self.state += dir
    if self.state > 7:
      self.state = 0
    elif self.state < 0:
      self.state = 7
    for pin in range(4):    
      GPIO.output(self.pins[pin], self.sequence[self.state][pin])
    sleep(1)

  def __movesteps(self, steps, dir):
    #move actuatioon a given number of half steps
    for step in steps:
      self.__Halfstep(dir)
      sleep(0.1)
    return(0)

    
  def goangle(self, angle, dir):
    steps = (1/0.087875) * angle
    self.__movesteps(steps, dir)
    return(0)


  def zero(self):
    while self.pho <190:
      self.movestep(1,1)
    return(0)
