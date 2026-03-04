import os
import cv2
import numpy as np
from PIL import Image

def slice_image(input_path, output_dir, prefix):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read image with alpha channel
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Error loading {input_path}")
        return

    # Create a mask of the non-transparent pixels
    if img.shape[2] == 4:
        # If it has an alpha channel
        alpha_channel = img[:, :, 3]
        _, thresh = cv2.threshold(alpha_channel, 10, 255, cv2.THRESH_BINARY)
    else:
        # If no alpha, assume white or black background
        gray = cv2.cvtColor(img, cv2.Color(cv2.COLOR_BGR2GRAY))
        _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter small contours that might be noise
    min_area = 500
    valid_contours = [c for c in contours if cv2.contourArea(c) > min_area]
    
    # Sort contours geometrically, e.g., top-to-bottom, left-to-right
    # Simple sort based on y, then x
    bounding_boxes = [cv2.boundingRect(c) for c in valid_contours]
    # Sort by Y first (in rows of roughly same height)
    # A robust sort for grid: sort by Y, group into rows, then sort by X within rows
    # For now, just sort by Y, then X loosely
    def row_sort(box):
        x, y, w, h = box
        # Group by y in chunks of 50
        return (y // 150, x)
        
    bounding_boxes.sort(key=row_sort)

    count = 1
    for i, (x, y, w, h) in enumerate(bounding_boxes):
        # Add padding
        pad = 10
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(img.shape[1], x + w + pad)
        y2 = min(img.shape[0], y + h + pad)
        
        # Crop
        cropped = img[y1:y2, x1:x2]
        out_path = os.path.join(output_dir, f"{prefix}_{count}.png")
        cv2.imwrite(out_path, cropped)
        print(f"Saved {out_path}")
        count += 1

if __name__ == "__main__":
    drivers_img = r"d:\Autoverse\autoverse\static\img\F1_2026_Drivers.png"
    logos_img = r"d:\Autoverse\autoverse\static\img\infinity20.png"
    
    slice_image(drivers_img, r"d:\Autoverse\autoverse\static\img\drivers_sliced", "driver")
    slice_image(logos_img, r"d:\Autoverse\autoverse\static\img\logos_sliced", "logo")
