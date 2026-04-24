import sqlite3
import json
import os

DB_PATH = "autoverse.db"

SYLLABUS = [
    {"id": 301, "name": "The Engine: Thermodynamics & Block", "slug": "engine-thermo", "keywords": ["Otto Cycle", "Compression Ratio", "Thermal Efficiency", "Volumetric Efficiency"]},
    {"id": 302, "name": "Fuel Systems: Mix & Atomization", "slug": "fuel-systems", "keywords": ["Stoichiometric Ratio", "Direct Injection", "Venturi Effect", "Fuel Atomization"]},
    {"id": 303, "name": "Ignition: Spark Timing & Theory", "slug": "ignition-theory", "keywords": ["Ignition Advance", "Knock Sensor", "Combustion Propagation", "Plasma Ignition"]},
    {"id": 304, "name": "Cooling: Heat Exchange & Airflow", "slug": "cooling-heat", "keywords": ["Convective Cooling", "Heat Exchanger", "Thermostat Logic", "Aero-thermal Management"]},
    {"id": 305, "name": "Lubrication: Viscosity & Flow", "slug": "oil-viscosity", "keywords": ["Hydrodynamic Lubrication", "Shear Strength", "Viscosity Index", "Dry Sump Systems"]},
    {"id": 306, "name": "Clutch & Manual Transmission", "slug": "clutch-gearbox", "keywords": ["Coefficient of Friction", "Torque Capacity", "Synchromesh Logic", "Gear Ratio Calculus"]},
    {"id": 307, "name": "Automatic & Torque Converters", "slug": "auto-trans", "keywords": ["Planetary Gearsets", "Fluid Coupling", "Impeller Dynamics", "Lock-up Clutch"]},
    {"id": 308, "name": "Driveshafts & Final Drive", "slug": "driveshaft-drive", "keywords": ["Angular Velocity", "Differential Lock", "Torque Vectoring", "Universal Joints"]},
    {"id": 309, "name": "Steering Geometry & Rack Physics", "slug": "steering-physics", "keywords": ["Ackermann Geometry", "Caster Angle", "Scrub Radius", "Self-Centering Torque"]},
    {"id": 310, "name": "Suspension: Spring & Damper Dynamics", "slug": "suspension-dyn", "keywords": ["Spring Rate (K)", "Damping Coefficient", "Anti-Squat Geometry", "Unsprung Mass"]},
    {"id": 311, "name": "Braking: Hydraulic & ABS Logic", "slug": "braking-logic", "keywords": ["Pascal's Principle", "Brake Fade", "Kinetic Energy Recovery", "Thermal Dissipation"]},
    {"id": 312, "name": "Electrical Architecture & CAN-bus", "slug": "electrical-canbus", "keywords": ["Multiplexing", "Signal Latency", "Voltage Regulation", "EMI Shielding"]}
]

def generate_elite_curriculum():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try: cursor.execute("ALTER TABLE academy_lessons ADD COLUMN is_premium INTEGER DEFAULT 0;")
    except: pass

    lessons = []
    questions = []

    for s in SYLLABUS:
        for i in range(1, 31):
            lesson_id = (s['id'] * 1000) + i
            title = f"{s['name']} (Unit {i:02d})"
            k1, k2 = s['keywords'][i % 2], s['keywords'][(i+2) % 4]
            
            content = json.dumps({
                "sections": [
                    {"title": "Technical Objective", "content": f"Analyzing the role of <strong>{k1}</strong> in achieving peak performance for the {s['name']} subsystem."},
                    {"title": "Core Engineering Theory", "content": f"The physics of <strong>{k2}</strong> dictates the operational efficiency of this module. By managing the delta between input variables and environmental constraints, we optimize the entire vehicle lifecycle."},
                    {"title": "Case Study: F1 Engineering", "content": f"In Formula One, <strong>{k1}</strong> is monitored at 1000Hz via CAN-bus telemetry to ensure the car stays within its optimal thermal and mechanical window."},
                    {"title": "Summary", "content": f"A mastery of <strong>{k1}</strong> and <strong>{k2}</strong> is essential for any elite automotive engineer or researcher."}
                ]
            })
            
            is_premium = 1 if i > 20 else 0 
            lessons.append((lesson_id, s['id'], title, f"{s['slug']}-unit-{i}", content, i, is_premium))
            
            questions.append((
                lesson_id * 10, lesson_id, "multiple_choice",
                f"How does <strong>{k1}</strong> directly affect the efficiency of this system?",
                json.dumps(["By reducing thermal parasitic loss", "By increasing mass flow rate", "By optimizing kinetic conversion", "All of the above"]),
                "All of the above",
                f"{k1} is a critical variable that influences multiple vectors of automotive efficiency.",
                500
            ))

    cursor.executemany("INSERT OR REPLACE INTO academy_lessons (id, course_id, title, slug, content_json, order_num, is_premium) VALUES (?, ?, ?, ?, ?, ?, ?)", lessons)
    cursor.executemany("INSERT OR REPLACE INTO academy_questions (id, lesson_id, question_type, question, options_json, correct_answer, explanation, xp_reward) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", questions)
    conn.commit()
    conn.close()
    print("SUCCESS: 360 Optimized Technical Lessons injected.")

if __name__ == "__main__":
    generate_elite_curriculum()
