"""
download_car_models.py
Downloads free, legitimately licensed GLTF/GLB car models.

Sources used:
  - Three.js official repo (MIT) — Ferrari, etc.
  - KhronosGroup GLTF Sample Assets (CC0)
  - Quaternius (CC0 car pack via GitHub mirror)

All models saved to: autoverse/static/models/cars/
"""
import os, urllib.request, json

MODELS_DIR = os.path.join('static', 'models', 'cars')
os.makedirs(MODELS_DIR, exist_ok=True)

# ── Model manifest ─────────────────────────────────────────────
# key         → filename in static/models/cars/
# archetype   → which car categories use this model
# color_slot  → whether the model supports color tinting

MODELS = [
    {
        "key":        "supercar",
        "file":       "supercar.glb",
        "archetypes": ["Supercar", "Sports Car", "Coupe"],
        "url":        "https://raw.githubusercontent.com/mrdoob/three.js/master/examples/models/gltf/ferrari.glb",
        "note":       "Three.js Ferrari — MIT license"
    },
    {
        "key":        "toy_car",
        "file":       "toy_car.glb",
        "archetypes": ["Compact", "Hatchback", "City"],
        "url":        "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/main/Models/ToyCar/glTF-Binary/ToyCar.glb",
        "note":       "KhronosGroup ToyCar — CC0 1.0"
    },
]

# ── AO maps that go with three.js ferrari ──
EXTRA_MAPS = [
    {
        "file": "ferrari_ao.png",
        "url":  "https://raw.githubusercontent.com/mrdoob/three.js/master/examples/models/gltf/ferrari_ao.png"
    }
]

def download(url, dest, name):
    if os.path.exists(dest):
        size = os.path.getsize(dest)
        print(f"  [SKIP] {name} already exists ({size:,} bytes)")
        return True
    print(f"  Downloading {name}...")
    try:
        urllib.request.urlretrieve(url, dest)
        size = os.path.getsize(dest)
        print(f"  ✓ {name} saved ({size:,} bytes)")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {name} — {e}")
        # Remove partial file
        if os.path.exists(dest):
            os.remove(dest)
        return False

print("Downloading car model archetypes...\n")

manifest = {}
for m in MODELS:
    dest = os.path.join(MODELS_DIR, m["file"])
    ok = download(m["url"], dest, m["note"])
    if ok:
        manifest[m["key"]] = {
            "file":       m["file"],
            "archetypes": m["archetypes"]
        }

for em in EXTRA_MAPS:
    dest = os.path.join(MODELS_DIR, em["file"])
    download(em["url"], dest, em["file"])

# Write manifest JSON for the frontend to read
manifest_path = os.path.join(MODELS_DIR, 'manifest.json')
with open(manifest_path, 'w') as f:
    json.dump(manifest, f, indent=2)
print(f"\n✅ Manifest written: {manifest_path}")
print(f"   Models in: {MODELS_DIR}/")
print("\nCategory map:")
for k, v in manifest.items():
    print(f"  {k:12s} → {v['archetypes']}")
