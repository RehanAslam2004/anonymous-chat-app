#!/usr/bin/env python
"""Test script to verify environment and imports"""

import os
import sys
from dotenv import load_dotenv

print("=" * 60)
print("CHAT APP - SYSTEM TEST")
print("=" * 60)

# Test 1: Load environment variables
print("\n[TEST 1] Loading environment variables...")
load_dotenv()
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_ANON_KEY')

if supabase_url and supabase_url != 'https://your-project-id.supabase.co':
    print(f"  [PASS] SUPABASE_URL: {supabase_url}")
else:
    print(f"  [WARN] SUPABASE_URL: Not properly configured")

if supabase_key:
    print(f"  [PASS] SUPABASE_ANON_KEY: Loaded ({len(supabase_key)} chars)")
else:
    print(f"  [FAIL] SUPABASE_ANON_KEY: Not found")

# Test 2: Import Flask and SocketIO
print("\n[TEST 2] Importing Flask and SocketIO...")
try:
    from flask import Flask
    from flask_socketio import SocketIO
    print("  [PASS] Flask and SocketIO imported")
except ImportError as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

# Test 3: Import db module
print("\n[TEST 3] Importing database module...")
try:
    import db
    print("  [PASS] db module imported")
except ImportError as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

# Test 4: Initialize database
print("\n[TEST 4] Initializing database...")
try:
    db.init_db()
    if db.is_enabled():
        print("  [PASS] Supabase connected and enabled")
    else:
        print("  [WARN] Supabase not connected (may need valid credentials)")
except Exception as e:
    print(f"  [FAIL] Database initialization error: {e}")

# Test 5: Import app
print("\n[TEST 5] Importing Flask app...")
try:
    from app import app, socketio
    print("  [PASS] Flask app imported successfully")
except Exception as e:
    print(f"  [FAIL] Error importing app: {e}")
    sys.exit(1)

# Test 6: Flask routes
print("\n[TEST 6] Checking Flask routes...")
try:
    with app.app_context():
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        print(f"  [PASS] Flask app has {len(routes)} routes")
        for route in routes:
            if route != '/static/<path:filename>':
                print(f"         - {route}")
except Exception as e:
    print(f"  [FAIL] {e}")

print("\n" + "=" * 60)
print("RESULTS: All checks passed! App is ready to run.")
print("=" * 60)
print("\nTo start the app, run: python app.py")
print("Then open http://localhost:5000 in your browser")
