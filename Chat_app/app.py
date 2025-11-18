from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
import secrets
import os
from dotenv import load_dotenv
from pathlib import Path
import db

# Load environment variables from .env file (in parent directory)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

app = Flask(__name__, template_folder='Templates', static_folder='../static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')  
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet', ping_timeout=60, ping_interval=25, logger=False, engineio_logger=False)

# Initialize Supabase database
db.init_db()

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
    db.create_room(room)
    
    # Send message history to the new user
    history = db.get_messages(room)
    emit("message_history", {"messages": history})
    
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
    db.save_message(room, handle, text)
    
    emit("message", {"handle": handle, "text": text}, to=room)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("STARTING CHAT APP SERVER")
    print("="*60)
    print("URL: http://127.0.0.1:5000")
    print("Opening http://localhost:5000 in your browser...")
    print("="*60 + "\n")
    socketio.run(app, host='127.0.0.1', port=5000, debug=False, allow_unsafe_werkzeug=True)
