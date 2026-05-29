from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_text_risk(text):
    if not text:
        return 0
    risk_score = 0
    text_lower = text.lower()
    keywords = ['otp', 'urgent', 'click', 'verify', 'password', 'bank', 'account', 'blocked', 'winner', 'lottery']
    for keyword in keywords:
        if keyword in text_lower:
            risk_score += 20
    return min(risk_score, 100)

def get_url_risk(url):
    if not url:
        return 0, []
    risk_score = 0
    reasons = []
    
    if url.startswith('http://'):
        risk_score += 30
        reasons.append("Uses unsecured HTTP connection.")
    elif not url.startswith('https://'):
        risk_score += 10
        reasons.append("Missing standard HTTPS protocol.")
        
    url_lower = url.lower()
    suspicious_keywords = ['login', 'verify', 'update', 'secure', 'account', 'banking', 'free', 'bonus', 'admin']
    for keyword in suspicious_keywords:
        if keyword in url_lower:
            risk_score += 15
            reasons.append(f"Contains suspicious keyword: '{keyword}'.")
            
    if len(url) > 75:
        risk_score += 20
        reasons.append("Unusually long URL length.")
        
    if url.count('-') > 3:
        risk_score += 15
        reasons.append("Multiple hyphens often indicate deceptive domains.")
        
    return min(risk_score, 100), reasons

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"})

@app.route('/check-fraud', methods=['POST'])
def check_fraud():
    data = request.get_json() or {}
    text = data.get('text', '')
    
    risk_score = get_text_risk(text)
    
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
        
    risk_score, reasons = get_url_risk(url)
    is_phishing = risk_score >= 60
    explanation = " ".join(reasons) if reasons else "No suspicious patterns detected."
    
    return jsonify({
        "is_phishing": is_phishing,
        "risk_score": risk_score,
        "explanation": explanation
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json() or {}
    text = data.get('text', '')
    url = data.get('url', '')
    
    if not text and not url:
        return jsonify({"error": "Provide at least text or url"}), 400
        
    text_score = get_text_risk(text)
    url_score, url_reasons = get_url_risk(url)
    
    combined_score = min(text_score + url_score, 100)
    
    if combined_score >= 70:
        risk_level = "HIGH"
        message = "Warning! High risk of fraud detected. Do not proceed."
    elif combined_score >= 40:
        risk_level = "MEDIUM"
        message = "Caution! Suspicious elements found. Please verify the source."
    else:
        risk_level = "LOW"
        message = "Looks safe! No significant threat detected."
        
    if url_reasons:
        message += " URL flags: " + " ".join(url_reasons)
        
    return jsonify({
        "risk_score": combined_score,
        "risk_level": risk_level,
        "warning_message": message
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
