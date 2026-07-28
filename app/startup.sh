#!/bin/bash
# startup.sh

# تشغيل FastAPI في الخلفية
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# تشغيل Streamlit
streamlit run streamlit_app/app.py --server.port ${PORT:-8501} --server.address 0.0.0.0 --server.headless true
