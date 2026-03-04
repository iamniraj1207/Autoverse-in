import os
import cv2
import numpy as np
from PIL import Image, ImageStat
import imageio

# Configuration
SOURCE_DIR = r'd:\Autoverse\autoverse\static\img\hero'
OUTPUT_FILE = r'd:\Autoverse\autoverse\static\img\hero\hero.mp4'
FRAME_COUNT = 40
INTERPOLATION_FACTOR = 8  # Max smoothness (40 * 8 = 320 frames)
TARGET_FPS = 60           # Fluid cinematic motion
TARGET_RES = (1920, 1080) # Restoration of Full HD for sharpness

def match_luminance(images):
    print("Pre-processing frames (Deflicker Only)...")
    def get_b(img): return ImageStat.Stat(img).mean[0]
    avg_b = np.mean([get_b(i) for i in images])
    processed = []
    for img in images:
        ratio = avg_b / get_b(img) if get_b(img) > 0 else 1
        img_np = np.array(img).astype(np.float32)
        img_np = np.clip(img_np * ratio, 0, 255).astype(np.uint8)
        processed.append(Image.fromarray(img_np))
    return processed

def generate_video():
    frames = []
    for i in range(1, FRAME_COUNT + 1):
        path = os.path.join(SOURCE_DIR, f'ezgif-frame-{str(i).zfill(3)}.jpg')
        if os.path.exists(path):
            img = Image.open(path).convert('RGB')
            img = img.resize(TARGET_RES, Image.Resampling.LANCZOS)
            frames.append(img)
    
    if not frames: return

    frames = match_luminance(frames)
    frames.append(frames[0])

    print(f"Generating Ultra-Smooth 60fps Video: {OUTPUT_FILE}")
    # High-quality 60fps encoding with faster preset for compatibility
    writer = imageio.get_writer(OUTPUT_FILE, fps=TARGET_FPS, codec='libx264', 
                                quality=8, bitrate='4M',
                                ffmpeg_params=['-pix_fmt', 'yuv420p', '-preset', 'fast', '-crf', '22'])

    for i in range(len(frames) - 1):
        f1 = np.array(frames[i]).astype(np.float32)
        f2 = np.array(frames[i+1]).astype(np.float32)
        for j in range(INTERPOLATION_FACTOR):
            alpha = j / INTERPOLATION_FACTOR
            blended = (f1 * (1 - alpha) + f2 * alpha).astype(np.uint8)
            writer.append_data(blended)
            
    writer.close()
    print("Ultra-smooth video generation complete.")

if __name__ == "__main__":
    generate_video()
