from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load trained model
model = joblib.load("transformer_model.pkl")

@app.route('/')
def home():
    return "Transformer AI API Running"

@app.route('/predict', methods=['POST'])
def predict():

    data = request.json

    sample = [[
        data['Primary Voltage (V)'],
        data['Primary Current (A)'],
        data['Primary Power (W)'],
        data['Primary PF'],
        data['Primary Energy (kWh)'],
        data['Primary Frequency (Hz)'],

        data['Secondary Voltage (V)'],
        data['Secondary Current (A)'],
        data['Secondary Power (W)'],
        data['Secondary PF'],
        data['Secondary Energy (kWh)'],
        data['Secondary Frequency (Hz)'],

        data['Efficiency (%)'],
        data['Losses (W)']
    ]]

    prediction = model.predict(sample)[0]

    return jsonify({
        "prediction": str(prediction)
    })

if __name__ == '__main__':
    app.run(debug=True)