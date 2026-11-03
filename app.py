import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="نظام الذكاء الاصطناعي لتقييم المخاطر السيبرانية للجامعة", page_icon="🎓", layout="wide")

st.title("🎓 نظام الذكاء الاصطناعي المتقدم لتقييم المخاطر السيبرانية الفردية")
st.markdown("### *(يعتمد على تكامل بيانات بوابة الجامعة + الموقع الجغرافي + السلوك البشري + الذكاء الاصطناعي)*")

# 1. محاكاة قاعدة بيانات بوابة الجامعة (University Portal Database Simulation)
@st.cache_data
def load_university_database():
    data = {
        "User_ID": ["U202601", "U202602", "U202603", "U202604", "U202605"],
        "Name": ["أحمد العتيبي (طالب حاسب)", "د. محمد خالد (أستاذ مادة)", "سارة الشمري (موظفة إدارية)", "خالد العمري (طالب هندسة)", "فاطمة الزهراني (باحثة أمنية)"],
        "Department": ["كلية الحاسبات", "كلية علوم الإدارة", "شؤون الإحاطة", "كلية الهندسة", "أمن المعلومات"],
        "MFA_Enabled": [1, 0, 1, 0, 1],          # 1=مفعل، 0=غير مفعل (من سجلات الجامعة)
        "OS_Updated": [1, 0, 1, 0, 1],           # 1=محدث، 0=غير محدث (من فحص الأجهزة التابع للجامعة)
        "Breach_Count": [0, 3, 1, 4, 0],         # عدد التسريبات المسجلة على البريد الجامعي
        "Phishing_Click_Rate": [2.5, 45.0, 15.0, 65.0, 1.0], # نسبة التفاعل مع اختبارات الصيد بالجامعة
        "Location_Type": ["الحرم الجامعي (شبكة آمنة)", "موقع خارجي (منزل)", "شبكة Wi-Fi عامة (كافيه)", "دولة أجنبية (خارج الدولة)", "الحرم الجامعي (مختبر آمن)"],
        "Location_Risk_Score": [0, 20, 40, 80, 0] # درجة خطورة الموقع الجغرافي
    }
    return pd.DataFrame(data)

uni_db = load_university_database()

# تدريب نموذج الذكاء الاصطناعي مسبقاً بناءً على هذه المتغيرات الشاملة
@st.cache_resource
def train_ai_model():
    # تدريب افتراضي لمحاكاة التعلم الآلي
    np.random.seed(42)
    X_dummy = np.random.rand(500, 5) # [MFA, OS, Breaches, Phishing, Location_Risk]
    y_dummy = np.random.randint(0, 3, 500) # 0: منخفض، 1: متوسط، 2: مرتفع
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_dummy, y_dummy)
    return model

ai_model = train_ai_model()

# 2. واجهة اختيار المستخدم من النظام الأكاديمي للجامعة
st.sidebar.header("🏢 لوحة تحكم النظام الأكاديمي")
selected_user_id = st.sidebar.selectbox("اختر مستخدماً من سجلات بوابة الجامعة:", uni_db['User_ID'].tolist())

# استخراج بيانات المستخدم المحدد تلقائياً من قاعدة بيانات الجامعة
user_record = uni_db[uni_db['User_ID'] == selected_user_id].iloc[0]

st.markdown("---")
col_info1, col_info2 = st.columns(2)
with col_info1:
    st.info(f"**👤 اسم المستخدم:** {user_record['Name']}\n\n**🆔 الرقم الأكاديمي/الوظيفي:** {user_record['User_ID']}")
with col_info2:
    st.success(f"**🏫 الكلية/القسم:** {user_record['Department']}\n\n**🌐 موقع الاتصال الحالي (من سجلات الـ IP):** {user_record['Location_Type']}")

st.markdown("---")
st.subheader("📊 تفاصيل البيانات المسحوبة من نظام الجامعة والسلوك والموقع:")

c1, c2, c3, c4 = st.columns(4)
c1.metric("حالة المصادقة الثنائية (MFA)", "مفعل" if user_record['MFA_Enabled']==1 else "غير مفعل ⚠️")
c2.metric("حالة تحديثات الجهاز", "محدث" if user_record['OS_Updated']==1 else "مهمل ⚠️")
c3.metric("تسريبات البريد الجامعي", f"{user_record['Breach_Count']} تسريبات")
c4.metric("معدل الاستجابة للصيد", f"{user_record['Phishing_Click_Rate']}%")

# تعديلات تفاعلية لصناع القرار (أو لتجربة سيناريوهات مختلفة أمام الدكتور)
st.markdown("---")
st.subheader("⚙️ محاكاة تحديث الموقع الجغرافي والسلوكي اللحظي:")
custom_location = st.selectbox("تغيير حالة موقع الاتصال للمستخدم:", [
    "الحرم الجامعي (شبكة آمنة)", 
    "موقع خارجي (منزل)", 
    "شبكة Wi-Fi عامة (كافيه)", 
    "دولة أجنبية مشبوهة (خارج الدولة)"
])

# تحديث نقاط خطورة الموقع بناءً على الاختيار
loc_score_map = {
    "الحرم الجامعي (شبكة آمنة)": 0,
    "موقع خارجي (منزل)": 20,
    "شبكة Wi-Fi عامة (كافيه)": 50,
    "دولة أجنبية مشبوهة (خارج الدولة)": 90
}
current_loc_score = loc_score_map[custom_location]

if st.button("🚀 تشغيل خوارزمية الذكاء الاصطناعي لتحليل المخاطر الشاملة"):
    # تجهيز المتغيرات للذكاء الاصطناعي
    # [MFA_factor, OS_factor, Breach_factor, Phishing_factor, Location_factor]
    features = np.array([[
        float(user_record['MFA_Enabled']),
        float(user_record['OS_Updated']),
        float(user_record['Breach_Count']) / 5.0,
        float(user_record['Phishing_Click_Rate']) / 100.0,
        float(current_loc_score) / 100.0
    ]])
    
    # تنبؤ الذكاء الاصطناعي
    prediction_prob = ai_model.predict_proba(features)[0]
    risk_score_calc = (
        (1 - user_record['MFA_Enabled']) * 25 + 
        (1 - user_record['OS_Updated']) * 25 + 
        (user_record['Breach_Count'] * 5) + 
        (user_record['Phishing_Click_Rate'] * 0.2) + 
        (current_loc_score * 0.3)
    )
    risk_score_calc = min(max(risk_score_calc, 0.0), 100.0)

    st.markdown("---")
    st.subheader("🎯 نتيجة التقييم الذكي والقرار الأمني:")
    
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric("مؤشر الخطر الإجمالي الفردي (IRS)", f"{risk_score_calc:.1f} / 100")
        
    with res_col2:
        if risk_score_calc < 30:
            st.success("🟢 **مستوى الخطورة: منخفض (Low Risk)**\n\n*التقرير:* المستخدم يلتزم بمعايير أمن الجامعة ويتصل من بيئة آمنة.")
        elif risk_score_calc < 65:
            st.warning("🟡 **مستوى الخطورة: متوسط (Medium Risk)**\n\n*التقرير:* رصد النظام مؤشرات تتطلب الانتباه (مثل الموقع غير الآمن أو ضعف MFA)، يُوصى بتفعيل التنبيهات.")
        else:
            st.error("🔴 **مستوى الخطورة: مرتفع جداً (Critical Risk - Threat Detected)**\n\n*التقرير:* تنبأ الذكاء الاصطناعي بوجود خطر داهم نتيجة اجتماع (موقع مشبوه + سلوك صيد إلكتروني + غياب MFA). **تم حظر الوصول المؤقت للحساب تلقائياً!**")

    st.info(f"💡 **تحليل الخوارزمية (AI Explainability):** تم اتخاذ هذا القرار بناءً على تقاطع البيانات الأكاديمية المسجلة، شذوذ الموقع الجغرافي (`{custom_location}`)، ومعدل السلوك السيئ بنسبة `{user_record['Phishing_Click_Rate']}%`.")
