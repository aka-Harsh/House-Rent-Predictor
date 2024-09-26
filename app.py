from flask import Flask, render_template, request, jsonify
from model import load_data, preprocess_data, train_model, predict_rent, get_recommendations

app = Flask(__name__)

# Load and preprocess data
df = load_data()
X, y, le_city, le_area = preprocess_data(df)

# Train the model
model = train_model(X, y)

@app.route('/')
def index():
    cities = df['city'].unique().tolist()
    return render_template('index.html', cities=cities)

@app.route('/get_areas', methods=['POST'])
def get_areas():
    city = request.json['city']
    areas = df[df['city'] == city]['area'].unique().tolist()
    return jsonify(areas)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    city = data['city']
    area = data['area']
    rooms = int(data['rooms'])
    bathrooms = int(data['bathrooms'])
    budget = data['budget']

    predicted_rent = predict_rent(model, le_city, le_area, city, area, rooms, bathrooms)
    recommendations = get_recommendations(df, city, rooms, bathrooms, budget)

    return jsonify({
        'predicted_rent': predicted_rent,
        'recommendations': recommendations
    })

if __name__ == '__main__':
    app.run(debug=True)