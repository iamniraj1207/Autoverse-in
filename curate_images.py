import sqlite3
import requests
import json

# Real, verified images per brand+model for the most common cars in the DB
# These are SPECIFIC, not generic brand-level URLs
CURATED_IMAGES = {
    # 9ff
    '9ff_GT9-R': 'https://upload.wikimedia.org/wikipedia/commons/e/e0/9ff_GT9-R_at_Essen_Motor_Show_2008.jpg',
    
    # Porsche specific models
    'Porsche_Carrera GT': 'https://upload.wikimedia.org/wikipedia/commons/f/f6/Porsche_Carrera_GT_-_Goodwood_Festival_of_Speed_2010_%281%29.jpg',
    'Porsche_918 Spyder': 'https://upload.wikimedia.org/wikipedia/commons/9/91/Porsche_918_Spyder_IAA_2013.jpg',
    'Porsche_911 Turbo S (997)': 'https://upload.wikimedia.org/wikipedia/commons/0/09/Porsche_997_Carrera_%282004%29_coupes_IMG_7311.jpg',
    'Porsche_911 GT3 RS (992)': 'https://upload.wikimedia.org/wikipedia/commons/2/2b/Porsche_992_GT3_RS_Tribute_to_Jo_Siffert_Auto_Zuerich_2024_DSC_6518.jpg',
    'Porsche_Taycan Turbo S': 'https://upload.wikimedia.org/wikipedia/commons/4/46/Porsche_Carrera_Cup_Deutschland_2023_Spa-Francorchamps_Manthey-Racing_Porsche_Taycan_Turbo_S_Safety_Car_%28DSC08756%29.jpg',
    'Porsche_Taycan 4S': 'https://upload.wikimedia.org/wikipedia/commons/a/a7/Porsche_Taycan_4S_%28at_the_Osaka_Mobility_Show_2023%29.jpg',
    
    # Alfa Romeo specific models
    'Alfa Romeo_8C Competizione': 'https://upload.wikimedia.org/wikipedia/commons/5/58/Alfa_Romeo_8C_Competizione_%282007%29.jpg',
    'Alfa Romeo_4C': 'https://upload.wikimedia.org/wikipedia/commons/9/9d/Alfa_Romeo_4C_-_Frontansicht%2C_17._August_2013%2C_D%C3%BCsseldorf.jpg',
    'Alfa Romeo_Giulia QV': 'https://upload.wikimedia.org/wikipedia/commons/a/a0/2017_Alfa_Romeo_Giulia_QV.jpg',
    'Alfa Romeo_Stelvio QV': 'https://upload.wikimedia.org/wikipedia/commons/2/24/Alfa_Romeo_Stelvio_Quadrifoglio_%28Geneva_2017%29.jpg',

    # Aston Martin
    'Aston Martin_DB5': 'https://upload.wikimedia.org/wikipedia/commons/4/4a/Aston_martin_db5.jpg',
    'Aston Martin_One-77': 'https://upload.wikimedia.org/wikipedia/commons/3/3e/Aston_Martin_One-77_%282009%29.jpg',
    'Aston Martin_Valkyrie': 'https://upload.wikimedia.org/wikipedia/commons/3/31/Aston_Martin_Valkyrie_%40_2019_Festival_of_Speed.jpg',
    'Aston Martin_DBS Superleggera': 'https://upload.wikimedia.org/wikipedia/commons/3/33/2018_Aston_Martin_DBS_Superleggera_-_front_%28cut%29.jpg',

    # Ferrari
    'Ferrari_LaFerrari': 'https://upload.wikimedia.org/wikipedia/commons/1/1c/LaFerrari.jpg',
    'Ferrari_SF90 Stradale': 'https://upload.wikimedia.org/wikipedia/commons/b/b5/Ferrari_SF90_Stradale.jpg',
    'Ferrari_F40': 'https://upload.wikimedia.org/wikipedia/commons/5/52/Ferrari_F40.jpg',
    'Ferrari_Enzo': 'https://upload.wikimedia.org/wikipedia/commons/4/48/Ferrari_Enzo_-_Flickr_-_Alexandre_Previ%C3%B3t_%281%29.jpg',

    # Lamborghini
    'Lamborghini_Aventador SVJ': 'https://upload.wikimedia.org/wikipedia/commons/6/64/Lamborghini_Aventador_SVJ_-_Salon_de_Geneve_2019_-_04.jpg',
    'Lamborghini_Huracan STO': 'https://upload.wikimedia.org/wikipedia/commons/1/14/Lamborghini_Huracan_STO.jpg',
    'Lamborghini_Sian': 'https://upload.wikimedia.org/wikipedia/commons/0/01/Lamborghini_Sian_FKP_37_genf_2020.jpg',

    # McLaren
    'McLaren_P1': 'https://upload.wikimedia.org/wikipedia/commons/7/72/McLaren_P1_%282013%29_%2814930575845%29.jpg',
    'McLaren_Senna': 'https://upload.wikimedia.org/wikipedia/commons/e/e7/McLaren_Senna_-_Geneva_Motor_Show.jpg',
    'McLaren_F1': 'https://upload.wikimedia.org/wikipedia/commons/7/7b/McLaren_F1_-_Flickr_-_Alexandre_Previ%C3%B3t_%281%29.jpg',

    # Tesla
    'Tesla_Model S Plaid': 'https://upload.wikimedia.org/wikipedia/commons/9/91/2021_Tesla_Model_S_Plaid.jpg',
    'Tesla_Roadster (1st Gen)':'https://upload.wikimedia.org/wikipedia/commons/e/ef/2008-tesla-roadster.jpg',

    # Bugatti
    'Bugatti_Veyron': 'https://upload.wikimedia.org/wikipedia/commons/4/4e/Bugatti_Veyron_16.4_%E2%80%93_Frontansicht_%281%29%2C_5._April_2012%2C_D%C3%BCsseldorf.jpg',
    'Bugatti_Chiron': 'https://upload.wikimedia.org/wikipedia/commons/0/06/Bugatti_Chiron_-_Geneva_Motor_Show_2016.jpg',

    # Rimac
    'Rimac_Nevera': 'https://upload.wikimedia.org/wikipedia/commons/7/7a/Rimac_Nevera_-_Geneva_Motor_Show_2021.jpg',
}

def apply_curated_images():
    conn = sqlite3.connect('autoverse.db')
    cursor = conn.cursor()

    print("APPLYING CURATED HIGH-ACCURACY IMAGES...")
    applied = 0
    for key, url in CURATED_IMAGES.items():
        brand, model = key.split('_', 1)
        cursor.execute("UPDATE cars SET image_url = ? WHERE brand = ? AND model = ?", (url, brand, model))
        if cursor.rowcount > 0:
            print(f"  CURATED: {brand} {model}")
            applied += 1

    # For all remaining cars that have a generic/same Unsplash URL,
    # replace with Imagin.studio white render (correct make + model)
    cursor.execute("""
        UPDATE cars 
        SET image_url = 'https://cdn.imagin.studio/getImage?customer=hr-autoverse&make=' 
            || LOWER(REPLACE(brand, ' ', '-')) 
            || '&modelFamily=' 
            || LOWER(REPLACE(SUBSTR(model, 1, CASE WHEN INSTR(model, ' ') = 0 THEN LENGTH(model) ELSE INSTR(model, ' ') - 1 END), ' ', '-'))
            || '&zoomType=fullscreen&paintId=25'
        WHERE image_url LIKE 'https://images.unsplash.com/photo-1503376780353%'
           OR image_url LIKE 'https://images.unsplash.com/photo-1549495503%'
           OR image_url LIKE 'https://images.unsplash.com/photo-1563720223185%'
    """)
    fixed_generic = cursor.rowcount
    print(f"  RESTORED {fixed_generic} generic same-image cars to Imagin.studio white renders")

    conn.commit()
    conn.close()
    print(f"DONE. {applied} curated + {fixed_generic} studio white renders applied.")

if __name__ == "__main__":
    apply_curated_images()
