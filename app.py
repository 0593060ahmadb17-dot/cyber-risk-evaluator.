import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

st.set_page_config(page_title="نظام الذكاء الاصطناعي لتقييم المخاطر السيبرانية", page_icon="🤖", layout="wide")

st.title("🤖 مشروع تخرج: نموذج الذكاء الاصطناعي لتقييم المخاطر السيبرانية الفردية")
st.write("هذا النظام يعتمد على خوارزميات التعلم الآلي (Random Forest AI Model) لتحليل البيانات الرقمية والسلوكية والتنبؤ بمستوى الخطر السيبراني للأفراد.")

# 1. توليد بيانات تدريبية ذكية (Simulation Dataset for AI Training)
@st.cache_data
def load_training_data():
    np.random.seed(42)
    n_samples = 1000
    # المدخلات: [MFA_Enabled (0/1), OS_Updated (0/1), Breach_Count, Phishing_Click_Rate (%), Public_Wifi_VPN (0/1), Reused_Password (0/1)]
    mfa = np.random.randint(0, 2, n_samples)
    os_up = np.random.randint(0, 2, n_samples)
    breaches = np.random.randint(0, 5, n_samples)
    phishing = np.random.uniform(0, 100, n_samples)
    wifi = np.random.randint(0, 2, n_samples)
    pwd = np.random.randint(0, 2, n_samples)
    
    # حساب مستوى الخطر المستهدف (Target: 0=منخفض، 1=متوسط، 2=مرتفع)
    risk_target = []
    for i in range(n_samples):
        score = (1 - mfa[i])*25 + (1 - os_up[i])*25 + (breaches[i]*5) + (phishing[i]*0.3) + (wifi[i]*15) + (pwd[i]*15)
        if score < 30:
            risk_target.append(0) # منخفض
        elif score < 60:
            risk_target.append(1) # متوسط
        else:
            risk_target.append(2) # مرتفع
            
    df = pd.DataFrame({
        'MFA_Enabled': mfa,
        'OS_Updated': os_up,
        'Breach_Count': breaches,
        'Phishing_Click_Rate': phishing,
        'Public_Wifi_No_VPN': wifi,
        'Reused_Password': pwd,
        'Risk_Level': risk_target
    })
    return df

df_train = load_training_data()

# تدريب نموذج الذكاء الاصطناعي (Machine Learning Model)
X = df_train.drop('Risk_Level', axis=1)
y = df_train['Risk_Level']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

ai_model = RandomForestClassifier(n_estimators=100, random_state=42)
ai_model.fit(X_train, y_train)
y_pred = ai_model.predict(X_test)
model_acc = accuracy_score(y_test, y_pred)

# عرض أداء نموذج الذكاء الاصطناعي في واجهة التطبيق
st.sidebar.header("📊 إحصائيات نموذج الذكاء الاصطناعي")
st.sidebar.success(f"دقة نموذج التنبؤ (AI Accuracy): **{model_acc * 100:.2f}%**")
st.sidebar.info("الخوارزمية المستخدمة: Random Forest Classifier")

# 2. واجهة إدخال بيانات المستخدم الحقيقية للتنبؤ
st.markdown("---")
st.subheader("🎯 محاكاة وإدخال بيانات مستخدم جديد للتنبؤ الذكي")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💻 البيانات الرقمية والفنية")
    mfa_input = st.selectbox("تفعيل المصادقة الثنائية (MFA)", [1, 0], format_func=lambda x: "نعم (آمن)" if x==1 else "لا (غير آمن)")
    os_input = st.selectbox("تحديثات نظام التشغيل والتطبيقات", [1, 0], format_func=lambda x: "محدث باستمرار" if x==1 else "قديم/مهمل")
    breach_input = st.slider("عدد مرات تسريب البريد الإلكتروني (Breach Count)", 0, 10, 1)

with col2:
    st.markdown("### 🧠 البيانات السلوكية البشرية")
    phishing_input = st.slider("منسبة الاستجابة لاختبارات الصيد الإلكتروني (%)", 0.0, 100.0, 20.0)
    wifi_input = st.selectbox("استخدام Wi-Fi عام بدون VPN", [1, 0], format_func=lambda x: "نعم (خطر)" if x==1 else "لا (آمن)")
    pwd_input = st.selectbox("إعادة استخدام كلمات المرور الحساسة", [1, 0], format_func=lambda x: "نعم (خطر)" if x==1 else "لا (فريدة)")

# زر التنبؤ بالذكاء الاصطناعي
if st.button("🔍 تحليل المخاطر باستخدام نموذج الذكاء الاصطناعي"):
    # تجهيز المدخلات للنموذج
    user_features = np.array([[mfa_input, os_input, breach_input, phishing_input, wifi_input, pwd_input]])
    
    # توقع الذكاء الاصطناعي
    prediction = ai_model.predict(user_features)[0]
    prediction_proba = ai_model.predict_proba(user_features)[0]
    
    st.markdown("---")
    st.subheader("📋 نتيجة التحليل والتنبؤ الذكي:")
    
    if prediction == 0:
        st.success("🟢 **مستوى الخطر المتوقع: منخفض (Low Risk)**\n\n*التحليل:* السلوك الرقمي والسلوكي لهذا المستخدم مستقر وآمن ولا يظهر مؤشرات شاذة.")
    elif prediction == 1:
        st.warning("🟡 **مستوى الخطر المتوقع: متوسط (Medium Risk)**\n\n*التحليل:* رصد نموذج الذكاء الاصطناعي بعض الثغرات السلوكية أو الرقمية التي تتطلب تدخلاً توعوياً وتفعيل 2FA.")
    else:
        st.error("🔴 **مستوى الخطر المتوقع: مرتفع (High Risk - Critical)**\n\n*التحليل:* تنبأ النظام باحتمالية عالية تعرض هذا الفرد لاختراق سيبراني. يُوصى بتقييد الصلاحيات وفحص الجهاز فوراً!")
        
    st.write(f"Confidence Score (نسبة ثقة نموذج الذكاء الاصطناعي في القرار): **{np.max(prediction_proba)*100:.1f}%**")

# 3. إمكانية رفع ملف بيانات خارجي (CSV) لتحليل جماعي
st.markdown("---")
st.subheader("📁 أو قم برفع ملف بيانات (CSV) لتحليل جماعي بالذكاء الاصطناعي للموظفين/الأفراد")
uploaded_file = st.file_uploader("اختر ملف CSV يحتوي على بيانات الأفراد", type=["csv"])

if uploaded_file is not None:
    df_user = pd.read_csv(uploaded_file)
    st.write("عينة من البيانات المرفوعة:", df_user.head())
    if st.button("تشغيل التحليل الجماعي"):
        # تنبؤ للدفعة كاملة
        preds = ai_model.predict(df_user)
        df_user['Predicted_Risk_Level'] = preds
        st.success("تم تحليل الملف بنجاح وإليك النتائج المتوقعة:")
        st.dataframe(df_user)
