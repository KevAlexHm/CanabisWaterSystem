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


@app.route("/set_giesszeit", methods=["POST"])
def set_giesszeit():
    global giesszeit
    giesszeit = request.form.get("giesszeit")

    new_time = request.form.get("giesszeit")
    if new_time:
        with open("state_variables.json", "w") as f:
            json.dump({"WATERING_TIME_STATE": new_time}, f)
        print(f"[Flask] New watering time set: {new_time}")
    return redirect(url_for("index"))


@app.route("/activate_email", methods=["POST"])
def activate_email():
    global email_aktiviert, email_adresse
    email_adresse = request.form.get("email")
    email_aktiviert = True
    print(f"E-Mail aktiviert: {email_adresse}")
    return redirect(url_for("index"))


@app.route("/reset_fueller", methods=["POST"])
def reset_fueller():
    global fuellstand_absolut, fuellstand_relativ
    # Beispielhafte Rücksetzung
    fuellstand_absolut = "2.0 L"
    fuellstand_relativ = "100 %"
    print("Füllstand zurückgesetzt")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
