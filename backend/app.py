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

@app.route('/check-url', methods=['POST'])
def check_url():
    data = request.get_json() or {}
    url = data.get('url', '')
    
    if not url:
        return jsonify({"error": "url is required"}), 400
        
    risk_score = 0
    reasons = []
    
    # Rule 1: http vs https
    if url.startswith('http://'):
        risk_score += 30
        reasons.append("Uses unsecured HTTP connection.")
    elif not url.startswith('https://'):
        risk_score += 10
        reasons.append("Missing standard HTTPS protocol.")
        
    # Rule 2: Suspicious keywords
    url_lower = url.lower()
    suspicious_keywords = ['login', 'verify', 'update', 'secure', 'account', 'banking', 'free', 'bonus', 'admin']
    for keyword in suspicious_keywords:
        if keyword in url_lower:
            risk_score += 15
            reasons.append(f"Contains suspicious keyword: '{keyword}'.")
            
    # Rule 3: Long URLs
    if len(url) > 75:
        risk_score += 20
        reasons.append("Unusually long URL length.")
        
    # Rule 4: Multiple hyphens
    if url.count('-') > 3:
        risk_score += 15
        reasons.append("Multiple hyphens often indicate deceptive domains.")
        
    # Cap score at 100
    risk_score = min(risk_score, 100)
    
    is_phishing = risk_score >= 60
    
    explanation = " ".join(reasons) if reasons else "No suspicious patterns detected."
    
    return jsonify({
        "is_phishing": is_phishing,
        "risk_score": risk_score,
        "explanation": explanation
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
