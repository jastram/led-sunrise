import time
import pigpio
import lighteffects
import threading

SWITCH = 4 # GPIO 4 / Pin 7

# global variable to protect against chatter
last_tick = 0

# global variable to track switch state
switch_state = 1

# global variable of active dimming thread
dimming_thread = None

# Reference to pi
pi = pigpio.pi()

# Wait for button release 
def dimming(status):
  global last_tick
  lighteffects.toggle()
  while switch_state == 0: # Stop once released
    time.sleep(0.05) # Dimming speed
    diff = abs(pi.get_current_tick() - last_tick)
    if (diff > 1.7*1000000): # Wait for a little
      if (status == 0): # Was off
        lighteffects.down()
      else: # Was on
        lighteffects.up()

# Register Button listener
def button(gpio, level, tick):
  global button_running
  global switch_state
  global last_tick
  global dimming_thread
  diff = abs(tick - last_tick)
  last_tick = tick
  if diff > 1000 and level != switch_state:
    print("Button triggered: " + str(level) + " - " + str(diff))
    switch_state = level
    if level == 0:
      if dimming_thread == None or not dimming_thread.is_alive():
        dimming_thread = threading.Thread(target=dimming, args=(lighteffects.is_on(),), kwargs={})
        dimming_thread.start()
      else:
        print("Skipping Dimming")

pi.set_pull_up_down(SWITCH, pigpio.PUD_UP)
pi.callback(SWITCH, pigpio.EITHER_EDGE, button)

print("Button registered")

