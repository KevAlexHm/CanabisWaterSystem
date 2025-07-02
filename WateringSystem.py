import schedule
import smtplib
import time
import ssl
import SupplyEnergy
import SystemTime as ST
import EmailNotifier
import datetime
import time

# import board
# import adafruit_dht
import json

WATERING_TIME = "11:59:50 AM"
SECONDS_TO_WATER = 10
FILL_QUANTITY = ""
EMAIL_ADDRESS = ""
# dht_device = adafruit_dht.DHT11(board.D15)


# Transistor = SupplyEnergy.Transitor(2, True)


def water_plant(transistor, seconds):
    print(f"Function water plant called")

    transistor.on()
    print("Plant is being watered!")
    time.sleep(seconds)
    print("Watering is finished!")
    transistor.off()
    print(f"Function water finished")

    read_sensor_data()


def main():
    # read Data from file
    time_checker = ST.SystemTime(ST.SystemTime.get_current_time())
    # print(f"Current system time, {time_checker.current_time}")
    state_values = get_state_variables()
    WATERING_TIME = state_values.get("WATERING_TIME", "")
    FILL_QUANTITY = state_values.get("FILL_QUANTITY", "")
    EMAIL_ADDRESS = state_values.get("EMAIL_ADDRESS", "")

    print(f"Current, {EMAIL_ADDRESS}")
    """
    try:
        current_dt = datetime.datetime.strptime(
            time_checker.current_time, "%I:%M:%S %p"
        )
        user_dt = datetime.datetime.strptime(WATERING_TIME, "%I:%M:%S %p")

        print(f"Comparing: , {current_dt} and {user_dt}!")

        if current_dt == user_dt:
            # print(f"Entered to if condition : , {WATERING_TIME}!")
            water_plant(Transistor, SECONDS_TO_WATER)
    except:
        print("Invalid time format. Please use HH:MM:SS AM/PM.")
    """
    # time_checker.set_time_last_watered(ST.SystemTime.get_current_time())
    # print("\nPlant was last watered at {}".format(time_checker.time_last_watered))
    #   EmailNotifier.EmailNotifier.send_last_watered_email(
    #      time_checker.time_last_watered)


"""
def read_sensor_data():
    print(f"Function sensor data started")
    while True:
        try:
            # Read temperature (Celsius)
            temperature_c = dht_device.temperature
            # Read humidity (%)
            humidity = dht_device.humidity
            print(f"Temp: {temperature_c:.1f} C  Humidity: {humidity}%")
            # To-Do: call e-mail function here

            break
        except Exception as e:
            print("Reading from DHT11 failed:", e)
        time.sleep(2)  # Wait 2 seconds before next reading
    print(f"Function sensor data finished")

"""


def get_state_variables():
    try:
        with open("state_variables.json", "r") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"[System] Failed to read state variables file: {e}")
        return ""


# How man times do you want to water your plant, per day, week, month?

# WATERING_TIME = input("Enter a time in this format: (HH:MM:SS AM/PM): ")

main()
"""
while True:
    schedule.run_pending()
    time.sleep(1)
    main()
"""

# https://realpython.com/pysimplegui-python/
# https://realpython.com/python-gui-tkinter/#making-your-applications-interactive
# https://www.pythonguis.com/tutorials/create-gui-tkinter/
# https://medium.com/@fareedkhandev/modern-gui-using-tkinter-12da0b983e22
