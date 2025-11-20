from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
import secrets
import os
from dotenv import load_dotenv
from pathlib import Path
import db

# Load environment variables from .env file (in parent directory)
# NOTE: On Render, you must add these variables in the "Environment" tab manually.
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

app = Flask(__name__, template_folder='Templates', static_folder='../static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')  

# IMPORTANT: Since you are using async_mode='eventlet', make sure 'eventlet' is in your requirements.txt
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet', ping_timeout=60, ping_interval=25, logger=False, engineio_logger=False)

# Initialize Supabase database
try:
    db.init_db()
except Exception as e:
    print(f"[WARNING] Database initialization failed: {e}")

def random_handle():
    return "Anon-" + secrets.token_hex(3)

@socketio.on("connect")
def handle_connect():
    print(f"[LOG] Client connected: {request.sid}")

@socketio.on("disconnect")
def handle_disconnect():
    print(f"[LOG] Client disconnected: {request.sid}")

@app.route("/")
def home():
    return render_template("index.html")

# When user joins room
@socketio.on("join")
def handle_join(data):
    room = data["room"]
    handle = random_handle()
    join_room(room)
    
    print(f"[LOG] User {handle} joined room {room}")
    
    # Create room entry in database if enabled
    try:
        db.create_room(room)
        # Send message history to the new user
        history = db.get_messages(room)
        emit("message_history", {"messages": history})
    except Exception as e:
        print(f"[ERROR] Database error on join: {e}")
    
    emit("system", f"{handle} joined the room.", to=room)
    emit("your_handle", handle)

# When user sends a message
@socketio.on("message")
def handle_message(data):
    room = data["room"]
    handle = data["handle"]
    text = data["text"]

    print(f"[LOG] Message from {handle} in {room}: {text}")
    
    # Save to Supabase if enabled
    try:
        db.save_message(room, handle, text)
    except Exception as e:
        print(f"[ERROR] Database save failed: {e}")
    
    emit("message", {"handle": handle, "text": text}, to=room)

if __name__ == "__main__":
    # FIX: Get the PORT from Render environment variable, default to 5000 only for local testing
    port = int(os.environ.get("PORT", 5000))
    
    print("\n" + "="*60)
    print(f"STARTING CHAT APP SERVER on PORT {port}")
    print("="*60)
    
    # FIX: Host must be '0.0.0.0' for Render to route traffic correctly
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)