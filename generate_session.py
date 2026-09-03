"""
Run this LOCALLY (on your own PC) once to generate a SESSION_STRING for the
assistant account that will join voice chats. Do NOT run this on Render.

Usage:
    pip install pyrogram tgcrypto
    python3 generate_session.py

It will ask for your API_ID, API_HASH, phone number, and OTP.
Copy the printed session string into Render's SESSION_STRING env var.

NEVER share your session string with anyone — it gives full access to that account.
"""

from pyrogram import Client

api_id = int(input("Enter your API_ID: "))
api_hash = input("Enter your API_HASH: ").strip()

with Client("assistant_session", api_id=api_id, api_hash=api_hash) as app:
    print("\n\nYour SESSION_STRING (keep it secret):\n")
    print(app.export_session_string())
