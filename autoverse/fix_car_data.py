import sqlite3
import json

def fix_car_data():
    conn = sqlite3.connect('autoverse.db')
    cursor = conn.cursor()

    # 1. FIX TESLA / EV SPECS
    ev_brands = ['Tesla', 'Rivian', 'Lucid', 'Polestar', 'Rimac', 'BYD']
    
    cursor.execute("SELECT id, brand, model FROM cars")
    all_cars = cursor.fetchall()
    
    for car_id, brand, model in all_cars:
        # Fetch current specs
        cursor.execute("SELECT specs_json, engine, horsepower, torque FROM cars WHERE id = ?", (car_id,))
        row = cursor.fetchone()
        specs = json.loads(row[0]) if row[0] else {}
        engine_val = row[1]
        hp = row[2]
        torque = row[3]

        is_ev = any(ev_brand.lower() in brand.lower() for ev_brand in ev_brands) or 'electric' in (engine_val or '').lower()

        if is_ev:
            specs['engine'] = engine_val or "Dual Electric Motor"
            specs['displacement'] = "0 cc (EV)"
            specs['fuel'] = "Electric / 100kWh Battery"
            specs['transmission'] = "Single-Speed Direct Drive"
        else:
            # For non-EV, ensure it doesn't just say 'V6' if it's a known high-end car
            if 'Ferrari' in brand or 'Lamborghini' in brand:
                specs['engine'] = engine_val or "V12 Naturally Aspirated"
                specs['transmission'] = "7-Speed Dual-Clutch"
            elif 'Porsche' in brand:
                specs['engine'] = engine_val or "Flat-Six Twin-Turbo"
            
        # Ensure brand/model are correct in JSON
        specs['brand'] = brand
        specs['model'] = model
        specs['power'] = f"{hp} HP" if hp else "N/A"
        specs['torque'] = f"{torque} NM" if torque else "N/A"

        cursor.execute("UPDATE cars SET specs_json = ? WHERE id = ?", (json.dumps(specs), car_id))

    conn.commit()
    conn.close()
    print("CAR DATA CALIBRATION COMPLETE: EV/ICE logic corrected across fleet.")

if __name__ == "__main__":
    fix_car_data()
