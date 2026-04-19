import requests
import sqlite3
import os
import json

db_path = "autoverse.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT * FROM cars WHERE image_url LIKE '%imagin.studio%' LIMIT 1")
car = cursor.fetchone()

if car:
    print(f"Testing for {car['brand']} {car['model']}...")
    query = f"{car['year']} {car['brand']} {car['model']}"
    search_url = "https://commons.wikimedia.org/w/api.php"
    headers = {"User-Agent": "AutoVerse/1.0 (contact: support@autoverse.com)"}
    params = {
        "action": "query",
        "list": "search",
        "srsearch": "Pagani",
        "format": "json",
        "srlimit": 1
    }
    res = requests.get(search_url, params=params, headers=headers, timeout=10)
    print(f"Search Response: {res.status_code}")
    if res.status_code == 200:
        data = res.json()
        print(f"Data: {json.dumps(data, indent=2)}")
        results = data.get('query', {}).get('search', [])
        if results:
            print(f"Found {len(results)} results.")
            title = results[0]['title']
            print(f"Top Result Title: {title}")
            img_url_req = f"{search_url}?action=query&titles={title}&prop=imageinfo&iiprop=url&format=json"
            img_res = requests.get(img_url_req, headers=headers, timeout=10)
            pages = img_res.json().get('query', {}).get('pages', {})
            for p in pages.values():
                info = p.get('imageinfo', [])
                if info:
                    url = info[0]['url']
                    print(f"Success! URL: {url}")
                    cursor.execute("UPDATE cars SET image_url = ? WHERE id = ?", (url, car['id']))
                    conn.commit()
                    print("Updated database row.")
                else:
                    print("No image info in page.")
        else:
            print("No search results found.")
else:
    print("No imagin cars found.")

conn.close()
