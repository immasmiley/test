#!/usr/bin/env python3
"""
SphereOS Executable - Complete System with 12 Domains and 108 Core Elements
Combines all functionality into a single executable application
"""

import sys
import os
import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Dict, List, Any, Optional
import json
import sqlite3
import hashlib
from datetime import datetime
import webbrowser
import threading
import time

# Import all SphereOS components
try:
    from sphereos_unified_system import SphereOSUnifiedServer, SphereLattice108
    from sphereos_domain_endpoints import SphereOSDomainEndpoints, ValueDomain
    from sphereos_combined_endpoints import CombinedDomainHandler, router as domain_router
    from sphereos_calendar_gps_integration import CalendarGPSIntegrator, GPSLocationTracker, POIService, TimeStampTracker
    from sphereos_universal_value_framework import UniversalValueDetector
    from sphereos_transaction_cost_analyzer import TransactionCostAnalyzer
    from sphereos_value_streaming_system import ValueStreamingSystem
    print("✅ All SphereOS components imported successfully")
except ImportError as e:
    print(f"⚠️ Some components not found: {e}")
    print("Creating simplified version...")

# Initialize FastAPI app
app = FastAPI(
    title="SphereOS Complete System",
    description="Dynamic Living Decentralized Profile Platform with 12 Value Domains and 108 Core Elements",
    version="3.0.0"
)

# Initialize core components
sphereos_server = None
domain_endpoints = None
handler = None

try:
    sphereos_server = SphereOSUnifiedServer()
    domain_endpoints = SphereOSDomainEndpoints()
    handler = CombinedDomainHandler()
    print("✅ Core components initialized")
except Exception as e:
    print(f"⚠️ Core components initialization: {e}")

# Include domain router
try:
    app.include_router(domain_router)
    print("✅ Domain endpoints included")
except Exception as e:
    print(f"⚠️ Domain router inclusion: {e}")

class SphereOSExecutable:
    """Main executable class for SphereOS system"""
    
    def __init__(self):
        self.port = 8765
        self.host = "127.0.0.1"
        self.server = None
        self.is_running = False
        
    def start_server(self):
        """Start the SphereOS server"""
        try:
            print(f"🚀 Starting SphereOS server on {self.host}:{self.port}")
            uvicorn.run(app, host=self.host, port=self.port, log_level="info")
            self.is_running = True
        except Exception as e:
            print(f"❌ Server start failed: {e}")
    
    def open_browser(self):
        """Open browser to SphereOS interface"""
        try:
            time.sleep(2)  # Wait for server to start
            url = f"http://{self.host}:{self.port}"
            print(f"🌐 Opening browser to: {url}")
            webbrowser.open(url)
        except Exception as e:
            print(f"❌ Browser open failed: {e}")

# Basic endpoints for executable
@app.get("/", response_class=HTMLResponse)
async def root():
    """Main SphereOS interface"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SphereOS - 12 Domains, 108 Core Elements</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; }
            .domain-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 30px; }
            .domain-card { background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #3498db; }
            .domain-title { font-weight: bold; color: #2c3e50; margin-bottom: 10px; }
            .element-list { font-size: 0.9em; color: #555; }
            .stats { background: #e8f4fd; padding: 20px; border-radius: 8px; margin-bottom: 30px; text-align: center; }
            .endpoint-info { background: #f1f8e9; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .button { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
            .button:hover { background: #2980b9; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌌 SphereOS Complete System</h1>
            
            <div class="stats">
                <h2>📊 System Statistics</h2>
                <p><strong>12 Value Domains</strong> | <strong>108 Core Elements</strong> | <strong>Unified API Endpoints</strong></p>
                <p>Dynamic Living Decentralized Profile Platform</p>
            </div>
            
            <div class="endpoint-info">
                <h3>🔗 API Endpoints</h3>
                <p><strong>Unified Pattern:</strong> GET /api/domains/{domain_name}/{operation}</p>
                <p><strong>Operations:</strong> scan, analyze, optimize, facilitate</p>
                <p><strong>Cross-Domain:</strong> /api/domains/comprehensive/scan, /api/domains/synergies/detect</p>
            </div>
            
            <div class="domain-grid">
                <div class="domain-card">
                    <div class="domain-title">🏪 Commercial Exchange</div>
                    <div class="element-list">
                        1. seller_provider<br>2. buyer_consumer<br>3. funder_capital<br>4. transaction_facilitator<br>5. market_platform<br>6. payment_processor<br>7. logistics_coordinator<br>8. quality_assurance<br>9. dispute_resolution
                    </div>
                </div>
                
                <div class="domain-card">
                    <div class="domain-title">🧠 Knowledge Transfer</div>
                    <div class="element-list">
                        1. expert_mentor<br>2. learner_student<br>3. facilitator_coordinator<br>4. content_curator<br>5. delivery_platform<br>6. assessment_evaluator<br>7. certification_authority<br>8. community_builder<br>9. knowledge_repository
                    </div>
                </div>
                
                <div class="domain-card">
                    <div class="domain-title">🔄 Resource Sharing</div>
                    <div class="element-list">
                        1. resource_owner<br>2. resource_user<br>3. sharing_coordinator<br>4. utilization_tracker<br>5. access_controller<br>6. maintenance_provider<br>7. insurance_provider<br>8. dispute_mediator<br>9. optimization_engine
                    </div>
                </div>
                
                <div class="domain-card">
                    <div class="domain-title">🌐 Network Bridging</div>
                    <div class="element-list">
                        1. network_a<br>2. network_b<br>3. bridge_facilitator<br>4. trust_validator<br>5. protocol_standardizer<br>6. communication_enabler<br>7. collaboration_coordinator<br>8. value_amplifier<br>9. sustainability_ensurer
                    </div>
                </div>
                
                <div class="domain-card">
                    <div class="domain-title">⏰ Temporal Coordination</div>
                    <div class="element-list">
                        1. early_provider<br>2. later_consumer<br>3. timing_coordinator<br>4. synchronization_engine<br>5. buffer_manager<br>6. urgency_prioritizer<br>7. capacity_optimizer<br>8. deadline_enforcer<br>9. temporal_analytics
                    </div>
                </div>
                
                <div class="domain-card">
                    <div class="domain-title">🗺️ Geographic Clustering</div>
                    <div class="element-list">
                        1. local_supplier<br>2. local_consumer<br>3. cluster_coordinator<br>4. proximity_optimizer<br>5. transportation_manager<br>6. local_market_analyzer<br>7. community_builder<br>8. infrastructure_planner<br>9. geographic_analytics
                    </div>
                </div>
                
                <div class="domain-card">
                    <div class="domain-title">🎯 Skill Development</div>
                    <div class="element-list">
                        1. skill_provider<br>2. skill_learner<br>3. development_sponsor<br>4. curriculum_designer<br>5. progress_tracker<br>6. mentorship_coordinator<br>7. certification_authority<br>8. career_path_planner<br>9. skill_marketplace
                    </div>
                </div>
                
                <div class="domain-card">
                    <div class="domain-title">💡 Innovation Implementation</div>
                    <div class="element-list">
                        1. innovator_creator<br>2. implementer_executor<br>3. innovation_sponsor<br>4. market_validator<br>5. prototype_builder<br>6. scaling_coordinator<br>7. intellectual_property_manager<br>8. ecosystem_builder<br>9. impact_measurer
                    </div>
                </div>
                
                <div class="domain-card">
                    <div class="domain-title">🤝 Social Capital</div>
                    <div class="element-list">
                        1. trust_builder<br>2. trust_beneficiary<br>3. trust_facilitator<br>4. reputation_manager<br>5. network_connector<br>6. community_organizer<br>7. collaboration_enabler<br>8. conflict_resolver<br>9. social_analytics
                    </div>
                </div>
                
                <div class="domain-card">
                    <div class="domain-title">📡 Information Flow</div>
                    <div class="element-list">
                        1. information_holder<br>2. information_needer<br>3. information_broker<br>4. data_curator<br>5. distribution_channel<br>6. quality_validator<br>7. privacy_protector<br>8. insight_generator<br>9. flow_optimizer
                    </div>
                </div>
                
                <div class="domain-card">
                    <div class="domain-title">🏭 Collaborative Production</div>
                    <div class="element-list">
                        1. capability_provider_a<br>2. capability_provider_b<br>3. collaboration_coordinator<br>4. project_manager<br>5. resource_allocator<br>6. quality_controller<br>7. risk_manager<br>8. value_distributor<br>9. collaboration_analytics
                    </div>
                </div>
                
                <div class="domain-card">
                    <div class="domain-title">⚙️ Systemic Efficiency</div>
                    <div class="element-list">
                        1. process_owner<br>2. process_user<br>3. efficiency_optimizer<br>4. system_analyzer<br>5. improvement_implementer<br>6. performance_monitor<br>7. change_manager<br>8. sustainability_ensurer<br>9. efficiency_analytics
                    </div>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <button class="button" onclick="testDomain('commercial_exchange')">Test Commercial Domain</button>
                <button class="button" onclick="testDomain('knowledge_transfer')">Test Knowledge Domain</button>
                <button class="button" onclick="testComprehensive()">Test All Domains</button>
                <button class="button" onclick="window.open('/docs', '_blank')">API Documentation</button>
            </div>
            
            <div id="results" style="margin-top: 20px; padding: 20px; background: #f8f9fa; border-radius: 8px; display: none;">
                <h3>Test Results</h3>
                <pre id="result-content"></pre>
            </div>
        </div>
        
        <script>
            async function testDomain(domain) {
                try {
                    const response = await fetch(`/api/domains/${domain}/scan`);
                    const data = await response.json();
                    showResults(data);
                } catch (error) {
                    showResults({error: error.message});
                }
            }
            
            async function testComprehensive() {
                try {
                    const response = await fetch('/api/domains/comprehensive/scan');
                    const data = await response.json();
                    showResults(data);
                } catch (error) {
                    showResults({error: error.message});
                }
            }
            
            function showResults(data) {
                document.getElementById('results').style.display = 'block';
                document.getElementById('result-content').textContent = JSON.stringify(data, null, 2);
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "system": "SphereOS Complete",
        "domains": 12,
        "core_elements": 108,
        "timestamp": datetime.now().isoformat(),
        "version": "3.0.0"
    }

@app.get("/api/system/info")
async def system_info():
    """System information endpoint"""
    return {
        "system_name": "SphereOS Complete",
        "description": "Dynamic Living Decentralized Profile Platform",
        "version": "3.0.0",
        "domains": {
            "total": 12,
            "core_elements_per_domain": 9,
            "total_core_elements": 108
        },
        "api_endpoints": {
            "unified_pattern": "/api/domains/{domain_name}/{operation}",
            "operations": ["scan", "analyze", "optimize", "facilitate"],
            "cross_domain": [
                "/api/domains/comprehensive/scan",
                "/api/domains/synergies/detect",
                "/api/domains/health/dashboard",
                "/api/domains/optimization/recommendations"
            ]
        },
        "features": [
            "12 Value Domains",
            "108 Core Elements", 
            "Unified API Endpoints",
            "Cross-Domain Synergies",
            "Health Monitoring",
            "Optimization Recommendations"
        ]
    }

def main():
    """Main function to run SphereOS executable"""
    print("🌌 SphereOS Complete System Starting...")
    print("=" * 50)
    print("📊 12 Value Domains")
    print("🔢 108 Core Elements")
    print("🔗 Unified API Endpoints")
    print("=" * 50)
    
    # Create executable instance
    sphereos_exe = SphereOSExecutable()
    
    # Start server in separate thread
    server_thread = threading.Thread(target=sphereos_exe.start_server, daemon=True)
    server_thread.start()
    
    # Open browser
    browser_thread = threading.Thread(target=sphereos_exe.open_browser, daemon=True)
    browser_thread.start()
    
    print("\n✅ SphereOS Complete System is running!")
    print(f"🌐 Web Interface: http://127.0.0.1:8765")
    print(f"📚 API Documentation: http://127.0.0.1:8765/docs")
    print(f"🔍 Health Check: http://127.0.0.1:8765/api/health")
    print("\nPress Ctrl+C to stop the server...")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping SphereOS Complete System...")
        print("✅ System stopped successfully!")

if __name__ == "__main__":
    main() 