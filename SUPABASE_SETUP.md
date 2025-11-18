# Supabase Integration Guide

## Step 1: Create Supabase Account & Database

1. **Sign up at https://supabase.com** (free tier available)
2. **Create a new project:**
   - Click "New project"
   - Choose a name (e.g., "chat-app")
   - Set region closest to you
   - Choose a strong password
   - Click "Create new project" (wait 2-3 minutes)

3. **Get your credentials:**
   - Go to Settings → API
   - Copy:
     - **Project URL** (SUPABASE_URL)
     - **anon public key** (SUPABASE_ANON_KEY)

## Step 2: Create Database Tables

In Supabase dashboard:

1. **Go to SQL Editor** → Click "New Query"
2. **Paste this SQL and execute:**

```sql
-- Create messages table
CREATE TABLE messages (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  room_id TEXT NOT NULL,
  user_handle TEXT NOT NULL,
  message_text TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX idx_messages_room_created ON messages(room_id, created_at DESC);

-- Create rooms table (optional, for room info)
CREATE TABLE rooms (
  id TEXT PRIMARY KEY,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security (RLS) for security
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE rooms ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all reads/writes (development only!)
CREATE POLICY "Allow all reads on messages" ON messages FOR SELECT USING (true);
CREATE POLICY "Allow all inserts on messages" ON messages FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow all reads on rooms" ON rooms FOR SELECT USING (true);
CREATE POLICY "Allow all inserts on rooms" ON rooms FOR INSERT WITH CHECK (true);
```

## Step 3: Set Environment Variables

Create/update `.env` file:

```env
SUPABASE_URL=your-project-url-from-above
SUPABASE_ANON_KEY=your-anon-key-from-above
SECRET_KEY=your-random-secret-key
```

## Step 4: Install Supabase Client

Add to `Chat_app/requirements.txt`:
```
supabase==1.0.0
postgrest-py==0.13.1
```

## Done!

The app will now:
- Save all messages to Supabase
- Load message history when users join a room
- Persist data even after server restarts
