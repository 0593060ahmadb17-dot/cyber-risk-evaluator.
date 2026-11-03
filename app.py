import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# إعدادات صفحة Streamlit
st.set_page_config(
    page_title="نظام تقييم المخاطر السيبرانية الفردية",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص التصميم لدعم اللغة العربية والاتجاه من اليمين لليسار (RTL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
    * {
        font-family: 'Cairo', sans-serif;
    }
    .main {
        direction: rtl;
        text-align: right;
    }
    .sidebar .sidebar-content {
        direction: rtl;
        text-align: right;
    }
    h1, h2, h3, h4, h5, h6, p, div, span {
        direction: rtl;
        text-align: right;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# الاتصال بقاعدة البيانات وجلب البيانات
@st.cache_data
def load_data():
    conn = sqlite3.connect('cyber_risk_system.db')
    df = pd.read_sql('SELECT * FROM individual_risks', conn)
    conn.close()
    return df

df = load_data()

# تدريب نموذج التعلم الآلي (Machine Learning Model)
@st.cache_resource
def train_model(data):
    features = [
        'phishing_click_rate', 'password_strength_score', 
        'failed_login_attempts', 'mfa_enabled', 
        'cyber_awareness_score', 'data_sharing_level', 'browsing_risk_score'
    ]
    X = data[features]
    y = data['risk_level']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # نموذج Random Forest الأساسي
    rf_model = RandomForestClassifier(n_estimators=150, random_state=42)
    rf_model.fit(X_train, y_train)
    
    # نموذج للمقارنة Logistic Regression
    lr_model = LogisticRegression(max_iter=1000, random_state=42)
    lr_model.fit(X_train, y_train)
    
    y_pred_rf = rf_model.predict(X_test)
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred_rf),
        'precision': precision_score(y_test, y_pred_rf, average='weighted', zero_division=0),
        'recall': recall_score(y_test, y_pred_rf, average='weighted', zero_division=0),
        'f1': f1_score(y_test, y_pred_rf, average='weighted', zero_division=0),
        'conf_matrix': confusion_matrix(y_test, y_pred_rf),
        'classes': rf_model.classes_
    }
    
    return rf_model, lr_model, metrics, X_test, y_test

model, lr_model, metrics, X_test, y_test = train_model(df)

# الشريط الجانبي للتنقل
st.sidebar.title("🛡️ القائمة الرئيسية")
page = st.sidebar.radio("اختر القسم:", [
    "🏠 لوحة المؤشرات العامة (Dashboard)",
    "🔍 تحليل فرد جديد / محاكاة",
    "👥 إدارة وعرض الأفراد",
    "🤖 أداء نموذج الذكاء الاصطناعي",
    "📊 التقارير والتصدير"
])

# 1. لوحة المؤشرات العامة
if page == "🏠 لوحة المؤشرات العامة (Dashboard)":
    st.title("📊 لوحة التحكم والمؤشرات السيبرانية العامة")
    st.markdown("نظام ذكي لتحليل ومتابعة مستويات المخاطر السيبرانية الفردية استناداً إلى البيانات الرقمية والسلوكية.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("إجمالي الأفراد المحللين", f"{len(df):,}")
    with col2:
        high_critical = len(df[df['risk_level'].isin(['مرتفع', 'حرج'])])
        st.metric("الحالات المرتفعة والحرجة", f"{high_critical:,}", delta=f"{high_critical/len(df)*100:.1f}%", delta_color="inverse")
    with col3:
        avg_risk = df['risk_percentage'].mean()
        st.metric("متوسط درجة الخطر العام", f"{avg_risk:.1f}%")
    with col4:
        mfa_adherence = (df['mfa_enabled'].sum() / len(df)) * 100
        st.metric("التزام المصادقة الثنائية (MFA)", f"{mfa_adherence:.1f}%")
        
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("توزيع مستويات المخاطر السيبرانية")
        risk_counts = df['risk_level'].value_counts().reset_index()
        risk_counts.columns = ['مستوى الخطر', 'العدد']
        fig_pie = px.pie(risk_counts, values='العدد', names='مستوى الخطر', 
                         color='مستوى الخطر',
                         color_discrete_map={'منخفض':'#2ecc71', 'متوسط':'#f1c40f', 'مرتفع':'#e67e22', 'حرج':'#e74c3c'},
                         hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.subheader("متوسط نسب الخطر حسب الأقسام والإدارات")
        dept_risk = df.groupby('department')['risk_percentage'].mean().reset_index()
        fig_bar = px.bar(dept_risk, x='department', y='risk_percentage', 
                         color='risk_percentage',
                         color_continuous_scale='Reds',
                         labels={'department': 'القسم', 'risk_percentage': 'متوسط نسبة الخطر (%)'})
        st.plotly_chart(fig_bar, use_container_width=True)

# 2. تحليل فرد جديد / محاكاة
elif page == "🔍 تحليل فرد جديد / محاكاة":
    st.title("🔍 تقييم وتحليل المخاطر لفرد جديد")
    st.markdown("أدخل المؤشرات الرقمية والسلوكية للمستخدم ليقوم نموذج الذكاء الاصطناعي بتقييم خطورته الفورية وتوليد التوصيات الأمنية.")
    
    with st.form("risk_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            user_id = st.text_input("معرف الموظف / الفرد", value="EMP-9999")
            department = st.selectbox("القسم أو الإدارة", df['department'].unique())
            phishing_rate = st.slider("معدل النقر على روابط التصيد الإلكتروني (%)", 0.0, 100.0, 15.0)
            pwd_strength = st.slider("درجة قوة كلمات المرور (من 1 إلى 5)", 1, 5, 3)
            failed_logins = st.number_input("عدد محاولات تسجيل الدخول الفاشلة المتكررة", min_value=0, max_value=20, value=1)
            
        with col2:
            mfa_status = st.radio("استخدام المصادقة الثنائية (MFA)", options=[1, 0], format_func=lambda x: "مفعل (آمن)" if x==1 else "معطل (غير آمن)")
            awareness_score = st.slider("درجة اختبار الوعي السيبراني (من 0 إلى 100)", 0, 100, 60)
            data_sharing = st.slider("مستوى مشاركة البيانات الشخصية والحساسة (من 1 إلى 4)", 1, 4, 2)
            browsing_risk = st.slider("مستوى خطورة سلوك التصفح والتفاعل الرقمي (%)", 0.0, 100.0, 30.0)
            
        submitted = st.form_submit_button("🚀 تشغيل التحليل والتنبؤ الذكي")
        
        if submitted:
            input_data = pd.DataFrame([[
                phishing_rate, pwd_strength, failed_logins, 
                mfa_status, awareness_score, data_sharing, browsing_risk
            ]], columns=[
                'phishing_click_rate', 'password_strength_score', 
                'failed_login_attempts', 'mfa_enabled', 
                'cyber_awareness_score', 'data_sharing_level', 'browsing_risk_score'
            ])
            
            prediction = model.predict(input_data)[0]
            probabilities = model.predict_proba(input_data)[0]
            classes = model.classes_
            
            # حساب تقديري لنسبة الخطر
            calc_percentage = (
                (phishing_rate * 0.3) +
                ((6 - pwd_strength) * 6) +
                (failed_logins * 3) +
                ((1 - mfa_status) * 20) +
                ((100 - awareness_score) * 0.2) +
                (data_sharing * 4) +
                (browsing_risk * 0.15)
            )
            calc_percentage = min(max(calc_percentage, 1.0), 99.0)
            
            st.markdown("---")
            st.subheader("📌 نتائج التقييم الأمني والذكاء الاصطناعي:")
            
            res_col1, res_col2, res_col3 = st.columns(3)
            with res_col1:
                st.metric("مستوى الخطر المتوقع", prediction)
            with res_col2:
                st.metric("درجة الخطر الرقمية", f"{calc_percentage:.1f}%")
            with res_col3:
                max_prob = np.max(probabilities) * 100
                st.metric("ثقة نموذج الذكاء الاصطناعي", f"{max_prob:.1f}%")
                
            # تفسير العوامل المؤثرة (Explainable AI Concept)
            st.markdown("### 💡 تحليل الأسباب والتفسير الأمني:")
            reasons = []
            if phishing_rate > 30:
                reasons.append("⚠️ ارتفاع معدل الاستجابة لرسائل التصيد الإلكتروني يزيد بشكل ملحوظ من احتمالية الاختراق.")
            if mfa_status == 0:
                reasons.append("🚨 تعطيل المصادقة الثنائية (MFA) يُمثل ثغرة حرجة تعرض الحساب للاختراق الفوري.")
            if pwd_strength < 3:
                reasons.append("🔑 ضعف كلمات المرور المستخدمة يجعلها عرضة لهجمات التخمين وقاموس الكلمات.")
            if failed_logins > 3:
                reasons.append("🔄 كثرة محاولات الدخول الفاشلة قد تشير إلى نشاط مشبوه أو محاولات وصول غير مصرح بها.")
            if not reasons:
                reasons.append("✅ السلوك الرقمي للمستخدم ضمن النطاق الآمن والمقبول سيبرانياً.")
                
            for r in reasons:
                st.write(r)
                
            st.markdown("### 🛠️ التوصيات الأمنية المخصصة:")
            if prediction in ['مرتفع', 'حرج']:
                st.error("1. إلزام المستخدم فوراً بتفعيل المصادقة الثنائية (MFA).\n2. إحالة الموظف إلى دورة تدريبية عاجلة متخصصة في مكافحة التصيد الهندسي الاجتماعي.\n3. تغيير كافة كلمات المرور الحالية واستخدام مدير كلمات مرور آمن.")
            elif prediction == 'متوسط':
                st.warning("1. توجيه إرشادات توعوية دورية للمستخدم حول حماية بياناته الشخصية.\n2. مراجعة وتحديث صلاحيات الوصول الخاصة بالحساب.")
            else:
                st.success("1. الاستمرار على الممارسات الأمنية الحالية الجيدة.\n2. إجراء اختبارات وعي دورية روتينية.")

# 3. إدارة وعرض الأفراد
elif page == "👥 إدارة وعرض الأفراد":
    st.title("👥 سجل الأفراد وتحليل قواعد البيانات")
    
    search_query = st.text_input("بحث برقم المعرف (User ID):", "")
    selected_dept = st.selectbox("تصفية حسب القسم:", ["الكل"] + list(df['department'].unique()))
    
    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[filtered_df['user_id'].str.contains(search_query, case=False)]
    if selected_dept != "الكل":
        filtered_df = filtered_df[filtered_df['department'] == selected_dept]
        
    st.dataframe(filtered_df, use_container_width=True)

# 4. أداء نموذج الذكاء الاصطناعي
elif page == "🤖 أداء نموذج الذكاء الاصطناعي":
    st.title("🤖 تقييم أداء نموذج تعلم الآلة (Model Evaluation)")
    st.markdown("استعراض المقاييس الإحصائية لتقييم كفاءة نموذج `Random Forest` في تصنيف المخاطر.")
    
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric("الدقة الإجمالية (Accuracy)", f"{metrics['accuracy']*100:.2f}%")
    with m_col2:
        st.metric("الدقة النوعية (Precision)", f"{metrics['precision']*100:.2f}%")
    with m_col3:
        st.metric("الاستدعاء (Recall)", f"{metrics['recall']*100:.2f}%")
    with m_col4:
        st.metric("مقياس F1-Score", f"{metrics['f1']*100:.2f}%")
        
    st.markdown("---")
    st.subheader("مصفوفة الالتباس (Confusion Matrix)")
    
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(metrics['conf_matrix'], annot=True, fmt='d', cmap='Blues', 
                xticklabels=metrics['classes'], yticklabels=metrics['classes'], ax=ax)
    plt.xlabel('التنبؤ المتوقع')
    plt.ylabel('القيمة الحقيقية')
    st.pyplot(fig)

# 5. التقارير والتصدير
elif page == "📊 التقارير والتصدير":
    st.title("📊 تصدير التقارير وتحليل البيانات")
    st.markdown("يمكنك تصدير تقارير المخاطر السيبرانية الكاملة بصيغة CSV لمشاركتها مع الإدارة العليا أو لجان المناقشة.")
    
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 تحميل تقرير المخاطر الشامل (CSV)",
        data=csv_data,
        file_name='cyber_risk_assessment_report.csv',
        mime='text/csv',
    )
    
    st.markdown("---")
    st.subheader("معاينة سريعة لملف التقرير")
    st.dataframe(df.head(20))
