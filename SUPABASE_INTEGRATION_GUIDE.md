# Supabase Integration Guide - Chat App

This guide explains how to set up Supabase PostgreSQL database for the chat app to persist messages.

## What's New?

Your chat app now has database integration enabled! Messages are automatically saved and loaded from Supabase.

**Features:**
- ✅ Messages persist across app restarts
- ✅ Message history loads when joining a room
- ✅ Automatic message storage (happens silently in the background)
- ✅ Development mode works without Supabase (optional)

## Step 1: Create Supabase Project

1. Go to https://supabase.com and sign up (free tier available)
2. Click "New Project" and fill in:
   - **Project Name**: `chat-app` (or your choice)
   - **Database Password**: Save this securely
   - **Region**: Choose closest to you
3. Wait for the project to initialize (5-10 minutes)

## Step 2: Create Database Tables

1. In Supabase dashboard, go to **SQL Editor**
2. Click **New Query**
3. Copy and paste this SQL:

```sql
-- Create rooms table
CREATE TABLE IF NOT EXISTS rooms (
    id TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
    id BIGSERIAL PRIMARY KEY,
    room_id TEXT NOT NULL REFERENCES rooms(id),
    user_handle TEXT NOT NULL,
    message_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_messages_room_created 
ON messages(room_id, created_at);

-- Enable RLS (Row Level Security)
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE rooms ENABLE ROW LEVEL SECURITY;

-- Create policies for development (allow all)
CREATE POLICY "Allow all reads" ON messages FOR SELECT TO authenticated, anon USING (true);
CREATE POLICY "Allow all inserts" ON messages FOR INSERT TO authenticated, anon WITH CHECK (true);
CREATE POLICY "Allow all room reads" ON rooms FOR SELECT TO authenticated, anon USING (true);
CREATE POLICY "Allow all room inserts" ON rooms FOR INSERT TO authenticated, anon WITH CHECK (true);
```

4. Click **Run** and wait for success

## Step 3: Get Your Credentials

1. In Supabase, go to **Settings** → **API**
2. Copy these values:
   - **Project URL** (looks like `https://xxxxx.supabase.co`)
   - **Anon Key** (public key)

## Step 4: Configure Your Chat App

1. Open `.env` file in your Chat app directory
2. Replace the placeholder values:

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SECRET_KEY=dev-secret-key-change-in-production
FLASK_ENV=development
```

3. Save the file

## Step 5: Install Dependencies

Open terminal in your Chat app directory and run:

```bash
pip install -r requirements.txt
```

This installs:
- `supabase` - Database client
- `python-dotenv` - Environment variable management
- `psycopg2-binary` - PostgreSQL adapter

## Step 6: Run Your Chat App

```bash
python app.py
```

The app will:
1. Load your Supabase credentials from `.env`
2. Initialize the database connection
3. Automatically save messages when sent
4. Load message history when users join rooms

## Testing the Integration

1. **Test 1: Single user**
   - Open http://localhost:5000
   - Join room "test-room"
   - Send a few messages
   - Close and reopen the app
   - Join "test-room" again
   - ✅ You should see your old messages!

2. **Test 2: Multiple users**
   - Open two browser windows
   - Join the same room from both
   - Send messages between them
   - ✅ All messages should persist and load

## Troubleshooting

### "ModuleNotFoundError: No module named 'supabase'"
- Run: `pip install -r requirements.txt`
- Make sure you're in the Chat_app directory

### "Database connection failed"
- Check your `.env` file has correct SUPABASE_URL and SUPABASE_ANON_KEY
- Verify Supabase project is running (check dashboard)
- Ensure you completed Step 2 (created the tables)

### Messages not saving
- Check app.py console logs for errors
- Verify `.env` file exists in Chat_app directory
- Make sure RLS policies are created (Step 2)

### Database works locally but not on production
- On Render/Railway/Heroku, add `.env` variables to their environment settings
- Dashboard → Environment variables → Add SUPABASE_URL and SUPABASE_ANON_KEY

## How It Works (Technical Details)

### Database Schema

**messages table:**
```
id: Unique message identifier
room_id: Which room the message is in
user_handle: Anonymous name (e.g., "Creative_Fox")
message_text: The actual message content
created_at: When the message was sent
updated_at: Last update timestamp
```

**rooms table:**
```
id: Room identifier (e.g., "1234")
created_at: When room was created
updated_at: Last activity
```

### How Messages Flow

1. **User sends message** → Socket.IO event "message"
2. **Server receives** → Calls `db.save_message(room, handle, text)`
3. **Database saves** → Inserted into messages table
4. **Server broadcasts** → Emits to all users in room
5. **User joins later** → Server calls `db.get_messages(room)`
6. **History loads** → All old messages sent to new user

### File Changes Made

- **app.py**: Added `import db`, calls `db.init_db()`, `db.save_message()`, `db.get_messages()`
- **Templates/index.html**: Added handler for `message_history` event
- **db.py**: New module with all database functions
- **requirements.txt**: Added supabase, python-dotenv, psycopg2-binary
- **.env**: Local development environment variables

## Production Deployment

When deploying to Render/Railway/Heroku:

1. **Don't commit `.env`** - It's in `.gitignore` for security
2. **Set env variables** in your hosting platform's dashboard:
   - SUPABASE_URL
   - SUPABASE_ANON_KEY
   - SECRET_KEY (generate a strong one)
3. **Database will work automatically** - No additional setup needed

See `HOSTING.md` for detailed deployment steps.

## Next Steps

- 📊 Add room cleanup (delete old messages after 7 days)
- 🔐 Add RLS security policies for production
- 📱 Add room analytics (message count, active users)
- 🗑️ Add delete message feature (admins only)

## Need Help?

Check these resources:
- Supabase Docs: https://supabase.com/docs
- Flask-SocketIO: https://flask-socketio.readthedocs.io
- Troubleshooting in-app logs at `app.py` console output
