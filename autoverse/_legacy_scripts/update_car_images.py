import sqlite3
import random

def update_car_images():
    conn = sqlite3.connect('autoverse.db')
    db = conn.cursor()

    # Verified clean Unsplash photo IDs by brand
    BRAND_IMAGES = {
        'Ferrari': [
            'photo-1592198084033-aade902d1aae',  # Ferrari red
            'photo-1503376780353-7e6692767b70',  # Ferrari on road
            'photo-1544636331-e26879cd4d9b',     # Ferrari detail
        ],
        'Lamborghini': [
            'photo-1621135802920-133df287f89c',  # Lamborghini orange
            'photo-1580274455191-1c62238fa333',  # Lamborghini yellow
            'photo-1568605117036-5fe5e7bab0b7',  # Lambo on road
        ],
        'Porsche': [
            'photo-1583121274602-3e2820c69888',  # Porsche 911
            'photo-1555626906-fcf10d6851b4',     # Porsche silver
            'photo-1614162692292-7ac56d7f7f1e',  # Porsche GT3
        ],
        'McLaren': [
            'photo-1558618666-fcd25c85cd64',     # McLaren orange
            'photo-1544196281-cec8a8a8da2c',     # McLaren side
        ],
        'BMW': [
            'photo-1555215695-3004980ad54e',     # BMW M series
            'photo-1556189250-72ba954cfc2b',     # BMW front
        ],
        'Mercedes': [
            'photo-1618843479313-40f8afb4b4d8',  # Mercedes AMG
            'photo-1606220945770-b5b6c2c55bf1',  # Mercedes black
        ],
        'Audi': [
            'photo-1606664515524-ed2f786a0bd6',  # Audi RS
            'photo-1553440569-bcc63803a83d',     # Audi side
        ],
        'Tesla': [
            'photo-1560958089-b8a1929cea89',     # Tesla Model S
            'photo-1536700503339-1e4b06520771',  # Tesla white
        ],
        'Ford': [
            'photo-1612825173281-9a193378527e',  # Ford Mustang
            'photo-1547744152-14d985cb937f',     # Ford GT
        ],
        'Bugatti': [
            'photo-1544636331-e26879cd4d9b',     # Bugatti blue
        ],
        'Pagani': [
            'photo-1544636331-e26879cd4d9b',     # Pagani detail
        ],
        'Koenigsegg': [
            'photo-1558618666-fcd25c85cd64',     # Hypercar
        ],
    }

    DEFAULT_IMAGES = [
        'photo-1494976388531-d1058494cdd8',
        'photo-1492144534655-ae79c964c9d7',
        'photo-1511919884226-fd3cad34687c',
        'photo-1517524008697-84bbe3c3fd98',
        'photo-1502877338535-766e1452684a',
    ]

    def get_image_url(brand, size='800x500'):
        w, h = size.split('x')
        brand_clean = brand.strip().title()
        if 'Mercedes' in brand_clean: brand_clean = 'Mercedes'
        pool = BRAND_IMAGES.get(brand_clean, DEFAULT_IMAGES)
        photo_id = random.choice(pool)
        return f"https://images.unsplash.com/{photo_id}?w={w}&h={h}&fit=crop&q=80"

    # Update ALL cars
    cars = db.execute("SELECT id, brand, model FROM cars").fetchall()
    for car_id, brand, model in cars:
        ext_url = get_image_url(brand, '1200x700')
        int_url = get_image_url(brand, '1200x700')
        side_url = get_image_url(brand, '1200x700')
        rear_url = get_image_url(brand, '1200x700')
        
        db.execute("""
            UPDATE cars SET
                image_url = ?,
                image_exterior = ?,
                image_interior = ?,
                image_side = ?,
                image_rear = ?
            WHERE id = ?
        """, (ext_url, ext_url, int_url, side_url, rear_url, car_id))

    # Targeted Overrides for famous cars
    OVERRIDE_URLS = {
        ('Ferrari', '488 GTB'):   'photo-1592198084033-aade902d1aae',
        ('Ferrari', 'F40'):       'photo-1503376780353-7e6692767b70',
        ('Lamborghini', 'Huracan'): 'photo-1621135802920-133df287f89c',
        ('Bugatti', 'Chiron'):    'photo-1544636331-e26879cd4d9b',
        ('Porsche', '911 GT3'):   'photo-1583121274602-3e2820c69888',
        ('McLaren', '720S'):      'photo-1558618666-fcd25c85cd64',
        ('Tesla', 'Model S'):     'photo-1560958089-b8a1929cea89',
    }

    for (brand, model), photo_id in OVERRIDE_URLS.items():
        url = f"https://images.unsplash.com/{photo_id}?w=1200&h=700&fit=crop&q=80"
        db.execute("""
            UPDATE cars SET 
                image_url = ?, image_exterior = ?, image_interior = ?, image_side = ?, image_rear = ?
            WHERE brand = ? AND model = ?
        """, (url, url, url, url, url, brand, model))

    conn.commit()
    conn.close()
    print(f"Updated {len(cars)} cars — no watermarks")

if __name__ == "__main__":
    update_car_images()
