import sqlite3
import requests
import json
import time

def sync_luxury_gallery():
    conn = sqlite3.connect('autoverse.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, brand, model FROM cars WHERE image_url NOT LIKE '%,%'")
    cars = cursor.fetchall()

    print(f"RESUMING LUXURY GALLERY SYNC (3 IMAGE HD PACK): {len(cars)} UNITS...")

    for car_id, brand, model in cars:
        gallery_urls = []
        
        # Pattern 1: Unsplash (High Fidelity)
        keywords = [
            f"{brand}+{model}+car",
            f"{brand}+{model}+interior",
            f"{brand}+{model}+rear"
        ]

        for k in keywords:
            try:
                # Limit size to 1200x800 for stability
                test_url = f"https://source.unsplash.com/featured/1200x800/?{k}"
                response = requests.head(test_url, allow_redirects=True, timeout=3)
                if response.status_code == 200 and "unsplash.com" in response.url:
                    gallery_urls.append(response.url)
            except:
                pass
            
            if len(gallery_urls) >= 3:
                break
        
        # Fallback to Imagin.studio (Corrected Python string methods)
        if len(gallery_urls) < 3:
            imagin_base = f"https://cdn.imagin.studio/getImage?customer=hr-autoverse&make={brand.lower().replace(' ', '-')}&modelFamily={model.split(' ')[0].lower()}&zoomType=fullscreen"
            gallery_urls.append(f"{imagin_base}&angle=01")
            gallery_urls.append(f"{imagin_base}&angle=29")
            gallery_urls.append(f"{imagin_base}&angle=35")

        final_string = ",".join(gallery_urls[:3])
        cursor.execute("UPDATE cars SET image_url = ? WHERE id = ?", (final_string, car_id))
        
        print(f"  SYNCED: {brand} {model}")
        conn.commit()

    conn.close()
    print("GLOBAL MULTI-IMAGE SYNC COMPLETE.")

if __name__ == "__main__":
    sync_luxury_gallery()
