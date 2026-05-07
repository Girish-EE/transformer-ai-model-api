import pyrebase
import joblib
import time

# ---------------- FIREBASE CONFIG ---------------- #

firebaseConfig = {
    "apiKey": "AIzaSyAwJjPAPuq6Q0yY28gdCTIiSe4X2DG4YR0",
    "authDomain": "major-8-240ea.firebaseapp.com",
    "databaseURL": "https://major-8-240ea-default-rtdb.asia-southeast1.firebasedatabase.app",
    "storageBucket": "major-8-240ea.firebasestorage.app",
}



# ---------------- INITIALIZE FIREBASE ---------------- #

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

# ---------------- LOAD AI MODEL ---------------- #

model = joblib.load("transformer_model.pkl")

print("AI Model Loaded Successfully")

# ---------------- REAL-TIME LOOP ---------------- #

while True:

    try:

        # Read Firebase live data
        data = db.child("live_data").get().val()

        print("Received Data:", data)

        # ---------------- READ 14 INPUT FEATURES ---------------- #

        primary_voltage = data["Primary Voltage (V)"]
        primary_current = data["Primary Current (A)"]
        primary_power = data["Primary Power (W)"]
        primary_pf = data["Primary PF"]
        primary_energy = data["Primary Energy (kWh)"]
        primary_frequency = data["Primary Frequency (Hz)"]

        secondary_voltage = data["Secondary Voltage (V)"]
        secondary_current = data["Secondary Current (A)"]
        secondary_power = data["Secondary Power (W)"]
        secondary_pf = data["Secondary PF"]
        secondary_energy = data["Secondary Energy (kWh)"]
        secondary_frequency = data["Secondary Frequency (Hz)"]

        efficiency = data["Efficiency (%)"]
        losses = data["Losses (W)"]

        # ---------------- PREPARE AI INPUT ---------------- #

        sample = [[
            primary_voltage,
            primary_current,
            primary_power,
            primary_pf,
            primary_energy,
            primary_frequency,

            secondary_voltage,
            secondary_current,
            secondary_power,
            secondary_pf,
            secondary_energy,
            secondary_frequency,

            efficiency,
            losses
        ]]

        # ---------------- AI PREDICTION ---------------- #

        prediction = model.predict(sample)[0]

        print("Prediction:", prediction)

        # ---------------- SEND PREDICTION TO FIREBASE ---------------- #

        db.child("prediction").set({
            "status": str(prediction)
        })

    except Exception as e:

        print("Error:", e)

    time.sleep(2)