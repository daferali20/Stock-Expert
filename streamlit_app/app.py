# streamlit_app/app.py
import streamlit as st
import requests
import json

st.set_page_config(
    page_title="ByToBy AI",
    page_icon="📈",
    layout="wide"
)

# تهيئة حالة الجلسة
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None

# العنوان الرئيسي
st.title("📈 ByToBy AI")
st.subheader("منصة تحليل الأسهم بالذكاء الاصطناعي")

# شريط جانبي
with st.sidebar:
    st.image("https://via.placeholder.com/150x50?text=ByToBy+AI", use_container_width=True)
    st.markdown("---")
    
    if not st.session_state.authenticated:
        st.subheader("🔐 تسجيل الدخول")
        
        with st.form("login_form"):
            email = st.text_input("📧 البريد الإلكتروني")
            password = st.text_input("🔑 كلمة المرور", type="password")
            submit = st.form_submit_button("🚀 دخول")
            
            if submit:
                if email and password:
                    try:
                        response = requests.post(
                            "http://localhost:8000/api/v1/auth/login",
                            json={"email": email, "password": password}
                        )
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.authenticated = True
                            st.session_state.token = data["access_token"]
                            st.session_state.user = {"email": email}
                            st.success("✅ تم تسجيل الدخول بنجاح!")
                            st.rerun()
                        else:
                            st.error("❌ فشل تسجيل الدخول")
                    except Exception as e:
                        st.error(f"❌ خطأ: {e}")
    else:
        st.write(f"👋 مرحباً، {st.session_state.user.get('email', 'مستخدم')}")
        st.markdown("---")
        
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.authenticated = False
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()

# المحتوى الرئيسي
if st.session_state.authenticated:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 الأسهم", "1,234")
    with col2:
        st.metric("📈 التغير", "+2.5%")
    with col3:
        st.metric("⭐ المفضلة", "12")
    
    st.markdown("---")
    st.subheader("🔍 بحث عن سهم")
    
    symbol = st.text_input("أدخل رمز السهم", placeholder="مثال: AAPL, TSLA, BTC-USD")
    if st.button("🔎 بحث"):
        if symbol:
            try:
                response = requests.get(
                    f"http://localhost:8000/api/v1/stocks/{symbol.upper()}",
                    headers={"Authorization": f"Bearer {st.session_state.token}"}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ تم العثور على {symbol.upper()}")
                    st.json(data)
                else:
                    st.error("❌ لم يتم العثور على السهم")
            except Exception as e:
                st.error(f"❌ خطأ: {e}")
else:
    st.info("👈 يرجى تسجيل الدخول من القائمة الجانبية")
    st.markdown("""
    ### 🚀 الميزات المتاحة:
    - 📊 تحليل الأسهم في الوقت الحقيقي
    - 🤖 توصيات مدعومة بالذكاء الاصطناعي
    - 📰 أخبار السوق المالية
    - 🔔 تنبيهات الأسعار
    - 📈 مؤشرات فنية متقدمة
    """)
