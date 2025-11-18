"""
Supabase database module for chat app
Handles message storage and retrieval
"""

import os
from supabase import create_client, Client
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import requests

# Load environment variables from .env file (in parent directory)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY', '')

supabase: Client = None

def init_db():
    """Initialize Supabase connection"""
    global supabase
    if SUPABASE_URL and SUPABASE_ANON_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        print("[DB] Supabase initialized")
        return True
    else:
        print("[DB] Supabase not configured - running in memory mode")
        return False

def is_enabled():
    """Check if Supabase is enabled"""
    return supabase is not None

def save_message(room_id: str, user_handle: str, message_text: str):
    """Save a message to the database"""
    if not is_enabled():
        return None
    
    data = {
        'room_id': str(room_id).strip(),
        'user_handle': str(user_handle).strip(),
        'message_text': str(message_text).strip()
    }
    # First attempt: supabase client
    if is_enabled():
        try:
            response = supabase.table('messages').insert([data]).execute()
            resp_data = getattr(response, 'data', None)
            resp_error = getattr(response, 'error', None)
            print(f"[DB] Insert response raw: {response!r}")
            print(f"[DB] Insert response data: {resp_data}")
            print(f"[DB] Insert response error: {resp_error}")
            if resp_error:
                print(f"[DB] Error saving message (supabase error): {resp_error}")
            else:
                print(f"[DB] Message saved (client): {user_handle} in {room_id}")
                return response
        except Exception as e:
            print(f"[DB] Exception saving message with client: {e}")

    # Fallback: use direct REST call to PostgREST
    try:
        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/messages"
        headers = {
            'apikey': SUPABASE_ANON_KEY,
            'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
        resp = requests.post(url, headers=headers, json=[data], timeout=10)
        print(f"[DB][REST] POST {url} status={resp.status_code} body={resp.text}")
        if resp.status_code in (200, 201):
            try:
                return resp.json()
            except Exception:
                return resp.text
        else:
            print(f"[DB][REST] Failed to save message: {resp.status_code} {resp.text}")
            return None
    except Exception as e:
        print(f"[DB][REST] Exception saving message: {e}")
        return None

def get_messages(room_id: str, limit: int = 50):
    """Retrieve message history for a room"""
    if not is_enabled():
        return []
    
    room_id = str(room_id).strip()
    # First attempt: supabase client
    if is_enabled():
        try:
            response = supabase.table('messages').select('*').eq('room_id', room_id).order('created_at', desc=False).limit(limit).execute()
            resp_data = getattr(response, 'data', None)
            resp_error = getattr(response, 'error', None)
            print(f"[DB] Select response raw: {response!r}")
            print(f"[DB] Select response data: {resp_data}")
            print(f"[DB] Select response error: {resp_error}")
            if resp_error:
                print(f"[DB] Error retrieving messages (supabase error): {resp_error}")
            else:
                messages = resp_data if resp_data else []
                print(f"[DB] Retrieved {len(messages)} messages for room {room_id} (client)")
                return messages
        except Exception as e:
            print(f"[DB] Exception retrieving messages with client: {e}")

    # Fallback: direct REST GET
    try:
        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/messages"
        params = {
            'select': '*',
            'room_id': f'eq.{room_id}',
            'order': 'created_at.asc',
            'limit': str(limit)
        }
        headers = {
            'apikey': SUPABASE_ANON_KEY,
            'Authorization': f'Bearer {SUPABASE_ANON_KEY}'
        }
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"[DB][REST] GET {url} status={resp.status_code} url={resp.url}")
        print(f"[DB][REST] body={resp.text}")
        if resp.status_code == 200:
            try:
                return resp.json()
            except Exception:
                return []
        else:
            print(f"[DB][REST] Failed to retrieve messages: {resp.status_code} {resp.text}")
            return []
    except Exception as e:
        print(f"[DB][REST] Exception retrieving messages: {e}")
        return []

def create_room(room_id: str):
    """Create a room entry (optional)"""
    if not is_enabled():
        return None
    
    try:
        room_id = str(room_id).strip()
        response = supabase.table('rooms').insert([{
            'id': room_id,
            'created_at': datetime.utcnow().isoformat()
        }]).execute()
        print(f"[DB] Room created: {room_id}")
        return response
    except Exception as e:
        # Room might already exist - this is OK
        if 'duplicate' in str(e).lower() or 'unique' in str(e).lower():
            print(f"[DB] Room exists: {room_id}")
        else:
            print(f"[DB] Room: {e}")
        return None

def delete_old_messages(room_id: str = None, days: int = 7):
    """Delete messages older than specified days (cleanup)"""
    if not is_enabled():
        return None
    
    try:
        query = supabase.table('messages').delete()
        if room_id:
            query = query.eq('room_id', room_id)
        # This would require Supabase to support date comparisons
        # For now, just log
        print(f"[DB] Message cleanup would delete messages older than {days} days")
        return None
    except Exception as e:
        print(f"[DB] Error in cleanup: {e}")
        return None
