# /mount/src/stock-expert/app.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ============================================
# إعدادات الصفحة
# ============================================
st.set_page_config(
    page_title="ByToBy AI - منصة تحليل الأسهم",
    page_icon="📈",
    layout="wide"
)

# ============================================
# العنوان
# ============================================
st.title("📈 ByToBy AI")
st.subheader("منصة تحليل الأسهم بالذكاء الاصطناعي")

# ============================================
# الشريط الجانبي
# ============================================
with st.sidebar:
    st.image("https://via.placeholder.com/150x50?text=ByToBy+AI", use_container_width=True)
    st.markdown("---")
    
    st.markdown("### 📊 القائمة")
    page = st.radio(
        "",
        ["🏠 الرئيسية", "📈 تحليل الأسهم", "📰 الأخبار", "👤 الملف الشخصي"],
        index=0
    )
    
    st.markdown("---")
    st.caption("v1.0.0")

# ============================================
# صفحة الرئيسية
# ============================================
if page == "🏠 الرئيسية":
    st.markdown("---")
    
    # مؤشرات سريعة
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 إجمالي الأسهم", "1,234", "+2.5%")
    with col2:
        st.metric("💰 القيمة السوقية", "$45.6B", "+1.2%")
    with col3:
        st.metric("📈 المكاسب اليومية", "+3.4%", "↑")
    with col4:
        st.metric("⭐ الأسهم المفضلة", "12", "3")
    
    st.markdown("---")
    
    # بحث
    st.subheader("🔍 بحث عن سهم")
    symbol = st.text_input("", placeholder="أدخل رمز السهم (مثال: AAPL, TSLA, 2222.SR)", label_visibility="collapsed")
    if st.button("🔎 بحث", use_container_width=True):
        if symbol:
            st.success(f"✅ جاري تحليل {symbol.upper()}...")
    
    # الأسهم الموصى بها
    st.subheader("📊 الأسهم الموصى بها")
    
    stocks_data = [
        {"symbol": "AAPL", "name": "Apple Inc.", "price": 189.50, "change": 1.2, "recommendation": "شراء", "score": 92},
        {"symbol": "TSLA", "name": "Tesla Inc.", "price": 245.30, "change": -0.8, "recommendation": "احتفاظ", "score": 65},
        {"symbol": "BTC-USD", "name": "Bitcoin", "price": 45678, "change": 3.4, "recommendation": "شراء قوي", "score": 95},
        {"symbol": "AMZN", "name": "Amazon", "price": 156.20, "change": 0.5, "recommendation": "شراء", "score": 88},
        {"symbol": "2222.SR", "name": "السعودية للكهرباء", "price": 24.50, "change": 2.1, "recommendation": "شراء", "score": 78},
    ]
    
    for stock in stocks_data:
        cols = st.columns([1.5, 2, 1.5, 1.5, 1.5, 1])
        cols[0].write(f"**{stock['symbol']}**")
        cols[1].write(stock['name'])
        cols[2].write(f"${stock['price']:,.2f}")
        
        change_color = "🟢" if stock['change'] >= 0 else "🔴"
        cols[3].write(f"{change_color} {stock['change']:+.1f}%")
        
        if stock['recommendation'] in ["شراء قوي", "شراء"]:
            cols[4].success(stock['recommendation'])
        else:
            cols[4].warning(stock['recommendation'])
        
        cols[5].progress(stock['score']/100, text=f"{stock['score']}%")
        st.markdown("---")

# ============================================
# صفحة تحليل الأسهم
# ============================================
elif page == "📈 تحليل الأسهم":
    st.markdown("---")
    st.subheader("📈 تحليل الأسهم المتقدم")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        symbol = st.text_input("🔍 رمز السهم", placeholder="مثال: AAPL")
    with col2:
        timeframe = st.selectbox("📅 الإطار الزمني", ["1d", "5d", "1mo", "3mo", "6mo", "1y"])
    with col3:
        indicator = st.selectbox("📊 المؤشر", ["RSI", "MACD", "Bollinger Bands", "SMA", "EMA"])
    
    if st.button("🚀 تحليل", use_container_width=True):
        if symbol:
            with st.spinner(f"جاري تحليل {symbol.upper()}..."):
                # بيانات وهمية للرسم
                dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
                prices = np.random.randn(100).cumsum() + 100
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=dates,
                    y=prices,
                    mode='lines',
                    name=symbol.upper(),
                    line=dict(color='#2E86AB', width=2)
                ))
                fig.update_layout(
                    title=f'📈 {symbol.upper()} - {timeframe}',
                    xaxis_title='التاريخ',
                    yaxis_title='السعر ($)',
                    height=500,
                    template='plotly_white'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # تحليل سريع
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("السعر الحالي", f"${prices[-1]:.2f}", f"{np.random.uniform(-5, 5):+.2f}%")
                with col_b:
                    rsi_value = np.random.randint(30, 70)
                    st.metric("RSI", rsi_value, "محايد" if 30 < rsi_value < 70 else "تذبذب")
                with col_c:
                    st.metric("التوصية", "شراء" if prices[-1] > prices[0] else "احتفاظ")

# ============================================
# صفحة الأخبار
# ============================================
elif page == "📰 الأخبار":
    st.markdown("---")
    st.subheader("📰 أخبار السوق المالية")
    
    # فلتر الأخبار
    category = st.selectbox("📂 التصنيف", ["الكل", "الأسهم السعودية", "الأسهم العالمية", "الاقتصاد", "الطاقة"])
    
    news_data = [
        {"title": "🚀 السوق السعودي يرتفع بنسبة 2% مدعوماً بارتفاع النفط", "source": "العربية", "time": "منذ ساعتين"},
        {"title": "📉 الذهب يتراجع مع قوة الدولار وتوقعات رفع الفائدة", "source": "الشرق", "time": "منذ 3 ساعات"},
        {"title": "💰 أرباح Apple تتجاوز التوقعات بفضل مبيعات iPhone", "source": "بلومبرغ", "time": "منذ 5 ساعات"},
        {"title": "📊 Tesla تعلن عن نموذج جديد بسعر منافس", "source": "رويترز", "time": "منذ 8 ساعات"},
        {"title": "🏦 البنك المركزي يثبت سعر الفائدة عند 5.5%", "source": "أرقام", "time": "منذ 12 ساعة"},
    ]
    
    for news in news_data:
        with st.container():
            st.markdown(f"**{news['title']}**")
            st.caption(f"📰 {news['source']} | 🕐 {news['time']}")
            st.markdown("---")

# ============================================
# صفحة الملف الشخصي
# ============================================
else:
    st.markdown("---")
    st.subheader("👤 الملف الشخصي")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 معلومات الحساب")
        st.write("**البريد الإلكتروني:** user@example.com")
        st.write("**اسم المستخدم:** testuser")
        st.write("**الدور:** مستخدم")
        st.write("**تاريخ التسجيل:** 2024-01-01")
    
    with col2:
        st.markdown("### ⚙️ الإعدادات")
        
        with st.expander("🔐 تغيير كلمة المرور"):
            old_pass = st.text_input("كلمة المرور الحالية", type="password")
            new_pass = st.text_input("كلمة المرور الجديدة", type="password")
            confirm_pass = st.text_input("تأكيد كلمة المرور", type="password")
            
            if st.button("تحديث كلمة المرور"):
                if new_pass == confirm_pass:
                    st.success("✅ تم تغيير كلمة المرور بنجاح")
                else:
                    st.error("❌ كلمتا المرور غير متطابقتين")

# ============================================
# التذييل
# ============================================
st.markdown("---")
st.caption("© 2024 ByToBy AI - جميع الحقوق محفوظة")
