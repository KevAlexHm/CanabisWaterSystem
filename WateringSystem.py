import schedule
import smtplib
import time
import ssl
import SupplyEnergy
import SystemTime as ST
import EmailNotifier
import datetime

WATERING_TIME = "11:59:50 AM"
SECONDS_TO_WATER = 10

Transistor = SupplyEnergy.Transitor(2, True)


def water_plant(transistor, seconds):
    print(f"Function water plant called")

    transistor.on()
    print("Plant is being watered!")
    time.sleep(seconds)
    print("Watering is finished!")
    transistor.off()
    print(f"Function water finished")


def main():

    time_checker = ST.SystemTime(ST.SystemTime.get_current_time())
    print(f"Current system time, {time_checker.current_time}")

    try:
        current_dt = datetime.datetime.strptime(
            time_checker.current_time, "%I:%M:%S %p"
        )
        user_dt = datetime.datetime.strptime(WATERING_TIME, "%I:%M:%S %p")

        print(f"Comparing: , {current_dt} and {user_dt}!")

        if current_dt == user_dt:
            print(f"Entered to if condition : , {WATERING_TIME}!")
            water_plant(Transistor, SECONDS_TO_WATER)
    except:
        print("Invalid time format. Please use HH:MM:SS AM/PM.")

    # time_checker.set_time_last_watered(ST.SystemTime.get_current_time())
    # print("\nPlant was last watered at {}".format(time_checker.time_last_watered))
    #   EmailNotifier.EmailNotifier.send_last_watered_email(
    #      time_checker.time_last_watered)


# Getting data from the user
# WATERING_TIME = input("Write the time to water your plant")
# How man times do you want to water your plant, per day, week, month?

WATERING_TIME = input("Enter a time (HH:MM:SS AM/PM): ")


while True:
    schedule.run_pending()
    time.sleep(1)
    main()
