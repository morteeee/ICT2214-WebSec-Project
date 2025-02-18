from flask import Flask, render_template, request, jsonify
import sys
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
    print(result)

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

    return {"success": True, "result" : result}

if __name__ == '__main__':
    app.run(debug=True)
