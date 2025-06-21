# from flask import Flask, request, jsonify
# import joblib
# from feature_extractor import extract_features_from_url_full  # or define in same file
# import os

# app = Flask(__name__)

# # Load model and scaler
# model = joblib.load('rf_model.pkl')
# scaler = joblib.load('scaler.pkl')

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json()

#     if 'url' not in data:
#         return jsonify({'error': 'URL not provided'}), 400

#     url = data['url']
#     opr_api_key = os.getenv('OPR_API_KEY', '')  # Optional API key
#     try:
#         features = extract_features_from_url_full(url, opr_api_key)
#         features_scaled = scaler.transform([features])
#         prediction = model.predict(features_scaled)[0]
#         result = 'Phishing' if prediction == 1 else 'Legit'
#         return jsonify({'prediction': result})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)





from flask import Flask, request, jsonify
import joblib
from feature_extractor import extract_features_from_url_full
import os

app = Flask(__name__)

# Load model and scaler
model = joblib.load('rf_model.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Check for 'urls' list
    if 'urls' not in data or not isinstance(data['urls'], list):
        return jsonify({'error': 'Please provide a list of URLs under the "urls" key'}), 400

    urls = data['urls']
    opr_api_key = os.getenv('OPR_API_KEY', '')  # Optional API key

    feature_list = []
    valid_urls = []
    errors = []

    for url in urls:
        try:
            features = extract_features_from_url_full(url, opr_api_key)
            feature_list.append(features)
            valid_urls.append(url)
        except Exception as e:
            errors.append({'url': url, 'error': str(e)})

    # If none succeeded
    if not feature_list:
        return jsonify({'error': 'Feature extraction failed for all URLs', 'details': errors}), 500

    try:
        features_scaled = scaler.transform(feature_list)
        predictions = model.predict(features_scaled)
        results = []

        for url, pred in zip(valid_urls, predictions):
            results.append({
                'url': url,
                'prediction': 'Phishing' if pred == 0 else 'Legit'
            })

        return jsonify({
            'results': results,
            'errors': errors  # include any URLs that failed
        })

    except Exception as e:
        return jsonify({'error': 'Prediction failed', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
