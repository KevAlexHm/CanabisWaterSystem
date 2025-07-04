import schedule
import smtplib
import time
import ssl
import SupplyEnergy
import SystemTime as ST
import email_notifier
import datetime
import time
import json

# ----- Uncomment this for RPGiS
"""
import board
import adafruit_dht
"""
WATERING_TIME = "11:59:50 AM"

# ----- This needs to follow the equation set by Lion
SECONDS_TO_WATER = 10
FILL_QUANTITY = ""
# -----  Uncomment this for RPGiS
"""
dht_device = adafruit_dht.DHT11(board.D14)
Transistor = SupplyEnergy.Transitor(15, True)
"""
last_watered_time = None
email_notifier.notifier = email_notifier.EmailNotifier()


def water_plant(transistor, seconds):
    print(f"[System]Function water plant called")

    # -----  Uncomment this for RPGiS
    """
    Add a try catch here, only if this works the writing in the JSON file
    and the read sensor data + E-mail should work
    transistor.on()
    print("Plant is being watered!")
    time.sleep(seconds)
    print("Watering is finished!")
    transistor.off()
    print(f"Function water finished")
    """
    # -----  This value needs to come from the calculation Giessdauer = ... (UPDATE)
    new_absolute = "10 L"
    new_relative = "50 %"
    try:
        with open("state_variables.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    data["ABSOLUTE_FILL_STAND"] = new_absolute
    data["RELATIVE_FILL_STAND"] = new_relative

    try:
        with open("state_variables.json", "w") as f:
            json.dump(data, f, indent=4)
        print(f"[System] Fill quantities reseted")
    except Exception as e:
        print(f"[System] Error saving fill stand to state_variables.json: {e}")

    read_sensor_data()


def main():
    global last_watered_time

    # read Data from file
    time_checker = ST.SystemTime(ST.SystemTime.get_current_time())
    # print(f"Current system time, {time_checker.current_time}")
    state_values = get_state_variables()
    WATERING_TIME = state_values.get("WATERING_TIME", "")
    FILL_QUANTITY = state_values.get("FILL_QUANTITY", "")
    EMAIL_ADDRESS = state_values.get("EMAIL_ADDRESS", "")
    RELATIVE_MOISTURE = state_values.get("RELATIVE_MOISTURE", "")

    print(f"Current, {WATERING_TIME}")

    # ----- Uncomment this for RPGiS
    """
    
    try:
        current_dt = datetime.datetime.strptime(
            time_checker.current_time, "%I:%M:%S %p"
        )
        user_dt = datetime.datetime.strptime(WATERING_TIME, "%I:%M %p")

        print(f"[System]Comparing times: {current_dt} and {user_dt}!")

        current_time_str = current_dt.strftime("%I:%M %p")
        user_time_str = user_dt.strftime("%I:%M %p")
        # (UPDATE) Add conditional if ABSOLUTE_FILL_STAND > FILL_QUANTITY: do watering, else send e-mail to user

        if current_time_str == user_time_str:
            if last_watered_time != user_time_str:
                print(
                    f"[System]Watering time & system time are equal: , {WATERING_TIME}!"
                )
                water_plant(Transistor, SECONDS_TO_WATER)
                last_watered_time = user_time_str
            else:
                print(f"[System] Already watered at {user_time_str}. Skipping.")
        else:
            last_watered_time = None
    except Exception as e:
        print(f"[System] Invalid time format or error: {e}")
    """

    # time_checker.set_time_last_watered(ST.SystemTime.get_current_time())
    # print("\nPlant was last watered at {}".format(time_checker.time_last_watered))
    #   EmailNotifier.EmailNotifier.send_last_watered_email(
    #      time_checker.time_last_watered)


def read_sensor_data():
    print(f"[System]Function sensor data started")

    # ----- Uncomment this for RPGiS
    """
    while True:
        try:
            # Read temperature (Celsius)
            temperature_c = dht_device.temperature
            # Read humidity (%)
            humidity = dht_device.humidity
            print(f"[Raspberry] Temp: {temperature_c:.1f} C  Humidity: {humidity}%")
            # To-Do: call e-mail function here

            break
        except Exception as e:
            print("[System] Reading from DHT11 failed:", e)
        time.sleep(2)  # Wait 2 seconds before next reading
    """

    # -----  This value needs to come from the sensor (UPDATE)
    new_relative_moisture = str("humidity") + " %"
    try:
        with open("state_variables.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    data["RELATIVE_MOISTURE"] = new_relative_moisture

    try:
        with open("state_variables.json", "w") as f:
            json.dump(data, f, indent=4)
        print(f"[System]  Moisture value updated")
    except Exception as e:
        print(f"[System] Error saving moisture to state_variables.json: {e}")

    print(f"[System] Function sensor data finished")

    state_values = get_state_variables()
    WATERING_TIME = state_values.get("WATERING_TIME", "")
    FILL_QUANTITY = state_values.get("FILL_QUANTITY", "")
    EMAIL_ADDRESS = state_values.get("EMAIL_ADDRESS", "")
    RELATIVE_MOISTURE = state_values.get("RELATIVE_MOISTURE", "")

    email_notifier.notifier.send_email(
        receiver_email=EMAIL_ADDRESS,
        subject="Warning: Low Water Level",
        body=f"Deine Cannabis-Pflanze wurde erfolgreich gegossen. Der relative Luftfeuchtigkeit Wert ist: {RELATIVE_MOISTURE}",
    )


def get_state_variables():
    try:
        with open("state_variables.json", "r") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"[System] Failed to read state variables file: {e}")
        return ""


# How man times do you want to water your plant, per day, week, month?

main()
# ----- Uncomment this for RPGiS
"""
while True:
    schedule.run_pending()
    time.sleep(5)
    main()
"""


# https://realpython.com/pysimplegui-python/
# https://realpython.com/python-gui-tkinter/#making-your-applications-interactive
# https://www.pythonguis.com/tutorials/create-gui-tkinter/
# https://medium.com/@fareedkhandev/modern-gui-using-tkinter-12da0b983e22
