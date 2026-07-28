#!/bin/bash
# /mount/src/stock-expert/startup.sh

echo "🚀 Starting ByToBy AI Platform..."
echo "===================================="

# تثبيت التبعيات أولاً
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn[standard] python-dotenv
pip install streamlit plotly pandas numpy requests

# تشغيل FastAPI
echo "📡 Starting FastAPI backend..."
cd /mount/src/stock-expert
python -c "
import sys
sys.path.insert(0, '/mount/src/stock-expert')
from app.main import app
import uvicorn
uvicorn.run(app, host='0.0.0.0', port=8000)
" &
BACKEND_PID=$!

# انتظار بدء الـ API
echo "⏳ Waiting for backend..."
sleep 5

# تشغيل Streamlit
echo "🎨 Starting Streamlit..."
streamlit run app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=true

# إيقاف FastAPI عند توقف Streamlit
kill $BACKEND_PID 2>/dev/null
