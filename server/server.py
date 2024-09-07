from flask import Flask, request, jsonify
import util
import tracemalloc
tracemalloc.start()

app = Flask(__name__)

from flask_cors import CORS
CORS(app)  

@app.route('/test_prediction')
def test_prediction():
    try:
        result = util.get_estimated_price(2, 1200, 0.500000, 'Super Area', 'location_name', 'city_name', 'Semi-Furnished', 'Family', 2, 'Contact Owner')
        return f"Test Prediction Result: {result}"
    except Exception as e:
        return f"Error: {e}"

@app.route('/hello')
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        no_of_bhk = float(request.form['bhk'])
        size = float(request.form['size'])
        import numpy as np
        floor = np.float64(request.form['floor'])
        area_type = request.form['area_type']
        area_location = request.form['area_location']
        city = request.form['city']
        furnishing_status = request.form['furnishing_status']
        tenant_preferred = request.form['tenant_preferred']
        bathroom = float(request.form['bathroom'])
        point_of_contact = request.form['point_of_contact']

        estimated_price = util.get_estimated_price(
            no_of_bhk, size, floor, area_type, area_location, city, furnishing_status,
            tenant_preferred, bathroom, point_of_contact
        )

        response = {
            'estimated_price': estimated_price
        }

        return jsonify(response),200

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
