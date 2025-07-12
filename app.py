from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


"""
giesszeit = "07:00"
email_aktiviert = False
email_adresse = ""
fuellstand_absolut = "1.5 L"
fuellstand_relativ = "75 %"
giessmenge = "22 °C"
luftfeuchtigkeit = "60 %"
"""

"""
    Reads the current state from 'state_variables.json'.
    Returns a dictionary with stored values or empty if error.
"""


def get_state_values():
    try:
        with open("state_variables.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Flask] Failed to read JSON: {e}")
        return {}


# --- Routes (Web Pages / API Endpoints) ---


@app.route("/", methods=["GET"])
# Main page: reads current values from JSON and passes them to the HTML template for display.
def index():
    state = get_state_values()

    # Reading data from state_variables file and assigning them to python variable to show them in
    # the UI.
    return render_template(
        "index.html",
        giesszeit=state.get("WATERING_TIME", "Nicht gesetzt"),
        email=state.get("EMAIL_ADDRESS", "Nicht gesetzt"),
        fuellstand_absolut=state.get("ABSOLUTE_FILL_STAND", "N/A"),
        fuellstand_relativ=state.get("RELATIVE_FILL_STAND", "N/A"),
        giessmenge=state.get("FILL_QUANTITY", "N/A"),
        luftfeuchtigkeit=state.get("RELATIVE_MOISTURE", "N/A"),
    )


# Sets a new watering time based on the user input.
# Updates the variable WATERING_TIME JSON state file. Triggered via a form POST request.
@app.route("/set_giesszeit", methods=["POST"])
def set_giesszeit():
    # Getting the watering time from the HTML form (index.html)
    new_time = request.form.get("giesszeit")
    if new_time:
        # Try to load the current state from JSON file
        try:
            with open("state_variables.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            # If file doesn't exist, start with an empty dictionary
            data = {}

        # Update watering time value
        data["WATERING_TIME"] = new_time
        # Saving watering time value in state_variables file
        try:
            with open("state_variables.json", "w") as f:
                json.dump(data, f, indent=4)
            print(f"[Flask] New watering time set: {new_time}")
        except Exception as e:
            print(f"[Flask] Error saving watering time to state_variables.json: {e}")

    return redirect(url_for("index"))


# Sets a new fill quantity based on the user input.
# Updates the variable FILL_QUANTITY in the JSON state file. Triggered via a form POST request.
@app.route("/set_fill_quantity", methods=["POST"])
def set_fill_quantity():
    # Getting the fill quantity from the HTML form (index.html)
    new_fill_quantity = request.form.get("fill_quantity")
    if new_fill_quantity:
        try:
            # Try to load the current state from JSON file
            with open("state_variables.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            # If file doesn't exist, start with an empty dictionary
            data = {}

        # Update fill quantity value
        data["FILL_QUANTITY"] = int(new_fill_quantity)

        # Save updated value back to JSON file
        try:
            with open("state_variables.json", "w") as f:
                json.dump(data, f, indent=4)
            print(f"[Flask] New fill quantity set: {new_fill_quantity}")
        except Exception as e:
            print(f"[Flask] Error saving fill quantity to state_variables.json: {e}")

    return redirect(url_for("index"))


# Saves a new email address for notifications.
# Updates the variable EMAIL_ADDRESS in the JSON state file. Triggered via a form POST request.
@app.route("/activate_email", methods=["POST"])
def activate_email():
    # Getting the email address from the HTML form (index.html)
    new_email = request.form.get("email")
    if new_email:
        try:
            # Try to load the current state from JSON file
            with open("state_variables.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        # Update email address
        data["EMAIL_ADDRESS"] = new_email

        try:
            with open("state_variables.json", "w") as f:
                json.dump(data, f, indent=4)
            print(f"[Flask] New fill quantity set: {new_email}")
        except Exception as e:
            print(f"[Flask] Error saving e-mail to state_variables.json: {e}")

    return redirect(url_for("index"))


# Resets the fill level back to full (after refilling the water tank).
# Sets default values for ABSOLUTE_FILL_STAND and RELATIVE_FILL_STAND in the JSON state file.
@app.route("/reset_fueller", methods=["POST"])
def reset_fueller():
    new_absolute = 20000  # Absolute value in milliliters (example: 20,000 ml)
    new_relative = 100  # Relative fill level in percent
    try:
        # Load the current state from JSON
        with open("state_variables.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    # Set new fill level values
    data["ABSOLUTE_FILL_STAND"] = new_absolute
    data["RELATIVE_FILL_STAND"] = new_relative

    # Save the updated values to the JSON file
    try:
        with open("state_variables.json", "w") as f:
            json.dump(data, f, indent=4)
        print(f"[Flask] Fill quantity reseted")
    except Exception as e:
        print(f"[Flask] Error saving fill stand to state_variables.json: {e}")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
