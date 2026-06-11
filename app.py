"""
app.py — AnemiaAI Flask Backend
"""
from flask import Flask, render_template, request, jsonify
import pickle, numpy as np, os

app = Flask(__name__)

# ── Load model ──
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
with open(MODEL_PATH, 'rb') as f:
    saved = pickle.load(f)

# Support both old format (direct model) and new format (dict)
if isinstance(saved, dict):
    model   = saved['model']
    imputer = saved['imputer']
else:
    model   = saved
    imputer = None


# ── Routes ──
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data   = request.get_json(force=True)
        gender = 1 if data.get('gender', 'male') == 'male' else 0
        hb     = float(data['hb'])
        mcv    = float(data['mcv'])
        mch    = float(data['mch'])
        mchc   = float(data['mchc'])

        features = np.array([[gender, hb, mch, mchc, mcv]])  # نفس ترتيب التدريب

        if imputer is not None:
            features = imputer.transform(features)

        pred = int(model.predict(features)[0])
        prob = float(model.predict_proba(features)[0][1])

        return jsonify({
            'anemic':      bool(pred),
            'probability': round(prob * 100, 1),
            'status':      'anemic' if pred else 'healthy'
        })
    except (KeyError, ValueError) as e:
        return jsonify({'error': f'بيانات غير صحيحة: {str(e)}'}), 400


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
