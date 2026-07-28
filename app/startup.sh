#!/bin/bash
# startup.sh

echo "🚀 Starting ByToBy AI Platform..."

# تشغيل FastAPI في الخلفية
echo "📡 Starting FastAPI backend..."
cd /app
python -c "
import sys
sys.path.insert(0, '/app')
from app.main import app
import uvicorn
uvicorn.run(app, host='0.0.0.0', port=8000)
" &
BACKEND_PID=$!

# انتظار بدء الـ API
sleep 5

# تشغيل Streamlit
echo "🎨 Starting Streamlit frontend..."
streamlit run streamlit_app/app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true

# في حال توقف Streamlit، أوقف الـ API أيضاً
kill $BACKEND_PID
