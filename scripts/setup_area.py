#!/usr/bin/env python3
"""
Script to create a default area for people tracking
"""
import requests
import sys
import time

API_BASE_URL = "http://localhost:8000"

def wait_for_api():
    """Wait for API to be ready"""
    print("Waiting for API to be ready...")
    for i in range(30):  # Wait up to 30 seconds
        try:
            response = requests.get(f"{API_BASE_URL}/docs", timeout=5)
            if response.status_code == 200:
                print("✅ API is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
        print(f"Waiting... {i+1}/30")
    return False

def create_default_area():
    """Create a default detection area"""
    area_data = {
        "name": "Default Detection Area",
        "polygon": [
            [300, 400],
            [900, 400], 
            [1000, 720],
            [200, 720]
        ]
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/config/area",
            json=area_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Area created successfully!")
            print(f"Area ID: {result.get('area_id')}")
            print(f"Message: {result.get('message')}")
            return True
        else:
            print(f"❌ Failed to create area: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creating area: {e}")
        return False

def main():
    print("🚀 Setting up default detection area...")
    
    # Wait for API to be ready
    if not wait_for_api():
        print("❌ API is not ready. Exiting.")
        sys.exit(1)
    
    # Create default area
    if create_default_area():
        print("✅ Setup completed successfully!")
        sys.exit(0)
    else:
        print("❌ Setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
