from flask import Flask, render_template, request, jsonify
import numpy as np
import json

from ByeBots import ByeBots
bb = ByeBots()

from CryptoProtection import CryptoProtection
cp = CryptoProtection()

# App launch
app = Flask(__name__)


@app.route('/')
def index():
    production_mode = True
    return render_template('index.html', production_mode=production_mode)

@app.route('/getPublicKey', methods=['GET'])
def get_public_key():
    return jsonify({"public_key": cp.get_public_key_pem()})

@app.route('/validateFingerprint', methods=['POST'])
def validate_fingerprint():
    data = request.get_json()
    if not all(k in data for k in ('encrypted_key', 'ciphertext', 'nonce', 'tag')):
        return jsonify({"error": "Missing encryption parameters"}), 400

    try:
        encrypted_aes_key = bytes.fromhex(data['encrypted_key'])
        aes_key = cp.decrypt_aes_key(encrypted_aes_key)
        decrypted_json_str = cp.aes_decrypt(data['ciphertext'],
                                            data['nonce'],
                                            data['tag'],
                                            aes_key)
        decrypted_data = json.loads(decrypted_json_str)
        fingerprint_data = decrypted_data.get('fingerprint')
        fingerprint = json.dumps(fingerprint_data)
        result = bb.validateFingerprint(fingerprint)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Define weights
WEIGHTS = {
    "avg_speed": 0.20,  # Humans tend to move at a consistent speed.
    "acceleration": 0.10,  # Less influence, as sudden acceleration can happen in both humans & bots.
    "jerk": 0.12,  # Still relevant, but reduced impact.
    "curvature": 0.15,  # Less weight, as human movement varies.
    "straightness": 0.15,  # Humans usually prefer straight paths.
    "jitter": 0.15,  # High jitter is a key bot indicator.
    "direction_changes": 0.13  # Moderate influence.
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

        # Compute weighted score for each instance
        instance_scores = np.dot(data_matrix, list(WEIGHTS.values()))

        # Compute the final score as an average of all weighted instance scores
        weighted_score = np.mean(instance_scores)  # Compute mean of weighted scores per instance

        # Categorization
        if weighted_score > 70:
            category = "Advanced Bot (Human-like)"
        elif 50 <= weighted_score < 70:
            category = "Intermediate Bot"
        else:
            category = "Basic Bot"

        return jsonify({"weighted_score": round(weighted_score, 2), "category": category})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
