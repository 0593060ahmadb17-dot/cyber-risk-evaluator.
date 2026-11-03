import streamlit as st
import numpy as np

st.set_page_config(page_title="نظام تقييم المخاطر السيبرانية الفردية", page_icon="🛡️")

st.title("🛡️ مشروع تخرج: نظام تقييم المخاطر السيبرانية الفردية (IRS)")
st.write("هذا التطبيق يمثل الجانب العملي لمشروع التخرج لتقييم المخاطر السيبرانية اعتماداً على البيانات الرقمية والسلوكية.")

user_id = st.text_input("معرف المستخدم (User ID)", "USER_101")

st.markdown("---")
st.subheader("أولاً: البيانات الرقمية والفنية (Digital Data)")
mfa = st.checkbox("تفعيل المصادقة الثنائية (MFA / 2FA)", value=False)
os_up = st.checkbox("تحديثات نظام التشغيل والتطبيقات مستمرة", value=True)
breaches = st.number_input("عدد مرات تسريب البريد الإلكتروني السابقة (Breach Count)", min_value=0, max_value=10, value=1)

st.markdown("---")
st.subheader("ثانيًا: البيانات السلوكية البشرية (Behavioral Data)")
phishing = st.slider("نسبة الاستجابة والضغط على روابط الصيد الإلكتروني (%)", 0.0, 100.0, 25.0)
wifi = st.checkbox("استخدام شبكات Wi-Fi العامة بدون شبكة افتراضية (VPN)", value=True)
pwd = st.checkbox("إعادة استخدام نفس كلمات المرور عبر الحسابات المختلفة", value=True)

if st.button("🚀 بدء حساب مؤشر الخطر (IRS)"):
    # حساب النتيجة الرقمية
    mfa_score = 0.0 if mfa else 30.0
    os_score = 0.0 if os_up else 30.0
    breach_score = min(breaches * 10.0, 40.0)
    d_score = min(mfa_score + os_score + breach_score, 100.0)

    # حساب النتيجة السلوكية
    phishing_score = (phishing / 100.0) * 40.0
    wifi_score = 30.0 if wifi else 0.0
    pwd_score = 30.0 if pwd else 0.0
    b_score = min(phishing_score + wifi_score + pwd_score, 100.0)

    # المعادلة الرياضية الترجيحية (40% رقمي و 60% سلوكي)
    irs = round((0.4 * d_score) + (0.6 * b_score), 2)

    st.markdown("---")
    st.subheader("📊 نتيجة التقييم والتقرير الآلي:")

    col1, col2, col3 = st.columns(3)
    col1.metric("المحور الرقمي", f"{d_score} / 100")
    col2.metric("المحور السلوكي", f"{b_score} / 100")
    col3.metric("مؤشر الخطر الإجمالي (IRS)", f"{irs} / 100")

    if irs <= 30.0:
        st.success("🟢 مستوى الخطر: منخفض (Low Risk)\n\nالتوصية: الالتزام بالممارسات الحالية وإجراء فحص فصلي دوري.")
    elif irs <= 65.0:
        st.warning("🟡 مستوى الخطر: متوسط (Medium Risk)\n\nالتوصية: تفعيل المصادقة الثنائية فوراً والالتحاق بدورة توعوية ضد الصيد الإلكتروني.")
    else:
        st.error("🔴 مستوى الخطر: مرتفع (High Risk)\n\nالتوصية: تقييد صلاحيات الوصول للحسابات الحساسة وإجراء تدريب مكثف وفحص شامل للأجهزة.")
