# setup.py
from setuptools import setup, find_packages

setup(
    name="bytoby-ai",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn[standard]>=0.23.0",
        "sqlalchemy>=2.0.0",
        "asyncpg>=0.29.0",
        "psycopg2-binary>=2.9.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.6",
        "email-validator>=2.0.0",
        "alembic>=1.11.0",
        "python-dotenv>=1.0.0",
    ],
)
