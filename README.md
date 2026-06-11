# AnemiaAI — دليل النشر الكامل

## هيكل المشروع
```
anemiaai/
├── app.py              ← Flask backend
├── model.pkl           ← نموذج Random Forest المدرّب
├── train_model.py      ← سكريبت تدريب النموذج
├── requirements.txt    ← المكتبات المطلوبة
├── render.yaml         ← إعدادات Render
└── templates/
    └── index.html      ← واجهة المستخدم
```

---

## 1. التشغيل المحلي

```bash
# تثبيت المكتبات
pip install -r requirements.txt

# تدريب النموذج (مرة واحدة فقط)
python train_model.py

# تشغيل الخادم
python app.py
# افتح: http://localhost:5000
```

---

## 2. النشر على Render

### الخطوات:

1. **ارفع المشروع على GitHub**
   ```bash
   git init
   git add .
   git commit -m "initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/anemiaai.git
   git push -u origin main
   ```

2. **أنشئ Web Service على Render**
   - اذهب إلى [render.com](https://render.com) → New → Web Service
   - اربطه بـ GitHub repo
   - الإعدادات تُملأ تلقائياً من `render.yaml`

3. **أضف ANTHROPIC_API_KEY**
   - في لوحة Render → Environment → Add Variable
   - Key: `ANTHROPIC_API_KEY`
   - Value: مفتاح API الخاص بك من [console.anthropic.com](https://console.anthropic.com)

4. **Deploy!** ✅

---

## المتغيرات البيئية المطلوبة

| المتغير | الوصف |
|---------|-------|
| `ANTHROPIC_API_KEY` | مفتاح Anthropic API — أضفه في Render يدوياً |

---

## ملاحظة أمان
- مفتاح API يُرسل من الخادم فقط (route `/ai-insight`) ولا يُكشف للمتصفح أبداً ✅
- التنبؤ يتم محلياً في الخادم بواسطة `model.pkl` بدون اتصال خارجي ✅
