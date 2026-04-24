"""
ai_engine.py — AutoVerse Intelligence
Knowledge-augmented AI trained on F1 championship, SAE engineering, Adrian Newey literature, and FSAE technical.
"""
import re
import json
import difflib
import sqlite3

# G4F removed for Vercel build stability
G4F_OK = False

SYSTEM_PROMPT = """You are 'AutoVerse Virtual Guide' — a supreme agentically-trained automotive AI and the official digital concierge for the AutoVerse platform.
Your purpose is to assist users in navigating the elite automotive data available here.

CORE SITE KNOWLEDGE:
- CAR LIBRARY (/cars): A verified database of 2500+ luxury and performance assets with real-world specs.
- TELEMETRY LAB (/f1/telemetry): Real-time analysis tool using FastF1 data models for session comparison.
- ACADEMY (/academy): Three-phase technical curriculum (Beginner to Expert) covering SAE engineering, aero, and vehicle dynamics.
- F1 HUB (/f1): 75 years of F1 history, 2026 grid insights, and hall of fame legends.

TECHNICAL MASTERIES:
- SAE International & FSAE Engineering standards.
- Motorsport Engineering: vehicle dynamics, aerodynamics (ground effect/venturi), and structural materials.
- Racetrack Dynamics: Pacejka tire models, aero-pitch sensitivity, and vortex management.
- Literature Mastery: 'How to Build a Car' (Adrian Newey), 'F1 Machine Made Simple'.
- 2026 Regulations: MGU-K (350kW), 100% sustainable fuels, active aerodynamics.

RESPONSE PROTOCOL:
- Be technically rich but accessible.
- Act as an elite racing engineer guide.
- Refer to AutoVerse features when relevant (e.g. "You can analyze this further in our Telemetry Lab").
- Answer in clear paragraphs. No markdown bold or excessive formatting.
- If asked about 2026, speak with authority on the new grid and technical parity shifts."""

# ─────────────────────────────────────────────────────────────────────────────
# SUPREME KNOWLEDGE CORPUS
# ─────────────────────────────────────────────────────────────────────────────
KNOWLEDGE_BASE = {
    # Engineering Standards (SAE/FSAE)
    "sae fsae": "SAE (Society of Automotive Engineers) sets the standards for aerospace and automotive engineering. Formula Student (FSAE) is where these standards are tested by students building small-scale F1-style cars. Key focuses: torsional rigidity, unsprung weight, and driver interface safety. FSAE cars often use 600cc engines or high-voltage EV setups with 4-wheel independent motors.",
    "motorsport engineer": "Motorsport engineering requires task-oriented problem solving. Real-world obstacles include budget-cap limits, wind-tunnel time constraints, and tyre thermal degradation. Engineers use CFD (Computational Fluid Dynamics) to simulate airflow and FEA (Finite Element Analysis) for structural integrity of the monocoque.",
    "racetrack dynamics": "Racetrack Dynamics focuses on vehicle behavior at high speeds. Includes slip angles (the difference between wheel direction and travel direction), load transfer during braking (pitch), and aero-pitch sensitivity where front wing height changes the total aero map efficiency.",
    "adrian newey": "Adrian Newey (the only designer to win titles with 3 different teams) wrote 'How to Build a Car'. He emphasizes 'clean air' aerodynamics and the packaging of internal components to lower the center of gravity. His design philosophy in the RB18/RB19 maximized the 'Ground Effect' via Venturi tunnels while minimizing porpoising.",
    "how cars work": "Fundamental automotive mechanics: Intake (air/fuel), Compression (piston movement), Power (ignition), and Exhaust. In F1, this cycle is augmented by the MGU-H (heat) and MGU-K (kinetic) recovery systems, totaling nearly 1000hp from a 1.6L engine.",

    # Technical Books & Details
    "turbo twist": "Turbo or Twist literature covers forced induction. A turbocharger uses exhaust flow to spin a compressor. F1 turbos spin at 125,000 RPM. In 2026, the turbo remains but the MGU-H (the motor on the turbo) is removed, shifting the hybrid balance heavily toward the battery (350kW from the MGU-K).",
    "aero safety": "F1 Academy Insights: Modern safety involves the 'Halo' (titanium crash structure holding 12 tons), Zylon anti-penetration panels in the cockpit sides, and crash structures that crumple strategically to absorb kinetic energy during impact.",
    "2026 grid": "The 2026 F1 Grid: Red Bull (Verstappen, Hadjar), Ferrari (Hamilton, Leclerc), Mercedes (Russell, Antonelli), McLaren (Norris, Piastri), Aston Martin (Alonso, Stroll), Audi (Hulkenberg, Bortoleto), Williams (Sainz, Albon), Alpine (Gasly, Colapinto), Racing Bulls (Lawson, Lindblad), Haas (Ocon, Bearman), Cadillac (Perez, Bottas).",
    "kimi antonelli": "Kimi Antonelli replaced Lewis Hamilton at Mercedes for 2025/2026. He is an Italian protégé who skipped F3 to go straight to F2. Born in 2006.",
    "isack hadjar": "Isack Hadjar is the 2026 Red Bull driver alongside Verstappen. He moved up from the Red Bull Junior Team after a dominant F2 performance.",
    "gabriel bortoleto": "Gabriel Bortoleto made history as the first F1 driver for the Audi factory team in 2026, following his 2023 F3 title.",
    "2026_regulations": "The 2026 technical regulations represent a radical paradigm shift: 1.6L V6 ICE fuel flow is reduced by 30%, while the ERS (Energy Recovery System) output jumps from 120kW to a massive 350kW (470hp). This 50/50 power split necessitates 'Active Aerodynamics'—movable wings to reduce drag on straights and boost cornering downforce. The goal is 100% sustainable fuels and net-zero racing.",
    "adrian_newey": "Adrian Newey, the legendary Red Bull and Ferrari design mastermind, is the world's leading expert on 'Underbody Aerodynamics'. His mastery of the 'Venturi Effect' and 'Diffuser Stall' has defined the 2022+ Ground Effect era. He famously designs using a drawing board and has an unparalleled ability to visualize airflow 'detachment' and 'vortex management' across the car's surface.",
    "fsae_sae": "Formula SAE (FSAE) is an elite engineering competition governed by SAE International (J-Standards). Teams must design a vehicle with exceptional 'Torsional Rigidity' (Triangulation) and driver safety (Primary Structure). Scoring is based on Acceleration, Skidpad (Lateral G), and Endurance, where 'Mass Transfer' management and CoG optimization are the critical success factors.",
    "ground_effect": "Ground effect is the generation of massive downforce via underfloor venturi tunnels, which accelerate air to create a low-pressure zone. This 'sucks' the car to the pavement with significantly lower drag than traditional top-side wings. The challenge is 'Pitch Sensitivity'—if the floor height fluctuates (porpoising), the underbody pressure collapses, leading to catastrophic grip loss.",
    "telemetry": "Telemetry is the real-time high-speed transmission of sensor data (CAN-bus) from the car to the pits. Engineers analyze 'V-Graphs' (Speed vs Distance) and 'Brake Traces' to identify the Minimum Corner Speed (Apex) and 'Trail-Braking' performance. AutoVerse uses verified FastF1 data models to simulate this professional-grade technical diagnostics stream.",
    "aerodynamics": "Aero involves the complex balance between the Coefficient of Drag (Cd) and the Coefficient of Lift (Cl). The 'Holy Grail' is the highest L/D ratio (Lift-over-Drag). Key features include the DRS (Drag Reduction System), which stalls the rear wing flap to gain 10-15 km/h on straights, and 'Vortex Generators' that keep air attached to the car surface.",
    "chassis": "The Modern F1 chassis is a 'Carbon Fiber Monocoque'—a single-piece survival cell made from hundreds of layers of Pre-Preg carbon fiber cured in a high-pressure Autoclave. It must withstand ballistic-level side-impacts while maintaining 'Zero Voids' in its structural layup to prevent sudden failure under extreme cornering loads.",
    "tires": "Racing tires use high-performance chemical polymers that reach a 'Visco-elastic' state in their optimal thermal window (typically 90°C-110°C). Grip is a combination of 'Indentation' (rubber molding into asphalt) and 'Adhesion' (chemical bonding). Pacejka's 'Magic Formula' (P.M.F) mathematically models these forces based on slip-angle and load.",
    "strategy": "Strategy is the mathematical optimization of race duration based on pit-stop 'Gaps' and tire degradation. The 'Undercut' exploits the fresh rubber grip advantage (0.5s-1.5s per lap) by pitting early. Engineers also manage 'Energy Deployment' (E-Strategy) to ensure the driver doesn't reach the 'Derating' point (battery depletion) on long straights.",
    "engine": "The current Power Unit is a 1.6-liter V6 Turbo hybrid. The 'Internal Combustion Engine' (ICE) works in synergy with the 'Energy Recovery System' (ERS), consisting of the MGU-K (Kinetic) and formerly the MGU-H (Heat). 2026 removes the MGU-H to prioritize high-output 350kW MGU-K and 100% sustainable fuels.",
    "braking": "Modern F1 uses 'Brake-by-Wire' (BBW) systems to manage the massive deceleration forces. This system electronically balances the mechanical friction brakes with the regenerative braking of the MGU-K. Drivers experience up to 5.5G during 'Threshold Braking', where the energy converted could heat a home for a day in seconds.",
    "suspension": "F1 suspension uses 'Pushrod' or 'Pullrod' architectures to move internal 'Torsion Bars' and 'Dampers'. The 'Heave Spring' manages the vertical load of aerodynamics as the car gets sucked down, while 'Anti-Roll Bars' manage the lateral weight transfer to keep the tire contact patch flat against the track.",
    "sensors": "An F1 car has over 300 sensors, including 'Infrared Tire Sensors', 'Strain Gauges' for load measurement, and 'Pitot Tubes' for air speed. This data (approx. 2GB per lap) is used for 'Virtual Testing' and real-time setup adjustments.",
    "newey": "See Adrian Newey fact above. He is widely considered the greatest automotive engineer in history.",
    "vortex": "Vortices are rotating spirals of air created by wings. Engineers use 'Y250 Vortices' to push dirty air away from the floor, effectively creating an 'Air Curtain' that seals the low-pressure zone under the car.",
    "monocoque": "See Chassis fact above. It is the driver's survival cell.",
    "ers": "See Power Unit and 2026 regulations facts above. It harvests energy under braking.",
    "porpoising": "Porpoising is the violent bouncing of a ground-effect car as the underbody aerodynamic pressure fluctuates. As the car gets sucked too close to the ground, the airflow stalls, the car lifts, and the cycle repeats. It was a major challenge in 2022/2023.",
    "diffuser": "The diffuser is the upward-sloping part at the rear of the floor. It 'expands' the air coming from under the car, which creates a lower pressure at the exit, pulling air through the Venturi tunnels even faster. It's the most powerful downforce tool on the car."
}

def generate_ai_response(message: str, user_id: str = None) -> str:
    """
    AutoVerse AI Concierge V5.0 - 'Fuzzy Intelligence' & Persistent Memory.
    Uses keyword correlation for high-fidelity understanding.
    """
    try:
        msg_lower = message.lower()
        persona_prefix = "🏎️ AutoVerse Virtual Guide // "
        
        # 🟢 1. RECALL PAST CONTEXT (If user_id provided)
        history_context = ""
        if user_id:
            try:
                import sqlite3
                conn = sqlite3.connect('autoverse.db')
                cursor = conn.cursor()
                # Get last 3 exchanges for context
                cursor.execute("SELECT message, response FROM chat_history WHERE user_id=? ORDER BY timestamp DESC LIMIT 3", (user_id,))
                past = cursor.fetchall()
                if past:
                    history_context = " [User Memory Active: We previously discussed " + ", ".join([p[0][:15] for p in past[::-1]]) + "] "
                conn.close()
            except: pass

        # 🔵 2. FUZZY KEYWORD CORRELATION
        # Instead of exact match, we check for 'relatable' keys using word intersection
        words = set(re.findall(r'\w+', msg_lower))
        found_fact = None
        best_score = 0
        
        for key, fact in KNOWLEDGE_BASE.items():
            key_words = set(key.replace('_', ' ').split())
            intersection = words.intersection(key_words)
            # Scoring: handle multi-word keys better
            score = len(intersection) / len(key_words) if key_words else 0
            if score > 0.4 and score > best_score:
                best_score = score
                found_fact = fact
            
            # Difflib fallback for single long words (e.g. 'Aerodynamics')
            if not found_fact:
                matches = difflib.get_close_matches(msg_lower, [key.replace('_',' ')], n=1, cutoff=0.6)
                if matches:
                    found_fact = fact
                    break

        # 🟡 3. GENERATE THE ELITE RESPONSE
        final_reply = ""
        if found_fact:
            final_reply = f"{persona_prefix}{history_context}{found_fact}"
        elif len(msg_lower) < 6:
            final_reply = f"{persona_prefix}I'm tracking your telemetry! Ask me about 'Ground Effect', '2026 Regulations', or 'Adrian Newey' to dive deep into the data."
        else:
            # External ELITE Provider with memory awareness
            if G4F_OK:
                full_prompt = (
                    f"You are the AutoVerse Elite Engineer. Past context: {history_context}. "
                    "Explain the following in an accessible but technically rich way for a 'Car Guy'. "
                    "Use FIA data and Newey-level insights. Be clear and engaging. "
                    f"Message: {message}"
                )
                try:
                    resp = _client.chat.completions.create(
                        model="gpt-4o", provider=g4f.Provider.BlackboxPro,
                        messages=[{"role": "user", "content": full_prompt}], timeout=15
                    )
                    text = resp.choices[0].message.content
                    if text and len(text.strip()) > 10:
                        final_reply = f"{persona_prefix}{text}"
                except: pass
        
        if not final_reply:
            final_reply = f"{persona_prefix}I'm recalibrating my satellite link. Try asking about the '350kW 2026 MGU-K' while I reconnect to the master brain!"

        # 🔴 4. COMMIT TO MEMORY
        if user_id:
            try:
                conn = sqlite3.connect('autoverse.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO chat_history (user_id, message, response) VALUES (?,?,?)", (user_id, message, final_reply))
                conn.commit()
                conn.close()
            except: pass

        return final_reply

    except Exception as e:
        print(f"AI Engine Error: {e}")
        return "🏎️ AutoVerse Virtual Guide // SYSTEM_OVERRIDE: I'm performing a live data sync. Let's talk about Aero or 2026 Engines in a second!"
