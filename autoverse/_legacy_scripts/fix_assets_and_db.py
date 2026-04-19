import cv2
import os
import sqlite3

os.makedirs('static/img/logos_sliced', exist_ok=True)

img = cv2.imread('static/img/infinity20.png')
if img is None:
    print("Could not load infinity20.png")
    exit(1)

# Remove the outer 10 pixels to prevent a massive contour border
border_trim = 10
img_trimmed = img[border_trim:-border_trim, border_trim:-border_trim]

gray = cv2.cvtColor(img_trimmed, cv2.COLOR_BGR2GRAY)
# Since logos usually have a white background, invert to find objects
_, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

boxes = []
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    # Adjust x,y back to original image coordinates
    x += border_trim
    y += border_trim
    area = w * h
    if 2000 < area < 100000:
        boxes.append((x, y, w, h))

def row_sort(box):
    return (box[1] // 100, box[0])
boxes.sort(key=row_sort)

count = 1
for x, y, w, h in boxes:
    pad = 15
    x1 = max(0, x - pad)
    y1 = max(0, y - pad)
    x2 = min(img.shape[1], x + w + pad)
    y2 = min(img.shape[0], y + h + pad)
    
    cropped = img[y1:y2, x1:x2]
    out = f"static/img/logos_sliced/logo_{count}.png"
    cv2.imwrite(out, cropped)
    print(f"Saved logo slice: {out}")
    count += 1

print("\nRunning DB Update for Imagin.studio & Sliced Assets...")
conn = sqlite3.connect('autoverse.db')

# 1. Revert cars to imagin.studio 
# The user wants imagin.studio back for cars. 
imagin_query = "https://cdn.imagin.studio/getImage?customer=img&make="
conn.execute(f"UPDATE cars SET image_url = '{imagin_query}' || brand || '&modelFamily=' || model || '&angle=01&zoomType=fullscreen&transparent=true'")
conn.execute(f"UPDATE cars SET image_exterior = '{imagin_query}' || brand || '&modelFamily=' || model || '&angle=01&zoomType=fullscreen&transparent=true'")
conn.execute(f"UPDATE cars SET image_interior = '{imagin_query}' || brand || '&modelFamily=' || model || '&angle=09&zoomType=fullscreen&transparent=true'")
conn.execute(f"UPDATE cars SET image_side = '{imagin_query}' || brand || '&modelFamily=' || model || '&angle=05&zoomType=fullscreen&transparent=true'")
conn.execute(f"UPDATE cars SET image_rear = '{imagin_query}' || brand || '&modelFamily=' || model || '&angle=13&zoomType=fullscreen&transparent=true'")

# 2. Assign Sliced Driver Images
# There are 17 driver slices. Let's assign them sequentially to Drivers table (sorted by id)
drivers = conn.execute("SELECT id FROM drivers ORDER BY id").fetchall()
for i, (d_id,) in enumerate(drivers):
    slice_idx = (i % 17) + 1
    slice_path = f"/static/img/drivers_sliced/driver_{slice_idx}.png"
    conn.execute("UPDATE drivers SET image_url = ? WHERE id = ?", (slice_path, d_id))

# 3. Assign Sliced Team Logos
# Assume we have up to 10 logos sliced.
teams = conn.execute("SELECT id FROM teams ORDER BY id").fetchall()
num_logos = max(1, count - 1)
for i, (t_id,) in enumerate(teams):
    slice_idx = (i % num_logos) + 1
    slice_path = f"/static/img/logos_sliced/logo_{slice_idx}.png"
    conn.execute("UPDATE teams SET logo_url = ? WHERE id = ?", (slice_path, t_id))

conn.commit()
conn.close()
print("DB Sync Complete.")
