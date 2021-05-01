import pigpio
import time
import numpy
import scipy as sp
from scipy.interpolate import interp1d

LED = numpy.empty(4)
LED[0] = 24 # Pin 18 = GPIO 24 = white
LED[1] = 27 # Pin 13 = GPIO 27 = blue
LED[2] = 22 # Pin 15 = GPIO 22 = red
LED[3] = 23 # Pin 16 = GPIO 23 = green

# initialize
pi=pigpio.pi()
for i in range(0, 4):
  pi.set_PWM_range(int(LED[i]), 10000)
  pi.set_PWM_dutycycle(int(LED[i]), 0)

# Sunrise
def sunrise(led, pos):
  # default
  x = [0, 0.25, 0.5, 0.75, 1]
  y = [0, 0.1, 0.3, 0.75, 1]
  if led == 1: # blue
    y = [0, 0, 0.1, 0.2, 0.8]
  elif led == 2: # red
    y = [0, 0.2, 0.5, 0.8, 1]
  elif led == 3: # green
    y = [0, 0, 0.2, 0.5, 1]
  return sp.interpolate.interp1d(x, y, kind='cubic')(pos)

# Fade out from current brightness
def fade_off():
  while True:
    still_on = down();
    time.sleep(0.05)
    if (still_on == False):
      break

# Step down brightness, returns true if still on
def down():
    still_on = False;
    for i in range(0, 4):
      value = pi.get_PWM_dutycycle(int(LED[i]))
      if (value > 0):
        value = value - 500
        if (value < 0):
          value = 0
        pi.set_PWM_dutycycle(int(LED[i]), value)
        still_on = True
    return still_on

def up():
    not_full = False;
    for i in range(0, 4):
      value = pi.get_PWM_dutycycle(int(LED[i]))
      if (value < 10000):
        value = value + 500
        if (value > 10000):
          value = 10000
        pi.set_PWM_dutycycle(int(LED[i]), value)
        not_full = True
    return not_full
  
# Fade out from current brightness
def fade_on():
  for j in range(1, 20):
    for i in range(0, 4):
      level = j * 500 if i == 0 else j * 200
      pi.set_PWM_dutycycle(int(LED[i]), level)
    time.sleep(0.05)

# Fade in
def on(led, pos):
  if (led == 0):
    return pos
  else:
    return pos * 0.5

# find oiut whether LED is on or off
def is_on():
  # is at least one LED on?
  status = 0
  for i in range(0, 4):
    if (pi.get_PWM_dutycycle(int(LED[i])) > 0):
      status = 1
  return (status == 1)
  
# Toggle
def toggle():
  if is_on():
    fade_off()
  else:
    fade_on()

# Run a cycle
def cycle(seconds, lightfunction):
  steps = seconds * 10
  for dc in range(0, steps + 1):
    if (dc % 10) == 0:
      print("Time: " + str(int(dc/10)) + "s =================")
    for i in range(0, 4):
      value = lightfunction(i, dc/steps)
      cleanvalue = int(min(max(0,value),1)*10000)
      pi.set_PWM_dutycycle(int(LED[i]), cleanvalue)
      if (dc % 10) == 0:
        print (str(cleanvalue))
      # Watch the light switch and abort if pressed.
      if (switch.switch_state == 0):
        return
    time.sleep(0.1) # 1/100th of a second
  return;

