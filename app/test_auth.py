# test_auth.py
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_register():
    """اختبار تسجيل مستخدم جديد"""
    url = f"{BASE_URL}/auth/register"
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "TestPassword123"
    }
    response = requests.post(url, json=data)
    print(f"Register Status: {response.status_code}")
    print(f"Register Response: {response.json()}")
    return response.json()

def test_login():
    """اختبار تسجيل الدخول"""
    url = f"{BASE_URL}/auth/login"
    data = {
        "email": "test@example.com",
        "password": "TestPassword123"
    }
    response = requests.post(url, json=data)
    print(f"Login Status: {response.status_code}")
    print(f"Login Response: {response.json()}")
    return response.json()

def test_get_me(token):
    """اختبار الحصول على معلومات المستخدم"""
    url = f"{BASE_URL}/auth/me"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"Get Me Status: {response.status_code}")
    print(f"Get Me Response: {response.json()}")
    return response.json()

if __name__ == "__main__":
    print("=" * 50)
    print("اختبار نظام المصادقة")
    print("=" * 50)
    
    # تسجيل مستخدم
    user = test_register()
    print("-" * 50)
    
    # تسجيل الدخول
    login_data = test_login()
    print("-" * 50)
    
    # الحصول على معلومات المستخدم
    if "access_token" in login_data:
        test_get_me(login_data["access_token"])
