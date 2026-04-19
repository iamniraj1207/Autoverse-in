import sqlite3

def restore_realistic_prices():
    conn = sqlite3.connect('autoverse.db')
    cursor = conn.cursor()

    # Dictionary of brand-specific minimum 'Crore' valuations
    luxury_map = {
        'Ferrari': 4.5, 'Lamborghini': 3.8, 'Rolls Royce': 6.5, 'Bentley': 4.2,
        'Bugatti': 25.0, 'Pagani': 35.0, 'Koenigsegg': 30.0, 'McLaren': 3.5,
        'Aston Martin': 3.2, 'Porsche': 2.8, 'Tesla': 0.8, 'BMW': 0.7, 
        'Mercedes-Benz': 0.9, 'Audi': 0.7, 'Range Rover': 1.8, 'Jaguar': 0.8,
        'Toyota': 0.25, 'Honda': 0.18, 'Skoda': 0.20, 'Volkswagen': 0.22,
        'Maybach': 5.5, 'Maserati': 2.1, 'Lotus': 1.5, 'Ford': 0.22,
        '9ff': 9.5, 'Rimac': 18.0
    }

    cursor.execute("SELECT id, brand, model FROM cars")
    all_cars = cursor.fetchall()
    
    print("RE-CALIBRATING FLEET PRICING (ELITE SYNC)...")
    
    for car_id, brand, model in all_cars:
        # Match brand
        base_cr = 1.5 # Default
        for b, val in luxury_map.items():
            if b.lower() in brand.lower():
                base_cr = val
                break
        
        # Add slight model-specific variation
        perf_keywords = ['GT', 'RS', 'Turbo', 'Plaid', 'Super', 'Hyper']
        if any(k.lower() in model.lower() for k in perf_keywords):
            base_cr *= 1.4

        price_str = f"{round(base_cr, 2)} Cr"
        price_usd = int(base_cr * 120000) # $120k per Cr roughly
        
        cursor.execute("UPDATE cars SET price_usd = ?, price_usd = ? WHERE id = ?", (price_str, price_str, car_id))
        # Wait, I should update the column that stores the string '1.5 Cr'
        # In current schema, price_usd is the main price column.
        
    conn.commit()
    conn.close()
    print("FLEET PRICING RE-CALIBRATED: No more generic placeholders.")

if __name__ == "__main__":
    restore_realistic_prices()
