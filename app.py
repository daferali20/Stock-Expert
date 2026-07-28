# /mount/src/stock-expert/streamlit_app/app.py
import streamlit as st
import sys
import os

# إضافة المسار الحالي
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ============================================
# إعدادات الصفحة - يجب أن تكون أول شيء
# ============================================
st.set_page_config(
    page_title="ByToBy AI - منصة تحليل الأسهم",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# تهيئة حالة الجلسة
# ============================================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = "main"

# ============================================
# الوظائف المساعدة
# ============================================
def login_user(email, password):
    """تسجيل الدخول (محاكاة)"""
    if email and password:
        st.session_state.authenticated = True
        st.session_state.user = {"email": email, "name": "مستخدم"}
        return True
    return False

def logout_user():
    """تسجيل الخروج"""
    st.session_state.authenticated = False
    st.session_state.token = None
    st.session_state.user = None

# ============================================
# صفحة تسجيل الدخول
# ============================================
def login_page():
    """صفحة تسجيل الدخول"""
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
    }
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: #f8f9fa;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.image("https://via.placeholder.com/200x80?text=ByToBy+AI", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("### 🔐 تسجيل الدخول")
        
        with st.form("login_form"):
            email = st.text_input("📧 البريد الإلكتروني", placeholder="example@email.com")
            password = st.text_input("🔑 كلمة المرور", type="password", placeholder="••••••••")
            
            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("🚀 دخول", use_container_width=True)
            with col_b:
                if st.form_submit_button("📝 تسجيل", use_container_width=True):
                    st.info("سيتم تفعيل التسجيل قريباً")
            
            if submit:
                if not email or not password:
                    st.error("❌ يرجى إدخال البريد الإلكتروني وكلمة المرور")
                else:
                    if login_user(email, password):
                        st.success("✅ تم تسجيل الدخول بنجاح!")
                        st.rerun()
                    else:
                        st.error("❌ فشل تسجيل الدخول")
        
        st.markdown("---")
        st.caption("📌 حساب تجريبي: admin@bytoby.ai / password123")
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# لوحة التحكم الرئيسية
# ============================================
def dashboard_page():
    """صفحة لوحة التحكم"""
    st.markdown("### 📊 لوحة التحكم")
    
    # معلومات المستخدم
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 إجمالي الأسهم", "1,234", "+2.5%")
    with col2:
        st.metric("💰 قيمة المحفظة", "$45,678", "+1.2%")
    with col3:
        st.metric("📈 المكاسب اليومية", "+3.4%", "↑")
    with col4:
        st.metric("⭐ الأسهم المفضلة", "12", "3")
    
    st.markdown("---")
    
    # قسم البحث عن الأسهم
    st.subheader("🔍 بحث عن سهم")
    
    col_search, col_btn = st.columns([4, 1])
    with col_search:
        symbol = st.text_input("", placeholder="أدخل رمز السهم (مثال: AAPL, TSLA, 2222.SR)", label_visibility="collapsed")
    with col_btn:
        if st.button("🔎 بحث", use_container_width=True):
            if symbol:
                st.success(f"✅ جاري تحليل {symbol.upper()}...")
    
    # عرض الأسهم الموصى بها
    st.subheader("📊 الأسهم الموصى بها")
    
    stocks_data = [
        {"symbol": "AAPL", "name": "Apple Inc.", "price": "$189.50", "change": "+1.2%", "recommendation": "شراء", "score": 92},
        {"symbol": "TSLA", "name": "Tesla Inc.", "price": "$245.30", "change": "-0.8%", "recommendation": "احتفاظ", "score": 65},
        {"symbol": "BTC", "name": "Bitcoin", "price": "$45,678", "change": "+3.4%", "recommendation": "شراء قوي", "score": 95},
        {"symbol": "AMZN", "name": "Amazon", "price": "$156.20", "change": "+0.5%", "recommendation": "شراء", "score": 88},
        {"symbol": "2222.SR", "name": "السعودية للكهرباء", "price": "﷼24.50", "change": "+2.1%", "recommendation": "شراء", "score": 78},
    ]
    
    for stock in stocks_data:
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns([1.5, 2, 1.5, 1.5, 1.5, 1])
            with col1:
                st.write(f"**{stock['symbol']}**")
            with col2:
                st.caption(stock['name'])
            with col3:
                st.write(stock['price'])
            with col4:
                if stock['change'].startswith('+'):
                    st.success(stock['change'])
                else:
                    st.error(stock['change'])
            with col5:
                if stock['recommendation'] in ["شراء قوي", "شراء"]:
                    if stock['recommendation'] == "شراء قوي":
                        st.info("🔥 شراء قوي")
                    else:
                        st.success("✅ شراء")
                else:
                    st.warning("⚠️ احتفاظ")
            with col6:
                st.progress(stock['score']/100, text=f"{stock['score']}%")
            st.markdown("---")

# ============================================
# صفحة تحليل الأسهم
# ============================================
def analysis_page():
    """صفحة تحليل الأسهم المتقدم"""
    st.markdown("### 📈 تحليل الأسهم المتقدم")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        symbol = st.text_input("🔍 رمز السهم", placeholder="مثال: AAPL, TSLA, 2222.SR")
    
    with col2:
        timeframe = st.selectbox("📅 الإطار الزمني", ["1d", "5d", "1mo", "3mo", "6mo", "1y"])
    
    col3, col4, col5 = st.columns(3)
    with col3:
        indicator = st.selectbox("📊 المؤشر", ["RSI", "MACD", "Bollinger Bands", "SMA"])
    with col4:
        chart_type = st.selectbox("📉 نوع الرسم", ["Line", "Candlestick", "Bar"])
    with col5:
        if st.button("🚀 تحليل", use_container_width=True):
            if symbol:
                st.success(f"✅ تم تحليل {symbol.upper()} بنجاح")
    
    # عرض بيانات تحليلية وهمية
    if symbol:
        st.markdown("---")
        st.subheader(f"📊 تحليل {symbol.upper()}")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("السعر الحالي", "$189.50", "+1.2%")
        with col_b:
            st.metric("RSI", "62", "محايد")
        with col_c:
            st.metric("التوصية", "شراء", "قوية")
        
        # رسم بياني توضيحي
        st.info("📈 الرسم البياني التفاعلي سيظهر هنا")
        st.line_chart([100, 105, 102, 108, 112, 110, 115, 120, 118, 125])

# ============================================
# صفحة الملف الشخصي
# ============================================
def profile_page():
    """صفحة الملف الشخصي"""
    st.markdown("### 👤 الملف الشخصي")
    
    if st.session_state.user:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 معلومات الحساب")
            st.write(f"**البريد الإلكتروني:** {st.session_state.user.get('email', 'غير محدد')}")
            st.write(f"**الاسم:** {st.session_state.user.get('name', 'غير محدد')}")
            st.write(f"**الدور:** مستخدم")
            st.write(f"**تاريخ التسجيل:** 2024-01-01")
        
        with col2:
            st.subheader("⚙️ الإعدادات")
            
            with st.expander("🔐 تغيير كلمة المرور"):
                old_pass = st.text_input("كلمة المرور الحالية", type="password")
                new_pass = st.text_input("كلمة المرور الجديدة", type="password")
                confirm_pass = st.text_input("تأكيد كلمة المرور", type="password")
                
                if st.button("تحديث كلمة المرور"):
                    st.success("✅ تم تغيير كلمة المرور بنجاح")

# ============================================
# الوظيفة الرئيسية
# ============================================
def main():
    """الدالة الرئيسية للتطبيق"""
    
    # القائمة الجانبية
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50?text=ByToBy+AI", use_container_width=True)
        st.markdown("---")
        
        if st.session_state.authenticated:
            st.write(f"👋 مرحباً، {st.session_state.user.get('name', 'مستخدم')}")
            st.markdown("---")
            
            # قائمة التنقل
            page = st.radio(
                "📱 القائمة",
                ["📊 لوحة التحكم", "📈 تحليل الأسهم", "👤 الملف الشخصي"],
                index=0
            )
            
            st.markdown("---")
            
            if st.button("🚪 تسجيل الخروج", use_container_width=True):
                logout_user()
                st.rerun()
        else:
            page = "login"
    
    # عرض الصفحات
    if not st.session_state.authenticated:
        login_page()
    else:
        if page == "📊 لوحة التحكم":
            dashboard_page()
        elif page == "📈 تحليل الأسهم":
            analysis_page()
        elif page == "👤 الملف الشخصي":
            profile_page()

# ============================================
# تشغيل التطبيق
# ============================================
if __name__ == "__main__":
    main()
