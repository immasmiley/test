"""
SphereOS Calendar-GPS Integration Module
Integrates calendar events with GPS location tracking and POI identification
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from enum import Enum


class EventType(Enum):
    MEETING = "meeting"
    TRAVEL = "travel"
    WORK = "work"
    PERSONAL = "personal"
    SOCIAL = "social"


@dataclass
class GPSLocation:
    latitude: float
    longitude: float
    accuracy: float
    timestamp: datetime
    speed: Optional[float] = None
    heading: Optional[float] = None


@dataclass
class PointOfInterest:
    name: str
    location: GPSLocation
    poi_type: str
    description: Optional[str] = None
    rating: Optional[float] = None


@dataclass
class TimeStamp:
    start_time: datetime
    end_time: Optional[datetime] = None
    location: Optional[GPSLocation] = None
    activity_type: str = "unknown"


@dataclass
class CalendarEvent:
    event_id: str
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    location: Optional[GPSLocation] = None
    event_type: EventType = EventType.MEETING
    attendees: List[str] = None
    reminder_minutes: int = 15


class GPSLocationTracker:
    """Tracks GPS location and movement patterns"""
    
    def __init__(self):
        self.location_history: List[GPSLocation] = []
        self.current_location: Optional[GPSLocation] = None
    
    def update_location(self, latitude: float, longitude: float, accuracy: float = 10.0,
                       speed: Optional[float] = None, heading: Optional[float] = None):
        """Update current GPS location"""
        location = GPSLocation(
            latitude=latitude,
            longitude=longitude,
            accuracy=accuracy,
            timestamp=datetime.now(),
            speed=speed,
            heading=heading
        )
        
        self.current_location = location
        self.location_history.append(location)
        
        # Keep only last 1000 locations
        if len(self.location_history) > 1000:
            self.location_history = self.location_history[-1000:]
    
    def get_location_history(self, hours: int = 24) -> List[GPSLocation]:
        """Get location history for specified hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [loc for loc in self.location_history if loc.timestamp > cutoff_time]
    
    def calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate distance between two GPS coordinates in meters"""
        import math
        
        R = 6371000  # Earth's radius in meters
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat / 2) * math.sin(delta_lat / 2) +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lng / 2) * math.sin(delta_lng / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c


class POIService:
    """Service for Points of Interest identification and management"""
    
    def __init__(self):
        self.poi_database: List[PointOfInterest] = []
        self._initialize_sample_pois()
    
    def _initialize_sample_pois(self):
        """Initialize with sample POIs for demonstration"""
        sample_pois = [
            PointOfInterest("Google Headquarters", GPSLocation(37.4220, -122.0841, 10.0, datetime.now()), "office"),
            PointOfInterest("Stanford University", GPSLocation(37.4275, -122.1697, 10.0, datetime.now()), "education"),
            PointOfInterest("San Francisco Airport", GPSLocation(37.6213, -122.3790, 10.0, datetime.now()), "transport"),
            PointOfInterest("Golden Gate Bridge", GPSLocation(37.8199, -122.4783, 10.0, datetime.now()), "landmark"),
        ]
        self.poi_database.extend(sample_pois)
    
    def find_nearby_pois(self, latitude: float, longitude: float, radius_meters: float = 1000.0) -> List[PointOfInterest]:
        """Find POIs within specified radius"""
        nearby_pois = []
        tracker = GPSLocationTracker()
        
        for poi in self.poi_database:
            distance = tracker.calculate_distance(
                latitude, longitude,
                poi.location.latitude, poi.location.longitude
            )
            if distance <= radius_meters:
                nearby_pois.append(poi)
        
        return nearby_pois
    
    def identify_poi(self, latitude: float, longitude: float) -> Optional[PointOfInterest]:
        """Identify POI at specific coordinates"""
        nearby_pois = self.find_nearby_pois(latitude, longitude, radius_meters=100.0)
        if nearby_pois:
            return nearby_pois[0]  # Return closest POI
        return None
    
    def add_poi(self, name: str, latitude: float, longitude: float, poi_type: str, description: str = None):
        """Add new POI to database"""
        poi = PointOfInterest(
            name=name,
            location=GPSLocation(latitude, longitude, 10.0, datetime.now()),
            poi_type=poi_type,
            description=description
        )
        self.poi_database.append(poi)


class TimeStampTracker:
    """Tracks time spent at different locations"""
    
    def __init__(self):
        self.active_sessions: Dict[str, TimeStamp] = {}
        self.session_history: List[TimeStamp] = []
    
    def start_session(self, user_id: str, location_id: str, activity_type: str = "unknown"):
        """Start a new time tracking session"""
        if user_id in self.active_sessions:
            self.end_session(user_id)
        
        session = TimeStamp(
            start_time=datetime.now(),
            activity_type=activity_type
        )
        self.active_sessions[user_id] = session
    
    def end_session(self, user_id: str):
        """End an active time tracking session"""
        if user_id in self.active_sessions:
            session = self.active_sessions[user_id]
            session.end_time = datetime.now()
            self.session_history.append(session)
            del self.active_sessions[user_id]
    
    def get_session_duration(self, user_id: str) -> Optional[timedelta]:
        """Get duration of active session"""
        if user_id in self.active_sessions:
            session = self.active_sessions[user_id]
            return datetime.now() - session.start_time
        return None
    
    def get_user_history(self, user_id: str, days: int = 7) -> List[TimeStamp]:
        """Get session history for user"""
        cutoff_time = datetime.now() - timedelta(days=days)
        return [session for session in self.session_history 
                if session.start_time > cutoff_time]


class CalendarGPSIntegrator:
    """Integrates calendar events with GPS location data"""
    
    def __init__(self):
        self.gps_tracker = GPSLocationTracker()
        self.poi_service = POIService()
        self.timestamp_tracker = TimeStampTracker()
        self.events: List[CalendarEvent] = []
    
    def add_event(self, event: CalendarEvent):
        """Add calendar event"""
        self.events.append(event)
    
    def get_events_for_location(self, latitude: float, longitude: float, radius_meters: float = 1000.0) -> List[CalendarEvent]:
        """Get events near specific location"""
        nearby_events = []
        for event in self.events:
            if event.location:
                distance = self.gps_tracker.calculate_distance(
                    latitude, longitude,
                    event.location.latitude, event.location.longitude
                )
                if distance <= radius_meters:
                    nearby_events.append(event)
        return nearby_events
    
    def suggest_poi_for_event(self, event: CalendarEvent) -> Optional[PointOfInterest]:
        """Suggest POI for calendar event based on title/description"""
        if not event.location:
            return None
        
        # Find nearby POIs
        nearby_pois = self.poi_service.find_nearby_pois(
            event.location.latitude, event.location.longitude
        )
        
        if nearby_pois:
            return nearby_pois[0]
        return None
    
    def track_event_attendance(self, event_id: str, user_id: str, latitude: float, longitude: float):
        """Track user attendance at event location"""
        event = next((e for e in self.events if e.event_id == event_id), None)
        if event and event.location:
            distance = self.gps_tracker.calculate_distance(
                latitude, longitude,
                event.location.latitude, event.location.longitude
            )
            
            if distance <= 100.0:  # Within 100 meters of event
                self.timestamp_tracker.start_session(user_id, event_id, "event_attendance")
                return True
        return False 