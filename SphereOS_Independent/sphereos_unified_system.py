#!/usr/bin/env python3
"""
SphereOS Unified System
Core 108-Sphere Lattice implementation with 3-constituent addressing
"""

import sqlite3
import hashlib
import json
import zlib
import base64
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass


@dataclass
class SpherePosition:
    position_id: int
    layer: int
    data: Optional[bytes] = None
    checksum: Optional[str] = None
    created_at: Optional[str] = None


class SphereLattice108:
    """108-Sphere Lattice with 3-constituent addressing system"""
    
    def __init__(self, db_path: str = "sphereos_lattice.db"):
        self.db_path = db_path
        self.initialize_database()
    
    def initialize_database(self):
        """Initialize the sphere lattice database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create sphere positions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sphere_positions (
                position_id INTEGER PRIMARY KEY,
                layer INTEGER CHECK (layer BETWEEN 1 AND 11),
                data BLOB,
                checksum TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create atlas positions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS atlas_positions (
                position_id INTEGER PRIMARY KEY,
                hierarchical_path TEXT UNIQUE NOT NULL,
                layer_number INTEGER CHECK (layer_number BETWEEN 1 AND 11),
                data_chunk BLOB,
                checksum TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create content positions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_positions (
                content_hash TEXT PRIMARY KEY,
                sphere_position INTEGER NOT NULL,
                content_type TEXT,
                data_chunk BLOB,
                compression_ratio REAL DEFAULT 1.0,
                checksum TEXT
            )
        ''')
        
        # Create coordinate positions table
        cursor.execute('''
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
        ''')
        
        # Create cross-reference table
        cursor.execute('''
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
        ''')
        
        conn.commit()
        conn.close()
    
    def store_data_atlas(self, hierarchical_path: str, data: str) -> bool:
        """Store data using Atlas (hierarchical) addressing"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Determine layer from path depth
            layer_number = len(hierarchical_path.split('/')) - 1
            layer_number = max(1, min(11, layer_number))
            
            # Compress and hash data
            data_bytes = data.encode('utf-8')
            compressed_data = zlib.compress(data_bytes)
            checksum = hashlib.sha256(compressed_data).hexdigest()
            
            cursor.execute('''
                INSERT OR REPLACE INTO atlas_positions 
                (hierarchical_path, layer_number, data_chunk, checksum)
                VALUES (?, ?, ?, ?)
            ''', (hierarchical_path, layer_number, compressed_data, checksum))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing atlas data: {e}")
            return False
    
    def retrieve_data_atlas(self, hierarchical_path: str) -> Optional[str]:
        """Retrieve data using Atlas addressing"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT data_chunk, checksum FROM atlas_positions 
                WHERE hierarchical_path = ?
            ''', (hierarchical_path,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                compressed_data, stored_checksum = result
                # Verify checksum
                if hashlib.sha256(compressed_data).hexdigest() == stored_checksum:
                    decompressed_data = zlib.decompress(compressed_data)
                    return decompressed_data.decode('utf-8')
            
            return None
        except Exception as e:
            print(f"Error retrieving atlas data: {e}")
            return None
    
    def store_data_content(self, content_hash: str, data: str) -> bool:
        """Store data using Content (hash-based) addressing"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Find available sphere position
            cursor.execute('''
                SELECT position_id FROM sphere_positions 
                WHERE data IS NULL LIMIT 1
            ''')
            result = cursor.fetchone()
            
            if not result:
                # Create new sphere position
                cursor.execute('''
                    INSERT INTO sphere_positions (layer) 
                    VALUES (?) 
                    RETURNING position_id
                ''', (1,))
                sphere_position = cursor.lastrowid
            else:
                sphere_position = result[0]
            
            # Compress and store data
            data_bytes = data.encode('utf-8')
            original_size = len(data_bytes)
            compressed_data = zlib.compress(data_bytes)
            compressed_size = len(compressed_data)
            compression_ratio = compressed_size / original_size if original_size > 0 else 1.0
            
            checksum = hashlib.sha256(compressed_data).hexdigest()
            
            cursor.execute('''
                INSERT OR REPLACE INTO content_positions 
                (content_hash, sphere_position, content_type, data_chunk, compression_ratio, checksum)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (content_hash, sphere_position, 'text', compressed_data, compression_ratio, checksum))
            
            # Update sphere position
            cursor.execute('''
                UPDATE sphere_positions 
                SET data = ?, checksum = ? 
                WHERE position_id = ?
            ''', (compressed_data, checksum, sphere_position))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing content data: {e}")
            return False
    
    def retrieve_data_content(self, content_hash: str) -> Optional[str]:
        """Retrieve data using Content addressing"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT data_chunk, checksum FROM content_positions 
                WHERE content_hash = ?
            ''', (content_hash,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                compressed_data, stored_checksum = result
                # Verify checksum
                if hashlib.sha256(compressed_data).hexdigest() == stored_checksum:
                    decompressed_data = zlib.decompress(compressed_data)
                    return decompressed_data.decode('utf-8')
            
            return None
        except Exception as e:
            print(f"Error retrieving content data: {e}")
            return None
    
    def store_data_coordinate(self, latitude: float, longitude: float, data: str, precision: int = 6) -> bool:
        """Store data using Coordinate (GPS-based) addressing"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create coordinate ID
            coordinate_id = f"{latitude:.{precision}f}_{longitude:.{precision}f}"
            
            # Find available sphere position
            cursor.execute('''
                SELECT position_id FROM sphere_positions 
                WHERE data IS NULL LIMIT 1
            ''')
            result = cursor.fetchone()
            
            if not result:
                cursor.execute('''
                    INSERT INTO sphere_positions (layer) 
                    VALUES (?) 
                    RETURNING position_id
                ''', (1,))
                sphere_position = cursor.lastrowid
            else:
                sphere_position = result[0]
            
            # Compress and store data
            data_bytes = data.encode('utf-8')
            compressed_data = zlib.compress(data_bytes)
            checksum = hashlib.sha256(compressed_data).hexdigest()
            
            cursor.execute('''
                INSERT OR REPLACE INTO coordinate_positions 
                (coordinate_id, latitude, longitude, precision_level, sphere_position, 
                 temporal_start, temporal_end, data_chunk, checksum)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (coordinate_id, latitude, longitude, precision, sphere_position,
                  datetime.now().isoformat(), None, compressed_data, checksum))
            
            # Update sphere position
            cursor.execute('''
                UPDATE sphere_positions 
                SET data = ?, checksum = ? 
                WHERE position_id = ?
            ''', (compressed_data, checksum, sphere_position))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing coordinate data: {e}")
            return False
    
    def retrieve_data_coordinate(self, latitude: float, longitude: float, precision: int = 6) -> Optional[str]:
        """Retrieve data using Coordinate addressing"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            coordinate_id = f"{latitude:.{precision}f}_{longitude:.{precision}f}"
            
            cursor.execute('''
                SELECT data_chunk, checksum FROM coordinate_positions 
                WHERE coordinate_id = ?
            ''', (coordinate_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                compressed_data, stored_checksum = result
                # Verify checksum
                if hashlib.sha256(compressed_data).hexdigest() == stored_checksum:
                    decompressed_data = zlib.decompress(compressed_data)
                    return decompressed_data.decode('utf-8')
            
            return None
        except Exception as e:
            print(f"Error retrieving coordinate data: {e}")
            return None
    
    def get_sphere_statistics(self) -> Dict[str, Any]:
        """Get statistics about the sphere lattice"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Count positions by layer
            cursor.execute('''
                SELECT layer, COUNT(*) FROM sphere_positions 
                GROUP BY layer ORDER BY layer
            ''')
            layer_counts = dict(cursor.fetchall())
            
            # Count occupied vs empty positions
            cursor.execute('''
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN data IS NOT NULL THEN 1 END) as occupied,
                    COUNT(CASE WHEN data IS NULL THEN 1 END) as empty
                FROM sphere_positions
            ''')
            total, occupied, empty = cursor.fetchone()
            
            # Count by constituent type
            cursor.execute('SELECT COUNT(*) FROM atlas_positions')
            atlas_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM content_positions')
            content_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM coordinate_positions')
            coordinate_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "total_positions": total,
                "occupied_positions": occupied,
                "empty_positions": empty,
                "occupancy_rate": occupied / total if total > 0 else 0,
                "layer_distribution": layer_counts,
                "constituent_counts": {
                    "atlas": atlas_count,
                    "content": content_count,
                    "coordinate": coordinate_count
                }
            }
        except Exception as e:
            print(f"Error getting sphere statistics: {e}")
            return {}


class SphereOSUnifiedServer:
    """Unified server for SphereOS with all core functionality"""
    
    def __init__(self):
        self.sphere_lattice = SphereLattice108()
        self.metrics = {}
    
    def get_metrics(self, metric_type: str) -> Dict[str, Any]:
        """Get system metrics"""
        if metric_type == "real-time":
            return {
                "timestamp": datetime.now().isoformat(),
                "sphere_statistics": self.sphere_lattice.get_sphere_statistics(),
                "system_health": "healthy",
                "active_connections": 0
            }
        elif metric_type == "sphere":
            return self.sphere_lattice.get_sphere_statistics()
        else:
            return {"error": f"Unknown metric type: {metric_type}"}
    
    async def get_sphere_data(self, position_id: str) -> Dict[str, Any]:
        """Get data from sphere position"""
        try:
            position_id_int = int(position_id)
            conn = sqlite3.connect(self.sphere_lattice.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT position_id, layer, data, checksum, created_at 
                FROM sphere_positions 
                WHERE position_id = ?
            ''', (position_id_int,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                pos_id, layer, data, checksum, created_at = result
                return {
                    "position_id": pos_id,
                    "layer": layer,
                    "has_data": data is not None,
                    "checksum": checksum,
                    "created_at": created_at
                }
            else:
                return {"error": f"Position {position_id} not found"}
        except ValueError:
            return {"error": f"Invalid position ID: {position_id}"}
        except Exception as e:
            return {"error": f"Error retrieving sphere data: {e}"}
    
    def store_data(self, data: str, reference_type: str, reference_value: str, compress: bool = True) -> Dict[str, Any]:
        """Store data using specified reference type"""
        try:
            if reference_type == "atlas":
                success = self.sphere_lattice.store_data_atlas(reference_value, data)
            elif reference_type == "content":
                success = self.sphere_lattice.store_data_content(reference_value, data)
            elif reference_type == "coordinate":
                # Parse coordinate from reference_value (format: "lat,lng")
                coords = reference_value.split(',')
                if len(coords) == 2:
                    lat, lng = float(coords[0]), float(coords[1])
                    success = self.sphere_lattice.store_data_coordinate(lat, lng, data)
                else:
                    return {"error": "Invalid coordinate format. Use 'latitude,longitude'"}
            else:
                return {"error": f"Unknown reference type: {reference_type}"}
            
            if success:
                return {
                    "success": True,
                    "reference_type": reference_type,
                    "reference_value": reference_value,
                    "stored_at": datetime.now().isoformat()
                }
            else:
                return {"error": "Failed to store data"}
        except Exception as e:
            return {"error": f"Error storing data: {e}"} 