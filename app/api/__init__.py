# backend/app/api/__init__.py
from . import auth, users, stocks, watchlist, ai, news, alerts, subscription, admin

__all__ = [
    "auth",
    "users", 
    "stocks",
    "watchlist",
    "ai",
    "news",
    "alerts",
    "subscription",
    "admin"
]
