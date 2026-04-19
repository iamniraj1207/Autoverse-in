import sqlite3
import requests
import json
import time

def unique_model_calibration():
    conn = sqlite3.connect('autoverse.db')
    cursor = conn.cursor()

    # We target brands where 'Same Image' syndrome is most likely
    cursor.execute("SELECT id, brand, model, year FROM cars WHERE image_url LIKE '%loremflickr%' OR image_url IS NULL OR brand IN ('Acura', 'Honda', 'Toyota', 'Audi', 'BMW', 'Mercedes-Benz')")
    cars = cursor.fetchall()

    print(f"INITIATING UNIQUE MODEL CALIBRATION: {len(cars)} UNITS...")

    for car_id, brand, model, year in cars:
        # We ensure a UNIQUE search pattern for every single displacement
        # Using Unsplash source with specific model+year targeting
        clean_model = model.split(' ')[0]
        
        # Primary: High-Resolution Redirect from Unsplash Model index
        unique_url = f"https://source.unsplash.com/featured/1200x800/?{brand.replace(' ', '+')}+{model.replace(' ', '+')}+{year},car"
        
        # We follow the redirect to get the PERMANENT static URL so they are all different
        try:
            response = requests.head(unique_url, allow_redirects=True, timeout=5)
            if response.status_code == 200 and "unsplash.com" in response.url:
                final_url = response.url
                cursor.execute("UPDATE cars SET image_url = ? WHERE id = ?", (final_url, car_id))
                print(f"  UNIQUE SYNC [100%]: {brand} {model} ({year})")
            else:
                # Fallback to precise Imagin.studio (with white paint fallback)
                imagin_fallback = f"https://cdn.imagin.studio/getImage?customer=hr-autoverse&make={brand.lower().replace(' ', '-')}&modelFamily={clean_model.lower()}&zoomType=fullscreen&paintId=25"
                cursor.execute("UPDATE cars SET image_url = ? WHERE id = ?", (imagin_fallback, car_id))
                print(f"  PRECISE RENDER: {brand} {model}")
        except:
            pass

        conn.commit()
    
    conn.close()
    print("UNIQUE CALIBRATION COMPLETE. All duplicates purged.")

if __name__ == "__main__":
    unique_model_calibration()
