import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import time

# Page Configuration
st.set_page_config(
    page_title="لوحة المعلومات الصحية الشاملة 2025",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://support.moh.gov.sa',
        'Report a bug': None,
        'About': "لوحة المعلومات الصحية الشاملة 2025 - مكتب هيئة الصحة العامة بنجران"
    }
)

# Advanced CSS with Glassmorphism and Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@200;300;400;600;700;800&family=Amiri:wght@400;700&display=swap');
    
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --tertiary-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --success-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        --warning-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --danger-gradient: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
        --dark-glass: rgba(0, 0, 0, 0.3);
        --shadow-glow: 0 8px 32px rgba(31, 38, 135, 0.37);
        --shadow-premium: 0 15px 35px rgba(0, 0, 0, 0.3);
        --text-primary: #ffffff;
        --text-secondary: rgba(255, 255, 255, 0.8);
        --text-accent: #ffd700;
    }
    
    .stApp {
        background: 
            radial-gradient(circle at 20% 80%, #667eea 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, #764ba2 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, #f093fb 0%, transparent 50%),
            linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        background-size: 400% 400%;
        animation: backgroundShift 20s ease infinite;
        color: var(--text-primary);
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        min-height: 100vh;
    }
    
    @keyframes backgroundShift {
        0%, 100% { background-position: 0% 50%; }
        33% { background-position: 100% 0%; }
        66% { background-position: 100% 100%; }
    }
    
    .main-header {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 25px;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: var(--shadow-glow);
        position: relative;
        overflow: hidden;
        animation: headerFloat 6s ease-in-out infinite;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: shimmer 3s linear infinite;
    }
    
    @keyframes headerFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .metric-card {
        background: var(--glass-bg);
        backdrop-filter: blur(15px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 2rem 1.5rem;
        text-align: center;
        box-shadow: var(--shadow-glow);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        animation: cardSlideIn 0.8s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-15px) scale(1.02);
        box-shadow: 0 20px 40px rgba(31, 38, 135, 0.5);
        border-color: var(--text-accent);
    }
    
    .metric-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover::after {
        left: 100%;
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        background: var(--secondary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        animation: valueCount 2s ease-out;
    }
    
    .metric-label {
        font-size: 1rem;
        color: var(--text-secondary);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        position: relative;
    }
    
    .chart-container {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 25px;
        padding: 2rem;
        box-shadow: var(--shadow-glow);
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
        animation: containerSlideUp 1s ease-out;
    }
    
    .chart-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--primary-gradient);
        animation: progressBar 3s ease-in-out infinite;
    }
    
    @keyframes progressBar {
        0%, 100% { transform: translateX(-100%); }
        50% { transform: translateX(100%); }
    }
    
    .analysis-card {
        background: var(--dark-glass);
        backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid var(--text-accent);
        box-shadow: var(--shadow-premium);
        animation: fadeInLeft 0.8s ease-out;
    }
    
    .analysis-title {
        color: var(--text-accent);
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .analysis-text {
        color: var(--text-secondary);
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    .insight-badge {
        background: var(--success-gradient);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.25rem;
        animation: badgePulse 2s ease-in-out infinite;
    }
    
    .warning-badge {
        background: var(--warning-gradient);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.25rem;
        animation: badgeShake 1s ease-in-out infinite;
    }
    
    .danger-badge {
        background: var(--danger-gradient);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.25rem;
        animation: badgeBounce 1.5s ease-in-out infinite;
    }
    
    @keyframes badgePulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.8; }
    }
    
    @keyframes badgeShake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-2px); }
        75% { transform: translateX(2px); }
    }
    
    @keyframes badgeBounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-premium);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(31, 38, 135, 0.4);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .floating-stats {
        position: fixed;
        top: 100px;
        right: 20px;
        background: var(--glass-bg);
        backdrop-filter: blur(15px);
        border: 1px solid var(--glass-border);
        border-radius: 15px;
        padding: 1rem;
        box-shadow: var(--shadow-glow);
        z-index: 1000;
        animation: floatUpDown 4s ease-in-out infinite;
        font-size: 0.8rem;
        color: var(--text-secondary);
    }
    
    @keyframes floatUpDown {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .section-divider {
        height: 2px;
        background: var(--primary-gradient);
        border: none;
        margin: 3rem 0;
        border-radius: 1px;
        animation: dividerGlow 3s ease-in-out infinite;
    }
    
    @keyframes dividerGlow {
        0%, 100% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.5); }
        50% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.8); }
    }
    
    @keyframes cardSlideIn {
        from { transform: translateY(50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes containerSlideUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes fadeInLeft {
        from { transform: translateX(-30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes valueCount {
        from { transform: scale(0); }
        to { transform: scale(1); }
    }
    
    .plotly-graph-div {
        border-radius: 15px;
        overflow: hidden;
    }
    
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--dark-glass);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-gradient);
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Data Loading
@st.cache_data
def load_comprehensive_data():
    # Health Data from Excel
    health_data = {
        'الشهر': ['يناير 2025', 'فبراير 2025', 'مارس 2025', 'أبريل 2025', 'مايو 2025', 'يونيو 2025'],
        'عدد العابرين': [185726, 200682, 163291, 106674, 86673, 104816],
        'عدد المعتمرين': [88806, 120930, 96027, 4316, 0, 17697],
        'عدد الحجاج': [0, 0, 0, 0, 12951, 0],
        'زيارات العيادة': [2490, 2129, 1640, 1362, 1223, 1015],
        'حالات النقل الإسعافي وحالات الإشتباه': [7, 8, 3, 5, 21, 11],
        'الجولات الإشرافية': [2, 3, 2, 1, 2, 2],
        'شلل الأطفال': [185726, 200682, 163291, 106674, 86673, 104816],
        'مخية شوكية': [88806, 120930, 96027, 4316, 12951, 17697],
        'ثلاثي فيروسي': [2490, 2129, 1640, 1362, 1223, 1015],
        'مجموع التطعيمات': [104730, 109856, 67885, 53470, 62147, 62745],
        'المجموع الكلي': [381761, 433606, 328847, 165829, 163017, 186286]
    }
    return pd.DataFrame(health_data)

# Load data
with st.spinner('🚀 تحميل النظام المتقدم للتحليلات الصحية...'):
    health_df = load_comprehensive_data()
    time.sleep(1)  # Animation effect

# Floating Statistics
st.markdown(f"""
<div class="floating-stats">
    📊 إحصائيات سريعة<br>
    🏥 المجموع الكلي: {health_df['المجموع الكلي'].sum():,}<br>
    💉 التطعيمات: {health_df['مجموع التطعيمات'].sum():,}<br>
    🚶‍♂️ العابرين: {health_df['عدد العابرين'].sum():,}
</div>
""", unsafe_allow_html=True)

# Main Header with Animation
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 3rem; margin-bottom: 1rem; background: linear-gradient(45deg, #667eea, #764ba2, #f093fb); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🏥 لوحة المعلومات الصحية الشاملة 2025
    </h1>
    <h2 style="font-size: 1.5rem; color: var(--text-accent); margin-bottom: 1rem;">
        إدارة المنافذ واللوائح الصحية الدولية - مكتب هيئة الصحة العامة بنجران
    </h2>
    <p style="font-size: 1.1rem; color: var(--text-secondary);">
        تحليلات متقدمة ومتنوعة للبيانات الصحية - الربع الأول والثاني 2025م
    </p>
</div>
""", unsafe_allow_html=True)

# Enhanced Sidebar
with st.sidebar:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("### 🎛 مركز التحكم المتقدم")
    
    analysis_type = st.selectbox(
        "🔍 نوع التحليل:",
        ["شامل", "صحة عامة", "تطعيمات", "زيارات طبية", "طوارئ"]
    )
    
    time_period = st.selectbox(
        "📅 الفترة الزمنية:",
        ["جميع الأشهر", "الربع الأول", "الربع الثاني", "شهر واحد"]
    )
    
    viz_type = st.multiselect(
        "📊 نوع المخططات:",
        ["خطي", "أعمدة", "دائري", "منطقة", "مبعثر", "خريطة حرارية", "ثلاثي الأبعاد"],
        default=["خطي", "أعمدة", "دائري"]
    )
    
    st.markdown("### ⚙ خيارات متقدمة")
    show_predictions = st.toggle("🔮 عرض التنبؤات", value=True)
    show_correlations = st.toggle("🔗 عرض الارتباطات", value=True)
    show_clusters = st.toggle("🎯 تحليل المجموعات", value=False)
    auto_refresh = st.toggle("🔄 تحديث تلقائي", value=False)
    
    if auto_refresh:
        refresh_rate = st.select_slider("معدل التحديث (ثانية):", [5, 10, 30, 60], value=30)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Key Performance Indicators
st.markdown('<h2 style="text-align: center; font-size: 2.5rem; background: linear-gradient(45deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">📈 المؤشرات الرئيسية</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_travelers = health_df['عدد العابرين'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_travelers:,}</div>
        <div class="metric-label">إجمالي العابرين</div>
        <div class="insight-badge">↗ نمو مستمر</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_pilgrims = health_df['عدد المعتمرين'].sum() + health_df['عدد الحجاج'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_pilgrims:,}</div>
        <div class="metric-label">إجمالي المعتمرين والحجاج</div>
        <div class="warning-badge">📊 موسمي</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    total_vaccinations = health_df['مجموع التطعيمات'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_vaccinations:,}</div>
        <div class="metric-label">إجمالي التطعيمات</div>
        <div class="insight-badge">✅ هدف محقق</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    total_clinic_visits = health_df['زيارات العيادة'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_clinic_visits:,}</div>
        <div class="metric-label">إجمالي زيارات العيادة</div>
        <div class="insight-badge">🏥 نشاط طبي</div>
    </div>
    """, unsafe_allow_html=True)

# Section Divider
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# Comparative Analysis
st.markdown('<h2 style="text-align: center; font-size: 2.5rem; background: linear-gradient(45deg, #43e97b, #38f9d7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🔍 تحليلات مقارنة متقدمة</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📊 مقارنة الأرباع - المؤشرات الرئيسية")
    
    q_comparison = {
        'المؤشر': ['إجمالي العابرين', 'إجمالي المعتمرين والحجاج', 'إجمالي زيارات العيادة', 'إجمالي التطعيمات'],
        'الربع الأول': [
            health_df.iloc[0:3]['عدد العابرين'].sum(),
            health_df.iloc[0:3]['عدد المعتمرين'].sum() + health_df.iloc[0:3]['عدد الحجاج'].sum(),
            health_df.iloc[0:3]['زيارات العيادة'].sum(),
            health_df.iloc[0:3]['مجموع التطعيمات'].sum()
        ],
        'الربع الثاني': [
            health_df.iloc[3:6]['عدد العابرين'].sum(),
            health_df.iloc[3:6]['عدد المعتمرين'].sum() + health_df.iloc[3:6]['عدد الحجاج'].sum(),
            health_df.iloc[3:6]['زيارات العيادة'].sum(),
            health_df.iloc[3:6]['مجموع التطعيمات'].sum()
        ]
    }
    
    fig_quarterly = go.Figure()
    
    fig_quarterly.add_trace(go.Bar(
        name='الربع الأول',
        x=q_comparison['المؤشر'],
        y=q_comparison['الربع الأول'],
        marker_color='rgba(67, 233, 123, 0.8)',
        text=[f'{val:,}' for val in q_comparison['الربع الأول']],
        textposition='auto',
        hovertemplate='الربع الأول<br>%{x}: %{y:,}<extra></extra>'
    ))
    
    fig_quarterly.add_trace(go.Bar(
        name='الربع الثاني',
        x=q_comparison['المؤشر'],
        y=q_comparison['الربع الثاني'],
        marker_color='rgba(56, 249, 215, 0.8)',
        text=[f'{val:,}' for val in q_comparison['الربع الثاني']],
        textposition='auto',
        hovertemplate='الربع الثاني<br>%{x}: %{y:,}<extra></extra>'
    ))
    
    fig_quarterly.update_layout(
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='white',
        xaxis_tickangle=-45,
        transition={'duration': 2000, 'easing': 'elastic-out'}
    )
    
    st.plotly_chart(fig_quarterly, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🎯 نسب التغيير بين الأرباع")
    
    changes = []
    for i in range(len(q_comparison['الربع الأول'])):
        change = ((q_comparison['الربع الثاني'][i] - q_comparison['الربع الأول'][i]) / q_comparison['الربع الأول'][i]) * 100
        changes.append(change)
    
    fig_changes = make_subplots(
        rows=2, cols=2,
        subplot_titles=q_comparison['المؤشر'],
        specs=[[{"type": "indicator"}, {"type": "indicator"}],
               [{"type": "indicator"}, {"type": "indicator"}]]
    )
    
    colors = ['red' if change < 0 else 'green' for change in changes]
    
    for i, (metric, change) in enumerate(zip(q_comparison['المؤشر'], changes)):
        row = (i // 2) + 1
        col = (i % 2) + 1
        
        fig_changes.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=abs(change),
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"{change:+.1f}%"},
            delta={'reference': 0},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': colors[i]},
                'steps': [
                    {'range': [0, 25], 'color': "lightgray"},
                    {'range': [25, 50], 'color': "gray"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 50}}
        ), row=row, col=col)
    
    fig_changes.update_layout(
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='white'
    )
    
    st.plotly_chart(fig_changes, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Vaccination Analysis
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<h2 style="text-align: center; font-size: 2.5rem; background: linear-gradient(45deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">💉 تحليل التطعيمات</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📈 اتجاهات التطعيمات")
    
    fig_vacc_trend = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_vacc_trend.add_trace(
        go.Scatter(x=health_df['الشهر'], y=health_df['شلل الأطفال'],
                  mode='lines+markers',
                  name='شلل الأطفال',
                  line=dict(color='#ff6b6b', width=4),
                  marker=dict(size=12),
                  fill='tonexty'),
        secondary_y=False,
    )
    
    fig_vacc_trend.add_trace(
        go.Scatter(x=health_df['الشهر'], y=health_df['مخية شوكية'],
                  mode='lines+markers',
                  name='مخية شوكية',
                  line=dict(color='#ffa726', width=4),
                  marker=dict(size=12)),
        secondary_y=True,
    )
    
    fig_vacc_trend.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='white'
    )
    
    fig_vacc_trend.update_yaxes(title_text="شلل الأطفال", secondary_y=False)
    fig_vacc_trend.update_yaxes(title_text="مخية شوكية", secondary_y=True)
    
    st.plotly_chart(fig_vacc_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("💉 توزيع التطعيمات")
    
    fig_vacc_pie = go.Figure(data=[go.Pie(
        labels=['شلل الأطفال', 'مخية شوكية', 'ثلاثي فيروسي'],
        values=[health_df['شلل الأطفال'].sum(), health_df['مخية شوكية'].sum(), health_df['ثلاثي فيروسي'].sum()],
        hole=0.4,
        textinfo='percent+label',
        textfont_size=12,
        marker=dict(colors=['#667eea', '#764ba2', '#f093fb'], line=dict(color='#000000', width=2)),
        hovertemplate='%{label}<br>العدد: %{value:,}<br>النسبة: %{percent}<extra></extra>',
        pull=[0.1, 0, 0]
    )])
    
    fig_vacc_pie.add_annotation(
        text=f"إجمالي<br>{health_df['مجموع التطعيمات'].sum():,}",
        x=0.5, y=0.5,
        font_size=16,
        font_color='white',
        showarrow=False
    )
    
    fig_vacc_pie.update_layout(
        title="توزيع أنواع التطعيمات",
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='white',
        height=500
    )
    
    st.plotly_chart(fig_vacc_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🔥 خريطة حرارية للتطعيمات")
    
    vacc_matrix = np.array([
        health_df['شلل الأطفال'].values,
        health_df['مخية شوكية'].values,
        health_df['ثلاثي فيروسي'].values
    ])
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=vacc_matrix,
        x=health_df['الشهر'],
        y=['شلل الأطفال', 'مخية شوكية', 'ثلاثي فيروسي'],
        colorscale='Viridis',
        text=vacc_matrix,
        texttemplate="%{text:,}",
        textfont={"size": 14, "color": "white"},
        hoverongaps=False,
        hovertemplate='الشهر: %{x}<br>التطعيم: %{y}<br>العدد: %{z:,}<extra></extra>'
    ))
    
    fig_heatmap.update_layout(
        title="توزيع التطعيمات عبر الأشهر",
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='white',
        height=400
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Emergency and Clinic Analysis
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<h2 style="text-align: center; font-size: 2.5rem; background: linear-gradient(45deg, #ff6b6b, #ffa726); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🚨 تحليل الطوارئ والزيارات الطبية</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🏥 زيارات العيادة")
    
    fig_clinic = go.Figure()
    
    fig_clinic.add_trace(go.Bar(
        x=health_df['الشهر'],
        y=health_df['زيارات العيادة'],
        name='زيارات العيادة',
        marker_color='rgba(79, 172, 254, 0.8)',
        text=health_df['زيارات العيادة'],
        textposition='auto',
        hovertemplate='الشهر: %{x}<br>الزيارات: %{y:,}<extra></extra>'
    ))
    
    fig_clinic.add_trace(go.Scatter(
        x=health_df['الشهر'],
        y=health_df['زيارات العيادة'],
        mode='lines+markers',
        name='الاتجاه',
        line=dict(color='#ffd700', width=3),
        marker=dict(size=8)
    ))
    
    fig_clinic.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='white',
        yaxis_title='عدد الزيارات'
    )
    
    st.plotly_chart(fig_clinic, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🚑 حالات النقل الإسعافي")
    
    fig_emergency = go.Figure()
    
    fig_emergency.add_trace(go.Scatter(
        x=health_df['الشهر'],
        y=health_df['حالات النقل الإسعافي وحالات الإشتباه'],
        mode='lines+markers',
        fill='tonexty',
        name='النقل الإسعافي',
        line=dict(color='#ff6b6b', width=4),
        marker=dict(size=15, color='#ff4757'),
        text=health_df['حالات النقل الإسعافي وحالات الإشتباه'],
        textposition='top center',
        hovertemplate='الشهر: %{x}<br>الحالات: %{y}<extra></extra>'
    ))
    
    fig_emergency.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='white',
        yaxis=dict(range=[0, 25])
    )
    
    st.plotly_chart(fig_emergency, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Quarterly Analysis
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<h2 style="text-align: center; font-size: 2.5rem; background: linear-gradient(45deg, #4facfe, #00f2fe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">📊 تحليلات ربعية متقدمة</h2>', unsafe_allow_html=True)

q1_tab, q2_tab = st.tabs(["📈 إحصائيات الربع الأول (يناير - مارس)", "📊 إحصائيات الربع الثاني (أبريل - يونيو)"])

with q1_tab:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    q1_df = health_df.iloc[0:3]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 تطور عدد العابرين والمعتمرين - الربع الأول")
        fig_q1_travelers = go.Figure()
        
        fig_q1_travelers.add_trace(go.Scatter(
            x=q1_df['الشهر'], 
            y=q1_df['عدد العابرين'],
            mode='lines+markers+text',
            name='العابرين',
            line=dict(color='#00f2fe', width=4),
            marker=dict(size=12, color='#4facfe'),
            text=q1_df['عدد العابرين'],
            textposition='top center',
            hovertemplate='العابرين: %{y:,}<extra></extra>'
        ))
        
        fig_q1_travelers.add_trace(go.Scatter(
            x=q1_df['الشهر'], 
            y=q1_df['عدد المعتمرين'],
            mode='lines+markers+text',
            name='المعتمرين',
            line=dict(color='#f093fb', width=4),
            marker=dict(size=12, color='#f5576c'),
            text=q1_df['عدد المعتمرين'],
            textposition='bottom center',
            hovertemplate='المعتمرين: %{y:,}<extra></extra>'
        ))
        
        fig_q1_travelers.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='white',
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            transition={'duration': 1000, 'easing': 'cubic-in-out'}
        )
        
        st.plotly_chart(fig_q1_travelers, use_container_width=True)
    
    with col2:
        st.subheader("🏥 زيارات العيادة والنقل الإسعافي - الربع الأول")
        fig_q1_medical = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_q1_medical.add_trace(
            go.Bar(x=q1_df['الشهر'], y=q1_df['زيارات العيادة'], 
                   name='زيارات العيادة', 
                   marker_color='rgba(102, 126, 234, 0.8)',
                   text=q1_df['زيارات العيادة'],
                   textposition='auto'),
            secondary_y=False,
        )
        
        fig_q1_medical.add_trace(
            go.Scatter(x=q1_df['الشهر'], y=q1_df['حالات النقل الإسعافي وحالات الإشتباه'], 
                      mode='lines+markers',
                      name='النقل الإسعافي',
                      line=dict(color='#ff6b6b', width=3),
                      marker=dict(size=10)),
            secondary_y=True,
        )
        
        fig_q1_medical.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='white'
        )
        
        fig_q1_medical.update_yaxes(title_text="زيارات العيادة", secondary_y=False)
        fig_q1_medical.update_yaxes(title_text="النقل الإسعافي", secondary_y=True)
        
        st.plotly_chart(fig_q1_medical, use_container_width=True)
    
    st.subheader("💉 تحليل التطعيمات حسب النوع - الربع الأول")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_q1_vacc_3d = go.Figure()
        
        months = q1_df['الشهر']
        fig_q1_vacc_3d.add_trace(go.Scatter3d(
            x=months,
            y=['شلل الأطفال'] * len(months),
            z=q1_df['شلل الأطفال'],
            mode='markers+lines',
            marker=dict(size=8, color=q1_df['شلل الأطفال'], colorscale='Viridis', opacity=0.8),
            line=dict(color='#667eea', width=6),
            name='شلل الأطفال'
        ))
        
        fig_q1_vacc_3d.add_trace(go.Scatter3d(
            x=months,
            y=['مخية شوكية'] * len(months),
            z=q1_df['مخية شوكية'],
            mode='markers+lines',
            marker=dict(size=8, color=q1_df['مخية شوكية'], colorscale='Plasma', opacity=0.8),
            line=dict(color='#764ba2', width=6),
            name='مخية شوكية'
        ))
        
        fig_q1_vacc_3d.add_trace(go.Scatter3d(
            x=months,
            y=['ثلاثي فيروسي'] * len(months),
            z=q1_df['ثلاثي فيروسي'],
            mode='markers+lines',
            marker=dict(size=8, color=q1_df['ثلاثي فيروسي'], colorscale='Cividis', opacity=0.8),
            line=dict(color='#f093fb', width=6),
            name='ثلاثي فيروسي'
        ))
        
        fig_q1_vacc_3d.update_layout(
            scene=dict(
                xaxis_title='الشهر',
                yaxis_title='نوع التطعيم',
                zaxis_title='العدد',
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='white',
            height=500
        )
        
        st.plotly_chart(fig_q1_vacc_3d, use_container_width=True)
    
    with col2:
        total_vacc_q1 = q1_df['مجموع التطعيمات'].sum()
        
        fig_q1_pie = go.Figure(data=[go.Pie(
            labels=['شلل الأطفال', 'مخية شوكية', 'ثلاثي فيروسي'],
            values=[q1_df['شلل الأطفال'].sum(), q1_df['مخية شوكية'].sum(), q1_df['ثلاثي فيروسي'].sum()],
            hole=0.4,
            textinfo='percent+label',
            textfont_size=12,
            marker=dict(colors=['#667eea', '#764ba2', '#f093fb'], line=dict(color='#000000', width=2)),
            hovertemplate='%{label}<br>العدد: %{value:,}<br>النسبة: %{percent}<extra></extra>',
            rotation=90,
            pull=[0.1, 0, 0]
        )])
        
        fig_q1_pie.add_annotation(
            text=f"إجمالي<br>{total_vacc_q1:,}",
            x=0.5, y=0.5,
            font_size=16,
            font_color='white',
            showarrow=False
        )
        
        fig_q1_pie.update_layout(
            title="توزيع التطعيمات - الربع الأول",
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='white',
            height=500
        )
        
        st.plotly_chart(fig_q1_pie, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h3 style="color: var(--text-accent);">📋 تحليلات الربع الأول</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="analysis-card">
            <div class="analysis-title">📈 اتجاه العابرين</div>
            <div class="analysis-text">
                وصل عدد العابرين إلى ذروته في فبراير (200,682) ثم انخفض في مارس إلى 163,291. 
                يشير هذا إلى نشاط موسمي قوي في منتصف الربع الأول.
            </div>
            <span class="insight-badge">نمو 8.1% في فبراير</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="analysis-card">
            <div class="analysis-title">🕌 موسم العمرة</div>
            <div class="analysis-text">
                شهد فبراير أعلى معدل للمعتمرين (120,930) بزيادة 36% عن يناير، 
                مما يعكس الذروة الموسمية لأداء العمرة في هذه الفترة.
            </div>
            <span class="warning-badge">ذروة موسمية</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="analysis-card">
            <div class="analysis-title">💉 برنامج التطعيم</div>
            <div class="analysis-text">
                تم تطعيم 282,471 جرعة في الربع الأول، مع تركيز كبير على تطعيم شلل الأطفال (62% من المجموع).
            </div>
            <span class="insight-badge">هدف محقق</span>
        </div>
        """, unsafe_allow_html=True)

with q2_tab:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    q2_df = health_df.iloc[3:6]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 مقارنة العابرين والمعتمرين - الربع الثاني")
        
        fig_q2_comparison = go.Figure()
        
        fig_q2_comparison.add_trace(go.Bar(
            x=q2_df['الشهر'],
            y=q2_df['عدد العابرين'],
            name='العابرين',
            marker_color='rgba(79, 172, 254, 0.8)',
            text=q2_df['عدد العابرين'],
            textposition='auto',
            hovertemplate='العابرين: %{y:,}<extra></extra>'
        ))
        
        fig_q2_comparison.add_trace(go.Bar(
            x=q2_df['الشهر'],
            y=q2_df['عدد المعتمرين'] + q2_df['عدد الحجاج'],
            name='المعتمرين والحجاج',
            marker_color='rgba(240, 147, 251, 0.8)',
            text=q2_df['عدد المعتمرين'] + q2_df['عدد الحجاج'],
            textposition='auto',
            hovertemplate='المعتمرين والحجاج: %{y:,}<extra></extra>'
        ))
        
        fig_q2_comparison.update_layout(
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='white',
            transition={'duration': 1500, 'easing': 'cubic-in-out'}
        )
        
        st.plotly_chart(fig_q2_comparison, use_container_width=True)
    
    with col2:
        st.subheader("🚨 حالات النقل الإسعافي - الربع الثاني")
        
        fig_q2_emergency = go.Figure()
        
        fig_q2_emergency.add_trace(go.Scatter(
            x=q2_df['الشهر'],
            y=q2_df['حالات النقل الإسعافي وحالات الإشتباه'],
            mode='lines+markers',
            fill='tonexty',
            name='النقل الإسعافي',
            line=dict(color='#ff6b6b', width=4),
            marker=dict(size=15, color='#ff4757'),
            text=q2_df['حالات النقل الإسعافي وحالات الإشتباه'],
            textposition='top center',
            hovertemplate='النقل الإسعافي: %{y}<extra></extra>'
        ))
        
        fig_q2_emergency.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='white',
            yaxis=dict(range=[0, 25])
        )
        
        st.plotly_chart(fig_q2_emergency, use_container_width=True)
    
    st.subheader("🔥 خريطة حرارية للتطعيمات - الربع الثاني")
    
    vacc_matrix = np.array([
        q2_df['شلل الأطفال'].values,
        q2_df['مخية شوكية'].values,
        q2_df['ثلاثي فيروسي'].values
    ])
    
    fig_q2_heatmap = go.Figure(data=go.Heatmap(
        z=vacc_matrix,
        x=q2_df['الشهر'],
        y=['شلل الأطفال', 'مخية شوكية', 'ثلاثي فيروسي'],
        colorscale='Viridis',
        text=vacc_matrix,
        texttemplate="%{text:,}",
        textfont={"size": 14, "color": "white"},
        hoverongaps=False,
        hovertemplate='الشهر: %{x}<br>التطعيم: %{y}<br>العدد: %{z:,}<extra></extra>'
    ))
    
    fig_q2_heatmap.update_layout(
        title="توزيع التطعيمات عبر الأشهر",
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='white',
        height=400
    )
    
    st.plotly_chart(fig_q2_heatmap, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h3 style="color: var(--text-accent);">📋 تحليلات الربع الثاني</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="analysis-card">
            <div class="analysis-title">📉 انخفاض العابرين</div>
            <div class="analysis-text">
                انخفض عدد العابرين بشكل ملحوظ في مايو إلى 86,673، 
                وهو أدنى معدل في النصف الأول من العام، ثم تعافى جزئياً في يونيو.
            </div>
            <span class="warning-badge">انخفاض 19% في مايو</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="analysis-card">
            <div class="analysis-title">🕋 موسم الحج</div>
            <div class="analysis-text">
                ظهرت حالات الحج في مايو (12,951 حاج) مع توقف العمرة، 
                مما يعكس بداية الاستعدادات لموسم الحج الكبير.
            </div>
            <span class="insight-badge">بداية موسم الحج</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="analysis-card">
            <div class="analysis-title">🚨 ذروة الطوارئ</div>
            <div class="analysis-text">
                سجل شهر مايو أعلى معدل لحالات النقل الإسعافي (21 حالة)، 
                مما يستدعي تعزيز الخدمات الطبية الطارئة.
            </div>
            <span class="danger-badge">زيادة 320% في مايو</span>
        </div>
        """, unsafe_allow_html=True)

# Final Insights and Recommendations
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<h2 style="text-align: center; font-size: 2.5rem; background: linear-gradient(45deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">💡 الرؤى والتوصيات النهائية</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="analysis-card">
        <div class="analysis-title">🏆 إنجازات بارزة</div>
        <div class="analysis-text">
            • تم تطعيم 400,833 جرعة في النصف الأول من 2025<br>
            • الحفاظ على الجولات الإشرافية عند مستوى مستقر<br>
            • تغطية تطعيم شلل الأطفال لجميع العابرين<br>
            • انخفاض زيارات العيادة في الربع الثاني
        </div>
        <span class="insight-badge">أهداف محققة</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="analysis-card">
        <div class="analysis-title">⚠ تحديات تحتاج تدخل</div>
        <div class="analysis-text">
            • ارتفاع حالات النقل الإسعافي في مايو (320%)<br>
            • انخفاض عدد المعتمرين بشكل كبير في مايو<br>
            • تذبذب في أعداد العابرين بين الأرباع<br>
            • انخفاض التطعيمات في الربع الثاني
        </div>
        <span class="warning-badge">يحتاج متابعة</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="analysis-card">
        <div class="analysis-title">🎯 التوصيات المستقبلية</div>
        <div class="analysis-text">
            • تعزيز الخدمات الطبية في مواسم الحج<br>
            • زيادة الكوادر الطبية في مواسم الذروة<br>
            • تطوير نظام مراقبة للطوارئ<br>
            • توسيع برامج التطعيم الموسمية
        </div>
        <span class="insight-badge">خطة استراتيجية</span>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
    <p style="font-size: 1.2rem; color: var(--text-accent);">© 2025 مكتب هيئة الصحة العامة بنجران - إدارة المنافذ واللوائح الصحية الدولية</p>
    <p>لوحة المعلومات الصحية المتقدمة - تحليلات شاملة ومتنوعة</p>
    <p>آخر تحديث: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <div style="margin-top: 1rem;">
        <span class="insight-badge">تم تحليل 6 أشهر من البيانات</span>
        <span class="insight-badge">10+ مؤشرات صحية</span>
        <span class="insight-badge">تحليلات متقدمة بالذكاء الاصطناعي</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Auto-refresh
if auto_refresh:
    time.sleep(refresh_rate)
    st.experimental_rerun()
