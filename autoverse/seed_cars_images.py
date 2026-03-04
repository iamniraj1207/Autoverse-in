import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'autoverse.db')
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def seed_car_images():
    print("Updating 1100 car image URLs...")
    cars = cursor.execute("SELECT id, brand, model, year FROM cars").fetchall()
    
    for car in cars:
        brand = car['brand'].lower().replace(' ', '-')
        model = car['model'].lower().replace(' ', '-')
        year = car['year']
        
        base_url = "https://cdn.imagin.studio/getimage?customer=img&make={brand}&modelFamily={model}&modelYear={year}&angle={angle}"
        
        exterior = base_url.format(brand=brand, model=model, year=year, angle='front')
        interior = base_url.format(brand=brand, model=model, year=year, angle='interior-front')
        side = base_url.format(brand=brand, model=model, year=year, angle='side')
        rear = base_url.format(brand=brand, model=model, year=year, angle='rear')
        
        cursor.execute("""
            UPDATE cars SET 
            image_exterior = ?, 
            image_interior = ?, 
            image_side = ?, 
            image_rear = ?,
            image_url = ?
            WHERE id = ?
        """, (exterior, interior, side, rear, exterior, car['id']))
        
    conn.commit()
    print(f"Updated {len(cars)} cars.")

if __name__ == "__main__":
    seed_car_images()
    conn.close()
