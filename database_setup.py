import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_and_populate_database():
    conn = sqlite3.connect('cyber_risk_system.db')
    cursor = conn.cursor()
    
    # إنشاء جدول الأفراد وتحليل المخاطر
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS individual_risks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE,
            department TEXT,
            phishing_click_rate REAL,
            password_strength_score INTEGER,
            failed_login_attempts INTEGER,
            mfa_enabled INTEGER,
            cyber_awareness_score INTEGER,
            data_sharing_level INTEGER,
            browsing_risk_score REAL,
            risk_level TEXT,
            risk_percentage REAL,
            analysis_date TEXT
        )
    ''')
    
    # التحقق مما إذا كانت البيانات موجودة مسبقاً
    cursor.execute('SELECT COUNT(*) FROM individual_risks')
    count = cursor.fetchone()[0]
    
    if count == 0:
        np.random.seed(42)
        n_samples = 1000
        
        departments = ['كلية الحاسبات وتقنية المعلومات', 'كلية الهندسة', 'إدارة الموارد البشرية', 'المالية والمحاسبة', 'الشؤون القانونية', 'كلية الطب']
        
        user_ids = [f"EMP-{1000 + i}" for i in range(n_samples)]
        depts = np.random.choice(departments, n_samples)
        phishing_rates = np.round(np.random.beta(2, 5, n_samples) * 100, 2)
        pwd_strengths = np.random.randint(1, 6, n_samples) # 1 ضعيف جداً إلى 5 قوي جداً
        failed_logins = np.random.poisson(2, n_samples)
        mfa_status = np.random.choice([0, 1], n_samples, p=[0.3, 0.7]) # 0 معطل، 1 مفعل
        awareness_scores = np.random.randint(20, 100, n_samples)
        data_sharing = np.random.randint(1, 5, n_samples)
        browsing_risks = np.round(np.random.uniform(5, 95, n_samples), 2)
        
        risk_levels = []
        risk_percentages = []
        
        for i in range(n_samples):
            # معادلة منطقية لحساب نسبة الخطر بناءً على المدخلات لتوجيه النموذج
            score = (
                (phishing_rates[i] * 0.3) +
                ((6 - pwd_strengths[i]) * 6) +
                (failed_logins[i] * 3) +
                ((1 - mfa_status[i]) * 20) +
                ((100 - awareness_scores[i]) * 0.2) +
                (data_sharing[i] * 4) +
                (browsing_risks[i] * 0.15)
            )
            score = min(max(score, 2.0), 98.5)
            risk_percentages.append(round(score, 2))
            
            if score < 30:
                risk_levels.append('منخفض')
            elif score < 60:
                risk_levels.append('متوسط')
            elif score < 85:
                risk_levels.append('مرتفع')
            else:
                risk_levels.append('حرج')
                
        base_date = datetime.now() - timedelta(days=90)
        dates = [(base_date + timedelta(days=int(np.random.randint(0, 90)))).strftime('%Y-%m-%d') for _ in range(n_samples)]
        
        for i in range(n_samples):
            cursor.execute('''
                INSERT OR IGNORE INTO individual_risks (
                    user_id, department, phishing_click_rate, password_strength_score,
                    failed_login_attempts, mfa_enabled, cyber_awareness_score,
                    data_sharing_level, browsing_risk_score, risk_level, risk_percentage, analysis_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_ids[i], depts[i], phishing_rates[i], int(pwd_strengths[i]),
                int(failed_logins[i]), int(mfa_status[i]), int(awareness_scores[i]),
                int(data_sharing[i]), browsing_risks[i], risk_levels[i], risk_percentages[i], dates[i]
            ))
            
        conn.commit()
    conn.close()

if __name__ == "__main__":
    create_and_populate_database()
    print("تم إنشاء قاعدة البيانات وتوليد 1000 سجل بنجاح!")
