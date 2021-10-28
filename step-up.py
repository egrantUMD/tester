from time import sleep
import json
import mainy

step = mainy.stepper()
p1 = 0
angle = [100, 300, 60, 270, 57]

#with open('angle.txt', 'r') as f:
#    data = json.load(f)
#    p1 = int(data['PIN'])
#    slide = int(data['slider1'])
angle2 = 0
n = 0 
while n < 5: 
  if angle[n] > angle2 and p1 ==0 :
    a = angle[n] - angle2
    b = 360 - a
    if a>=b:
      step.goangle(b, -1 )
    elif a < b:
      step.goangle(a, 1)
    angle2 = angle[n]
  elif angle[n] < angle2 and p1 == 0:
    a = angle2 - angle[n]
    b = 360 - a
    if a>=b:
      step.goangle(b, 1 )
    elif a < b:
      step.goangle(a, -1)
    angle2 = angle[n]
  elif p1 == 1:
    step.zero()
  n = n + 1