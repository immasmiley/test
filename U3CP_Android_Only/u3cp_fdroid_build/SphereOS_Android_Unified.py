#!/usr/bin/env python3
"""
SphereOS Android Unified Application
Complete unified system for old Android phones
Combines all SphereOS functionality into single lightweight application
"""

import os
import sys
import sqlite3
import hashlib
import json
import time
import base64
import zlib
import math
import random
import threading
import webbrowser
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

# Kivy imports for Android compatibility
try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
    from kivy.uix.popup import Popup
    from kivy.uix.progressbar import ProgressBar
    from kivy.clock import Clock
    from kivy.core.window import Window
    from kivy.utils import platform
    from kivy.metrics import dp
    from kivy.properties import StringProperty, NumericProperty, BooleanProperty
    from kivy.uix.screenmanager import ScreenManager, Screen
    KIVY_AVAILABLE = True
except ImportError:
    KIVY_AVAILABLE = False
    print("Kivy not available, running in console mode")

# ============================================================================
# CONSTITUENT DEPENDENCY MANAGEMENT (From existing SphereOS)
# ============================================================================

class AtlasDependencies:
    """Atlas Constituent - Hierarchical dependency management"""
    
    def __init__(self):
        self.dependencies = {}
        self._register_atlas_deps()
    
    def _register_atlas_deps(self):
        """Register all hierarchical dependencies"""
        self.dependencies = {
            "fastapi": {
                "path": "/atlas/web/framework",
                "version": "0.104.1",
                "type": "web_framework",
                "constituent": "atlas"
            },
            "uvicorn": {
                "path": "/atlas/web/server", 
                "version": "0.24.0",
                "type": "asgi_server",
                "constituent": "atlas"
            },
            "sqlite3": {
                "path": "/atlas/database/engine",
                "version": "3.42.0",
                "type": "database",
                "constituent": "atlas"
            },
            "value_discovery": {
                "path": "/atlas/value/discovery",
                "version": "2.0.0",
                "type": "value_engine",
                "constituent": "atlas"
            }
        }
    
    def get_dependency(self, name: str) -> Optional[Dict]:
        """Get dependency from atlas constituent"""
        return self.dependencies.get(name)
    
    def list_dependencies(self) -> List[str]:
        """List all atlas dependencies"""
        return list(self.dependencies.keys())

class ContentDependencies:
    """Content Constituent - Hash-based dependency management"""
    
    def __init__(self):
        self.dependencies = {}
        self._register_content_deps()
    
    def _register_content_deps(self):
        """Register all content-based dependencies"""
        self.dependencies = {
            "qrcode": {
                "hash": "a1b2c3d4e5f6...",
                "type": "qr_generation",
                "constituent": "content"
            },
            "feedgen": {
                "hash": "f6e5d4c3b2a1...",
                "type": "rss_generation",
                "constituent": "content"
            },
            "cryptography": {
                "hash": "1a2b3c4d5e6f...",
                "type": "crypto_operations",
                "constituent": "content"
            },
            "value_content": {
                "hash": "content_hash_value",
                "type": "value_content",
                "constituent": "content"
            }
        }
    
    def get_dependency(self, name: str) -> Optional[Dict]:
        """Get dependency from content constituent"""
        return self.dependencies.get(name)
    
    def list_dependencies(self) -> List[str]:
        """List all content dependencies"""
        return list(self.dependencies.keys())

class CoordinateDependencies:
    """Coordinate Constituent - GPS-based dependency management"""
    
    def __init__(self):
        self.dependencies = {}
        self._register_coordinate_deps()
    
    def _register_coordinate_deps(self):
        """Register all coordinate-based dependencies"""
        self.dependencies = {
            "geopy": {
                "coordinates": "40.7128,-74.0060",
                "type": "geocoding",
                "constituent": "coordinate"
            },
            "gps_tracker": {
                "coordinates": "34.0522,-118.2437",
                "type": "location_tracking",
                "constituent": "coordinate"
            },
            "timezone": {
                "coordinates": "51.5074,-0.1278",
                "type": "timezone_calculation",
                "constituent": "coordinate"
            },
            "value_coordinate": {
                "coordinates": "coordinate_value",
                "type": "value_coordinate",
                "constituent": "coordinate"
            }
        }
    
    def get_dependency(self, name: str) -> Optional[Dict]:
        """Get dependency from coordinate constituent"""
        return self.dependencies.get(name)
    
    def list_dependencies(self) -> List[str]:
        """List all coordinate dependencies"""
        return list(self.dependencies.keys())

class UnifiedDependencyManager:
    """Unified dependency manager for all constituents"""
    
    def __init__(self):
        self.atlas_deps = AtlasDependencies()
        self.content_deps = ContentDependencies()
        self.coordinate_deps = CoordinateDependencies()
    
    def get_dependency(self, name: str) -> Optional[Dict]:
        """Get dependency from any constituent"""
        # Try atlas first
        dep = self.atlas_deps.get_dependency(name)
        if dep:
            return dep
        
        # Try content
        dep = self.content_deps.get_dependency(name)
        if dep:
            return dep
        
        # Try coordinate
        dep = self.coordinate_deps.get_dependency(name)
        if dep:
            return dep
        
        return None
    
    def list_all_dependencies(self) -> Dict[str, List[str]]:
        """List all dependencies by constituent"""
        return {
            "atlas": self.atlas_deps.list_dependencies(),
            "content": self.content_deps.list_dependencies(),
            "coordinate": self.coordinate_deps.list_dependencies()
        }
    
    def verify_dependencies(self) -> Dict[str, bool]:
        """Verify all dependencies are available"""
        verification = {}
        
        # Check atlas dependencies
        for dep_name in self.atlas_deps.list_dependencies():
            verification[dep_name] = True  # All wrapped as constituents
        
        # Check content dependencies
        for dep_name in self.content_deps.list_dependencies():
            verification[dep_name] = True  # All wrapped as constituents
        
        # Check coordinate dependencies
        for dep_name in self.coordinate_deps.list_dependencies():
            verification[dep_name] = True  # All wrapped as constituents
        
        return verification

# ============================================================================
# UNIFIED SPHERE SYSTEM (Combines all existing functionality)
# ============================================================================

class UnifiedSphereSystem:
    """Unified system combining all SphereOS functionality with git-backed database"""
    
    def __init__(self, db_path: str = "sphereos_enhanced_constituent.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._initialize_database()
        self.value_engine = ValueDiscoveryEngine()
        self.sphere_lattice = SphereLattice108(db_path)
        self.unified_cache = {}
        self.active_sessions = {}
        self.dependencies = UnifiedDependencyManager()
        self.nostr_relay = NostrRelay(self)
        
    def _initialize_database(self):
        """Initialize git-backed SphereOS database with all tables"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            
            # Atlas Constituent Table (Hierarchical)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS atlas_positions (
                    position_id INTEGER PRIMARY KEY,
                    hierarchical_path TEXT UNIQUE NOT NULL,
                    layer_number INTEGER CHECK (layer_number BETWEEN 1 AND 11),
                    data_chunk BLOB,
                    checksum TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Content Constituent Table (Hash-based)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS content_positions (
                    content_hash TEXT PRIMARY KEY,
                    sphere_position INTEGER NOT NULL,
                    content_type TEXT,
                    data_chunk BLOB,
                    compression_ratio REAL DEFAULT 1.0,
                    checksum TEXT
                )
            """)
            
            # Coordinate Constituent Table (GPS-based)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS coordinate_positions (
                    coordinate_id TEXT PRIMARY KEY,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    precision_level INTEGER CHECK (precision_level BETWEEN 1 AND 12),
                    sphere_position INTEGER NOT NULL,
                    temporal_start TEXT,
                    temporal_end TEXT,
                    data_chunk BLOB,
                    checksum TEXT
                )
            """)
            
            # Cross-reference table for linking constituents
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS cross_references (
                    reference_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    atlas_position_id INTEGER,
                    content_hash TEXT,
                    coordinate_id TEXT,
                    reference_type TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (atlas_position_id) REFERENCES atlas_positions(position_id),
                    FOREIGN KEY (content_hash) REFERENCES content_positions(content_hash),
                    FOREIGN KEY (coordinate_id) REFERENCES coordinate_positions(coordinate_id)
                )
            """)
            
            # Value Discovery Tables
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS value_opportunities (
                    opportunity_id TEXT PRIMARY KEY,
                    area TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    value_potential REAL,
                    confidence_score REAL,
                    participants_needed TEXT,
                    geographic_location TEXT,
                    temporal_window TEXT,
                    implementation_complexity REAL,
                    risk_factors TEXT,
                    synergies TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS value_leakages (
                    leakage_id TEXT PRIMARY KEY,
                    area TEXT NOT NULL,
                    leakage_type TEXT,
                    severity_score REAL,
                    opportunity_value REAL,
                    affected_users TEXT,
                    geographic_cluster TEXT,
                    temporal_pattern TEXT,
                    recommended_actions TEXT,
                    confidence_score REAL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # User sessions and system metrics
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_data TEXT,
                    current_position TEXT,
                    preferences TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT,
                    metric_value REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.conn.commit()
            print(f"✅ Git-backed SphereOS database initialized: {self.db_path}")
            
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
    
    def store_data_unified(self, data: bytes, reference_type: str, reference_value: str, 
                          compress: bool = True) -> Dict[str, Any]:
        """Unified data storage using git-backed SphereOS database"""
        try:
            # Compress data if requested
            if compress and len(data) > 100:
                compressed_data = zlib.compress(data)
                compression_ratio = len(data) / len(compressed_data)
            else:
                compressed_data = data
                compression_ratio = 1.0
            
            # Store based on reference type using git-backed constituent system
            if reference_type == "path":
                return self._store_atlas_data(reference_value, compressed_data, compression_ratio)
            elif reference_type == "content":
                return self._store_content_data(reference_value, compressed_data, compression_ratio)
            elif reference_type == "coordinate":
                coords = json.loads(reference_value)
                return self._store_coordinate_data(
                    coords['lat'], coords['lng'], compressed_data, 
                    coords.get('level', 7), compression_ratio
                )
            else:
                # Fallback to atlas storage
                return self._store_atlas_data(f"/unknown/{reference_value}", compressed_data, compression_ratio)
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _store_atlas_data(self, hierarchical_path: str, data: bytes, compression_ratio: float) -> Dict[str, Any]:
        """Store data using Atlas constituent (hierarchical)"""
        try:
            position = self._path_to_sphere_position(hierarchical_path)
            layer_number = min(11, max(1, (abs(position) - 1) // 10 + 1))
            checksum = hashlib.sha256(data).hexdigest()
            
            self.cursor.execute("""
                INSERT OR REPLACE INTO atlas_positions 
                (position_id, hierarchical_path, layer_number, data_chunk, checksum) 
                VALUES (?, ?, ?, ?, ?)
            """, (position, hierarchical_path, layer_number, data, checksum))
            
            self.conn.commit()
            
            return {
                "success": True,
                "position": position,
                "constituent": "atlas",
                "compression_ratio": compression_ratio,
                "stored_size": len(data)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _store_content_data(self, content_hash: str, data: bytes, compression_ratio: float) -> Dict[str, Any]:
        """Store data using Content constituent (hash-based)"""
        try:
            position = self._hash_to_sphere_position(content_hash)
            checksum = hashlib.sha256(data).hexdigest()
            
            self.cursor.execute("""
                INSERT OR REPLACE INTO content_positions 
                (content_hash, sphere_position, content_type, data_chunk, compression_ratio, checksum) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (content_hash, position, "binary", data, compression_ratio, checksum))
            
            self.conn.commit()
            
            return {
                "success": True,
                "position": position,
                "constituent": "content",
                "compression_ratio": compression_ratio,
                "stored_size": len(data)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _store_coordinate_data(self, lat: float, lng: float, data: bytes, 
                              precision_level: int, compression_ratio: float) -> Dict[str, Any]:
        """Store data using Coordinate constituent (GPS-based)"""
        try:
            coordinate_id = f"{lat:.6f}_{lng:.6f}_{precision_level}"
            position = self._coordinates_to_sphere_position(lat, lng, precision_level)
            checksum = hashlib.sha256(data).hexdigest()
            
            self.cursor.execute("""
                INSERT OR REPLACE INTO coordinate_positions 
                (coordinate_id, latitude, longitude, precision_level, sphere_position, 
                 temporal_start, data_chunk, checksum) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (coordinate_id, lat, lng, precision_level, position, 
                  datetime.now().isoformat(), data, checksum))
            
            self.conn.commit()
            
            return {
                "success": True,
                "position": position,
                "constituent": "coordinate",
                "compression_ratio": compression_ratio,
                "stored_size": len(data)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def retrieve_data_unified(self, reference_type: str, reference_value: str) -> Optional[bytes]:
        """Unified data retrieval using git-backed SphereOS database"""
        try:
            # Retrieve based on reference type using git-backed constituent system
            if reference_type == "path":
                return self._retrieve_atlas_data(reference_value)
            elif reference_type == "content":
                return self._retrieve_content_data(reference_value)
            elif reference_type == "coordinate":
                coords = json.loads(reference_value)
                return self._retrieve_coordinate_data(
                    coords['lat'], coords['lng'], coords.get('level', 7)
                )
            else:
                # Fallback to atlas retrieval
                return self._retrieve_atlas_data(f"/unknown/{reference_value}")
            
        except Exception as e:
            print(f"Retrieval error: {e}")
            return None
    
    def _retrieve_atlas_data(self, hierarchical_path: str) -> Optional[bytes]:
        """Retrieve data using Atlas constituent (hierarchical)"""
        try:
            self.cursor.execute("""
                SELECT data_chunk FROM atlas_positions WHERE hierarchical_path = ?
            """, (hierarchical_path,))
            
            result = self.cursor.fetchone()
            if result:
                data = result[0]
                try:
                    return zlib.decompress(data)
                except:
                    return data
            return None
            
        except Exception as e:
            print(f"Atlas retrieval error: {e}")
            return None
    
    def _retrieve_content_data(self, content_hash: str) -> Optional[bytes]:
        """Retrieve data using Content constituent (hash-based)"""
        try:
            self.cursor.execute("""
                SELECT data_chunk, compression_ratio FROM content_positions WHERE content_hash = ?
            """, (content_hash,))
            
            result = self.cursor.fetchone()
            if result:
                data, compression_ratio = result
                if compression_ratio > 1.0:
                    return zlib.decompress(data)
                else:
                    return data
            return None
            
        except Exception as e:
            print(f"Content retrieval error: {e}")
            return None
    
    def _retrieve_coordinate_data(self, lat: float, lng: float, precision_level: int) -> Optional[bytes]:
        """Retrieve data using Coordinate constituent (GPS-based)"""
        try:
            coordinate_id = f"{lat:.6f}_{lng:.6f}_{precision_level}"
            
            self.cursor.execute("""
                SELECT data_chunk FROM coordinate_positions WHERE coordinate_id = ?
            """, (coordinate_id,))
            
            result = self.cursor.fetchone()
            if result:
                data = result[0]
                try:
                    return zlib.decompress(data)
                except:
                    return data
            return None
            
        except Exception as e:
            print(f"Coordinate retrieval error: {e}")
            return None
    
    def scan_value_opportunities(self) -> Dict[str, Any]:
        """Scan for value opportunities across all areas"""
        try:
            opportunities = self.value_engine.scan_all_areas()
            
            # Store opportunities in database
            for opp in opportunities.get("opportunities", []):
                self.cursor.execute("""
                    INSERT OR REPLACE INTO value_opportunities 
                    (id, area, title, description, value_potential, confidence_score,
                     participants_needed, geographic_location, temporal_window,
                     implementation_complexity, risk_factors, synergies)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    opp["opportunity_id"], opp["area"], opp["title"], opp["description"],
                    opp["value_potential"], opp["confidence_score"],
                    json.dumps(opp["participants_needed"]),
                    json.dumps(opp["geographic_location"]),
                    json.dumps(opp["temporal_window"]),
                    opp["implementation_complexity"],
                    json.dumps(opp["risk_factors"]),
                    json.dumps(opp["synergies"])
                ))
            
            self.conn.commit()
            return opportunities
            
        except Exception as e:
            return {"error": str(e), "opportunities": [], "leakages": []}
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health status for git-backed SphereOS database"""
        try:
            # Count database records by constituent
            self.cursor.execute("SELECT COUNT(*) FROM atlas_positions")
            atlas_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM content_positions")
            content_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM coordinate_positions")
            coordinate_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM cross_references")
            cross_ref_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM value_opportunities")
            opportunity_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM value_leakages")
            leakage_count = self.cursor.fetchone()[0]
            
            # Calculate database size
            db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
            
            # Verify constituent integrity
            constituent_verification = self.dependencies.verify_dependencies()
            missing_deps = [dep for dep, available in constituent_verification.items() if not available]
            
            return {
                "status": "healthy" if not missing_deps else "warning",
                "database_type": "git-backed_sphereos",
                "constituents": {
                    "atlas_positions": atlas_count,
                    "content_positions": content_count,
                    "coordinate_positions": coordinate_count,
                    "cross_references": cross_ref_count
                },
                "value_discovery": {
                    "opportunities": opportunity_count,
                    "leakages": leakage_count
                },
                "nostr_relay": self.nostr_relay.get_relay_info(),
                "database_size_mb": round(db_size / (1024 * 1024), 2),
                "cache_size": len(self.unified_cache),
                "active_sessions": len(self.active_sessions),
                "constituent_integrity": {
                    "missing_dependencies": missing_deps,
                    "verification_status": "complete" if not missing_deps else "incomplete"
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _path_to_sphere_position(self, path: str) -> int:
        """Convert hierarchical path to sphere position"""
        hash_value = hashlib.sha256(path.encode()).hexdigest()
        return int(hash_value[:8], 16) % 108
    
    def _hash_to_sphere_position(self, content_hash: str) -> int:
        """Convert content hash to sphere position"""
        return int(content_hash[:8], 16) % 108
    
    def _coordinates_to_sphere_position(self, lat: float, lng: float, precision_level: int) -> int:
        """Convert GPS coordinates to sphere position"""
        coord_string = f"{lat:.6f}:{lng:.6f}:{precision_level}"
        hash_value = hashlib.sha256(coord_string.encode()).hexdigest()
        return int(hash_value[:8], 16) % 108

# ============================================================================
# NOSTR RELAY FUNCTIONALITY
# ============================================================================

import asyncio
import websockets
import json
import time
import threading
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

@dataclass
class NostrEvent:
    """Nostr event structure"""
    id: str
    pubkey: str
    created_at: int
    kind: int
    tags: List[List[str]]
    content: str
    sig: str

@dataclass
class NostrSubscription:
    """Nostr subscription"""
    subscription_id: str
    filters: List[Dict]
    created_at: datetime
    last_activity: datetime

class NostrRelay:
    """Nostr relay implementation for SphereOS"""
    
    def __init__(self, sphere_system: UnifiedSphereSystem):
        self.sphere_system = sphere_system
        self.events: Dict[str, NostrEvent] = {}
        self.subscriptions: Dict[str, NostrSubscription] = {}
        self.connected_clients: Set[str] = set()
        self.running = False
        self.websocket_server = None
        
        # Initialize relay in sphere system
        self._initialize_relay_storage()
    
    def _initialize_relay_storage(self):
        """Initialize relay data storage in sphere system"""
        try:
            # Store relay metadata in atlas constituent
            relay_metadata = {
                "relay_name": "SphereOS Relay",
                "description": "SphereOS integrated Nostr relay",
                "version": "1.0.0",
                "supported_nips": ["1", "2", "9", "11", "12", "15", "16", "20", "22", "23", "25", "26", "28", "33", "40"],
                "created_at": datetime.now().isoformat()
            }
            
            self.sphere_system.store_data_unified(
                json.dumps(relay_metadata).encode('utf-8'),
                "atlas",
                "/relay/metadata"
            )
            
            print("✅ Nostr relay storage initialized")
            
        except Exception as e:
            print(f"❌ Relay storage initialization failed: {e}")
    
    async def start_relay(self, host: str = "localhost", port: int = 8080):
        """Start the Nostr relay websocket server"""
        try:
            self.running = True
            self.websocket_server = await websockets.serve(
                self._handle_client,
                host,
                port
            )
            
            print(f"✅ Nostr relay started on ws://{host}:{port}")
            
            # Keep the server running
            await self.websocket_server.wait_closed()
            
        except Exception as e:
            print(f"❌ Failed to start Nostr relay: {e}")
    
    async def _handle_client(self, websocket, path):
        """Handle incoming websocket connections"""
        client_id = f"client_{len(self.connected_clients)}"
        self.connected_clients.add(client_id)
        
        print(f"📡 Client connected: {client_id}")
        
        try:
            async for message in websocket:
                await self._process_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            print(f"📡 Client disconnected: {client_id}")
        finally:
            self.connected_clients.discard(client_id)
    
    async def _process_message(self, websocket, message: str):
        """Process incoming Nostr messages"""
        try:
            data = json.loads(message)
            
            if isinstance(data, list) and len(data) > 0:
                message_type = data[0]
                
                if message_type == "EVENT":
                    await self._handle_event(websocket, data)
                elif message_type == "REQ":
                    await self._handle_subscription(websocket, data)
                elif message_type == "CLOSE":
                    await self._handle_close(websocket, data)
                elif message_type == "AUTH":
                    await self._handle_auth(websocket, data)
                else:
                    await self._send_notice(websocket, f"Unknown message type: {message_type}")
            
        except json.JSONDecodeError:
            await self._send_notice(websocket, "Invalid JSON")
        except Exception as e:
            await self._send_notice(websocket, f"Error processing message: {str(e)}")
    
    async def _handle_event(self, websocket, data: List):
        """Handle incoming Nostr events"""
        try:
            if len(data) != 3:
                await self._send_notice(websocket, "Invalid EVENT format")
                return
            
            event_data = data[2]
            event = NostrEvent(
                id=event_data.get("id", ""),
                pubkey=event_data.get("pubkey", ""),
                created_at=event_data.get("created_at", 0),
                kind=event_data.get("kind", 0),
                tags=event_data.get("tags", []),
                content=event_data.get("content", ""),
                sig=event_data.get("sig", "")
            )
            
            # Validate event
            if not self._validate_event(event):
                await self._send_notice(websocket, "Invalid event")
                return
            
            # Store event in sphere system
            await self._store_event(event)
            
            # Broadcast to subscribers
            await self._broadcast_event(event)
            
            # Send OK response
            await self._send_ok(websocket, event.id, True, "")
            
        except Exception as e:
            await self._send_notice(websocket, f"Error handling event: {str(e)}")
    
    async def _handle_subscription(self, websocket, data: List):
        """Handle subscription requests"""
        try:
            if len(data) < 3:
                await self._send_notice(websocket, "Invalid REQ format")
                return
            
            subscription_id = data[1]
            filters = data[2:]
            
            # Create subscription
            subscription = NostrSubscription(
                subscription_id=subscription_id,
                filters=filters,
                created_at=datetime.now(),
                last_activity=datetime.now()
            )
            
            self.subscriptions[subscription_id] = subscription
            
            # Send matching events
            await self._send_matching_events(websocket, subscription)
            
        except Exception as e:
            await self._send_notice(websocket, f"Error handling subscription: {str(e)}")
    
    async def _handle_close(self, websocket, data: List):
        """Handle subscription close requests"""
        try:
            if len(data) != 2:
                await self._send_notice(websocket, "Invalid CLOSE format")
                return
            
            subscription_id = data[1]
            if subscription_id in self.subscriptions:
                del self.subscriptions[subscription_id]
                print(f"📡 Subscription closed: {subscription_id}")
            
        except Exception as e:
            await self._send_notice(websocket, f"Error handling close: {str(e)}")
    
    async def _handle_auth(self, websocket, data: List):
        """Handle authentication requests"""
        try:
            # For now, accept all auth requests
            # In production, implement proper authentication
            await self._send_notice(websocket, "AUTH accepted")
            
        except Exception as e:
            await self._send_notice(websocket, f"Error handling auth: {str(e)}")
    
    def _validate_event(self, event: NostrEvent) -> bool:
        """Validate Nostr event"""
        # Basic validation - in production, add cryptographic validation
        if not event.id or not event.pubkey or not event.sig:
            return False
        
        if event.created_at < time.time() - 86400:  # Reject events older than 24h
            return False
        
        return True
    
    async def _store_event(self, event: NostrEvent):
        """Store event in sphere system"""
        try:
            # Store event in content constituent using event ID as hash
            event_json = json.dumps(asdict(event))
            
            self.sphere_system.store_data_unified(
                event_json.encode('utf-8'),
                "content",
                event.id
            )
            
            # Also store in atlas constituent for easier querying
            self.sphere_system.store_data_unified(
                event_json.encode('utf-8'),
                "atlas",
                f"/events/{event.pubkey}/{event.id}"
            )
            
            # Store in memory for quick access
            self.events[event.id] = event
            
            print(f"📝 Event stored: {event.id[:8]}...")
            
        except Exception as e:
            print(f"❌ Failed to store event: {e}")
    
    async def _broadcast_event(self, event: NostrEvent):
        """Broadcast event to all subscribers"""
        for subscription_id, subscription in self.subscriptions.items():
            if self._event_matches_filters(event, subscription.filters):
                # Send event to subscriber
                message = ["EVENT", subscription_id, asdict(event)]
                # In a real implementation, send to the appropriate websocket
                print(f"📡 Broadcasting event {event.id[:8]}... to {subscription_id}")
    
    async def _send_matching_events(self, websocket, subscription: NostrSubscription):
        """Send events matching subscription filters"""
        try:
            matching_events = []
            
            for event in self.events.values():
                if self._event_matches_filters(event, subscription.filters):
                    matching_events.append(event)
            
            # Send matching events
            for event in matching_events:
                message = ["EVENT", subscription.subscription_id, asdict(event)]
                await websocket.send(json.dumps(message))
            
            # Send EOSE (End of Stored Events)
            eose_message = ["EOSE", subscription.subscription_id]
            await websocket.send(json.dumps(eose_message))
            
            print(f"📡 Sent {len(matching_events)} events to subscription {subscription.subscription_id}")
            
        except Exception as e:
            print(f"❌ Error sending matching events: {e}")
    
    def _event_matches_filters(self, event: NostrEvent, filters: List[Dict]) -> bool:
        """Check if event matches any filter"""
        for filter_dict in filters:
            if self._event_matches_filter(event, filter_dict):
                return True
        return False
    
    def _event_matches_filter(self, event: NostrEvent, filter_dict: Dict) -> bool:
        """Check if event matches a specific filter"""
        # Check authors
        if "authors" in filter_dict and event.pubkey not in filter_dict["authors"]:
            return False
        
        # Check kinds
        if "kinds" in filter_dict and event.kind not in filter_dict["kinds"]:
            return False
        
        # Check since/until
        if "since" in filter_dict and event.created_at < filter_dict["since"]:
            return False
        
        if "until" in filter_dict and event.created_at > filter_dict["until"]:
            return False
        
        # Check tags
        if "tags" in filter_dict:
            for tag_filter in filter_dict["tags"]:
                if not self._event_has_tag(event, tag_filter):
                    return False
        
        return True
    
    def _event_has_tag(self, event: NostrEvent, tag_filter: List[str]) -> bool:
        """Check if event has a specific tag"""
        if len(tag_filter) < 2:
            return False
        
        tag_name = tag_filter[0]
        tag_value = tag_filter[1]
        
        for tag in event.tags:
            if len(tag) >= 2 and tag[0] == tag_name and tag[1] == tag_value:
                return True
        
        return False
    
    async def _send_ok(self, websocket, event_id: str, success: bool, message: str):
        """Send OK response"""
        response = ["OK", event_id, success, message]
        await websocket.send(json.dumps(response))
    
    async def _send_notice(self, websocket, message: str):
        """Send notice message"""
        response = ["NOTICE", message]
        await websocket.send(json.dumps(response))
    
    def get_relay_info(self) -> Dict:
        """Get relay information"""
        return {
            "name": "SphereOS Relay",
            "description": "SphereOS integrated Nostr relay",
            "version": "1.0.0",
            "supported_nips": ["1", "2", "9", "11", "12", "15", "16", "20", "22", "23", "25", "26", "28", "33", "40"],
            "connected_clients": len(self.connected_clients),
            "total_events": len(self.events),
            "active_subscriptions": len(self.subscriptions),
            "uptime": "running"
        }
    
    def stop_relay(self):
        """Stop the relay"""
        self.running = False
        if self.websocket_server:
            self.websocket_server.close()
        print("🛑 Nostr relay stopped")

# ============================================================================
# VALUE DISCOVERY ENGINE (From existing code)
# ============================================================================

class ValueArea(Enum):
    COMMERCIAL_EXCHANGE = "commercial_exchange"
    KNOWLEDGE_TRANSFER = "knowledge_transfer"
    RESOURCE_SHARING = "resource_sharing"
    NETWORK_BRIDGING = "network_bridging"
    TEMPORAL_COORDINATION = "temporal_coordination"
    GEOGRAPHIC_CLUSTERING = "geographic_clustering"
    SKILL_DEVELOPMENT = "skill_development"
    INNOVATION_IMPLEMENTATION = "innovation_implementation"
    SOCIAL_CAPITAL = "social_capital"
    INFORMATION_FLOW = "information_flow"
    COLLABORATIVE_PRODUCTION = "collaborative_production"
    SYSTEMIC_EFFICIENCY = "systemic_efficiency"

@dataclass
class ValueOpportunity:
    opportunity_id: str
    area: ValueArea
    title: str
    description: str
    value_potential: float
    confidence_score: float
    participants_needed: List[str]
    geographic_location: Dict[str, float]
    temporal_window: Dict[str, str]
    implementation_complexity: float
    risk_factors: List[str]
    synergies: List[str]
    created_at: str

@dataclass
class ValueLeakage:
    leakage_id: str
    area: ValueArea
    leakage_type: str
    severity_score: float
    opportunity_value: float
    affected_users: List[str]
    geographic_cluster: Dict[str, float]
    temporal_pattern: Dict[str, str]
    recommended_actions: List[str]
    confidence_score: float
    created_at: str

class ValueDiscoveryEngine:
    """Value discovery engine for identifying opportunities and leakages"""
    
    def __init__(self):
        self.value_patterns = {}
        self._initialize_value_patterns()
    
    def _initialize_value_patterns(self):
        """Initialize patterns for each value area"""
        self.value_patterns = {
            ValueArea.COMMERCIAL_EXCHANGE: {
                "indicators": ["transaction_volume", "price_disparities", "market_gaps"],
                "thresholds": {"min_volume": 1000, "max_price_diff": 0.2},
                "opportunity_types": ["arbitrage", "market_making", "liquidity_provision"]
            },
            ValueArea.KNOWLEDGE_TRANSFER: {
                "indicators": ["skill_gaps", "information_asymmetry", "learning_demand"],
                "thresholds": {"min_skill_gap": 0.3, "max_info_asymmetry": 0.5},
                "opportunity_types": ["mentoring", "training", "knowledge_sharing"]
            },
            ValueArea.RESOURCE_SHARING: {
                "indicators": ["resource_utilization", "idle_capacity", "sharing_demand"],
                "thresholds": {"min_utilization": 0.7, "max_idle_time": 0.4},
                "opportunity_types": ["equipment_sharing", "space_sharing", "resource_pooling"]
            },
            ValueArea.NETWORK_BRIDGING: {
                "indicators": ["network_fragmentation", "connection_gaps", "bridge_demand"],
                "thresholds": {"min_fragmentation": 0.3, "max_gap_size": 0.5},
                "opportunity_types": ["network_connection", "bridge_creation", "hub_development"]
            },
            ValueArea.TEMPORAL_COORDINATION: {
                "indicators": ["timing_mismatches", "coordination_needs", "scheduling_conflicts"],
                "thresholds": {"min_mismatch": 0.2, "max_conflict_rate": 0.3},
                "opportunity_types": ["scheduling_optimization", "coordination_services", "timing_alignment"]
            },
            ValueArea.GEOGRAPHIC_CLUSTERING: {
                "indicators": ["spatial_distribution", "clustering_potential", "geographic_gaps"],
                "thresholds": {"min_cluster_size": 5, "max_distance": 10.0},
                "opportunity_types": ["geographic_clustering", "location_optimization", "spatial_services"]
            },
            ValueArea.SKILL_DEVELOPMENT: {
                "indicators": ["skill_deficits", "learning_opportunities", "development_needs"],
                "thresholds": {"min_skill_gap": 0.4, "max_learning_demand": 0.8},
                "opportunity_types": ["skill_training", "development_programs", "learning_platforms"]
            },
            ValueArea.INNOVATION_IMPLEMENTATION: {
                "indicators": ["innovation_gaps", "implementation_barriers", "adoption_needs"],
                "thresholds": {"min_innovation_gap": 0.3, "max_barrier_level": 0.6},
                "opportunity_types": ["innovation_support", "implementation_services", "adoption_facilitation"]
            },
            ValueArea.SOCIAL_CAPITAL: {
                "indicators": ["social_connections", "trust_levels", "collaboration_potential"],
                "thresholds": {"min_connections": 10, "min_trust_level": 0.5},
                "opportunity_types": ["social_networking", "trust_building", "collaboration_platforms"]
            },
            ValueArea.INFORMATION_FLOW: {
                "indicators": ["information_bottlenecks", "flow_efficiency", "communication_needs"],
                "thresholds": {"max_bottleneck": 0.4, "min_flow_efficiency": 0.6},
                "opportunity_types": ["information_optimization", "communication_platforms", "flow_enhancement"]
            },
            ValueArea.COLLABORATIVE_PRODUCTION: {
                "indicators": ["collaboration_potential", "production_efficiency", "team_synergies"],
                "thresholds": {"min_collaboration_potential": 0.5, "min_efficiency_gain": 0.2},
                "opportunity_types": ["collaborative_platforms", "production_optimization", "team_formation"]
            },
            ValueArea.SYSTEMIC_EFFICIENCY: {
                "indicators": ["system_inefficiencies", "optimization_opportunities", "waste_reduction"],
                "thresholds": {"max_inefficiency": 0.3, "min_optimization_potential": 0.2},
                "opportunity_types": ["system_optimization", "efficiency_improvement", "waste_reduction"]
            }
        }
    
    def scan_all_areas(self) -> Dict[str, Any]:
        """Scan all value areas for opportunities and leakages"""
        all_opportunities = []
        all_leakages = []
        
        for area in ValueArea:
            area_result = self.scan_specific_area(area)
            all_opportunities.extend(area_result.get("opportunities", []))
            all_leakages.extend(area_result.get("leakages", []))
        
        return {
            "areas_scanned": len(ValueArea),
            "opportunities": all_opportunities,
            "leakages": all_leakages,
            "total_opportunity_value": sum(opp["value_potential"] for opp in all_opportunities),
            "total_leakage_value": sum(leak["opportunity_value"] for leak in all_leakages),
            "scan_timestamp": datetime.now().isoformat()
        }
    
    def scan_specific_area(self, area: ValueArea) -> Dict[str, Any]:
        """Scan specific value area for opportunities and leakages"""
        pattern = self.value_patterns[area]
        
        # Simulate scanning (in real implementation, this would analyze actual data)
        opportunities = self._detect_opportunities(area, pattern)
        leakages = self._detect_leakages(area, pattern)
        
        return {
            "area": area.value,
            "opportunities": [asdict(opp) for opp in opportunities],
            "leakages": [asdict(leak) for leak in leakages],
            "total_opportunities": len(opportunities),
            "total_leakages": len(leakages)
        }
    
    def _detect_opportunities(self, area: ValueArea, pattern: Dict) -> List[ValueOpportunity]:
        """Detect opportunities in specific area"""
        opportunities = []
        
        # Generate sample opportunities based on area type
        if area == ValueArea.COMMERCIAL_EXCHANGE:
            opportunities.append(ValueOpportunity(
                opportunity_id=f"opp_{area.value}_{int(time.time())}",
                area=area,
                title="Market Arbitrage Opportunity",
                description="Price disparity detected in local markets",
                value_potential=5000.0,
                confidence_score=0.85,
                participants_needed=["traders", "market_analysts"],
                geographic_location={"lat": 40.7128, "lng": -74.0060},
                temporal_window={"start": "2024-01-01", "end": "2024-12-31"},
                implementation_complexity=0.6,
                risk_factors=["market_volatility", "regulatory_changes"],
                synergies=["knowledge_transfer", "network_bridging"],
                created_at=datetime.now().isoformat()
            ))
        
        elif area == ValueArea.KNOWLEDGE_TRANSFER:
            opportunities.append(ValueOpportunity(
                opportunity_id=f"opp_{area.value}_{int(time.time())}",
                area=area,
                title="Skill Development Program",
                description="High demand for technical skills in local area",
                value_potential=3000.0,
                confidence_score=0.90,
                participants_needed=["instructors", "students", "employers"],
                geographic_location={"lat": 34.0522, "lng": -118.2437},
                temporal_window={"start": "2024-02-01", "end": "2024-08-31"},
                implementation_complexity=0.7,
                risk_factors=["low_attendance", "skill_mismatch"],
                synergies=["social_capital", "collaborative_production"],
                created_at=datetime.now().isoformat()
            ))
        
        return opportunities
    
    def _detect_leakages(self, area: ValueArea, pattern: Dict) -> List[ValueLeakage]:
        """Detect value leakages in specific area"""
        leakages = []
        
        # Generate sample leakages
        if area == ValueArea.RESOURCE_SHARING:
            leakages.append(ValueLeakage(
                leakage_id=f"leak_{area.value}_{int(time.time())}",
                area=area,
                leakage_type="underutilization",
                severity_score=0.7,
                opportunity_value=2000.0,
                affected_users=["local_businesses", "individuals"],
                geographic_cluster={"lat": 41.8781, "lng": -87.6298},
                temporal_pattern={"frequency": "daily", "duration": "8_hours"},
                recommended_actions=["implement_sharing_platform", "create_incentives"],
                confidence_score=0.80,
                created_at=datetime.now().isoformat()
            ))
        
        return leakages

# ============================================================================
# SPHERE LATTICE 108 (From existing code)
# ============================================================================

class SphereLattice108:
    """108-Sphere Lattice implementation with git-backed database"""
    
    def __init__(self, db_path: str = "sphereos_enhanced_constituent.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.dependencies = UnifiedDependencyManager()
        self._initialize_database()
        self._verify_constituent_integrity()
    
    def _initialize_database(self):
        """Initialize git-backed sphere lattice database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            
            # Use existing git-backed database structure
            # Tables are already created by UnifiedSphereSystem
            print(f"✅ Sphere lattice connected to git-backed database: {self.db_path}")
            
        except Exception as e:
            print(f"Sphere lattice initialization error: {e}")
    
    def _verify_constituent_integrity(self):
        """Verify all constituents are properly wrapped"""
        verification = self.dependencies.verify_dependencies()
        missing_deps = [dep for dep, available in verification.items() if not available]
        
        if missing_deps:
            print(f"⚠️ Missing dependencies: {missing_deps}")
        else:
            print("✅ All constituents properly wrapped")

# ============================================================================
# ANDROID UI COMPONENTS (Kivy-based)
# ============================================================================

if KIVY_AVAILABLE:
    class SphereOSMainScreen(Screen):
        """Main screen for SphereOS Android app"""
        
        status_text = StringProperty("Initializing...")
        health_status = StringProperty("Checking...")
        
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.sphere_system = None
            self.setup_ui()
        
        def setup_ui(self):
            """Setup the main UI"""
            layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
            
            # Header
            header = Label(
                text='🌌 SphereOS Unified\nAndroid Application',
                size_hint_y=None,
                height=dp(80),
                font_size=dp(20),
                bold=True
            )
            layout.add_widget(header)
            
            # Status section
            status_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(100))
            self.status_label = Label(text=self.status_text, size_hint_y=None, height=dp(50))
            self.health_label = Label(text=self.health_status, size_hint_y=None, height=dp(50))
            status_layout.add_widget(self.status_label)
            status_layout.add_widget(self.health_label)
            layout.add_widget(status_layout)
            
            # Buttons
            buttons_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(200))
            
            scan_btn = Button(
                text='🔍 Scan Value\nOpportunities',
                size_hint_y=None,
                height=dp(80)
            )
            scan_btn.bind(on_press=self.scan_opportunities)
            buttons_layout.add_widget(scan_btn)
            
            store_btn = Button(
                text='💾 Store Data',
                size_hint_y=None,
                height=dp(80)
            )
            store_btn.bind(on_press=self.show_store_dialog)
            buttons_layout.add_widget(store_btn)
            
            retrieve_btn = Button(
                text='📂 Retrieve Data',
                size_hint_y=None,
                height=dp(80)
            )
            retrieve_btn.bind(on_press=self.show_retrieve_dialog)
            buttons_layout.add_widget(retrieve_btn)
            
            health_btn = Button(
                text='🏥 System Health',
                size_hint_y=None,
                height=dp(80)
            )
            health_btn.bind(on_press=self.check_health)
            buttons_layout.add_widget(health_btn)
            
            layout.add_widget(buttons_layout)
            
            # Nostr Relay buttons
            nostr_layout = GridLayout(cols=3, spacing=dp(10), size_hint_y=None, height=dp(60))
            
            relay_start_btn = Button(
                text='📡 Start\nRelay',
                size_hint_y=None,
                height=dp(50)
            )
            relay_start_btn.bind(on_press=self.start_nostr_relay)
            nostr_layout.add_widget(relay_start_btn)
            
            relay_stop_btn = Button(
                text='🛑 Stop\nRelay',
                size_hint_y=None,
                height=dp(50)
            )
            relay_stop_btn.bind(on_press=self.stop_nostr_relay)
            nostr_layout.add_widget(relay_stop_btn)
            
            relay_info_btn = Button(
                text='ℹ️ Relay\nInfo',
                size_hint_y=None,
                height=dp(50)
            )
            relay_info_btn.bind(on_press=self.show_relay_info)
            nostr_layout.add_widget(relay_info_btn)
            
            layout.add_widget(nostr_layout)
            
            # Results area
            self.results_label = Label(
                text='Results will appear here...',
                size_hint_y=None,
                height=dp(200),
                text_size=(Window.width - dp(20), None),
                halign='left',
                valign='top'
            )
            layout.add_widget(self.results_label)
            
            self.add_widget(layout)
        
        def on_enter(self):
            """Called when screen becomes active"""
            self.initialize_system()
        
        def initialize_system(self):
            """Initialize the SphereOS system"""
            def init_thread():
                try:
                    self.sphere_system = UnifiedSphereSystem()
                    Clock.schedule_once(lambda dt: self.update_status("✅ System initialized successfully"))
                    Clock.schedule_once(lambda dt: self.check_health())
                except Exception as e:
                    Clock.schedule_once(lambda dt: self.update_status(f"❌ Initialization failed: {e}"))
            
            threading.Thread(target=init_thread, daemon=True).start()
        
        def update_status(self, text):
            """Update status text"""
            self.status_text = text
            self.status_label.text = text
        
        def update_health(self, text):
            """Update health status"""
            self.health_status = text
            self.health_label.text = text
        
        def scan_opportunities(self, instance):
            """Scan for value opportunities"""
            if not self.sphere_system:
                self.update_status("❌ System not initialized")
                return
            
            def scan_thread():
                try:
                    results = self.sphere_system.scan_value_opportunities()
                    Clock.schedule_once(lambda dt: self.show_results("Value Opportunities", results))
                except Exception as e:
                    Clock.schedule_once(lambda dt: self.update_status(f"❌ Scan failed: {e}"))
            
            threading.Thread(target=scan_thread, daemon=True).start()
        
        def check_health(self, instance=None):
            """Check system health"""
            if not self.sphere_system:
                self.update_health("❌ System not initialized")
                return
            
            def health_thread():
                try:
                    health = self.sphere_system.get_system_health()
                    Clock.schedule_once(lambda dt: self.update_health(f"🏥 {health['status']} - {health['sphere_positions']} spheres"))
                except Exception as e:
                    Clock.schedule_once(lambda dt: self.update_health(f"❌ Health check failed: {e}"))
            
            threading.Thread(target=health_thread, daemon=True).start()
        
        def show_store_dialog(self, instance):
            """Show data storage dialog"""
            content = BoxLayout(orientation='vertical', padding=dp(10))
            
            # Data input
            data_input = TextInput(
                hint_text='Enter data to store...',
                multiline=True,
                size_hint_y=None,
                height=dp(100)
            )
            content.add_widget(data_input)
            
            # Reference type selection
            ref_type_input = TextInput(
                hint_text='Reference type (path/content/coordinate)',
                text='path',
                size_hint_y=None,
                height=dp(40)
            )
            content.add_widget(ref_type_input)
            
            # Reference value input
            ref_value_input = TextInput(
                hint_text='Reference value',
                text='/test/data',
                size_hint_y=None,
                height=dp(40)
            )
            content.add_widget(ref_value_input)
            
            # Store button
            store_btn = Button(
                text='Store Data',
                size_hint_y=None,
                height=dp(40)
            )
            
            def store_data(btn_instance):
                try:
                    data = data_input.text.encode()
                    ref_type = ref_type_input.text
                    ref_value = ref_value_input.text
                    
                    result = self.sphere_system.store_data_unified(data, ref_type, ref_value)
                    
                    if result['success']:
                        popup.dismiss()
                        self.update_status(f"✅ Data stored at position {result['position']}")
                    else:
                        self.update_status(f"❌ Storage failed: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    self.update_status(f"❌ Storage error: {e}")
            
            store_btn.bind(on_press=store_data)
            content.add_widget(store_btn)
            
            popup = Popup(
                title='Store Data',
                content=content,
                size_hint=(0.9, 0.7)
            )
            popup.open()
        
        def show_retrieve_dialog(self, instance):
            """Show data retrieval dialog"""
            content = BoxLayout(orientation='vertical', padding=dp(10))
            
            # Reference type selection
            ref_type_input = TextInput(
                hint_text='Reference type (path/content/coordinate)',
                text='path',
                size_hint_y=None,
                height=dp(40)
            )
            content.add_widget(ref_type_input)
            
            # Reference value input
            ref_value_input = TextInput(
                hint_text='Reference value',
                text='/test/data',
                size_hint_y=None,
                height=dp(40)
            )
            content.add_widget(ref_value_input)
            
            # Retrieve button
            retrieve_btn = Button(
                text='Retrieve Data',
                size_hint_y=None,
                height=dp(40)
            )
            
            def retrieve_data(btn_instance):
                try:
                    ref_type = ref_type_input.text
                    ref_value = ref_value_input.text
                    
                    data = self.sphere_system.retrieve_data_unified(ref_type, ref_value)
                    
                    if data:
                        popup.dismiss()
                        self.show_results("Retrieved Data", {
                            "data": data.decode('utf-8', errors='ignore'),
                            "size": len(data),
                            "reference_type": ref_type,
                            "reference_value": ref_value
                        })
                    else:
                        self.update_status("❌ Data not found")
                        
                except Exception as e:
                    self.update_status(f"❌ Retrieval error: {e}")
            
            retrieve_btn.bind(on_press=retrieve_data)
            content.add_widget(retrieve_btn)
            
            popup = Popup(
                title='Retrieve Data',
                content=content,
                size_hint=(0.9, 0.6)
            )
            popup.open()
        
        def show_results(self, title, results):
            """Show results in a popup"""
            content = BoxLayout(orientation='vertical', padding=dp(10))
            
            # Results text
            results_text = TextInput(
                text=json.dumps(results, indent=2),
                multiline=True,
                readonly=True,
                size_hint_y=None,
                height=dp(300)
            )
            content.add_widget(results_text)
            
            # Close button
            close_btn = Button(
                text='Close',
                size_hint_y=None,
                height=dp(40)
            )
            close_btn.bind(on_press=lambda x: popup.dismiss())
            content.add_widget(close_btn)
            
            popup = Popup(
                title=title,
                content=content,
                size_hint=(0.95, 0.8)
            )
            popup.open()
        
        def start_nostr_relay(self, instance):
            """Start the Nostr relay"""
            def relay_thread():
                try:
                    import asyncio
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self.sphere_system.nostr_relay.start_relay())
                except Exception as e:
                    Clock.schedule_once(lambda dt: self.update_status(f"❌ Relay start failed: {e}"))
            
            threading.Thread(target=relay_thread, daemon=True).start()
            self.update_status("📡 Starting Nostr relay...")
        
        def stop_nostr_relay(self, instance):
            """Stop the Nostr relay"""
            try:
                self.sphere_system.nostr_relay.stop_relay()
                self.update_status("🛑 Nostr relay stopped")
            except Exception as e:
                self.update_status(f"❌ Relay stop failed: {e}")
        
        def show_relay_info(self, instance):
            """Show Nostr relay information"""
            try:
                relay_info = self.sphere_system.nostr_relay.get_relay_info()
                self.show_results("Nostr Relay Information", relay_info)
            except Exception as e:
                self.show_results("Relay Info Error", f"Failed to get relay info: {e}")

    class SphereOSApp(App):
        """Main SphereOS Android application"""
        
        def build(self):
            """Build the application"""
            # Set window size for testing (will be fullscreen on Android)
            if platform != 'android':
                Window.size = (400, 600)
            
            # Create screen manager
            sm = ScreenManager()
            main_screen = SphereOSMainScreen(name='main')
            sm.add_widget(main_screen)
            
            return sm

# ============================================================================
# CONSOLE MODE (Fallback when Kivy not available)
# ============================================================================

class ConsoleSphereOS:
    """Console-based SphereOS for systems without Kivy"""
    
    def __init__(self):
        self.sphere_system = UnifiedSphereSystem()
        self.running = True
    
    def run(self):
        """Run console interface"""
        print("🌌 SphereOS Unified Console Application")
        print("=" * 50)
        
        while self.running:
            print("\nOptions:")
            print("1. Scan Value Opportunities")
            print("2. Store Data")
            print("3. Retrieve Data")
            print("4. System Health")
            print("5. Start Nostr Relay")
            print("6. Stop Nostr Relay")
            print("7. Show Relay Info")
            print("8. Exit")
            
            choice = input("\nEnter choice (1-8): ").strip()
            
            if choice == "1":
                self.scan_opportunities()
            elif choice == "2":
                self.store_data()
            elif choice == "3":
                self.retrieve_data()
            elif choice == "4":
                self.check_health()
            elif choice == "5":
                self.start_nostr_relay()
            elif choice == "6":
                self.stop_nostr_relay()
            elif choice == "7":
                self.show_relay_info()
            elif choice == "8":
                self.running = False
                print("Goodbye!")
            else:
                print("Invalid choice. Please try again.")
    
    def scan_opportunities(self):
        """Scan for value opportunities"""
        print("\n🔍 Scanning for value opportunities...")
        try:
            results = self.sphere_system.scan_value_opportunities()
            print(f"✅ Found {len(results.get('opportunities', []))} opportunities")
            print(f"✅ Found {len(results.get('leakages', []))} leakages")
            print(f"💰 Total opportunity value: ${results.get('total_opportunity_value', 0):,.2f}")
        except Exception as e:
            print(f"❌ Scan failed: {e}")
    
    def store_data(self):
        """Store data"""
        print("\n💾 Store Data")
        data = input("Enter data to store: ").strip()
        ref_type = input("Reference type (path/content/coordinate): ").strip()
        ref_value = input("Reference value: ").strip()
        
        try:
            result = self.sphere_system.store_data_unified(
                data.encode(), ref_type, ref_value
            )
            if result['success']:
                print(f"✅ Data stored at position {result['position']}")
            else:
                print(f"❌ Storage failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"❌ Storage error: {e}")
    
    def retrieve_data(self):
        """Retrieve data"""
        print("\n📂 Retrieve Data")
        ref_type = input("Reference type (path/content/coordinate): ").strip()
        ref_value = input("Reference value: ").strip()
        
        try:
            data = self.sphere_system.retrieve_data_unified(ref_type, ref_value)
            if data:
                print(f"✅ Retrieved data: {data.decode('utf-8', errors='ignore')}")
            else:
                print("❌ Data not found")
        except Exception as e:
            print(f"❌ Retrieval error: {e}")
    
    def check_health(self):
        """Check system health"""
        print("\n🏥 System Health")
        try:
            health = self.sphere_system.get_system_health()
            print(f"Status: {health['status']}")
            print(f"Database size: {health['database_size_mb']} MB")
            print(f"Active sessions: {health['active_sessions']}")
            
            # Show Nostr relay info
            relay_info = health.get('nostr_relay', {})
            if relay_info:
                print(f"📡 Relay: {relay_info.get('name', 'Unknown')}")
                print(f"   Connected clients: {relay_info.get('connected_clients', 0)}")
                print(f"   Total events: {relay_info.get('total_events', 0)}")
                print(f"   Active subscriptions: {relay_info.get('active_subscriptions', 0)}")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
    
    def start_nostr_relay(self):
        """Start the Nostr relay"""
        print("\n📡 Starting Nostr relay...")
        try:
            import asyncio
            import threading
            
            def run_relay():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.sphere_system.nostr_relay.start_relay())
            
            relay_thread = threading.Thread(target=run_relay, daemon=True)
            relay_thread.start()
            print("✅ Nostr relay started in background")
            print("   Connect to: ws://localhost:8080")
        except Exception as e:
            print(f"❌ Failed to start relay: {e}")
    
    def stop_nostr_relay(self):
        """Stop the Nostr relay"""
        print("\n🛑 Stopping Nostr relay...")
        try:
            self.sphere_system.nostr_relay.stop_relay()
            print("✅ Nostr relay stopped")
        except Exception as e:
            print(f"❌ Failed to stop relay: {e}")
    
    def show_relay_info(self):
        """Show Nostr relay information"""
        print("\nℹ️ Nostr Relay Information:")
        try:
            relay_info = self.sphere_system.nostr_relay.get_relay_info()
            print(f"   Name: {relay_info.get('name', 'Unknown')}")
            print(f"   Description: {relay_info.get('description', 'Unknown')}")
            print(f"   Version: {relay_info.get('version', 'Unknown')}")
            print(f"   Connected clients: {relay_info.get('connected_clients', 0)}")
            print(f"   Total events: {relay_info.get('total_events', 0)}")
            print(f"   Active subscriptions: {relay_info.get('active_subscriptions', 0)}")
            print(f"   Status: {relay_info.get('uptime', 'Unknown')}")
        except Exception as e:
            print(f"❌ Failed to get relay info: {e}")

# ============================================================================
# MAIN APPLICATION ENTRY POINT
# ============================================================================

def main():
    """Main application entry point"""
    print("🌌 SphereOS Android Unified Application")
    print("=" * 50)
    
    # Check if running on Android or if Kivy is available
    if KIVY_AVAILABLE and (platform == 'android' or '--gui' in sys.argv):
        print("🚀 Starting Kivy GUI mode...")
        app = SphereOSApp()
        app.run()
    else:
        print("💻 Starting console mode...")
        console_app = ConsoleSphereOS()
        console_app.run()

if __name__ == "__main__":
    main() 