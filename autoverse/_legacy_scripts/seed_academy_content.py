import sqlite3
import json
import os

def seed_academy_content():
    conn = sqlite3.connect('autoverse.db')
    db = conn.cursor()

    # Course 1: Car Basics
    # Lesson: How Does an Engine Work?
    l1_content = {
      "slides": [
        {
          "type": "intro",
          "heading": "How a 4-Stroke Engine Works",
          "body": "Every petrol engine works on the same principle — internal combustion. It turns chemical energy from fuel into physical motion.",
          "image_url": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=1200&h=700&fit=crop",
          "image_caption": "Cross-section of a high-performance engine"
        },
        {
          "type": "concept",
          "heading": "Stroke 1: Intake",
          "body": "The piston moves DOWN. The intake valve opens. Air and fuel rush into the cylinder through the vacuum created.",
          "diagram": "intake",
          "key_point": "Piston down = air+fuel in"
        },
        {
          "type": "concept", 
          "heading": "Stroke 2: Compression",
          "body": "Both valves close. Piston moves UP. The air-fuel mixture is compressed to a tiny fraction of its volume, preparing for a powerful bang.",
          "diagram": "compression",
          "key_point": "Higher compression = more power"
        },
        {
          "type": "concept",
          "heading": "Stroke 3: Power (Combustion)",
          "body": "Spark plug fires. The controlled explosion forces the piston DOWN with enormous force. This is where your horsepower comes from.",
          "diagram": "combustion",
          "key_point": "This stroke makes ALL the power"
        },
        {
          "type": "concept",
          "heading": "Stroke 4: Exhaust",
          "body": "Exhaust valve opens. Piston moves UP again, pushing burnt gases out. The cycle repeats thousands of times per minute.",
          "diagram": "exhaust",
          "key_point": "What you hear from the exhaust pipe"
        },
        {
          "type": "stat_card",
          "heading": "Engine by the Numbers",
          "stats": [
            {"label": "RPM in a road car", "value": "6,000-7,000"},
            {"label": "RPM in an F1 car",  "value": "15,000+"},
            {"label": "Pistons in a V8",   "value": "8"}
          ]
        }
      ]
    }

    # Update Lesson 1
    db.execute("UPDATE academy_lessons SET content_json = ? WHERE slug = ?", (json.dumps(l1_content), 'engine-works'))

    # F1 Fundamentals Lesson
    f1_intro_content = {
      "slides": [
        {
          "type": "intro",
          "heading": "What is Formula One?",
          "body": "Formula One is the pinnacle of motorsport. 'Formula' refers to the set of rules all cars must comply with.",
          "image_url": "https://images.unsplash.com/photo-1541773079-82de5b9e4e4a?w=1200&h=700&fit=crop"
        },
        {
          "type": "concept",
          "heading": "DRS (Drag Reduction System)",
          "body": "A movable rear wing flap that opens to reduce drag, adding up to 20km/h on straights. Used for overtaking.",
          "key_point": "Flap open = Less drag, More speed"
        }
      ]
    }
    db.execute("UPDATE academy_lessons SET content_json = ? WHERE slug = ?", (json.dumps(f1_intro_content), 'f1-intro'))

    conn.commit()
    conn.close()
    print("Academy content updated with real data.")

if __name__ == "__main__":
    seed_academy_content()
