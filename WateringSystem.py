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
import board
import adafruit_dht

# -----  Uncomment this for RPGiS

# ----- Hardware and state setup -----

# Initialize DHT11 humidity sensor on GPIO pin D14
dht_device = adafruit_dht.DHT11(board.D14)
# Initialize the transistor module on GPIO pin 15
Transistor = SupplyEnergy.Transitor(15, True)

# Email notifier instance
email_notifier.notifier = email_notifier.EmailNotifier()

# Variable to track last time watering occurred (prevents multiple triggers within the same minute)
last_watered_time = None


# Function responsible of Watering the plant using a transistor-controlled pump.
# It updates the absolute and relative fill level in the state_variables JSON file.
def water_plant(transistor, seconds, absolute, relative, quantity):
    print(f"[System]Function water plant called")

    # -----  Uncomment this for RPGiS

    # Add a try catch here, only if this works the writing in the JSON file and the read sensor data + E-mail should work
    transistor.on()
    print("Plant is being watered!")
    time.sleep(seconds)
    print("Watering is finished!")
    transistor.off()
    print(f"Function water finished")

    # Calculate new fill levels after watering
    new_absolute = absolute - quantity
    new_relative = new_absolute / 20000

    # Update state_variables.json with new fill levels
    try:
        with open("state_variables.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    # Assigning new fill values to the varaibles in the JSON file
    data["ABSOLUTE_FILL_STAND"] = new_absolute
    data["RELATIVE_FILL_STAND"] = new_relative

    try:
        with open("state_variables.json", "w") as f:
            json.dump(data, f, indent=4)
        print(f"[System] Fill quantities reseted")
    except Exception as e:
        print(f"[System] Error saving fill stand to state_variables.json: {e}")

    # Calling read sensor data function
    read_sensor_data()


# Main function that checks current system time and triggers watering function if all conditions are met.
def main():
    global last_watered_time

    # Read current time and system state variables from state_variables JSON file
    time_checker = ST.SystemTime(ST.SystemTime.get_current_time())
    # print(f"Current system time, {time_checker.current_time}")
    # Reading values from the JSON file and assigning them to python variables
    state_values = get_state_variables()
    # Getting watering time value from the JSON file
    WATERING_TIME = state_values.get("WATERING_TIME", "")
    # Getting fill quantity value from the JSON file
    FILL_QUANTITY = state_values.get("FILL_QUANTITY", "")
    # Getting absolute fill stand (absolute Füllmenge) value from the JSON file
    ABSOLUTE_FILL_STAND = state_values.get("ABSOLUTE_FILL_STAND", "")
    # Getting relative fill stand (relative Füllmenge) value from the JSON file
    RELATIVE_FILL_STAND = state_values.get("RELATIVE_FILL_STAND", "")
    # Getting E-Mail Address value from the JSON file
    EMAIL_ADDRESS = state_values.get("EMAIL_ADDRESS", "")
    # print(f"Current, {WATERING_TIME}")

    # ----- Uncomment this for RPGiS

    try:
        # Converting both current system time and watering time from user input into comparable format
        current_dt = datetime.datetime.strptime(
            time_checker.current_time, "%I:%M:%S %p"
        )
        user_dt = datetime.datetime.strptime(WATERING_TIME, "%I:%M %p")

        print(f"[System]Comparing times: {current_dt} and {user_dt}!")

        current_time_str = current_dt.strftime("%I:%M %p")
        user_time_str = user_dt.strftime("%I:%M %p")

        # Check if the water tank has enough water (vergleich absolute Füllmenge mit Gießmenge) and it's the right time to water
        if ABSOLUTE_FILL_STAND > FILL_QUANTITY:
            # Checking if current system and watering time are equal
            if current_time_str == user_time_str:
                # Check if last watering time of time is not the same as the one set by the user
                if last_watered_time != user_time_str:
                    print(
                        f"[System]Watering time & system time are equal: , {WATERING_TIME}!"
                    )
                    # Calculate watering duration
                    SECONDS_TO_WATER = (50 + 22.14) / 9.84

                    # Call watering function
                    water_plant(
                        Transistor,
                        SECONDS_TO_WATER,
                        ABSOLUTE_FILL_STAND,
                        RELATIVE_FILL_STAND,
                        FILL_QUANTITY,
                    )
                    # Setting the las time the water function was called to avoid caling the function mor than once per minute
                    last_watered_time = user_time_str
                else:
                    print(f"[System] Already watered at {user_time_str}. Skipping.")
            else:
                last_watered_time = None
        else:
            # Send alert email to the user when water level is too low
            email_notifier.notifier.send_email(
                receiver_email=EMAIL_ADDRESS,
                subject="Deine Pflanze muss gepflegt werden",
                body="Füllmenge vom Wasserbehälter reicht zum Gießen nicht aus, bitte füll die Behälter aus",
            )
    except Exception as e:
        print(f"[System] Invalid time format or error: {e}")


# Reads sensor data from DHT11 and updates the humidity value in the state file.
# Also sends an email to notify that watering was successful.
def read_sensor_data():
    print(f"[System]Function sensor data started")

    # ----- Uncomment this for RPGiS

    while True:
        try:

            # Read humidity from sensor
            humidity = dht_device.humidity
            print(f"[Raspberry] Humidity: {humidity}%")
            # To-Do: call e-mail function here
            break
        except Exception as e:
            print("[System] Reading from DHT11 failed:", e)
        time.sleep(2)  # Wait 2 seconds before next reading

    # Store relative moisture value in JSON state
    new_relative_moisture = str(humidity) + " %"
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

    # Retrieve updated values from state_variable JSON file and send email notification
    state_values = get_state_variables()
    WATERING_TIME = state_values.get("WATERING_TIME", "")
    FILL_QUANTITY = state_values.get("FILL_QUANTITY", "")
    EMAIL_ADDRESS = state_values.get("EMAIL_ADDRESS", "")
    RELATIVE_MOISTURE = state_values.get("RELATIVE_MOISTURE", "")

    # Sending e-mail to the user after succefully watering the plant and reading the humidity data from the sensor
    email_notifier.notifier.send_email(
        receiver_email=EMAIL_ADDRESS,
        subject="Deine Pflanze wurde gepflegt :)",
        body=f"Deine Cannabis-Pflanze wurde erfolgreich gegossen. Der relative Luftfeuchtigkeit Wert ist: {RELATIVE_MOISTURE}",
    )


# Helper function to read state variables from state_variable JSON file.
def get_state_variables():
    try:
        with open("state_variables.json", "r") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"[System] Failed to read state variables file: {e}")
        return ""


# ----- Continuous background loop -----

# Infinite loop to regularly check if watering should happen (every 5 seconds)
while True:
    schedule.run_pending()
    time.sleep(5)
    main()
