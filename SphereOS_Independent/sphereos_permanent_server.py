#!/usr/bin/env python3
"""
SphereOS Permanent Server - Automatic Endpoint Management & Value Leakage Discovery
Revolutionary system that never has missing endpoints and automatically detects value opportunities
"""

from fastapi import FastAPI, HTTPException, Query, Request, BackgroundTasks, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Union
import uvicorn
import sqlite3
import hashlib
import json
import time
import base64
import zlib
import asyncio
import math
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum


# Import existing unified system
from sphereos_unified_system import SphereOSUnifiedServer, SphereLattice108

# Import Calendar-GPS integration
from sphereos_calendar_gps_integration import (
    CalendarGPSIntegrator, GPSLocationTracker, POIService, TimeStampTracker,
    GPSLocation, PointOfInterest, TimeStamp, CalendarEvent, EventType
)

# Import Universal Value Framework
from sphereos_universal_value_framework import (
    UniversalValueDetector, ValueOpportunity, ValueLeakage, ValueArea, OpportunityType,
    CommercialExchangeDetector, KnowledgeTransferDetector, ResourceSharingDetector,
    NetworkBridgingDetector, TemporalCoordinationDetector, GeographicClusteringDetector,
    SkillDevelopmentDetector, InnovationImplementationDetector, SocialCapitalDetector,
    InformationFlowDetector, CollaborativeProductionDetector, SystemicEfficiencyDetector
)

# Add imports for transaction cost analyzer
from sphereos_transaction_cost_analyzer import (
    TransactionCostAnalyzer, ProfitabilityAnalysis, TransactionCostType, 
    ProfitabilityStatus, FrictionFactor
)

# Add imports for value streaming system
from sphereos_value_streaming_system import (
    ValueStreamingSystem, ValueContent, UserValueProfile, ValueMatch,
    ContentType, ValueCategory
)

# Add imports for authentication and sessions
import secrets
import uuid

# ============================================================================
# AUTHENTICATION & SESSION MANAGEMENT
# ============================================================================

class UserSession:
    """Manages user sessions and authentication"""
    
    def __init__(self):
        self.active_sessions = {}  # session_token -> user_data
        self.session_timeout = 24 * 60 * 60  # 24 hours in seconds
    
    def create_session(self, user_data: Dict) -> str:
        """Create a new session for a user"""
        session_token = secrets.token_urlsafe(32)
        user_data['session_created'] = datetime.now().isoformat()
        self.active_sessions[session_token] = user_data
        return session_token
    
    def get_session(self, session_token: str) -> Optional[Dict]:
        """Get user data from session token"""
        if session_token in self.active_sessions:
            session_data = self.active_sessions[session_token]
            created_time = datetime.fromisoformat(session_data['session_created'])
            if datetime.now() - created_time < timedelta(seconds=self.session_timeout):
                return session_data
            else:
                # Session expired
                del self.active_sessions[session_token]
        return None
    
    def invalidate_session(self, session_token: str):
        """Invalidate a session"""
        if session_token in self.active_sessions:
            del self.active_sessions[session_token]

# Global session manager
session_manager = UserSession()

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def initialize_social_database():
    """Initialize database tables for social media features"""
    conn = sqlite3.connect('sphereos_social.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            npub TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            bio TEXT,
            location TEXT,
            interests TEXT,
            avatar_data TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Friends table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS friends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_npub TEXT NOT NULL,
            to_npub TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(from_npub, to_npub),
            FOREIGN KEY (from_npub) REFERENCES users(npub),
            FOREIGN KEY (to_npub) REFERENCES users(npub)
        )
    ''')
    
    # Averments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS averments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            verifier_npub TEXT NOT NULL,
            verified_npub TEXT NOT NULL,
            institution_name TEXT NOT NULL,
            role TEXT NOT NULL,
            time_period TEXT NOT NULL,
            location TEXT NOT NULL,
            confidence_score REAL DEFAULT 1.0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (verifier_npub) REFERENCES users(npub),
            FOREIGN KEY (verified_npub) REFERENCES users(npub)
        )
    ''')
    
    # Institutions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS institutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            coordinates_lat REAL,
            coordinates_lng REAL,
            institution_type TEXT DEFAULT 'general',
            created_by TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users(npub)
        )
    ''')
    
    # Institution members table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS institution_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            institution_id INTEGER NOT NULL,
            user_npub TEXT NOT NULL,
            joined_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(institution_id, user_npub),
            FOREIGN KEY (institution_id) REFERENCES institutions(id),
            FOREIGN KEY (user_npub) REFERENCES users(npub)
        )
    ''')
    
    # Groups table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            group_type TEXT DEFAULT 'general',
            is_private BOOLEAN DEFAULT 0,
            creator_npub TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (creator_npub) REFERENCES users(npub)
        )
    ''')
    
    # Group members table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL,
            user_npub TEXT NOT NULL,
            joined_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(group_id, user_npub),
            FOREIGN KEY (group_id) REFERENCES groups(id),
            FOREIGN KEY (user_npub) REFERENCES users(npub)
        )
    ''')
    
    # User activity table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_npub TEXT NOT NULL,
            activity_type TEXT NOT NULL,
            activity_data TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_npub) REFERENCES users(npub)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Social media database initialized")

# Initialize database
initialize_social_database()

# ============================================================================
# AUTHENTICATION MODELS
# ============================================================================

class LoginRequest(BaseModel):
    npub: str
    private_key: Optional[str] = None

class RegisterRequest(BaseModel):
    name: str
    bio: Optional[str] = None
    location: Optional[str] = None
    interests: Optional[str] = None
    avatar_data: Optional[str] = None

class AuthResponse(BaseModel):
    success: bool
    session_token: Optional[str] = None
    user_data: Optional[Dict] = None
    message: str

# Add frontend data models
class UserProfileUpdate(BaseModel):
    npub: str
    name: str
    bio: Optional[str] = None
    location: Optional[str] = None
    interests: Optional[str] = None
    avatar_data: Optional[str] = None

class FriendRequest(BaseModel):
    from_npub: str
    to_npub: str
    message: Optional[str] = None

class AvermentSubmission(BaseModel):
    verifier_npub: str
    verified_npub: str
    institution_name: str
    role: str
    time_period: str
    location: str
    confidence_score: float = 1.0

class InstitutionJoin(BaseModel):
    user_npub: str
    institution_name: str
    coordinates_lat: Optional[float] = None
    coordinates_lng: Optional[float] = None
    time_period: Optional[str] = None

class GroupCreate(BaseModel):
    creator_npub: str
    group_name: str
    description: str
    group_type: str = "general"
    is_private: bool = False

class GroupJoin(BaseModel):
    user_npub: str
    group_name: str

class SearchQuery(BaseModel):
    query: str
    filter_type: str = "all"
    user_npub: Optional[str] = None

class UserActivity(BaseModel):
    user_npub: str
    activity_type: str
    activity_data: Dict[str, Any]
    timestamp: Optional[str] = None

# Initialize FastAPI app
app = FastAPI(
    title="SphereOS Permanent System",
    description="Dynamic Living Decentralized Profile Platform with Automatic Endpoint Management & Value Leakage Discovery",
    version="2.0.0"
)

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Initialize unified system
sphereos_server = SphereOSUnifiedServer()

# ============================================================================
# AUTOMATIC ENDPOINT MANAGEMENT SYSTEM
# ============================================================================

class EndpointManager:
    """Automatically manages all endpoints - no missing endpoints ever"""
    
    def __init__(self):
        self.endpoints = {}
        self.endpoint_patterns = {}
        self.auto_generated = set()
        self.initialize_endpoint_patterns()
    
    def initialize_endpoint_patterns(self):
        """Define patterns for automatic endpoint generation"""
        self.endpoint_patterns = {
            # Health and status patterns
            'health': {
                'path': '/api/health',
                'method': 'GET',
                'description': 'System health status',
                'auto_generate': True
            },
            'metrics': {
                'path': '/api/metrics/{metric_type}',
                'method': 'GET', 
                'description': 'System metrics',
                'auto_generate': True
            },
            'status': {
                'path': '/api/status/{component}',
                'method': 'GET',
                'description': 'Component status',
                'auto_generate': True
            },
            
            # Identity management patterns
            'identity': {
                'path': '/api/identity/{action}',
                'method': 'POST',
                'description': 'Identity operations',
                'auto_generate': True
            },
            'profile': {
                'path': '/api/profile/{npub}/{action}',
                'method': 'GET',
                'description': 'Profile operations',
                'auto_generate': True
            },
            
            # Sphere operations patterns
            'sphere': {
                'path': '/api/sphere/{action}/{identifier}',
                'method': 'GET',
                'description': 'Sphere operations',
                'auto_generate': True
            },
            'sphere_store': {
                'path': '/api/sphere/store/{reference_type}',
                'method': 'POST',
                'description': 'Store data in sphere',
                'auto_generate': True
            },
            
            # Institution patterns
            'institution': {
                'path': '/api/institutions/{action}',
                'method': 'POST',
                'description': 'Institution operations',
                'auto_generate': True
            },
            'institution_search': {
                'path': '/api/institutions/search/{search_type}',
                'method': 'GET',
                'description': 'Institution search',
                'auto_generate': True
            },
            
            # Value Leakage Discovery patterns
            'value_leakage': {
                'path': '/api/value-leakage/{action}',
                'method': 'GET',
                'description': 'Value leakage detection',
                'auto_generate': True
            },
            'opportunities': {
                'path': '/api/opportunities/{opportunity_type}',
                'method': 'GET',
                'description': 'Opportunity discovery',
                'auto_generate': True
            },
            'commercial': {
                'path': '/api/commercial/{action}',
                'method': 'GET',
                'description': 'Commercial transaction detection',
                'auto_generate': True
            }
        }
    
    def register_endpoint(self, path: str, method: str, handler, description: str = ""):
        """Register an endpoint with the manager"""
        key = f"{method}:{path}"
        self.endpoints[key] = {
            'path': path,
            'method': method,
            'handler': handler,
            'description': description,
            'registered_at': datetime.utcnow().isoformat()
        }
    
    def auto_generate_missing_endpoints(self):
        """Automatically generate any missing endpoints based on patterns"""
        generated = []
        
        for pattern_name, pattern in self.endpoint_patterns.items():
            if not pattern['auto_generate']:
                continue
                
            # Check if pattern endpoints exist
            pattern_path = pattern['path']
            method = pattern['method']
            
            # Generate specific endpoints based on pattern
            specific_endpoints = self.generate_specific_endpoints(pattern_name, pattern_path, method)
            
            for endpoint in specific_endpoints:
                if endpoint['key'] not in self.endpoints:
                    # Auto-generate the endpoint
                    handler = self.create_auto_handler(endpoint)
                    self.register_endpoint(endpoint['path'], endpoint['method'], handler, endpoint['description'])
                    self.auto_generated.add(endpoint['key'])
                    generated.append(endpoint)
        
        return generated
    
    def generate_specific_endpoints(self, pattern_name: str, pattern_path: str, method: str) -> List[Dict]:
        """Generate specific endpoints from a pattern"""
        endpoints = []
        
        if pattern_name == 'health':
            endpoints.append({
                'key': f"{method}:/api/health",
                'path': '/api/health',
                'method': method,
                'description': 'System health status'
            })
            
        elif pattern_name == 'metrics':
            for metric_type in ['real-time', 'daily', 'weekly', 'monthly']:
                endpoints.append({
                    'key': f"{method}:/api/metrics/{metric_type}",
                    'path': f'/api/metrics/{metric_type}',
                    'method': method,
                    'description': f'{metric_type.title()} system metrics'
                })
                
        elif pattern_name == 'sphere':
            for action in ['get', 'store', 'delete', 'update', 'search']:
                endpoints.append({
                    'key': f"{method}:/api/sphere/{action}/{{identifier}}",
                    'path': f'/api/sphere/{action}/{{identifier}}',
                    'method': method,
                    'description': f'Sphere {action} operation'
                })
                
        elif pattern_name == 'value_leakage':
            for action in ['scan', 'detect', 'analyze', 'report']:
                endpoints.append({
                    'key': f"{method}:/api/value-leakage/{action}",
                    'path': f'/api/value-leakage/{action}',
                    'method': method,
                    'description': f'Value leakage {action}'
                })
                
        elif pattern_name == 'opportunities':
            for opp_type in ['professional', 'economic', 'social', 'knowledge', 'geographic']:
                endpoints.append({
                    'key': f"{method}:/api/opportunities/{opp_type}",
                    'path': f'/api/opportunities/{opp_type}',
                    'method': method,
                    'description': f'{opp_type.title()} opportunities'
                })
                
        elif pattern_name == 'commercial':
            for action in ['opportunities', 'transactions', 'matches', 'analysis']:
                endpoints.append({
                    'key': f"{method}:/api/commercial/{action}",
                    'path': f'/api/commercial/{action}',
                    'method': method,
                    'description': f'Commercial {action}'
                })
        
        return endpoints
    
    def create_auto_handler(self, endpoint: Dict):
        """Create an automatic handler for an endpoint"""
        
        async def auto_handler(request: Request):
            try:
                # Extract path parameters
                path_params = request.path_params
                
                # Route to appropriate handler based on endpoint type
                if 'health' in endpoint['path']:
                    return await self.handle_health()
                elif 'metrics' in endpoint['path']:
                    return await self.handle_metrics(endpoint['path'])
                elif 'sphere' in endpoint['path']:
                    return await self.handle_sphere(endpoint['path'], path_params)
                elif 'value-leakage' in endpoint['path']:
                    return await self.handle_value_leakage(endpoint['path'])
                elif 'opportunities' in endpoint['path']:
                    return await self.handle_opportunities(endpoint['path'])
                elif 'commercial' in endpoint['path']:
                    return await self.handle_commercial(endpoint['path'])
                else:
                    return {"status": "auto_generated", "endpoint": endpoint['path'], "message": "Endpoint auto-generated"}
                    
            except Exception as e:
                return {"error": str(e), "endpoint": endpoint['path']}
        
        return auto_handler
    
    async def handle_health(self):
        """Handle health check requests"""
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "system": "SphereOS Permanent",
            "auto_generated": True
        }
    
    async def handle_metrics(self, path: str):
        """Handle metrics requests"""
        metric_type = path.split('/')[-1]
        return {
            "metric_type": metric_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": sphereos_server.get_metrics(metric_type),
            "auto_generated": True
        }
    
    async def handle_sphere(self, path: str, params: Dict):
        """Handle sphere operation requests"""
        action = path.split('/')[3]
        identifier = params.get('identifier', 'default')
        
        if action == 'get':
            return await sphereos_server.get_sphere_data(identifier)
        elif action == 'store':
            return {"status": "store_operation", "identifier": identifier}
        else:
            return {"status": "sphere_operation", "action": action, "identifier": identifier}
    
    async def handle_value_leakage(self, path: str):
        """Handle value leakage detection requests"""
        action = path.split('/')[-1]
        
        # Initialize value leakage detector
        detector = ValueLeakageDetector()
        
        if action == 'scan':
            leakages = await detector.run_comprehensive_scan()
            return {"leakages": [asdict(l) for l in leakages], "count": len(leakages)}
        elif action == 'detect':
            return {"status": "detection_running", "message": "Value leakage detection initiated"}
        else:
            return {"status": "value_leakage", "action": action}
    
    async def handle_opportunities(self, path: str):
        """Handle opportunity discovery requests"""
        opp_type = path.split('/')[-1]
        
        detector = ValueLeakageDetector()
        matcher = OpportunityMatcher()
        
        # Get leakages for this opportunity type
        leakages = await detector.detect_leakages_by_type(opp_type)
        opportunities = await matcher.generate_opportunity_matches(leakages)
        
        return {
            "opportunity_type": opp_type,
            "opportunities": [asdict(op) for op in opportunities],
            "count": len(opportunities)
        }
    
    async def handle_commercial(self, path: str):
        """Handle commercial transaction requests"""
        action = path.split('/')[-1]
        
        detector = CommercialTransactionDetector()
        
        if action == 'opportunities':
            opportunities = await detector.detect_commercial_opportunities()
            return {"opportunities": [asdict(op) for op in opportunities]}
        else:
            return {"status": "commercial", "action": action}

# Initialize endpoint manager
endpoint_manager = EndpointManager()

# ============================================================================
# VALUE LEAKAGE DISCOVERY ENGINE
# ============================================================================

class TransactionType(Enum):
    SKILL_TRAINING = "skill_training"
    EQUIPMENT_PURCHASE = "equipment_purchase"
    SERVICE_CONTRACT = "service_contract"
    ASSET_TRANSFER = "asset_transfer"
    CONSULTATION = "consultation"
    PARTNERSHIP = "partnership"
    LICENSING = "licensing"

@dataclass
class ValueLeakage:
    id: str
    leakage_type: str
    severity_score: float
    opportunity_value: float
    affected_users: List[str]
    geographic_cluster: Dict
    temporal_pattern: Dict
    recommended_actions: List[str]
    confidence_score: float
    created_at: str

@dataclass
class OpportunityMatch:
    match_id: str
    match_type: str
    participants: List[str]
    value_potential: float
    geographic_proximity: float
    temporal_alignment: float
    skill_complementarity: float
    network_strength: float
    recommended_action: str

@dataclass
class CommercialOpportunity:
    opportunity_id: str
    transaction_type: TransactionType
    seller: Dict
    buyer: Dict
    funders: List[Dict]
    transaction_value: float
    confidence_score: float
    geographic_feasibility: float
    temporal_alignment: float
    risk_assessment: Dict
    recommended_structure: Dict
    created_at: str

class ValueLeakageDetector:
    """Core engine for detecting value leakages in SphereOS network"""
    
    def __init__(self):
        self.db_path = "sphereos_profiles.db"
        self.leakage_patterns = self.initialize_detection_patterns()
        self.opportunity_cache = {}
        
    def initialize_detection_patterns(self) -> Dict:
        """Initialize ML patterns for different types of value leakages"""
        return {
            'professional_skill_gaps': {
                'min_cluster_size': 3,
                'max_distance_km': 50,
                'skill_similarity_threshold': 0.7,
                'experience_gap_years': 5
            },
            'mentor_mentee_gaps': {
                'experience_differential': 10,
                'same_institution_bonus': 0.3,
                'geographic_proximity_km': 100,
                'pathway_similarity_threshold': 0.8
            },
            'collaboration_opportunities': {
                'complementary_skill_threshold': 0.4,
                'network_overlap_optimal': 0.2,
                'project_timeline_alignment': 0.6,
                'success_probability_threshold': 0.75
            },
            'market_inefficiencies': {
                'supply_demand_imbalance_threshold': 0.5,
                'price_variance_threshold': 0.3,
                'geographic_arbitrage_opportunity': 0.25,
                'network_density_threshold': 0.15
            }
        }

    async def run_comprehensive_scan(self) -> List[ValueLeakage]:
        """Run comprehensive value leakage detection across all categories"""
        
        print("🔍 Starting comprehensive value leakage scan...")
        
        all_leakages = []
        
        # Professional value leakages
        professional_leakages = await self.detect_professional_leakages()
        all_leakages.extend(professional_leakages)
        
        # Economic value leakages  
        economic_leakages = await self.detect_economic_leakages()
        all_leakages.extend(economic_leakages)
        
        # Social capital leakages
        social_leakages = await self.detect_social_capital_leakages()
        all_leakages.extend(social_leakages)
        
        # Knowledge value leakages
        knowledge_leakages = await self.detect_knowledge_leakages()
        all_leakages.extend(knowledge_leakages)
        
        # Geographic value leakages
        geographic_leakages = await self.detect_geographic_leakages()
        all_leakages.extend(geographic_leakages)
        
        # Sort by severity and opportunity value
        all_leakages.sort(key=lambda x: x.severity_score * x.opportunity_value, reverse=True)
        
        print(f"✅ Scan complete: Found {len(all_leakages)} value leakages")
        
        return all_leakages

    async def detect_professional_leakages(self) -> List[ValueLeakage]:
        """Detect professional skill gaps, mentorship opportunities, collaboration gaps"""
        
        leakages = []
        
        # Simulate detection for demo
        sample_leakage = ValueLeakage(
            id="skill_gap_001",
            leakage_type="professional_skill_gap",
            severity_score=0.85,
            opportunity_value=5000.0,
            affected_users=["user1", "user2", "user3"],
            geographic_cluster={"lat": 40.7128, "lng": -74.0060, "radius_km": 25},
            temporal_pattern={"skill": "data_analysis", "supply_count": 5, "demand_count": 12},
            recommended_actions=[
                "Create data analysis skill-sharing network",
                "Organize local data analysis meetups",
                "Establish data analysis mentorship program"
            ],
            confidence_score=0.85,
            created_at=datetime.utcnow().isoformat()
        )
        
        leakages.append(sample_leakage)
        return leakages

    async def detect_economic_leakages(self) -> List[ValueLeakage]:
        """Detect economic value leakages"""
        return []

    async def detect_social_capital_leakages(self) -> List[ValueLeakage]:
        """Detect social capital leakages"""
        return []

    async def detect_knowledge_leakages(self) -> List[ValueLeakage]:
        """Detect knowledge value leakages"""
        return []

    async def detect_geographic_leakages(self) -> List[ValueLeakage]:
        """Detect geographic value leakages"""
        return []

    async def detect_leakages_by_type(self, leakage_type: str) -> List[ValueLeakage]:
        """Detect leakages of a specific type"""
        if leakage_type == "professional":
            return await self.detect_professional_leakages()
        elif leakage_type == "economic":
            return await self.detect_economic_leakages()
        elif leakage_type == "social":
            return await self.detect_social_capital_leakages()
        elif leakage_type == "knowledge":
            return await self.detect_knowledge_leakages()
        elif leakage_type == "geographic":
            return await self.detect_geographic_leakages()
        else:
            return []

class OpportunityMatcher:
    """Matches detected value leakages to specific actionable opportunities"""
    
    def __init__(self):
        self.detector = ValueLeakageDetector()
    
    async def generate_opportunity_matches(self, leakages: List[ValueLeakage]) -> List[OpportunityMatch]:
        """Convert value leakages into specific matchmaking opportunities"""
        
        opportunities = []
        
        for leakage in leakages:
            if leakage.leakage_type == "professional_skill_gap":
                skill_opportunities = await self.create_skill_matching_opportunities(leakage)
                opportunities.extend(skill_opportunities)
        
        # Sort by value potential
        opportunities.sort(key=lambda x: x.value_potential, reverse=True)
        
        return opportunities
    
    async def create_skill_matching_opportunities(self, leakage: ValueLeakage) -> List[OpportunityMatch]:
        """Create specific skill-sharing opportunities from skill gap leakages"""
        
        opportunities = []
        
        # Create sample opportunities
        opportunity = OpportunityMatch(
            match_id=f"skill_match_{leakage.id}",
            match_type="skill_exchange",
            participants=leakage.affected_users[:2],
            value_potential=leakage.opportunity_value,
            geographic_proximity=0.8,
            temporal_alignment=0.8,
            skill_complementarity=0.7,
            network_strength=0.6,
            recommended_action=f"Connect users for {leakage.temporal_pattern.get('skill', 'skill')} collaboration"
        )
        
        opportunities.append(opportunity)
        return opportunities

class CommercialTransactionDetector:
    """Detects three-party commercial transaction opportunities"""
    
    def __init__(self):
        self.db_path = "sphereos_profiles.db"
    
    async def detect_commercial_opportunities(self) -> List[CommercialOpportunity]:
        """Main function to detect three-party commercial opportunities"""
        
        print("💰 Detecting commercial transaction opportunities...")
        
        # Create sample commercial opportunity
        opportunity = CommercialOpportunity(
            opportunity_id="comm_001",
            transaction_type=TransactionType.SKILL_TRAINING,
            seller={
                'user_npub': 'npub1seller...',
                'name': 'Alice Expert',
                'offering_type': 'data_analysis_training',
                'price_range': [2000, 4000]
            },
            buyer={
                'user_npub': 'npub1buyer...',
                'name': 'Bob Junior',
                'need_type': 'data_analysis_skills',
                'budget_range': [1500, 3500]
            },
            funders=[{
                'funder_npub': 'npub1funder...',
                'name': 'Tech Corp Training Budget',
                'amount_available': 5000,
                'funding_purpose': 'employee_skill_development'
            }],
            transaction_value=3000,
            confidence_score=0.85,
            geographic_feasibility=0.9,
            temporal_alignment=0.8,
            risk_assessment={'risk_level': 'low', 'mitigation': 'outcome_guarantee'},
            recommended_structure={
                'payment_method': 'corporate_reimbursement',
                'milestone_structure': ['initial_assessment', 'training_delivery', 'competency_verification']
            },
            created_at=datetime.utcnow().isoformat()
        )
        
        return [opportunity]

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class IdentityCreate(BaseModel):
    name: str
    username: str
    email: Optional[str] = None
    age_range: Optional[str] = None
    location: Optional[str] = None

class InstitutionCreate(BaseModel):
    coordinates_lat: float
    coordinates_lng: float
    coordinates_precision: str
    temporal_start: str
    temporal_end: str
    institution_type: str
    created_by: str

class DataStore(BaseModel):
    data: str
    reference_type: str
    reference_value: str
    compress: bool = True

# ============================================================================
# CORE API ENDPOINTS (PERMANENT)
# ============================================================================

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

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
            user_data = {
                'npub': user[0],
                'name': user[1],
                'bio': user[2],
                'location': user[3],
                'interests': user[4],
                'avatar_data': user[5]
            }
            session_token = session_manager.create_session(user_data)
            
            # Log activity
            cursor.execute(
                "INSERT INTO user_activity (user_npub, activity_type, activity_data) VALUES (?, ?, ?)",
                (login_data.npub, 'login', json.dumps({'timestamp': datetime.now().isoformat()}))
            )
            
            conn.commit()
            conn.close()
            
            return AuthResponse(
                success=True,
                session_token=session_token,
                user_data=user_data,
                message="Login successful"
            )
        else:
            conn.close()
            return AuthResponse(
                success=False,
                message="User not found. Please register first."
            )
            
    except Exception as e:
        return AuthResponse(
            success=False,
            message=f"Login failed: {str(e)}"
        )

@app.post("/api/auth/register")
async def register_user(register_data: RegisterRequest):
    """Register new user"""
    try:
        conn = sqlite3.connect('sphereos_social.db')
        cursor = conn.cursor()
        
        # Generate npub if not provided
        npub = f"npub1{secrets.token_hex(32)}"
        
        # Create user
        cursor.execute(
            "INSERT INTO users (npub, name, bio, location, interests, avatar_data) VALUES (?, ?, ?, ?, ?, ?)",
            (npub, register_data.name, register_data.bio, register_data.location, 
             register_data.interests, register_data.avatar_data)
        )
        
        # Create session
        user_data = {
            'npub': npub,
            'name': register_data.name,
            'bio': register_data.bio,
            'location': register_data.location,
            'interests': register_data.interests,
            'avatar_data': register_data.avatar_data
        }
        session_token = session_manager.create_session(user_data)
        
        # Log activity
        cursor.execute(
            "INSERT INTO user_activity (user_npub, activity_type, activity_data) VALUES (?, ?, ?)",
            (npub, 'register', json.dumps({'timestamp': datetime.now().isoformat()}))
        )
        
        conn.commit()
        conn.close()
        
        return AuthResponse(
            success=True,
            session_token=session_token,
            user_data=user_data,
            message="Registration successful"
        )
        
    except Exception as e:
        return AuthResponse(
            success=False,
            message=f"Registration failed: {str(e)}"
        )

@app.post("/api/auth/logout")
async def logout_user(session_token: str):
    """Logout user and invalidate session"""
    try:
        session_manager.invalidate_session(session_token)
        return {"success": True, "message": "Logout successful"}
    except Exception as e:
        return {"success": False, "message": f"Logout failed: {str(e)}"}

@app.get("/api/auth/session")
async def get_session_data(session_token: str):
    """Get current session data"""
    try:
        user_data = session_manager.get_session(session_token)
        if user_data:
            return {"success": True, "user_data": user_data}
        else:
            return {"success": False, "message": "Invalid or expired session"}
    except Exception as e:
        return {"success": False, "message": f"Session check failed: {str(e)}"}

# ============================================================================
# CORE API ENDPOINTS (PERMANENT)
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Main application page with traditional social media interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/health")
async def get_health():
    """System health status - PERMANENT ENDPOINT"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "system": "SphereOS Permanent",
        "version": "2.0.0",
        "features": [
            "Automatic Endpoint Management",
            "Value Leakage Discovery Engine",
            "3 Constituents Architecture",
            "Commercial Transaction Detection"
        ],
        "endpoints": {
            "total": len(endpoint_manager.endpoints),
            "auto_generated": len(endpoint_manager.auto_generated),
            "permanent": len(endpoint_manager.endpoints) - len(endpoint_manager.auto_generated)
        }
    }

@app.get("/api/metrics/{metric_type}")
async def get_metrics(metric_type: str):
    """System metrics - AUTO-GENERATED ENDPOINT"""
    return {
        "metric_type": metric_type,
        "timestamp": datetime.utcnow().isoformat(),
        "data": sphereos_server.get_metrics(metric_type),
        "auto_generated": True
    }

@app.get("/api/sphere/{action}/{identifier}")
async def sphere_operations(action: str, identifier: str):
    """Sphere operations - AUTO-GENERATED ENDPOINT"""
    if action == "get":
        return await sphereos_server.get_sphere_data(identifier)
    elif action == "store":
        return {"status": "store_operation", "identifier": identifier}
    else:
        return {"status": "sphere_operation", "action": action, "identifier": identifier}

@app.get("/api/value-leakage/{action}")
async def value_leakage_operations(action: str):
    """Value leakage detection - AUTO-GENERATED ENDPOINT"""
    detector = ValueLeakageDetector()
    
    if action == "scan":
        leakages = await detector.run_comprehensive_scan()
        return {"leakages": [asdict(l) for l in leakages], "count": len(leakages)}
    elif action == "detect":
        return {"status": "detection_running", "message": "Value leakage detection initiated"}
    else:
        return {"status": "value_leakage", "action": action}

@app.get("/api/opportunities/{opportunity_type}")
async def opportunity_discovery(opportunity_type: str):
    """Opportunity discovery - AUTO-GENERATED ENDPOINT"""
    detector = ValueLeakageDetector()
    matcher = OpportunityMatcher()
    
    leakages = await detector.detect_leakages_by_type(opportunity_type)
    opportunities = await matcher.generate_opportunity_matches(leakages)
    
    return {
        "opportunity_type": opportunity_type,
        "opportunities": [asdict(op) for op in opportunities],
        "count": len(opportunities)
    }

@app.get("/api/commercial/{action}")
async def commercial_operations(action: str):
    """Commercial transaction detection - AUTO-GENERATED ENDPOINT"""
    detector = CommercialTransactionDetector()
    
    if action == "opportunities":
        opportunities = await detector.detect_commercial_opportunities()
        return {"opportunities": [asdict(op) for op in opportunities]}
    else:
        return {"status": "commercial", "action": action}

# ============================================================================
# CALENDAR-GPS-POI INTEGRATION ENDPOINTS
# ============================================================================

# Initialize Calendar-GPS integrator
calendar_integrator = CalendarGPSIntegrator()

@app.post("/api/gps/location")
async def record_gps_location(
    user_id: str = Query(...),
    latitude: float = Query(...),
    longitude: float = Query(...),
    accuracy: float = Query(10.0),
    speed: Optional[float] = Query(None),
    heading: Optional[float] = Query(None)
):
    """Record GPS location and potentially create calendar event"""
    
    try:
        # Process location data
        calendar_event = calendar_integrator.process_location_data(
            user_id, latitude, longitude, accuracy
        )
        
        if calendar_event:
            return {
                "status": "success",
                "message": "Calendar event created",
                "event": asdict(calendar_event)
            }
        else:
            return {
                "status": "success",
                "message": "Location recorded, no calendar event created",
                "location_recorded": True
            }
            
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/poi/nearby")
async def get_nearby_pois(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius_meters: float = Query(100.0)
):
    """Get nearby Points of Interest"""
    
    try:
        gps_tracker = GPSLocationTracker()
        nearby_pois = gps_tracker.get_nearby_pois(latitude, longitude, radius_meters)
        
        return {
            "status": "success",
            "pois": [asdict(poi) for poi in nearby_pois],
            "count": len(nearby_pois)
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/poi/identify")
async def identify_poi(
    latitude: float = Query(...),
    longitude: float = Query(...)
):
    """Identify POI at specific coordinates"""
    
    try:
        poi_service = POIService()
        poi = poi_service.identify_poi(latitude, longitude)
        
        if poi:
            return {
                "status": "success",
                "poi": asdict(poi)
            }
        else:
            return {
                "status": "not_found",
                "message": "No POI found at these coordinates"
            }
            
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/timestamp/start")
async def start_timestamp_session(
    user_id: str = Query(...),
    location_id: str = Query(...)
):
    """Start a timestamp session at a location"""
    
    try:
        timestamp_tracker = TimeStampTracker()
        timestamp_data = timestamp_tracker.start_session(user_id, location_id)
        
        return {
            "status": "success",
            "message": "Session started",
            "session": asdict(timestamp_data)
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/timestamp/end")
async def end_timestamp_session(user_id: str = Query(...)):
    """End a timestamp session"""
    
    try:
        timestamp_tracker = TimeStampTracker()
        timestamp_data = timestamp_tracker.end_session(user_id)
        
        if timestamp_data:
            return {
                "status": "success",
                "message": "Session ended",
                "session": asdict(timestamp_data)
            }
        else:
            return {
                "status": "not_found",
                "message": "No active session found"
            }
            
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/calendar/events")
async def get_calendar_events(
    user_id: str = Query(...),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    """Get calendar events for a user"""
    
    try:
        events = calendar_integrator.get_user_events(user_id, start_date, end_date)
        
        return {
            "status": "success",
            "events": [asdict(event) for event in events],
            "count": len(events)
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/calendar/gps-integration")
async def gps_calendar_integration(
    user_id: str = Query(...),
    latitude: float = Query(...),
    longitude: float = Query(...),
    accuracy: float = Query(10.0)
):
    """Complete GPS-Calendar integration endpoint"""
    
    try:
        # This endpoint demonstrates the complete integration
        # 1. Record GPS location
        gps_tracker = GPSLocationTracker()
        gps_location = gps_tracker.record_gps_location(user_id, latitude, longitude, accuracy)
        
        # 2. Identify POI
        poi_service = POIService()
        poi = poi_service.identify_poi(latitude, longitude)
        
        # 3. Process timestamp
        timestamp_tracker = TimeStampTracker()
        
        if user_id not in timestamp_tracker.active_sessions:
            # Start new session
            timestamp_data = timestamp_tracker.start_session(user_id, poi.poi_id if poi else "unknown")
            return {
                "status": "session_started",
                "message": f"Started session at {poi.name if poi else 'unknown location'}",
                "gps": asdict(gps_location),
                "poi": asdict(poi) if poi else None,
                "session": asdict(timestamp_data)
            }
        else:
            # End current session and potentially create calendar event
            timestamp_data = timestamp_tracker.end_session(user_id)
            
            if timestamp_data and timestamp_data.duration_minutes >= 5 and poi:
                # Create calendar event
                calendar_event = calendar_integrator.create_calendar_event(
                    user_id, gps_location, poi, timestamp_data
                )
                
                return {
                    "status": "calendar_event_created",
                    "message": f"Created calendar event: {poi.name}",
                    "event": asdict(calendar_event)
                }
            else:
                return {
                    "status": "session_ended",
                    "message": "Session ended, no calendar event created",
                    "duration_minutes": timestamp_data.duration_minutes if timestamp_data else 0
                }
                
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ============================================================================
# UNIVERSAL VALUE DISCOVERY FRAMEWORK ENDPOINTS
# ============================================================================

# Initialize Universal Value Detector
universal_value_detector = UniversalValueDetector()

@app.get("/api/value-discovery/scan")
async def comprehensive_value_scan():
    """Perform comprehensive value discovery across all 12 foundational areas"""
    
    try:
        opportunities = await universal_value_detector.comprehensive_value_scan()
        
        return {
            "status": "success",
            "message": f"Value discovery complete: {len(opportunities)} opportunities found",
            "opportunities": [asdict(opp) for opp in opportunities],
            "total_count": len(opportunities),
            "areas_covered": [area.value for area in ValueArea]
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/value-discovery/area/{area_name}")
async def scan_specific_area(area_name: str):
    """Scan a specific value discovery area"""
    
    try:
        # Find the detector for this area
        area_detectors = {
            "commercial_exchange": CommercialExchangeDetector(),
            "knowledge_transfer": KnowledgeTransferDetector(),
            "resource_sharing": ResourceSharingDetector(),
            "network_bridging": NetworkBridgingDetector(),
            "temporal_coordination": TemporalCoordinationDetector(),
            "geographic_clustering": GeographicClusteringDetector(),
            "skill_development": SkillDevelopmentDetector(),
            "innovation_implementation": InnovationImplementationDetector(),
            "social_capital": SocialCapitalDetector(),
            "information_flow": InformationFlowDetector(),
            "collaborative_production": CollaborativeProductionDetector(),
            "systemic_efficiency": SystemicEfficiencyDetector()
        }
        
        if area_name not in area_detectors:
            return {
                "status": "error",
                "message": f"Unknown area: {area_name}",
                "available_areas": list(area_detectors.keys())
            }
        
        detector = area_detectors[area_name]
        opportunities = await detector.detect_value_leakages()
        
        return {
            "status": "success",
            "area": area_name,
            "opportunities": [asdict(opp) for opp in opportunities],
            "count": len(opportunities)
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/value-discovery/areas")
async def list_value_areas():
    """List all 12 foundational value discovery areas"""
    
    areas_info = {
        "commercial_exchange": {
            "name": "Commercial Exchange Triangulation",
            "pattern": "Seller ↔ Buyer ↔ Funder",
            "description": "Connect sellers, buyers, and funders for optimal transactions",
            "examples": ["Service providers", "Product sales", "Equipment purchases", "Licensing deals"]
        },
        "knowledge_transfer": {
            "name": "Knowledge Transfer Optimization",
            "pattern": "Expert ↔ Learner ↔ Facilitator",
            "description": "Optimize knowledge flow between experts and learners",
            "examples": ["Training programs", "Mentorship", "Academic instruction", "Professional development"]
        },
        "resource_sharing": {
            "name": "Resource Sharing Networks",
            "pattern": "Resource Owner ↔ Resource Needer ↔ Sharing Coordinator",
            "description": "Enable efficient sharing of underutilized resources",
            "examples": ["Equipment sharing", "Facility utilization", "Tool libraries", "Workspace sharing"]
        },
        "network_bridging": {
            "name": "Network Bridging Opportunities",
            "pattern": "Isolated Group A ↔ Isolated Group B ↔ Bridge Builder",
            "description": "Connect valuable but isolated groups",
            "examples": ["Industry collaboration", "Cross-cultural exchange", "Inter-departmental cooperation"]
        },
        "temporal_coordination": {
            "name": "Temporal Coordination Optimization",
            "pattern": "Early Actor ↔ Later Actor ↔ Timing Coordinator",
            "description": "Optimize timing and sequencing of activities",
            "examples": ["Supply chain coordination", "Event scheduling", "Project sequencing"]
        },
        "geographic_clustering": {
            "name": "Geographic Clustering Advantages",
            "pattern": "Local Resource ↔ Local Need ↔ Proximity Optimizer",
            "description": "Leverage geographic proximity for efficiency",
            "examples": ["Local sourcing", "Regional specialization", "Transportation optimization"]
        },
        "skill_development": {
            "name": "Skill Development Acceleration",
            "pattern": "Skill Developer ↔ Career Advancer ↔ Development Sponsor",
            "description": "Accelerate career advancement through skill development",
            "examples": ["Professional certification", "Career coaching", "Skill-based hiring"]
        },
        "innovation_implementation": {
            "name": "Innovation Implementation Bridging",
            "pattern": "Innovator ↔ Implementer ↔ Innovation Sponsor",
            "description": "Bridge the gap between innovation and implementation",
            "examples": ["Startup ecosystems", "R&D commercialization", "Creative project funding"]
        },
        "social_capital": {
            "name": "Social Capital Formation",
            "pattern": "Trust Builder ↔ Trust Beneficiary ↔ Trust Facilitator",
            "description": "Build trust networks and social capital",
            "examples": ["Professional networking", "Community building", "Institutional partnerships"]
        },
        "information_flow": {
            "name": "Information Flow Optimization",
            "pattern": "Information Holder ↔ Information Needer ↔ Information Broker",
            "description": "Optimize information flow and reduce asymmetries",
            "examples": ["Market intelligence", "Research sharing", "Data analytics", "Trend forecasting"]
        },
        "collaborative_production": {
            "name": "Collaborative Production Enhancement",
            "pattern": "Capability A ↔ Capability B ↔ Collaboration Coordinator",
            "description": "Enhance production through collaborative capabilities",
            "examples": ["Joint ventures", "Research collaboration", "Creative partnerships", "Team formation"]
        },
        "systemic_efficiency": {
            "name": "Systemic Efficiency Optimization",
            "pattern": "Process Owner ↔ Process User ↔ Process Optimizer",
            "description": "Optimize processes and systems for efficiency",
            "examples": ["Workflow optimization", "Resource allocation", "Quality improvement", "Automation"]
        }
    }
    
    return {
        "status": "success",
        "areas": areas_info,
        "total_areas": 12,
        "framework_description": "Universal Value Discovery Framework - 12 Foundational Areas for systematic value leakage detection"
    }

@app.get("/api/value-discovery/opportunities")
async def get_value_opportunities(
    area: Optional[str] = Query(None),
    min_value: Optional[float] = Query(None),
    max_risk: Optional[str] = Query(None)
):
    """Get value opportunities with optional filtering"""
    
    try:
        with sqlite3.connect(universal_value_detector.db_path) as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM value_opportunities WHERE 1=1"
            params = []
            
            if area:
                query += " AND area = ?"
                params.append(area)
            
            if min_value:
                query += " AND opportunity_value >= ?"
                params.append(min_value)
            
            if max_risk:
                query += " AND risk_level = ?"
                params.append(max_risk)
            
            query += " ORDER BY opportunity_value DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
        
        opportunities = []
        for row in rows:
            opportunity = ValueOpportunity(
                opportunity_id=row[0],
                area=ValueArea(row[1]),
                title=row[2],
                description=row[3],
                component_a=row[4],
                component_b=row[5],
                component_c=row[6],
                opportunity_value=row[7],
                feasibility_score=row[8],
                risk_level=row[9],
                time_sensitivity=row[10],
                network_effect_potential=row[11],
                sustainability_score=row[12],
                geographic_proximity=row[13],
                temporal_proximity=row[14],
                network_proximity=row[15],
                status=row[16],
                created_at=row[17]
            )
            opportunities.append(opportunity)
        
        return {
            "status": "success",
            "opportunities": [asdict(opp) for opp in opportunities],
            "count": len(opportunities),
            "filters_applied": {
                "area": area,
                "min_value": min_value,
                "max_risk": max_risk
            }
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/value-discovery/synergies")
async def get_cross_area_synergies():
    """Get cross-area synergy opportunities"""
    
    try:
        with sqlite3.connect(universal_value_detector.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM value_opportunities 
                WHERE status LIKE 'synergy%' OR status LIKE 'priority_%'
                ORDER BY opportunity_value DESC
            """)
            
            rows = cursor.fetchall()
        
        synergies = []
        for row in rows:
            opportunity = ValueOpportunity(
                opportunity_id=row[0],
                area=ValueArea(row[1]),
                title=row[2],
                description=row[3],
                component_a=row[4],
                component_b=row[5],
                component_c=row[6],
                opportunity_value=row[7],
                feasibility_score=row[8],
                risk_level=row[9],
                time_sensitivity=row[10],
                network_effect_potential=row[11],
                sustainability_score=row[12],
                geographic_proximity=row[13],
                temporal_proximity=row[14],
                network_proximity=row[15],
                status=row[16],
                created_at=row[17]
            )
            synergies.append(opportunity)
        
        return {
            "status": "success",
            "synergies": [asdict(syn) for syn in synergies],
            "count": len(synergies)
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ============================================================================
# FRONTEND DATA FEEDBACK ENDPOINTS
# ============================================================================

@app.post("/api/frontend/profile/update")
async def update_user_profile(profile_data: UserProfileUpdate):
    """Update user profile from frontend"""
    try:
        # Store profile data in sphere lattice
        profile_json = json.dumps({
            "npub": profile_data.npub,
            "name": profile_data.name,
            "bio": profile_data.bio,
            "location": profile_data.location,
            "interests": profile_data.interests,
            "avatar_data": profile_data.avatar_data,
            "updated_at": datetime.now().isoformat()
        })
        
        # Store in atlas constituent
        success = sphereos_server.store_data_unified(
            profile_json.encode('utf-8'),
            "atlas",
            f"/users/{profile_data.npub}/profile"
        )
        
        if success['success']:
            return {
                "success": True,
                "message": "Profile updated successfully",
                "profile": profile_data.dict()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to store profile data")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile update failed: {str(e)}")

@app.post("/api/frontend/friends/request")
async def send_friend_request(request_data: FriendRequest):
    """Send friend request from frontend"""
    try:
        # Store friend request in sphere lattice
        request_json = json.dumps({
            "from_npub": request_data.from_npub,
            "to_npub": request_data.to_npub,
            "message": request_data.message,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        })
        
        # Store in content constituent using hash
        request_hash = hashlib.sha256(request_json.encode('utf-8')).hexdigest()
        success = sphereos_server.store_data_unified(
            request_json.encode('utf-8'),
            "content",
            request_hash
        )
        
        if success['success']:
            return {
                "success": True,
                "message": "Friend request sent successfully",
                "request_id": request_hash
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to store friend request")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Friend request failed: {str(e)}")

@app.post("/api/frontend/friends/accept")
async def accept_friend_request(request_id: str, user_npub: str):
    """Accept friend request from frontend"""
    try:
        # Retrieve friend request
        request_data = sphereos_server.retrieve_data_unified("content", request_id)
        if not request_data:
            raise HTTPException(status_code=404, detail="Friend request not found")
        
        request_info = json.loads(request_data.decode('utf-8'))
        if request_info['to_npub'] != user_npub:
            raise HTTPException(status_code=403, detail="Not authorized to accept this request")
        
        # Update status to accepted
        request_info['status'] = 'accepted'
        request_info['accepted_at'] = datetime.now().isoformat()
        
        # Store updated request
        updated_json = json.dumps(request_info)
        success = sphereos_server.store_data_unified(
            updated_json.encode('utf-8'),
            "content",
            request_id
        )
        
        if success['success']:
            return {
                "success": True,
                "message": "Friend request accepted successfully",
                "friend_npub": request_info['from_npub']
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to update friend request")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Accept friend request failed: {str(e)}")

@app.post("/api/frontend/averments/submit")
async def submit_averment(averment_data: AvermentSubmission):
    """Submit averment from frontend"""
    try:
        # Store averment in sphere lattice
        averment_json = json.dumps({
            "verifier_npub": averment_data.verifier_npub,
            "verified_npub": averment_data.verified_npub,
            "institution_name": averment_data.institution_name,
            "role": averment_data.role,
            "time_period": averment_data.time_period,
            "location": averment_data.location,
            "confidence_score": averment_data.confidence_score,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        })
        
        # Store in coordinate constituent using location
        coords = averment_data.location.split(',') if ',' in averment_data.location else ['0', '0']
        lat, lng = float(coords[0]), float(coords[1])
        
        success = sphereos_server.store_data_unified(
            averment_json.encode('utf-8'),
            "coordinate",
            f"{lat},{lng},7"
        )
        
        if success['success']:
            return {
                "success": True,
                "message": "Averment submitted successfully",
                "averment": averment_data.dict()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to store averment")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Averment submission failed: {str(e)}")

@app.post("/api/frontend/institutions/join")
async def join_institution(join_data: InstitutionJoin):
    """Join institution from frontend"""
    try:
        # Store institution membership
        membership_json = json.dumps({
            "user_npub": join_data.user_npub,
            "institution_name": join_data.institution_name,
            "coordinates_lat": join_data.coordinates_lat,
            "coordinates_lng": join_data.coordinates_lng,
            "time_period": join_data.time_period,
            "joined_at": datetime.now().isoformat()
        })
        
        # Store in atlas constituent
        success = sphereos_server.store_data_unified(
            membership_json.encode('utf-8'),
            "atlas",
            f"/institutions/{join_data.institution_name}/members/{join_data.user_npub}"
        )
        
        if success['success']:
            return {
                "success": True,
                "message": f"Successfully joined {join_data.institution_name}",
                "membership": join_data.dict()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to join institution")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Join institution failed: {str(e)}")

@app.post("/api/frontend/groups/create")
async def create_group(group_data: GroupCreate):
    """Create group from frontend"""
    try:
        # Store group data
        group_json = json.dumps({
            "creator_npub": group_data.creator_npub,
            "group_name": group_data.group_name,
            "description": group_data.description,
            "group_type": group_data.group_type,
            "is_private": group_data.is_private,
            "members": [group_data.creator_npub],
            "created_at": datetime.now().isoformat()
        })
        
        # Store in atlas constituent
        success = sphereos_server.store_data_unified(
            group_json.encode('utf-8'),
            "atlas",
            f"/groups/{group_data.group_name}"
        )
        
        if success['success']:
            return {
                "success": True,
                "message": f"Group '{group_data.group_name}' created successfully",
                "group": group_data.dict()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to create group")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Create group failed: {str(e)}")

@app.post("/api/frontend/groups/join")
async def join_group(join_data: GroupJoin):
    """Join group from frontend"""
    try:
        # Retrieve group data
        group_data = sphereos_server.retrieve_data_unified(
            "atlas",
            f"/groups/{join_data.group_name}"
        )
        
        if not group_data:
            raise HTTPException(status_code=404, detail="Group not found")
        
        group_info = json.loads(group_data.decode('utf-8'))
        
        # Add user to group
        if join_data.user_npub not in group_info['members']:
            group_info['members'].append(join_data.user_npub)
        
        # Store updated group
        updated_json = json.dumps(group_info)
        success = sphereos_server.store_data_unified(
            updated_json.encode('utf-8'),
            "atlas",
            f"/groups/{join_data.group_name}"
        )
        
        if success['success']:
            return {
                "success": True,
                "message": f"Successfully joined group '{join_data.group_name}'",
                "group_name": join_data.group_name
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to join group")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Join group failed: {str(e)}")

@app.post("/api/frontend/search/query")
async def search_query(search_data: SearchQuery):
    """Process search query from frontend"""
    try:
        # Store search query for analytics
        query_json = json.dumps({
            "query": search_data.query,
            "filter_type": search_data.filter_type,
            "user_npub": search_data.user_npub,
            "timestamp": datetime.now().isoformat()
        })
        
        # Store in content constituent
        query_hash = hashlib.sha256(query_json.encode('utf-8')).hexdigest()
        sphereos_server.store_data_unified(
            query_json.encode('utf-8'),
            "content",
            query_hash
        )
        
        # Simulate search results based on query
        results = []
        if search_data.filter_type == "users":
            results = [
                {"name": "Alice Johnson", "npub": "npub1abc...", "bio": "Software Engineer", "type": "user"},
                {"name": "Bob Smith", "npub": "npub1def...", "bio": "Data Scientist", "type": "user"}
            ]
        elif search_data.filter_type == "institutions":
            results = [
                {"name": "Google", "location": "Mountain View, CA", "type": "institution"},
                {"name": "Stanford University", "location": "Stanford, CA", "type": "institution"}
            ]
        else:
            results = [
                {"name": "Alice Johnson", "npub": "npub1abc...", "bio": "Software Engineer", "type": "user"},
                {"name": "Google", "location": "Mountain View, CA", "type": "institution"}
            ]
        
        # Filter results based on query
        filtered_results = [
            result for result in results 
            if search_data.query.lower() in result['name'].lower() or 
               search_data.query.lower() in result.get('bio', '').lower()
        ]
        
        return {
            "success": True,
            "query": search_data.query,
            "results": filtered_results,
            "total_results": len(filtered_results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search query failed: {str(e)}")

@app.post("/api/frontend/activity/log")
async def log_user_activity(activity_data: UserActivity):
    """Log user activity from frontend"""
    try:
        # Store activity data
        activity_json = json.dumps({
            "user_npub": activity_data.user_npub,
            "activity_type": activity_data.activity_type,
            "activity_data": activity_data.activity_data,
            "timestamp": activity_data.timestamp or datetime.now().isoformat()
        })
        
        # Store in coordinate constituent using timestamp
        timestamp = datetime.now()
        success = sphereos_server.store_data_unified(
            activity_json.encode('utf-8'),
            "coordinate",
            f"{timestamp.hour},{timestamp.minute},8"
        )
        
        if success['success']:
            return {
                "success": True,
                "message": "Activity logged successfully",
                "activity_id": f"{activity_data.user_npub}_{timestamp.timestamp()}"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to log activity")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Activity logging failed: {str(e)}")

@app.get("/api/frontend/user/{npub}/profile")
async def get_user_profile(npub: str):
    """Get user profile for frontend"""
    try:
        # Retrieve profile from atlas constituent
        profile_data = sphereos_server.retrieve_data_unified(
            "atlas",
            f"/users/{npub}/profile"
        )
        
        if profile_data:
            profile = json.loads(profile_data.decode('utf-8'))
            return {
                "success": True,
                "profile": profile
            }
        else:
            # Return default profile
            return {
                "success": True,
                "profile": {
                    "npub": npub,
                    "name": f"User {npub[:8]}",
                    "bio": "New SphereOS user",
                    "location": "Unknown",
                    "interests": "Technology",
                    "avatar_data": None
                }
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get profile failed: {str(e)}")

@app.get("/api/frontend/user/{npub}/friends")
async def get_user_friends(npub: str):
    """Get user friends for frontend"""
    try:
        # Simulate friends data (in real implementation, this would query the database)
        friends = [
            {"name": "Alice Johnson", "npub": "npub1abc...", "status": "accepted"},
            {"name": "Bob Smith", "npub": "npub1def...", "status": "accepted"},
            {"name": "Carol Davis", "npub": "npub1ghi...", "status": "pending"}
        ]
        
        return {
            "success": True,
            "friends": friends,
            "total_friends": len(friends)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get friends failed: {str(e)}")

@app.get("/api/frontend/user/{npub}/averments")
async def get_user_averments(npub: str):
    """Get user averments for frontend"""
    try:
        # Simulate averments data
        averments = [
            {
                "verifier_npub": "npub1xyz...",
                "verified_npub": npub,
                "institution_name": "Google",
                "role": "Software Engineer",
                "time_period": "2020-2023",
                "location": "Mountain View, CA",
                "confidence_score": 1.0,
                "status": "verified"
            }
        ]
        
        return {
            "success": True,
            "averments": averments,
            "total_averments": len(averments)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get averments failed: {str(e)}")

@app.get("/api/frontend/user/{npub}/institutions")
async def get_user_institutions(npub: str):
    """Get user institutions for frontend"""
    try:
        # Simulate institutions data
        institutions = [
            {
                "institution_name": "Google",
                "coordinates_lat": 37.4220,
                "coordinates_lng": -122.0841,
                "time_period": "2020-2023",
                "joined_at": "2020-01-15T10:30:00Z"
            }
        ]
        
        return {
            "success": True,
            "institutions": institutions,
            "total_institutions": len(institutions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get institutions failed: {str(e)}")

@app.get("/api/frontend/user/{npub}/groups")
async def get_user_groups(npub: str):
    """Get user groups for frontend"""
    try:
        # Simulate groups data
        groups = [
            {
                "group_name": "Bay Area Tech",
                "description": "Tech professionals in Bay Area",
                "group_type": "professional",
                "is_private": False,
                "member_count": 45
            }
        ]
        
        return {
            "success": True,
            "groups": groups,
            "total_groups": len(groups)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get groups failed: {str(e)}")

@app.get("/api/frontend/analytics/user/{npub}")
async def get_user_analytics(npub: str):
    """Get user analytics for frontend"""
    try:
        # Simulate analytics data
        analytics = {
            "profile_views": 127,
            "friend_requests_sent": 15,
            "friend_requests_received": 8,
            "averments_submitted": 3,
            "averments_received": 12,
            "institutions_joined": 2,
            "groups_joined": 4,
            "search_queries": 23,
            "last_active": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "analytics": analytics
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get analytics failed: {str(e)}")

# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize the permanent system on startup"""
    print("🚀 Starting SphereOS Permanent System...")
    
    # Auto-generate any missing endpoints
    generated = endpoint_manager.auto_generate_missing_endpoints()
    print(f"✅ Auto-generated {len(generated)} endpoints")
    
    # Initialize value leakage detection
    print("💰 Initializing Value Leakage Discovery Engine...")
    
    print("✅ SphereOS Permanent System ready!")

# Initialize transaction cost analyzer
transaction_analyzer = TransactionCostAnalyzer()

# Initialize value streaming system
value_streaming = ValueStreamingSystem()

# Add new API endpoints for transaction cost analysis
@app.get("/api/transaction-cost/analyze")
async def analyze_transaction_cost(
    opportunity_id: str,
    distance_km: float = 0,
    participants: int = 2,
    complexity_score: float = 1.0,
    risk_factors: str = None
):
    """Analyze transaction costs and profitability for a value opportunity"""
    
    try:
        # Parse risk factors
        risk_dict = {}
        if risk_factors:
            risk_dict = json.loads(risk_factors)
        
        # Get opportunity from database
        with sqlite3.connect("sphereos_profiles.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT opportunity_id, area, title, opportunity_value, feasibility_score
                FROM value_opportunities WHERE opportunity_id = ?
            """, (opportunity_id,))
            
            result = cursor.fetchone()
            if not result:
                return {"error": "Opportunity not found"}
            
            opportunity = {
                'opportunity_id': result[0],
                'area': result[1],
                'title': result[2],
                'opportunity_value': result[3],
                'feasibility_score': result[4]
            }
        
        # Perform profitability analysis
        analysis = transaction_analyzer.analyze_profitability(
            opportunity, distance_km, participants, complexity_score, risk_dict
        )
        
        # Save analysis
        transaction_analyzer.save_analysis(analysis)
        
        return {
            "opportunity_id": analysis.opportunity_id,
            "gross_value": analysis.gross_value,
            "total_costs": analysis.total_costs,
            "net_value": analysis.net_value,
            "profitability_status": analysis.profitability_status.value,
            "cost_breakdown": analysis.cost_breakdown,
            "critical_factors": analysis.critical_factors,
            "recommendations": analysis.recommendations,
            "breakeven_distance": analysis.breakeven_distance,
            "breakeven_volume": analysis.breakeven_volume,
            "risk_adjusted_return": analysis.risk_adjusted_return
        }
        
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

@app.get("/api/transaction-cost/friction-impact")
async def analyze_friction_impact(
    opportunity_id: str,
    friction_types: str = None
):
    """Analyze impact of friction factors on profitability"""
    
    try:
        # Get opportunity
        with sqlite3.connect("sphereos_profiles.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT opportunity_id, opportunity_value FROM value_opportunities 
                WHERE opportunity_id = ?
            """, (opportunity_id,))
            
            result = cursor.fetchone()
            if not result:
                return {"error": "Opportunity not found"}
            
            opportunity = {
                'opportunity_id': result[0],
                'opportunity_value': result[1]
            }
        
        # Parse friction types
        friction_list = []
        if friction_types:
            friction_list = json.loads(friction_types)
        else:
            friction_list = ['distance_barrier', 'time_zone_difference', 'language_barrier']
        
        # Analyze friction impact
        impact_analysis = transaction_analyzer.analyze_friction_impact(opportunity, friction_list)
        
        return {
            "opportunity_id": opportunity_id,
            "friction_impact": impact_analysis
        }
        
    except Exception as e:
        return {"error": f"Friction analysis failed: {str(e)}"}

@app.get("/api/transaction-cost/breakeven-analysis")
async def breakeven_analysis(
    opportunity_id: str,
    cost_scenarios: str = None
):
    """Analyze breakeven points for different cost scenarios"""
    
    try:
        # Get opportunity
        with sqlite3.connect("sphereos_profiles.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT opportunity_id, opportunity_value FROM value_opportunities 
                WHERE opportunity_id = ?
            """, (opportunity_id,))
            
            result = cursor.fetchone()
            if not result:
                return {"error": "Opportunity not found"}
            
            opportunity = {
                'opportunity_id': result[0],
                'opportunity_value': result[1]
            }
        
        # Parse scenarios
        scenarios = []
        if cost_scenarios:
            scenarios = json.loads(cost_scenarios)
        else:
            # Default scenarios
            scenarios = [
                {"distance_km": 50, "participants": 2, "complexity_score": 1.0},
                {"distance_km": 100, "participants": 3, "complexity_score": 1.5},
                {"distance_km": 200, "participants": 4, "complexity_score": 2.0},
                {"distance_km": 500, "participants": 5, "complexity_score": 2.5}
            ]
        
        breakeven_results = []
        
        for scenario in scenarios:
            analysis = transaction_analyzer.analyze_profitability(opportunity, **scenario)
            
            breakeven_results.append({
                "scenario": scenario,
                "gross_value": analysis.gross_value,
                "total_costs": analysis.total_costs,
                "net_value": analysis.net_value,
                "profitability_status": analysis.profitability_status.value,
                "breakeven_distance": analysis.breakeven_distance,
                "breakeven_volume": analysis.breakeven_volume
            })
        
        return {
            "opportunity_id": opportunity_id,
            "breakeven_analysis": breakeven_results
        }
        
    except Exception as e:
        return {"error": f"Breakeven analysis failed: {str(e)}"}

@app.get("/api/transaction-cost/history/{opportunity_id}")
async def get_analysis_history(opportunity_id: str):
    """Get analysis history for an opportunity"""
    
    try:
        analyses = transaction_analyzer.get_analysis_history(opportunity_id)
        
        return {
            "opportunity_id": opportunity_id,
            "analysis_history": [
                {
                    "created_at": analysis.created_at,
                    "gross_value": analysis.gross_value,
                    "total_costs": analysis.total_costs,
                    "net_value": analysis.net_value,
                    "profitability_status": analysis.profitability_status.value,
                    "risk_adjusted_return": analysis.risk_adjusted_return
                }
                for analysis in analyses
            ]
        }
        
    except Exception as e:
        return {"error": f"Failed to retrieve history: {str(e)}"}

@app.get("/api/transaction-cost/unprofitable-opportunities")
async def find_unprofitable_opportunities(
    min_distance_km: float = 100,
    max_participants: int = 10
):
    """Find opportunities that become unprofitable due to transaction costs"""
    
    try:
        with sqlite3.connect("sphereos_profiles.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT opportunity_id, area, title, opportunity_value, feasibility_score
                FROM value_opportunities 
                WHERE opportunity_value > 0
                ORDER BY opportunity_value DESC
                LIMIT 20
            """)
            
            opportunities = cursor.fetchall()
        
        unprofitable_opportunities = []
        
        for opp in opportunities:
            opportunity = {
                'opportunity_id': opp[0],
                'area': opp[1],
                'title': opp[2],
                'opportunity_value': opp[3],
                'feasibility_score': opp[4]
            }
            
            # Test with high distance and participants
            analysis = transaction_analyzer.analyze_profitability(
                opportunity, 
                distance_km=min_distance_km,
                participants=max_participants,
                complexity_score=2.0
            )
            
            if analysis.profitability_status in [ProfitabilityStatus.UNPROFITABLE, ProfitabilityStatus.MARGINAL]:
                unprofitable_opportunities.append({
                    "opportunity_id": opportunity['opportunity_id'],
                    "title": opportunity['title'],
                    "area": opportunity['area'],
                    "gross_value": analysis.gross_value,
                    "total_costs": analysis.total_costs,
                    "net_value": analysis.net_value,
                    "profitability_status": analysis.profitability_status.value,
                    "critical_factors": analysis.critical_factors,
                    "recommendations": analysis.recommendations[:2]  # Top 2 recommendations
                })
        
        return {
            "unprofitable_opportunities": unprofitable_opportunities,
            "total_found": len(unprofitable_opportunities),
            "analysis_criteria": {
                "min_distance_km": min_distance_km,
                "max_participants": max_participants
            }
        }
        
    except Exception as e:
        return {"error": f"Failed to find unprofitable opportunities: {str(e)}"}

# Add new API endpoints for value streaming
@app.get("/api/value-streaming/feeds")
async def get_value_feeds():
    """Get available value streaming feeds"""
    
    try:
        return {
            "feeds": value_streaming.value_feeds,
            "total_feeds": len(value_streaming.value_feeds),
            "categories": [category.value for category in ValueCategory]
        }
    except Exception as e:
        return {"error": f"Failed to get feeds: {str(e)}"}

@app.post("/api/value-streaming/fetch-content")
async def fetch_value_content():
    """Fetch and process value content from RSS feeds"""
    
    try:
        content = await value_streaming.fetch_and_process_feeds()
        
        return {
            "success": True,
            "content_fetched": len(content),
            "content_summary": [
                {
                    "content_id": item.content_id,
                    "title": item.title,
                    "content_type": item.content_type.value,
                    "value_category": item.value_category.value,
                    "value_score": item.value_score,
                    "target_audience": item.target_audience
                }
                for item in content[:10]  # Show first 10 items
            ]
        }
    except Exception as e:
        return {"error": f"Failed to fetch content: {str(e)}"}

@app.post("/api/value-streaming/user-profile")
async def create_user_value_profile(profile_data: Dict):
    """Create or update user value profile for content matching"""
    
    try:
        with sqlite3.connect("sphereos_profiles.db") as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO user_value_profiles 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                profile_data.get('user_npub'),
                json.dumps(profile_data.get('interests', [])),
                json.dumps(profile_data.get('skills', [])),
                json.dumps(profile_data.get('goals', [])),
                profile_data.get('location'),
                profile_data.get('industry'),
                json.dumps(profile_data.get('value_preferences', {})),
                json.dumps(profile_data.get('content_history', [])),
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            
            conn.commit()
        
        return {
            "success": True,
            "message": "User value profile created/updated successfully",
            "user_npub": profile_data.get('user_npub')
        }
    except Exception as e:
        return {"error": f"Failed to create profile: {str(e)}"}

@app.get("/api/value-streaming/matches/{user_npub}")
async def get_user_value_matches(user_npub: str, limit: int = 20):
    """Get value content matches for a specific user"""
    
    try:
        # First, generate matches if they don't exist
        matches = await value_streaming.match_content_to_users()
        
        # Get matches for specific user
        with sqlite3.connect("sphereos_profiles.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT vm.*, vc.title, vc.description, vc.source_url, vc.published_date
                FROM value_matches vm
                JOIN value_content vc ON vm.content_id = vc.content_id
                WHERE vm.user_npub = ?
                ORDER BY vm.match_score DESC, vm.created_at DESC
                LIMIT ?
            """, (user_npub, limit))
            
            user_matches = cursor.fetchall()
        
        return {
            "user_npub": user_npub,
            "matches": [
                {
                    "content_id": match[2],
                    "match_score": match[3],
                    "value_category": match[4],
                    "relevance_reason": match[5],
                    "action_recommendation": match[6],
                    "title": match[8],
                    "description": match[9],
                    "source_url": match[10],
                    "published_date": match[11]
                }
                for match in user_matches
            ],
            "total_matches": len(user_matches)
        }
    except Exception as e:
        return {"error": f"Failed to get matches: {str(e)}"}

@app.get("/api/value-streaming/content")
async def get_value_content(
    content_type: Optional[str] = None,
    value_category: Optional[str] = None,
    min_value_score: float = 0.0,
    limit: int = 50
):
    """Get value content with filtering options"""
    
    try:
        with sqlite3.connect("sphereos_profiles.db") as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT * FROM value_content 
                WHERE value_score >= ?
            """
            params = [min_value_score]
            
            if content_type:
                query += " AND content_type = ?"
                params.append(content_type)
            
            if value_category:
                query += " AND value_category = ?"
                params.append(value_category)
            
            query += " ORDER BY value_score DESC, created_at DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            content_items = cursor.fetchall()
        
        return {
            "content": [
                {
                    "content_id": item[0],
                    "content_type": item[1],
                    "value_category": item[2],
                    "title": item[3],
                    "description": item[4],
                    "source_url": item[5],
                    "value_score": item[8],
                    "target_audience": json.loads(item[9]) if item[9] else [],
                    "value_impact": item[10],
                    "tags": json.loads(item[11]) if item[11] else [],
                    "published_date": item[7]
                }
                for item in content_items
            ],
            "total_items": len(content_items),
            "filters_applied": {
                "content_type": content_type,
                "value_category": value_category,
                "min_value_score": min_value_score
            }
        }
    except Exception as e:
        return {"error": f"Failed to get content: {str(e)}"}

@app.get("/u/{user_npub}/value-feed.xml")
async def get_user_value_rss_feed(user_npub: str):
    """Get personalized value RSS feed for user"""
    
    try:
        rss_content = await value_streaming.generate_user_rss_feed(user_npub)
        
        return Response(
            content=rss_content,
            media_type="application/xml",
            headers={
                "Content-Disposition": f"attachment; filename=value-feed-{user_npub}.xml"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate RSS feed: {str(e)}")

@app.post("/api/value-streaming/subscribe-feed")
async def subscribe_to_value_feed(subscription_data: Dict):
    """Subscribe to a new value RSS feed"""
    
    try:
        with sqlite3.connect("sphereos_profiles.db") as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO rss_feed_subscriptions 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                subscription_data.get('feed_id'),
                subscription_data.get('feed_url'),
                subscription_data.get('feed_name'),
                subscription_data.get('content_type'),
                subscription_data.get('value_category'),
                True,  # is_active
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            
            conn.commit()
        
        return {
            "success": True,
            "message": "Feed subscription created successfully",
            "feed_id": subscription_data.get('feed_id')
        }
    except Exception as e:
        return {"error": f"Failed to subscribe to feed: {str(e)}"}

@app.get("/api/value-streaming/subscriptions")
async def get_feed_subscriptions():
    """Get all RSS feed subscriptions"""
    
    try:
        with sqlite3.connect("sphereos_profiles.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM rss_feed_subscriptions 
                WHERE is_active = 1
                ORDER BY created_at DESC
            """)
            
            subscriptions = cursor.fetchall()
        
        return {
            "subscriptions": [
                {
                    "feed_id": sub[0],
                    "feed_url": sub[1],
                    "feed_name": sub[2],
                    "content_type": sub[3],
                    "value_category": sub[4],
                    "last_fetch": sub[6]
                }
                for sub in subscriptions
            ],
            "total_subscriptions": len(subscriptions)
        }
    except Exception as e:
        return {"error": f"Failed to get subscriptions: {str(e)}"}

@app.get("/api/value-streaming/analytics")
async def get_value_streaming_analytics():
    """Get analytics for value streaming system"""
    
    try:
        with sqlite3.connect("sphereos_profiles.db") as conn:
            cursor = conn.cursor()
            
            # Content statistics
            cursor.execute("SELECT COUNT(*) FROM value_content")
            total_content = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(value_score) FROM value_content")
            avg_value_score = cursor.fetchone()[0] or 0
            
            # User profile statistics
            cursor.execute("SELECT COUNT(*) FROM user_value_profiles")
            total_users = cursor.fetchone()[0]
            
            # Match statistics
            cursor.execute("SELECT COUNT(*) FROM value_matches")
            total_matches = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(match_score) FROM value_matches")
            avg_match_score = cursor.fetchone()[0] or 0
            
            # Content type distribution
            cursor.execute("""
                SELECT content_type, COUNT(*) 
                FROM value_content 
                GROUP BY content_type
            """)
            content_type_distribution = dict(cursor.fetchall())
            
            # Value category distribution
            cursor.execute("""
                SELECT value_category, COUNT(*) 
                FROM value_content 
                GROUP BY value_category
            """)
            value_category_distribution = dict(cursor.fetchall())
        
        return {
            "content_analytics": {
                "total_content": total_content,
                "average_value_score": round(avg_value_score, 3),
                "content_type_distribution": content_type_distribution,
                "value_category_distribution": value_category_distribution
            },
            "user_analytics": {
                "total_users_with_profiles": total_users,
                "total_matches_generated": total_matches,
                "average_match_score": round(avg_match_score, 3)
            },
            "system_health": {
                "feeds_configured": len(value_streaming.value_feeds),
                "content_processors": len(value_streaming.content_processors),
                "last_updated": datetime.now().isoformat()
            }
        }
    except Exception as e:
        return {"error": f"Failed to get analytics: {str(e)}"}

if __name__ == "__main__":
    print("🌌 SphereOS Permanent System - Starting...")
    print("🔧 Automatic Endpoint Management: ENABLED")
    print("💰 Value Leakage Discovery Engine: ENABLED")
    print("🚀 Commercial Transaction Detection: ENABLED")
    
    uvicorn.run(app, host="127.0.0.1", port=8765, log_level="info") 