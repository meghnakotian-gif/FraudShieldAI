from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"})

@app.route('/check-fraud', methods=['POST'])
def check_fraud():
    data = request.get_json() or {}
    text = data.get('text', '')
    
    risk_score = 0
    if text:
        text_lower = text.lower()
        # Simple rule-based logic keywords
        keywords = ['otp', 'urgent', 'click', 'verify', 'password', 'bank', 'account', 'blocked', 'winner', 'lottery']
        
        for keyword in keywords:
            if keyword in text_lower:
                risk_score += 20
                
        # Cap score at 100
        risk_score = min(risk_score, 100)
        
    if risk_score >= 70:
        risk_level = "HIGH"
    elif risk_score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
        
    return jsonify({
        "risk_score": risk_score,
        "risk_level": risk_level
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
