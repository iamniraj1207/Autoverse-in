import requests
import sqlite3
import os
import time

# API Configurations
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "") # User adds this to .env
NHTSA_BASE_URL = "https://vpic.nhtsa.dot.gov/api/vehicles"

def get_car_specs(make, model, year):
    """Fetches specs from NHTSA vPIC API."""
    try:
        # Example: Get all models for a make and year to verify
        url = f"{NHTSA_BASE_URL}/GetModelsForMakeYear/make/{make}/modelyear/{year}?format=json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Basic validation that model exists
            models = [m['Model_Name'].lower() for m in data.get('Results', [])]
            if model.lower() in models:
                return {"valid": True, "source": "NHTSA"}
        return {"valid": False}
    except Exception as e:
        print(f"NHTSA Error: {e}")
        return {"valid": False}

def get_pexels_image(query):
    """Fetches a high-quality car image from Pexels."""
    if not PEXELS_API_KEY:
        return None
    try:
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
        headers = {"Authorization": PEXELS_API_KEY}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['photos']:
                return data['photos'][0]['src']['landscape']
        return None
    except Exception as e:
        print(f"Pexels Error: {e}")
        return None

def sync_cars():
    conn = sqlite3.connect('autoverse.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, brand, model, year FROM cars WHERE image_url IS NULL OR image_url = ''")
    cars_to_update = cursor.fetchall()
    
    for car_id, brand, model, year in cars_to_update:
        print(f"Processing {year} {brand} {model}...")
        
        # Verify specs via NHTSA (Optional sanity check)
        specs = get_car_specs(brand, model, year)
        
        # Get image via Pexels
        img_url = get_pexels_image(f"{year} {brand} {model}")
        
        if img_url:
            cursor.execute("UPDATE cars SET image_url = ? WHERE id = ?", (img_url, car_id))
            conn.commit()
            print(f"  Updated image: {img_url}")
        
        time.sleep(1) # Rate limiting
        
    conn.close()

if __name__ == "__main__":
    sync_cars()
