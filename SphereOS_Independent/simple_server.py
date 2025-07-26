#!/usr/bin/env python3
"""
Simple SphereOS Server with Social Media Interface
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3
import hashlib
import json
import secrets
from datetime import datetime
from typing import Optional, Dict, Any, List
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="SphereOS Social Media", version="1.0.0")

# Templates
templates = Jinja2Templates(directory="templates")

# Database initialization
def init_database():
    conn = sqlite3.connect('sphereos_social.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            npub TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            bio TEXT,
            location TEXT,
            avatar_url TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_token TEXT PRIMARY KEY,
            user_npub TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            expires_at TEXT,
            FOREIGN KEY (user_npub) REFERENCES users(npub)
        )
    ''')
    
    # Friends table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS friends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_npub TEXT NOT NULL,
            friend_npub TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_npub) REFERENCES users(npub),
            FOREIGN KEY (friend_npub) REFERENCES users(npub)
        )
    ''')
    
    # Posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_npub TEXT NOT NULL,
            content TEXT NOT NULL,
            post_type TEXT DEFAULT 'text',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_npub) REFERENCES users(npub)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database
init_database()

# Pydantic models
class LoginRequest(BaseModel):
    npub: str
    private_key: Optional[str] = None

class RegisterRequest(BaseModel):
    npub: str
    name: str
    bio: Optional[str] = None
    location: Optional[str] = None

class PostRequest(BaseModel):
    content: str
    post_type: str = "text"

class FriendRequest(BaseModel):
    friend_npub: str

# Authentication functions
def create_session(user_npub: str) -> str:
    session_token = secrets.token_urlsafe(32)
    expires_at = datetime.now().replace(hour=datetime.now().hour + 24).isoformat()
    
    conn = sqlite3.connect('sphereos_social.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sessions (session_token, user_npub, expires_at)
        VALUES (?, ?, ?)
    ''', (session_token, user_npub, expires_at))
    conn.commit()
    conn.close()
    
    return session_token

def get_user_from_session(session_token: str) -> Optional[str]:
    conn = sqlite3.connect('sphereos_social.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT user_npub FROM sessions 
        WHERE session_token = ? AND expires_at > ?
    ''', (session_token, datetime.now().isoformat()))
    
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else None

# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Main social media interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.post("/api/auth/login")
async def login_user(login_data: LoginRequest):
    """Login user and create session"""
    try:
        conn = sqlite3.connect('sphereos_social.db')
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE npub = ?", (login_data.npub,))
        user = cursor.fetchone()
        
        if user:
            # User exists, create session
            session_token = create_session(login_data.npub)
            return {
                "success": True,
                "session_token": session_token,
                "user": {
                    "npub": user[0],
                    "name": user[1],
                    "bio": user[2],
                    "location": user[3]
                }
            }
        else:
            return {"success": False, "error": "User not found"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/auth/register")
async def register_user(register_data: RegisterRequest):
    """Register new user"""
    try:
        conn = sqlite3.connect('sphereos_social.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (npub, name, bio, location)
            VALUES (?, ?, ?, ?)
        ''', (register_data.npub, register_data.name, register_data.bio, register_data.location))
        
        conn.commit()
        conn.close()
        
        # Create session for new user
        session_token = create_session(register_data.npub)
        
        return {
            "success": True,
            "session_token": session_token,
            "user": {
                "npub": register_data.npub,
                "name": register_data.name,
                "bio": register_data.bio,
                "location": register_data.location
            }
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/profile/{npub}")
async def get_profile(npub: str):
    """Get user profile"""
    try:
        conn = sqlite3.connect('sphereos_social.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE npub = ?", (npub,))
        user = cursor.fetchone()
        
        if user:
            return {
                "success": True,
                "profile": {
                    "npub": user[0],
                    "name": user[1],
                    "bio": user[2],
                    "location": user[3],
                    "avatar_url": user[4],
                    "created_at": user[5]
                }
            }
        else:
            return {"success": False, "error": "User not found"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/posts/create")
async def create_post(post_data: PostRequest, session_token: str):
    """Create a new post"""
    try:
        user_npub = get_user_from_session(session_token)
        if not user_npub:
            return {"success": False, "error": "Invalid session"}
        
        conn = sqlite3.connect('sphereos_social.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO posts (author_npub, content, post_type)
            VALUES (?, ?, ?)
        ''', (user_npub, post_data.content, post_data.post_type))
        
        conn.commit()
        conn.close()
        
        return {"success": True, "message": "Post created successfully"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/posts")
async def get_posts(limit: int = 20):
    """Get recent posts"""
    try:
        conn = sqlite3.connect('sphereos_social.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, u.name as author_name 
            FROM posts p 
            JOIN users u ON p.author_npub = u.npub 
            ORDER BY p.created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        posts = []
        for row in cursor.fetchall():
            posts.append({
                "id": row[0],
                "author_npub": row[1],
                "content": row[2],
                "post_type": row[3],
                "created_at": row[4],
                "author_name": row[5]
            })
        
        conn.close()
        return {"success": True, "posts": posts}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/friends/request")
async def send_friend_request(friend_data: FriendRequest, session_token: str):
    """Send friend request"""
    try:
        user_npub = get_user_from_session(session_token)
        if not user_npub:
            return {"success": False, "error": "Invalid session"}
        
        conn = sqlite3.connect('sphereos_social.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO friends (user_npub, friend_npub, status)
            VALUES (?, ?, 'pending')
        ''', (user_npub, friend_data.friend_npub))
        
        conn.commit()
        conn.close()
        
        return {"success": True, "message": "Friend request sent"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/friends")
async def get_friends(session_token: str):
    """Get user's friends"""
    try:
        user_npub = get_user_from_session(session_token)
        if not user_npub:
            return {"success": False, "error": "Invalid session"}
        
        conn = sqlite3.connect('sphereos_social.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT f.*, u.name as friend_name 
            FROM friends f 
            JOIN users u ON f.friend_npub = u.npub 
            WHERE f.user_npub = ? AND f.status = 'accepted'
        ''', (user_npub,))
        
        friends = []
        for row in cursor.fetchall():
            friends.append({
                "id": row[0],
                "friend_npub": row[2],
                "status": row[3],
                "created_at": row[4],
                "friend_name": row[5]
            })
        
        conn.close()
        return {"success": True, "friends": friends}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/search/users")
async def search_users(query: str, limit: int = 10):
    """Search for users"""
    try:
        conn = sqlite3.connect('sphereos_social.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM users 
            WHERE name LIKE ? OR bio LIKE ? 
            LIMIT ?
        ''', (f'%{query}%', f'%{query}%', limit))
        
        users = []
        for row in cursor.fetchall():
            users.append({
                "npub": row[0],
                "name": row[1],
                "bio": row[2],
                "location": row[3]
            })
        
        conn.close()
        return {"success": True, "users": users}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    print("🌐 Starting SphereOS Social Media Server...")
    print("📍 Server will be available at: http://localhost:8765")
    uvicorn.run(app, host="127.0.0.1", port=8765) 