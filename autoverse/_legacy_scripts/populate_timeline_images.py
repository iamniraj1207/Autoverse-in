import sqlite3
import requests
import urllib.parse
import time

def get_wikimedia_image(query):
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&generator=search&gsrsearch={urllib.parse.quote(query)}&gsrlimit=1&pithumbsize=600"
        res = requests.get(url, headers={'User-Agent': 'Autoverse Bot'}, timeout=5)
        data = res.json()
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_data in pages.items():
            if 'thumbnail' in page_data:
                return page_data['thumbnail']['source']
    except Exception as e:
        print(f"Failed for {query}: {e}")
    return None

conn = sqlite3.connect('autoverse.db')
cursor = conn.cursor()

cursor.execute("SELECT id, year, title, entity_type FROM f1_timeline WHERE image_url IS NULL OR image_url = ''")
rows = cursor.fetchall()

print(f"Found {len(rows)} timeline events missing images.")

count = 0
for row in rows:
    tid, year, title, etype = row
    
    # Construct a search query
    search_query = f"{year} Formula One {title}"
    if etype == 'team':
         search_query = f"{year} {title} Formula One"
         
    img_url = get_wikimedia_image(search_query)
    
    if img_url:
        cursor.execute("UPDATE f1_timeline SET image_url = ? WHERE id = ?", (img_url, tid))
        conn.commit()
        print(f"Updated {tid} ({year} {title}) -> {img_url}")
        count += 1
    else:
        print(f"No image found for {tid} ({year} {title})")
        
    time.sleep(0.1) # Be nice to wikipedia

print(f"Done. Successfully populated {count} images.")
conn.close()
