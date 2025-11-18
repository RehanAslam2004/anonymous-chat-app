#!/usr/bin/env python
"""Quick status check for the chat app"""

import requests
import json
from time import sleep

print("\n" + "="*60)
print("CHAT APP - STATUS CHECK")
print("="*60)

# Check if server is running
try:
    response = requests.get('http://localhost:5000', timeout=5)
    print("\n[SERVER] Status: RUNNING")
    print(f"         URL: http://localhost:5000")
    print(f"         HTTP Status: {response.status_code}")
    
    if 'Anonymous Chat' in response.text:
        print("[PAGE]   Status: LOADED")
        print("         Title: Anonymous Chat found")
    
    if 'socket.io' in response.text.lower():
        print("[SOCKET.IO] Status: INCLUDED")
        print("           Client library loaded")
    
    print("\n" + "="*60)
    print("APP IS READY!")
    print("="*60)
    print("\nTo use the app:")
    print("  1. Open http://localhost:5000 in your browser")
    print("  2. Join a room (e.g., 'room-1', 'test-room')")
    print("  3. Send messages - they will save to Supabase!")
    print("\nTo test persistence:")
    print("  1. Send 3-4 messages")
    print("  2. Stop the app (Ctrl+C)")
    print("  3. Restart it: python app.py")
    print("  4. Rejoin the room")
    print("  5. Your messages should reappear!")
    print("="*60 + "\n")
    
except requests.exceptions.ConnectionError:
    print("[ERROR] Cannot connect to server!")
    print("        Is app.py running?")
    print("        Run: python app.py")
except Exception as e:
    print(f"[ERROR] {e}")
