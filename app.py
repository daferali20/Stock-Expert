# /mount/src/stock-expert/app.py (في الجذر)
import streamlit as st

# ============================================
# إعدادات الصفحة - يجب أن تكون أول شيء
# ============================================
st.set_page_config(
    page_title="ByToBy AI",
    page_icon="📈",
    layout="wide"
)

# ============================================
# العنوان الرئيسي
# ============================================
st.title("📈 ByToBy AI")
st.subheader("منصة تحليل الأسهم بالذكاء الاصطناعي")
st.markdown("---")

# ============================================
# المحتوى الرئيسي
# ============================================

# عرض الميزات في أعمدة
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📊 تحليل فني
    - رسوم بيانية تفاعلية
    - مؤشرات فنية متقدمة
    - تنبيهات الأسعار
    """)

with col2:
    st.markdown("""
    ### 🤖 ذكاء اصطناعي
    - توصيات مدروسة
    - تحليل المشاعر
    - توقعات الأسعار
    """)

with col3:
    st.markdown("""
    ### 📰 أخبار السوق
    - تحديثات لحظية
    - تحليل الأخبار
    - تأثير على الأسهم
    """)

st.markdown("---")

# ============================================
# قسم البحث عن الأسهم
# ============================================
st.subheader("🔍 بحث عن سهم")

col_search, col_btn = st.columns([4, 1])

with col_search:
    symbol = st.text_input("", placeholder="أدخل رمز السهم (مثال: AAPL, TSLA, 2222.SR)", label_visibility="collapsed")

with col_btn:
    if st.button("🔎 بحث", use_container_width=True):
        if symbol:
            st.success(f"✅ جاري تحليل {symbol.upper()}...")
            st.info(f"📊 عرض بيانات {symbol.upper()}")

# ============================================
# عرض الأسهم الموصى بها
# ============================================
st.subheader("📊 الأسهم الموصى بها")

# بيانات وهمية للأسهم
stocks = [
    {"symbol": "AAPL", "name": "Apple Inc.", "price": "$189.50", "change": "+1.2%", "recommendation": "🟢 شراء"},
    {"symbol": "TSLA", "name": "Tesla Inc.", "price": "$245.30", "change": "-0.8%", "recommendation": "🟡 احتفاظ"},
    {"symbol": "BTC", "name": "Bitcoin", "price": "$45,678", "change": "+3.4%", "recommendation": "🟢 شراء قوي"},
    {"symbol": "AMZN", "name": "Amazon", "price": "$156.20", "change": "+0.5%", "recommendation": "🟢 شراء"},
    {"symbol": "2222.SR", "name": "السعودية للكهرباء", "price": "﷼24.50", "change": "+2.1%", "recommendation": "🟢 شراء"},
]

for stock in stocks:
    col1, col2, col3, col4, col5 = st.columns([2, 3, 2, 2, 3])
    
    with col1:
        st.write(f"**{stock['symbol']}**")
    with col2:
        st.write(stock['name'])
    with col3:
        st.write(stock['price'])
    with col4:
        if stock['change'].startswith('+'):
            st.success(stock['change'])
        else:
            st.error(stock['change'])
    with col5:
        st.write(stock['recommendation'])
    
    st.markdown("---")

# ============================================
# أخبار السوق
# ============================================
st.subheader("📰 آخر الأخبار")

news_items = [
    "🚀 السوق السعودي يرتفع بنسبة 2% مدعوماً بارتفاع النفط",
    "📉 الذهب يتراجع مع قوة الدولار وتوقعات رفع الفائدة",
    "💰 أرباح Apple تتجاوز التوقعات بفضل مبيعات iPhone",
    "📊 Tesla تعلن عن نموذج جديد بسعر منافس",
    "🏦 البنك المركزي يثبت سعر الفائدة عند 5.5%",
]

for news in news_items:
    st.info(news)

# ============================================
# تذييل الصفحة
# ============================================
st.markdown("---")
st.caption("© 2024 ByToBy AI - جميع الحقوق محفوظة | v1.0.0")
