from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Beispielhafte Zustände
giesszeit = "07:00"
email_aktiviert = False
email_adresse = ""
fuellstand_absolut = "1.5 L"
fuellstand_relativ = "75 %"
temperatur = "22 °C"
luftfeuchtigkeit = "60 %"


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        giesszeit=giesszeit,
        email=email_adresse if email_aktiviert else "Nicht aktiviert",
        fuellstand_absolut=fuellstand_absolut,
        fuellstand_relativ=fuellstand_relativ,
        temperatur=temperatur,
        luftfeuchtigkeit=luftfeuchtigkeit,
    )


# Getting the watering time
@app.route("/set_giesszeit", methods=["POST"])
def set_giesszeit():
    new_time = request.form.get("giesszeit")
    if new_time:
        try:
            with open("state_variables.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        data["WATERING_TIME"] = new_time

        with open("state_variables.json", "w") as f:
            json.dump(data, f, indent=4)
        print(f"[Flask] New watering time set: {new_time}")
    return redirect(url_for("index"))


@app.route("/set_fill_quantity", methods=["POST"])
def set_fill_quantity():
    new_fill_quantity = request.form.get("fill_quantity")
    if new_fill_quantity:
        try:
            with open("state_variables.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        data["FILL_QUANTITY"] = new_fill_quantity

        with open("state_variables.json", "w") as f:
            json.dump(data, f, indent=4)
        print(f"[Flask] New fill quantity set: {new_fill_quantity}")
    return redirect(url_for("index"))


@app.route("/activate_email", methods=["POST"])
def activate_email():
    new_email = request.form.get("email")
    if new_email:
        try:
            with open("state_variables.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        data["EMAIL_ADDRESS"] = new_email

        with open("state_variables.json", "w") as f:
            json.dump(data, f, indent=4)
        print(f"[Flask] New fill quantity set: {new_email}")
    return redirect(url_for("index"))


@app.route("/reset_fueller", methods=["POST"])
def reset_fueller():
    new_absolute = "20 L"
    new_relative = "100 %"
    try:
        with open("state_variables.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    data["ABSOLUTE_FILL_STAND"] = new_absolute
    data["RELATIVE_FILL_STAND"] = new_relative

    with open("state_variables.json", "w") as f:
        json.dump(data, f, indent=4)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
