import time
import pigpio
import lighteffects
import threading

SWITCH = 4 # GPIO 4 / Pin 7

# global variable to protect against chatter
last_tick = 0

# global variable to track switch state
switch_state = 1

# Reference to pi
pi = pigpio.pi()

# Wait for button release 
def dimming(status):
  while switch_state == 0:
    time.sleep(0.05)
    diff = abs(pi.get_current_tick() - last_tick)
    if (diff > 3*1000000):
      if (status == 0): # Was off
        lighteffects.down()
      else: # Was on
        lighteffects.up()

# Register Button listener
def button(gpio, level, tick):
  global switch_state
  global last_tick
  diff = abs(tick - last_tick)
  last_tick = tick
  if diff > 1000:
    print("Button triggered")
    switch_state = level
    if level == 0:
      thr = threading.Thread(target=dimming, args=(lighteffects.is_on(),), kwargs={})
      thr.start()
      lighteffects.toggle()     

pi.set_pull_up_down(SWITCH, pigpio.PUD_UP)
pi.callback(SWITCH, pigpio.EITHER_EDGE, button)

print("Button registered")

