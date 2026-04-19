import sqlite3
import json
import random

def populate():
    conn = sqlite3.connect('autoverse.db')
    cursor = conn.cursor()

    # Clear existing to prevent duplicates during testing (optional, but cleaner for a refresh)
    # cursor.execute("DELETE FROM academy_courses")
    # cursor.execute("DELETE FROM academy_lessons")
    # cursor.execute("DELETE FROM academy_questions")

    phases = [
        {
            "name": "Phase 1: The Beginner",
            "courses": [
                {
                    "title": "Module 1: ICE Basics",
                    "slug": "ice-basics",
                    "desc": "Understand the 4-stroke cycle and basic engine anatomy.",
                    "topics": ["Intake Stroke", "Compression Stroke", "Power Stroke", "Exhaust Stroke", "Pistons & Crankshafts", "Valvetrain Fundamentals"]
                },
                {
                    "title": "Module 2: Fluids & Vital Signs",
                    "slug": "fluids-survival",
                    "desc": "Checking and changing oil, coolant, and brake fluids.",
                    "topics": ["Oil Viscosity", "Coolant Chemistry", "Hydraulic Brake Fluid", "Power Steering Systems", "Leak Detection", "Warning Lights"]
                },
                {
                    "title": "Module 3: Wheels & Tires",
                    "slug": "wheels-tires",
                    "desc": "Tire sidewalls, pressure management, and changing flats.",
                    "topics": ["Sidewall Decoding", "Load Index", "UTQG Ratings", "Pressure & Temperature", "TPMS Sensors", "Emergency Tire Changes"]
                }
            ]
        },
        {
            "name": "Phase 2: The Intermediate",
            "courses": [
                {
                    "title": "Module 4: Electrical Nervous System",
                    "slug": "electrical-diagnostics",
                    "desc": "Batteries, alternators, and basic multimeter debugging.",
                    "topics": ["Voltage vs Amperage", "Parasitic Draw", "Alternator Ripple", "Fusible Links", "Grounding Issues", "Relay Operations"]
                },
                {
                    "title": "Module 5: Scanning & Diagnostics",
                    "slug": "obd-diagnostics",
                    "desc": "OBD-II scanners and deciphering check engine codes.",
                    "topics": ["P-Codes Decoding", "Fuel Trims", "O2 Sensor Data", "MAFS vs MAP", "Mode $06 Data", "Freeze Frame Analysis"]
                },
                {
                    "title": "Module 6: Suspension & Braking",
                    "slug": "suspension-brakes",
                    "desc": "Replacing brake pads, rotors, and shock absorber mechanics.",
                    "topics": ["Brake Fade Physics", "McPherson Struts", "Multi-link Geometry", "Camber & Toe", "ABS Pump Logic", "Torque Specs Importance"]
                }
            ]
        },
        {
            "name": "Phase 3: The Advanced",
            "courses": [
                {
                    "title": "Module 7: Forced Induction",
                    "slug": "engine-management",
                    "desc": "Turbos, Superchargers, Air-Fuel Ratios (AFR), and ECU remapping.",
                    "topics": ["Turbo Lag Mitigation", "Wastegate Duty Cycle", "Stoichiometric AFR", "Ignition Timing Advance", "Volumetric Efficiency", "Anti-Lag Systems"]
                },
                {
                    "title": "Module 8: Aerodynamics",
                    "slug": "aero-dynamics",
                    "desc": "Downforce, drag coefficients, and weight transfer physics.",
                    "topics": ["Venturi Effect", "Boundary Layer Separation", "Roll Center Migration", "Center of Pressure", "Computational Fluid Dynamics", "Gurney Flaps"]
                },
                {
                    "title": "Module 9: EV & Hybrid Engineering",
                    "slug": "ev-hybrid-future",
                    "desc": "Battery chemistry, regenerative braking, and high-voltage safety.",
                    "topics": ["Lithium-Ion Chemistry", "Inverter Pulse Modulation", "Regen Braking Torque", "Cell Balancing", "Thermal Runaway Prevention", "Permanent Magnet Motors"]
                },
                {
                    "title": "Module 10: F1 Telemetry Masterclass",
                    "slug": "f1-telemetry-mastery",
                    "desc": "Mastering the Apex: Professional telemetry analysis using FastF1.",
                    "topics": ["Speed Trace Interpretation", "Throttle & Brake Overlap", "Gear Sync Telemetry", "DRS Activation Windows", "Tire Surface Temps", "Fuel Flow Rate Analysis"]
                }
            ]
        }
    ]

    order_counter = 1
    for phase_idx, phase in enumerate(phases):
        difficulty = "beginner" if phase_idx == 0 else "intermediate" if phase_idx == 1 else "expert"
        
        for course_data in phase["courses"]:
            # Insert Course
            cursor.execute("""
                INSERT OR IGNORE INTO academy_courses (title, slug, description, category, difficulty, total_xp, icon, color, order_num)
                VALUES (?, ?, ?, 'engineering', ?, ?, ?, ?, ?)
            """, (
                course_data["title"],
                course_data["slug"],
                course_data["desc"],
                difficulty,
                0, # Will update later
                "🛠️",
                "#e83a3a",
                order_counter
            ))
            course_id = cursor.lastrowid or cursor.execute("SELECT id FROM academy_courses WHERE slug=?", (course_data["slug"],)).fetchone()[0]
            order_counter += 1

            # Generate ~111+ Lessons per Course to reach 1000 total
            for i in range(1, 115):
                topic = random.choice(course_data["topics"])
                title = f"{topic}: Deep Dive {i}"
                l_slug = f"{course_data['slug']}-lesson-{i}"
                xp = random.choice([50, 75, 100, 150])
                
                # Sample content generation
                content_body = f"Welcome to the {title}. This high-fidelity module explores the technical intricacies of {topic} as used in modern automotive engineering and high-performance racing. We analyze raw telemetry patterns and component metallurgy to understand how this system contributes to overall vehicle dynamics and thermal efficiency."
                
                cursor.execute("""
                    INSERT INTO academy_lessons (course_id, title, slug, lesson_type, content_json, xp_reward, order_num)
                    VALUES (?, ?, ?, 'learn', ?, ?, ?)
                """, (
                    course_id,
                    title,
                    l_slug,
                    json.dumps({"body": content_body}),
                    xp,
                    i
                ))
                lesson_id = cursor.lastrowid

                # Add 3 questions per lesson
                for q_idx in range(1, 4):
                    cursor.execute("""
                        INSERT INTO academy_questions (lesson_id, question_type, question, options_json, correct_answer, explanation, xp_reward)
                        VALUES (?, 'multiple_choice', ?, ?, ?, ?, ?)
                    """, (
                        lesson_id,
                        f"Technical Assessment for {topic} (Part {q_idx})",
                        json.dumps(["Option A", "Option B", "Option C", "Option D"]),
                        "Option A",
                        f"This correct answer reflects the fundamental mechanical laws governing {topic}.",
                        10
                    ))

            # Update Course XP
            cursor.execute("UPDATE academy_courses SET total_xp = (SELECT SUM(xp_reward) FROM academy_lessons WHERE course_id=?) WHERE id=?", (course_id, course_id))

    conn.commit()
    conn.close()
    print("Academy v3 populated with 1000+ lessons across 3 Phases.")

if __name__ == "__main__":
    populate()
