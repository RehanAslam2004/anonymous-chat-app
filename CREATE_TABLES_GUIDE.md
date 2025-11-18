# Step-by-Step: Create Tables in Supabase

Follow these exact steps to create your database tables.

## Prerequisites
✅ You have created a Supabase account
✅ You have a project created (Status: "Active")

---

## Step 1: Open SQL Editor

1. **Login to Supabase** → https://supabase.com
2. Click on your **project name** to enter the project
3. In the left sidebar, look for **SQL Editor** (or **Editor**)
4. Click on **SQL Editor**

You should see a window with "SQL" at the top.

---

## Step 2: Create a New Query

1. Click the **"+" button** or **"New Query"** button
2. You'll see an empty editor with a cursor

---

## Step 3: Copy the SQL Code

Copy all of this code (everything from -- Create rooms table to the last policy):

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

---

## Step 4: Paste into Supabase

1. Click in the **SQL editor window**
2. Press **Ctrl+A** to select all (if there's any existing text)
3. Press **Ctrl+V** to paste the code

Your editor should now show all the SQL commands.

---

## Step 5: Execute the Query

1. Look for a **"Run" button** (usually blue, top-right of editor)
2. Click **"Run"** or press **Ctrl+Enter**

Wait a few seconds...

---

## Step 6: Verify Success

You should see a **green checkmark** ✓ and a message like:
```
Query executed successfully
```

**That's it!** Your tables are now created.

---

## What Was Created?

### 1. **rooms** table
Stores information about each chat room:
- `id` - Room identifier (e.g., "1234")
- `created_at` - When the room was created
- `updated_at` - Last update time

### 2. **messages** table
Stores all the messages:
- `id` - Message ID (auto-incrementing)
- `room_id` - Which room this message belongs to
- `user_handle` - Anonymous name (e.g., "Creative_Fox")
- `message_text` - The actual message
- `created_at` - When sent
- `updated_at` - Last update time

### 3. **Index**
Speed up database queries when looking for messages in a room

### 4. **Security Policies** (RLS)
Allow your app to read and write messages (development mode - all access allowed)

---

## Troubleshooting

### "Error: relation already exists"
- This is OK! It means the tables already exist.
- Your chat app can still use them.

### "Error: syntax error"
- Make sure you copied the ENTIRE code block
- Check that no characters got cut off
- Try again from Step 3

### Nothing happens when I click Run
- Make sure the SQL editor window is active (click in it)
- Check that your internet connection is working
- Try refreshing the Supabase page

---

## Next Steps

1. Go back to the integration guide
2. **Step 3: Get Your Credentials**
   - Settings → API
   - Copy Project URL and Anon Key
3. Add them to your `.env` file in Chat_app directory
4. Run `pip install -r requirements.txt`
5. Run `python app.py`

---

## Visual Reference

If you get stuck, check the Supabase Docs:
https://supabase.com/docs/guides/database/overview
