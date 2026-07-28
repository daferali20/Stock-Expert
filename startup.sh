#!/bin/bash
# /mount/src/stock-expert/startup.sh

echo "🚀 Starting ByToBy AI Platform..."

# تشغيل FastAPI في الخلفية
echo "📡 Starting FastAPI backend on port 8000..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# انتظار بدء الـ API
echo "⏳ Waiting for backend to start..."
sleep 5

# تشغيل Streamlit
echo "🎨 Starting Streamlit frontend on port 8501..."
streamlit run streamlit_app/app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true --server.enableCORS=true

# في حال توقف Streamlit، أوقف الـ API أيضاً
kill $BACKEND_PID 2>/dev/null
