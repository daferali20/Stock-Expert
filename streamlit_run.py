# streamlit_run.py (في جذر المشروع)
import streamlit as st
import sys
import os

# أضف المسار الحالي إلى sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="ByToBy AI",
    page_icon="📈",
    layout="wide"
)

st.title("📈 ByToBy AI - منصة تحليل الأسهم")
st.write("🚀 جاري تحميل التطبيق...")

# استيراد تطبيق Streamlit الرئيسي
try:
    from streamlit_app.app import main as streamlit_main
    streamlit_main()
except ImportError as e:
    st.error(f"❌ خطأ في تحميل التطبيق: {e}")
    st.info("الرجاء التأكد من وجود مجلد streamlit_app")
