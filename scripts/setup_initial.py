#!/usr/bin/env python3
"""
Startup script untuk setup initial configuration
"""
import sys
import os
import requests
import json
import time
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal
from app.models.area import Area


def wait_for_api(host="localhost", port=8000, timeout=60):
    """Wait for API to be ready"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"http://{host}:{port}/docs")
            if response.status_code == 200:
                print(f"✅ API is ready at http://{host}:{port}")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(2)
    return False


def setup_initial_areas():
    """Setup initial area configurations"""
    session = SessionLocal()
    
    # Default area untuk pedestrian crossing
    default_areas = [
        {
            "area_id": "4aeb238c-be39-4c1b-8c9f-828669dddf62",
            "name": "Main Pedestrian Crossing",
            "polygon": [[300, 400], [900, 400], [1000, 720], [200, 720]]
        },
        {
            "area_id": "b5c6d7e8-f9a0-1b2c-3d4e-567890abcdef",
            "name": "Secondary Crossing Area",
            "polygon": [[100, 300], [600, 300], [700, 600], [50, 600]]
        }
    ]
    
    for area_config in default_areas:
        area = session.query(Area).filter_by(id=area_config["area_id"]).first()
        
        if not area:
            area = Area(
                id=area_config["area_id"],
                name=area_config["name"],
                coordinates=area_config["polygon"],  # Legacy field
                polygon=area_config["polygon"]       # New field
            )
            session.add(area)
            print(f"✅ Created area: {area_config['name']} ({area_config['area_id']})")
        else:
            area.polygon = area_config["polygon"]
            area.name = area_config["name"]
            print(f"✅ Updated area: {area_config['name']} ({area_config['area_id']})")
    
    session.commit()
    session.close()
    print("✅ Initial areas setup completed")


def setup_via_api(host="localhost", port=8000):
    """Setup areas via API endpoint"""
    base_url = f"http://{host}:{port}"
    
    default_areas = [
        {
            "area_id": "4aeb238c-be39-4c1b-8c9f-828669dddf62",
            "name": "Main Pedestrian Crossing",
            "polygon": [[300, 400], [900, 400], [1000, 720], [200, 720]]
        }
    ]
    
    for area_config in default_areas:
        try:
            response = requests.post(
                f"{base_url}/api/config/area",
                json=area_config,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                print(f"✅ Area configured via API: {area_config['name']}")
            else:
                print(f"❌ Failed to configure area via API: {response.text}")
        except Exception as e:
            print(f"❌ Error configuring area via API: {e}")


def main():
    """Main setup function"""
    mode = os.getenv("SETUP_MODE", "direct")  # direct or api
    
    print("🚀 Starting people-tracking setup...")
    
    if mode == "api":
        # Wait for API and setup via endpoints
        if wait_for_api():
            setup_via_api()
        else:
            print("❌ API not ready, falling back to direct database setup")
            setup_initial_areas()
    else:
        # Direct database setup
        setup_initial_areas()
    
    print("✅ Setup completed successfully!")


if __name__ == "__main__":
    main()
