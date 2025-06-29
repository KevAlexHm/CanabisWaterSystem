import schedule
import smtplib
import time
import ssl
import SupplyEnergy
import SystemTime as ST
import EmailNotifier

WATERING_TIME = "11:59:50 AM"
SECONDS_TO_WATER = 10

Transistor = SupplyEnergy.Transitor(12, False)


def water_plant(transistor, seconds):
    transistor.on()
    print("Plant is being watered!")
    time.sleep(seconds)
    print("Watering is finished!")
    transistor.off()


def main():
    time_checker = ST.SystemTime(ST.SystemTime.get_current_time())
    if time_checker.current_time == WATERING_TIME:
        water_plant(Transistor, SECONDS_TO_WATER)
        time_checker.set_time_last_watered(ST.SystemTime.get_current_time())
        print("\nPlant was last watered at {}".format(time_checker.time_last_watered))
        EmailNotifier.EmailNotifier.send_last_watered_email(
            time_checker.time_last_watered
        )


while True:
    # schedule.run_pending()
    time.sleep(30)
    main()
