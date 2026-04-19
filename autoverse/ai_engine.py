"""
ai_engine.py — AutoVerse Guide
Free AI powered by G4F, enriched with F1/Automotive knowledge base.
"""
import json
import re

try:
    import g4f
    from g4f.client import Client
    client = Client()
    G4F_AVAILABLE = True
except Exception:
    G4F_AVAILABLE = False

SYSTEM_PROMPT = """
You are 'AutoVerse Guide', an elite AI expert in:
- Formula 1 racing: strategy, regulations, team/driver performance, telemetry analysis
- Automotive engineering: powertrains, aerodynamics, materials, EV tech
- Car buying/valuation: market prices, comparisons, specs
- F1 history: champions, records, legendary races

Answer clearly and concisely. No markdown bold or headers. Plain text only.
When discussing telemetry, reference speed, throttle, gear changes, and lap times.
"""

# Expanded knowledge base with F1, automotive, and car data
KNOWLEDGE_BASE = {
    # F1 Technical
    "drs": "DRS (Drag Reduction System) opens a flap in the rear wing, reducing drag by ~15-25 points of downforce. Drivers can activate it within 1 second of the car ahead in designated zones, typically gaining 10-12 km/h. It was introduced in 2011 to aid overtaking.",
    "ers": "ERS (Energy Recovery System) stores energy from braking and exhaust heat. Drivers get about 33 seconds of extra power per lap from the MGU-K unit, deploying up to 120kW (160hp). Strategic deployment around corners and straights can mean 0.5s lap gains.",
    "drs zone": "DRS zones are designated straights where following drivers within 1 second of the car ahead can activate their drag reduction flap. Monaco has none. Monza has two. Bahrain has three.",
    "undercut": "The undercut is a pit strategy where a driver pits earlier than the competitor to gain track position using fresh tyres. The new rubber gives 2-3 seconds per lap advantage. The car behind pits, goes fast on fresh rubber, and emerges ahead after the leader pits.",
    "overcut": "The overcut is pitting later than the competitor, betting that staying out on degrading tyres while they're in the garage means you emerge ahead. Works best on circuits with slow pit lanes like Monaco.",
    "ground effect": "Ground effect uses the car's flat floor and Venturi tunnels to generate downforce by creating low-pressure zones under the car. 2022 regulations returned full ground effect. It generates 30-40% of a modern F1 car's total downforce.",
    "porpoising": "Porpoising is vertical oscillation caused by ground effect floors stalling at high speed. The low-pressure zones collapse, reducing downforce suddenly, then rebuild — causing a bouncing motion. It plagued early 2022 season cars.",
    "telemetry": "F1 telemetry captures 150+ data channels at 100Hz: speed, throttle, brakes, steering angle, gear, tyre temps, suspension travel, fuel load, DRS state. Teams transmit over 3GB of data per car per race weekend to their engineers.",
    "tyre compound": "F1 runs 5 dry compounds from C1 (hardest) to C5 (softest). Pirelli selects 3 per race weekend. Softer tyres give more grip but degrade faster. Strategies balance pace vs compounds on a given circuit's surface and temperature.",
    "power unit": "Modern F1 power units are 1.6L turbocharged V6 engines producing ~850HP from the internal combustion element alone. Combined with ERS (MGU-K + MGU-H), total power output exceeds 1,000HP. Thermal efficiency reached 50%+ — double that of road cars.",

    # Drivers
    "verstappen": "Max Verstappen holds 3 consecutive World Championships (2021-23) and won a record 19 races in 2023. Drives RB20 for Red Bull Racing. Known for aggressive trail-braking and exceptional wet-weather performances.",
    "hamilton": "Lewis Hamilton has 7 World Championships (joint record with Schumacher), 103 race wins, and 104 pole positions. Moved to Ferrari in 2025. Renowned for tire management, qualifying pace, and racecraft.",
    "norris": "Lando Norris claimed his first Grand Prix win at Miami 2024. Drive for McLaren MCL38. Strong in wet conditions and known for exceptional raw pace in qualifying.",
    "leclerc": "Charles Leclerc is a two-time Bahrain GP winner and 2024 Monaco GP winner. Drives for Ferrari and is known for pure qualifying speed — often extracting maximum from the car.",
    "schumacher": "Michael Schumacher won 7 World Titles with Benetton (1994, 1995) and Ferrari (2000-2004). 91 race wins. His technical feedback to engineers and relentless work ethic were legendary.",
    "senna": "Ayrton Senna won 3 championships (1988, 1990, 1991) with McLaren. 65 race wins. Held the record for most pole positions until Schumacher broke it. Famous for his rain-driving mastery at Monaco.",

    # Cars
    "9ff gt9-r": "The 9ff GT9-R is a hypercar tuner built on a Porsche 997 chassis by German company 9ff. It was once the world's fastest car, reaching 409 km/h. Powered by a twin-turbo flat-six producing over 1,120hp. Only 20 units were built.",
    "bugatti chiron": "The Bugatti Chiron uses an 8.0L quad-turbocharged W16 engine producing 1,479hp. It has a top speed of 420 km/h (verified on oval track in Super Sport 300+ spec). Price: ~$3 million USD.",
    "rimac nevera": "The Rimac Nevera is a Croatian electric hypercar producing 1,914hp from four motors. 0-100 km/h in 1.81 seconds, 1/4 mile in 8.58 seconds. Top speed 412 km/h. First fully electric production hypercar to outperform combustion classics.",
    "ferrari laferrari": "The LaFerrari is a V12 hybrid hypercar producing 963hp total (800hp from the V12 + 163hp from KERS HY-KERS). 0-100 in under 3 seconds. Only 499 hardtop + 210 Aperta convertible units were built.",
    "tesla plaid": "The Tesla Model S Plaid uses three electric motors producing 1,020hp. 0-100 km/h in 2.1 seconds. First production car to run a sub-9.2 second 1/4 mile. Uses carbon-sleeved motor rotors spinning at 20,000 RPM.",
    "mclaren f1": "The McLaren F1 (1992-1998) was the world's fastest production car at 391 km/h. Central driver's seat, gold-lined engine bay for heat reflection, BMW S70/2 V12 engine. Gordon Murray's masterpiece. Only 106 built.",
    "porsche 918": "The Porsche 918 Spyder is a plug-in hybrid hypercar producing 887hp from a 4.6L V8 + two electric motors. Set the Nurburgring production car lap record at 6:57 in 2013. Only 918 units produced.",
}

def _knowledge_lookup(user_message: str) -> str | None:
    """Search knowledge base for relevant answers."""
    msg_lower = user_message.lower()
    best_match = None
    best_score = 0
    for key, answer in KNOWLEDGE_BASE.items():
        words = key.split()
        score = sum(1 for w in words if w in msg_lower)
        if score > best_score:
            best_score = score
            best_match = answer
    return best_match if best_score > 0 else None


def generate_ai_response(user_message: str, conversation_history=None) -> str:
    """
    Generates a response using G4F providers, falling back to local knowledge base.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if conversation_history:
        messages.extend(conversation_history[-6:])  # Keep last 6 turns for context
    messages.append({"role": "user", "content": user_message})

    if G4F_AVAILABLE:
        providers_to_try = [
            (g4f.Provider.Blackbox, "gpt-4o"),
            (g4f.Provider.DuckDuckGo, "gpt-4o-mini"),
        ]
        for provider, model in providers_to_try:
            try:
                response = client.chat.completions.create(
                    model=model,
                    provider=provider,
                    messages=messages,
                    timeout=15
                )
                content = response.choices[0].message.content
                if content and len(content.strip()) > 10:
                    content = re.sub(r'\*+', '', content)
                    content = re.sub(r'^#+\s*', '', content, flags=re.MULTILINE)
                    content = content.replace('`', '').strip()
                    return content
            except Exception as e:
                print(f"G4F provider {provider.__name__} failed: {e}")
                continue

    # Knowledge base fallback
    kb_answer = _knowledge_lookup(user_message)
    if kb_answer:
        return kb_answer

    return ("I'm currently running diagnostics on my telemetry feed. "
            "I can answer questions about F1 strategy, car specifications, "
            "driver comparisons, and automotive engineering. What would you like to know?")
