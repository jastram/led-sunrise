import time
import pigpio
import lighteffects
import switch

from apscheduler.schedulers.background import BackgroundScheduler

# For Testing
def quicksun():
   lighteffects.cycle(10, lighteffects.sunrise)
   lighteffects.fade_off()

# Wakeup Sunrise
def morning():
   lighteffects.cycle(30*60, lighteffects.sunrise)
   
# Start the scheduler
sched = BackgroundScheduler()
sched.start()

#sched.add_job(quicksun, 'cron', second=00)
# sched.add_job(morning, 'cron', hour=6, minute=15, second=00, day_of_week='mon-fri')
sched.add_job(morning, 'cron', hour=6, minute=45, second=00, day_of_week='mon-fri')
sched.add_job(morning, 'cron', hour=9, minute=30, second=00, day_of_week='sat-sun')
     
# Event-Driven program: Wait forever
while True:
  time.sleep(60)

# Turn off
#lighteffects.cycle(2, lighteffects.fade);
