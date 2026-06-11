"""
train_model.py — تدريب نموذج التنبؤ بفقر الدم
البيانات: dataset مختبر بنغازي (CBC)
"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.impute import SimpleImputer
import pickle, os

# تحميل البيانات
df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'cbc_dataset_clean__1_.csv'), sep=';'
)

# ترميز الجنس
df['Gender'] = df['Gender'].map({'M': 1, 'F': 0})

X = df[['Gender', 'Hemoglobin', 'MCH', 'MCHC', 'MCV']]
y = df['Result']

# معالجة القيم المفقودة
imp = SimpleImputer(strategy='median')
X_imp = imp.fit_transform(X)

# تقسيم البيانات
X_train, X_test, y_train, y_test = train_test_split(
    X_imp, y, test_size=0.2, random_state=42, stratify=y
)

# تدريب النموذج
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# تقييم النموذج
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# حفظ النموذج والـ imputer معاً
with open(os.path.join(os.path.dirname(__file__), 'model.pkl'), 'wb') as f:
    pickle.dump({'model': model, 'imputer': imp}, f)

print("✅ model.pkl saved")
