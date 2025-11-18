#!/usr/bin/env python
import socketio
import time

# Create two Socket.IO clients
sio1 = socketio.Client()
sio2 = socketio.Client()

room = "test_room"
events1 = []
events2 = []

@sio1.event
def connect():
    print("Client 1: Connected")

@sio1.event
def disconnect():
    print("Client 1: Disconnected")

@sio1.on('your_handle')
def on_handle_1(data):
    print(f"Client 1: Got handle: {data}")
    events1.append(('your_handle', data))

@sio1.on('system')
def on_system_1(msg):
    print(f"Client 1: System message: {msg}")
    events1.append(('system', msg))

@sio1.on('message')
def on_message_1(data):
    print(f"Client 1: Message: {data}")
    events1.append(('message', data))

@sio2.event
def connect():
    print("Client 2: Connected")

@sio2.event
def disconnect():
    print("Client 2: Disconnected")

@sio2.on('your_handle')
def on_handle_2(data):
    print(f"Client 2: Got handle: {data}")
    events2.append(('your_handle', data))

@sio2.on('system')
def on_system_2(msg):
    print(f"Client 2: System message: {msg}")
    events2.append(('system', msg))

@sio2.on('message')
def on_message_2(data):
    print(f"Client 2: Message: {data}")
    events2.append(('message', data))

try:
    print("Connecting Client 1...")
    sio1.connect('http://localhost:5000')
    time.sleep(0.5)
    
    print(f"\nClient 1 joining room '{room}'...")
    sio1.emit('join', {'room': room})
    time.sleep(1)
    
    print("\nConnecting Client 2...")
    sio2.connect('http://localhost:5000')
    time.sleep(0.5)
    
    print(f"\nClient 2 joining room '{room}'...")
    sio2.emit('join', {'room': room})
    time.sleep(1)
    
    # Simulate Client 1 sending a message
    print("\nClient 1 sending a message...")
    if events1:
        handle1 = events1[0][1]  # Get the handle from 'your_handle' event
        sio1.emit('message', {'room': room, 'handle': handle1, 'text': 'Hello from Client 1!'})
    time.sleep(1)
    
    # Simulate Client 2 sending a message
    print("\nClient 2 sending a message...")
    if events2:
        handle2 = events2[0][1]  # Get the handle from 'your_handle' event
        sio2.emit('message', {'room': room, 'handle': handle2, 'text': 'Hi from Client 2!'})
    time.sleep(1)
    
    print("\n=== Summary ===")
    print(f"Client 1 events: {events1}")
    print(f"Client 2 events: {events2}")
    
finally:
    print("\nDisconnecting...")
    sio1.disconnect()
    sio2.disconnect()
