from flask import Flask, render_template, request, jsonify
import numpy as np
import json

from ByeBots import ByeBots
bb = ByeBots()


# App launch
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validateFingerprint', methods=['POST'])
def validate_fingerprint():
    data = request.get_json()
    rawFingerprint = data.get('fingerprint')
    fingerprint = json.dumps(data.get('fingerprint'))

    # originalText = open("fingerprint.txt", "r").read()
    # file = open('fingerprint.txt', 'w')
    # file.writelines(originalText + f"{fingerprint}\n")
    # file.close()

    result = bb.validateFingerprint(fingerprint)
    # print(result)

    # validUser = False
    # webdriverSupport = rawFingerprint['webdriver']
    # if(webdriverSupport):
    #     validUser = False
    # else:
    #     fingerprint = json.dumps(data.get('fingerprint'))
    #     result = bb.validateFingerprint(fingerprint, True)
    #     if result['anomaly'] == 'No':
    #         validUser = True
    #     else:
    #         validUser = False

    return {"success": True, "result": result}


# Define weights (you can adjust these based on importance)
WEIGHTS = {
    "avg_speed": 0.15,
    "acceleration": 0.20,
    "jerk": 0.10,
    "curvature": 0.10,
    "straightness": 0.15,
    "jitter": 0.15,
    "direction_changes": 0.15
}


@app.route('/calculateWeightedScore', methods=['POST'])
def calculate_weighted_score():
    data = request.get_json()
    instances = data.get("instances", [])

    if not instances:
        return jsonify({"error": "No data received"}), 400

    try:
        # Convert data to NumPy array
        data_matrix = np.array([[instance[key] for key in WEIGHTS.keys()] for instance in instances])

        # Compute mean values across all instances
        avg_values = np.mean(data_matrix, axis=0)

        # Compute weighted score
        weighted_score = np.dot(avg_values, list(WEIGHTS.values()))

        print(weighted_score)

        # Categorization
        if weighted_score >= 80:
            category = "Human-like"
        elif 50 <= weighted_score < 80:
            category = "Intermediate Bot"
        else:
            category = "Basic Bot"

        print(category)

        return jsonify({"weighted_score": round(weighted_score, 2), "category": category})
        # return jsonify({
        #     "weighted_score": round(weighted_score, 2),
        #     "category": category
        # })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
