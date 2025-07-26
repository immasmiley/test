#!/usr/bin/env python3
"""
U3CP Chat Message Client
Sends a chat message to a running U3CP core system instance.
"""

import os
import sys
import json
import time
import socket
import hashlib
import uuid

def send_message(message_text: str, host: str = '127.0.0.1', port: int = 8082):
    """Connects to the U3CP server and sends a single chat message."""
    
    print(f"[*] Attempting to connect to {host}:{port}...")
    
    try:
        # Create the message payload
        source_device_id = f"client_{uuid.uuid4().hex[:8]}"
        chat_payload = {
            'message': message_text,
            'timestamp': time.time(),
            'device_id': source_device_id
        }
        
        # Create the full AndroidMessage structure
        message_data = {
            'message_id': hashlib.sha256(f"chat_{time.time()}".encode()).hexdigest()[:16],
            'source_device': source_device_id,
            'destination_device': None, # Broadcasting to all listeners
            'message_type': "chat",
            'payload': json.dumps(chat_payload), # Payload is a JSON string
            'timestamp': time.time(),
            'priority': 1,
            'checksum': hashlib.sha256(message_text.encode()).hexdigest()[:8]
        }
        
        # The payload needs to be a JSON string, then encoded to bytes
        message_json_string = json.dumps(message_data)
        message_bytes = message_json_string.encode('utf-8')
        
        # Establish connection and send
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10) # 10 second timeout
            s.connect((host, port))
            s.sendall(message_bytes)
            print(f"[+] Message sent successfully!")
            print(f"    - To: {host}:{port}")
            print(f"    - Message: '{message_text}'")
            
    except ConnectionRefusedError:
        print(f"\n[ERROR] Connection refused. Is the core system running on the device?")
        print(f"        Ensure 'python launch_core_system.py' is active in another terminal.")
    except socket.timeout:
        print(f"\n[ERROR] Connection timed out. The U3CP server is not responding.")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Join all arguments after the script name to form the message
        message_to_send = " ".join(sys.argv[1:])
        send_message(message_to_send)
    else:
        print("Usage: python send_chat_message.py <Your message here>")
        print("Example: python send_chat_message.py \"Hello U3CP!\"") 