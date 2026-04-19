"""
populate_academy_v4.py — AutoVerse PEAK ELITE EDITION (V4.5.1)
The Ultimate "Car Guy" engineering curriculum. 
Massive 5-paragraph deep-dives for ALL 12 modules with 4 high-fidelity quizzes each.
"""
import sqlite3
import json

db = sqlite3.connect('autoverse.db')
cursor = db.cursor()

# Clear existing data
cursor.execute("DELETE FROM academy_questions")
cursor.execute("DELETE FROM academy_lessons")
cursor.execute("DELETE FROM academy_courses")
db.commit()

COURSES = [
    (1, "SAE Engineering Dynamics", "beginner", "society-automotive-engineers", "Deep dive into SAE technical standards and the physics of mass-transfer.", "📐", 1),
    (2, "F1 2026 Power Unit", "intermediate", "f1-power-units", "Mastering the 50/50 ERS balance and 350kW architecture.", "⚡", 2),
    (3, "The Newey Mastery", "expert", "newey-aerodynamics", "Venturi tunnels and pitch-sensitivity in ground-effect cars.", "💨", 3),
    (4, "FSAE Triangulation & Safety", "beginner", "fsae-design", "Understanding structural triangulation and crash-safety spars.", "🔧", 4),
    (5, "Tire Thermodynamics", "intermediate", "racetrack-dynamics", "Thermal windows and the Pacejka 'Magic Formula'.", "🏎️", 5),
    (6, "The Halo Ring & Zylon", "expert", "motorsport-reliability", "Analyzing Titanium stress-loading and ballistic protection.", "🛡️", 6),
    (7, "Composite Engineering", "intermediate", "chassis-engineering", "Autoclave curing and Pre-preg carbon fiber orientation.", "🏗️", 7),
    (8, "Impact Structures", "beginner", "safety-engineering", "Energy attenuation and side-impact survival spars.", "⛑️", 8),
    (9, "Race Strategy: Undercut", "intermediate", "race-strategy", "Fuel-flow limits and the mathematics of the 'Undercut'.", "⏱️", 9),
    (10, "Telemetry V-Graph", "expert", "telemetry-mastery", "Analyzing Minimum Corner Speed and G-force logs.", "📊", 10),
    (11, "F1 Academy: Technical", "beginner", "f1-academy-insights", "Basic aero coefficients and cooling-duct geometry.", "👩‍🎓", 11),
    (12, "2026 Active Aero", "expert", "future-f1-regs", "Analyzing X-mode and Z-mode active aerodynamics.", "🚀", 12),
]

# --- PEAK ELITE CONTENT LIBRARY ---
ELITE_DATA = {
    1: {
        "title": "SAE Mass-Transfer: The Physics of Load",
        "intro": "In the world of high-performance racing, mass-transfer is the silent dictator of speed.",
        "p1": "SAE J-670 describes the fundamental coordinate system used by every automotive engineer in the world. When you slams on the brakes, the car's weight 'dives' forward. This loads the front tires, making them dig into the asphalt. But, if you dive too hard, the rear tires lift and lose their grip, causing the car to spin. SAE J-Standards define the Center of Gravity (CoG) height as the critical variable here.",
        "p2": "A lower CoG means less weight moves around, making the car much more stable and predictable for the driver. Think of it like balancing a tall glass of water vs a half-filled one on a moving tray. In F1, we use ultra-low engine mounts and heavy ballast (often Tungsten) placed at the lowest possible point to combat this SAE-defined phenomenon.",
        "p3": "Load transfer isn't just about front-to-rear; it's also lateral. When you turn, the mass of the car wants to keep going straight (Inertia). This pushes the outside tires into the ground and unloads the inside tires. If the transfer is too violent, the tire's 'Contact Patch' is overwhelmed, leading to understeer. Mastering the 'Roll Center'—the imaginary point about which the car pivots—is critical here.",
        "p4": "At a beginner level, we look at the 'Jerk'—the rate of change of acceleration. A smooth driver minimizes jerk, keeping the tire in a 'Static State' for longer. A rough driver creates 'Dynamic Spikes' that break the tire's chemical bond with the road.",
        "p5": "Finally, we consider Aerodynamic Pitch. At high speeds, the wings add hundreds of kilograms of vertical load. The SAE standards help us distinguish between 'Mechanical Grip' (from springs) and 'Aerosmithing' (from air). Balancing these two is what separates a podium finisher from the rest of the pack.",
        "qs": [
            ("What variable determines the magnitude of load shift according to SAE?", ["Tire size", "CoG Height", "Paint color", "Radiator size"], "CoG Height"),
            ("What is 'Jerk' in vehicle dynamics?", ["Braking force", "Rate of change of acceleration", "The driver's name", "Engine weight"], "Rate of change of acceleration"),
            ("Why is Tungsten used as ballast in F1?", ["It's cheap", "It's extremely dense and lowers the CoG", "It makes the air faster", "It cools the engine"], "It's extremely dense and lowers the CoG"),
            ("What happens to the 'Contact Patch' during violent load transfer?", ["It gets bigger", "It gets overwhelmed and loses grip", "It turns into a liquid", "It disappears"], "It gets overwhelmed and loses grip")
        ]
    },
    2: {
        "title": "F1 2026: The 350kW Hybrid Warfare",
        "intro": "2026 marks the end of the fuel-burn era as we know it.",
        "p1": "The 2026 technical regulations represent the most radical powertrain shift in history. The goal is a 50/50 power split between the Internal Combustion Engine (ICE) and the Energy Recovery System (ERS). The ICE remains a 1.6L V6 Turbo, but its fuel flow is cut by nearly 30% to hit sustainability targets.",
        "p2": "To compensate, the electric motor (MGU-K) power is nearly tripled, jumping from 120kW to a staggering 350kW (470hp). This shift makes 2026 cars essentially 'electric-first' machines on corner exits. The power comes from harvesting energy under braking solely through the MGU-K, since the MGU-H (Heat converter) has been removed for cost reduction.",
        "p3": "Managing 'Derate' or 'Clipping' will be the primary driver challenge. If a driver uses all 350kW too early on a long straight, the battery will deplete before the braking zone, causing the car to lose massive top speed. Strategic energy deployment maps will be the secret weapon of top-tier teams.",
        "p4": "Safety in 2026 is also elevated. Low-voltage and high-voltage (800V+) systems are isolated in a triple-layered carbon-fiber and Zylon safety cell. This ensures that even in a crash, the high-output battery doesn't pose an electrical risk to the driver or marshals.",
        "p5": "Finally, 100% sustainable fuels make their debut. These are carbon-neutral synthetic fuels that deliver the same high-octane performance as traditional gasoline but ensure that F1 leads the world in clean combustion technology.",
        "qs": [
            ("What is the electric power output of the 2026 MGU-K?", ["120kW", "250kW", "350kW", "500kW"], "350kW"),
            ("Which critical component is being REMOVED in 2026?", ["Turbo", "MGU-H", "Battery", "Tires"], "MGU-H"),
            ("What is 'Clipping' in the context of energy management?", ["Cutting the grass", "Battery depletion at the end of a straight", "Hitting a wall", "Faster pit stops"], "Battery depletion at the end of a straight"),
            ("2026 F1 fuel will be:", ["Nitrous", "100% Sustainable/Carbon-Neutral", "Diesel", "Water"], "100% Sustainable/Carbon-Neutral")
        ]
    },
    3: {
        "title": "Newey Mastery: Underbody Aerodynamics",
        "intro": "Adrian Newey doesn't just build cars; he 'listens' to the air.",
        "p1": "Adrian Newey is widely considered the greatest aerodynamicist in F1 history. His mastery of the 2022+ 'Ground Effect' era comes from his understanding of the Venturi floor. Unlike topside wings, the underfloor creates downforce by accelerating air through a narrow throat, creating a low-pressure zone that sucks the car to the road.",
        "p2": "Newey identifies 'Pitch Sensitivity' as the primary enemy of ground effect. If the car’s floor gets too high or too low relative to the track, the airflow can 'detach' or stall. This leads to a sudden loss of downforce, known as porpoising. Managing this requires ultra-stiff suspensions and complex internal damping systems.",
        "p3": "Another Newey secret is 'Vortex Management'. He uses specific winglets and floor edges to generate rotating air spirals (vortices) that act like invisible 'Air Curtains'. These curtains seal the low-pressure zone under the car, preventing 'dirty air' from seeping in and ruining the downforce.",
        "p4": "He also pioneered 'Blown Diffusers' in the past—using the hot, fast exhaust gasses to accelerate air under the car. While now restricted, his ability to find performance in every square millimeter of the car's surface remains unmatched.",
        "p5": "When Newey designs a car, he thinks in three dimensions. He famously uses a drawing board instead of a computer (CAD) for initial layouts, allowing him to 'feel' the flow transitions in a way no algorithm can yet replicate.",
        "qs": [
            ("What is Newey's 'Air Curtain' designed to do?", ["Cool the driver", "Seal the low-pressure zone under the car", "Look cool", "Increase drag"], "Seal the low-pressure zone under the car"),
            ("What is the primary cause of 'Porpoising'?", ["Engine failure", "Fluctuating aerodynamic pressure under the floor", "Soft tires", "Radio interference"], "Fluctuating aerodynamic pressure under the floor"),
            ("Which tool does Adrian Newey famously use for initial designs?", ["iPad", "A traditional Drawing Board", "VR Headset", "AI Generator"], "A traditional Drawing Board"),
            ("What happens if a car is too 'Pitch Sensitive'?", ["It goes faster", "The airflow can detatch or stall", "The engine stalls", "It gets better fuel economy"], "The airflow can detatch or stall")
        ]
    },
    4: {
        "title": "FSAE: Structural Triangulation & Safety",
        "intro": "In FSAE, your chassis is only as good as its triangles.",
        "p1": "Chassis triangulation is the art of ensuring that every load path is supported by a triangular member. Why? Because triangles are the only polygons that are naturally rigid. A square frame can turn into a parallelogram (flexing) under load, but a triangle stays true. For safety, FSAE rules mandate 'Crash Spars' and a 'Primary Structure' that shields the driver.",
        "p2": "If the chassis flexes, your suspension geometry changes mid-corner, and you lose the race. We use Zylon-reinforced panels for added ballistic safety against flying debris. This is critical for Formula Student teams who build their own carbon monocoques from scratch.",
        "p3": "Safety engineering also includes the 'Impact Attenuator'—the nosecone designed to crush at a controlled rate. In a 30km/h impact test, the attenuator must decelerate the car without the main chassis ever deforming, protecting the driver's feet.",
        "p4": "Torsional Rigidity is the measured in Newton-meters per degree (Nm/deg). A higher number means the car is stiffer. In FSAE, we aim for a number that ensures the chassis is at least 10 times stiffer than the suspension springs themselves.",
        "p5": "Finally, the Cockpit Opening. Rules dictate that a driver must be able to exit the car in 5 seconds or less. This ergonomic constraint often clashes with the aerodynamic need for a narrow, slipper cockpit. Engineering is always a trade-off.",
        "qs": [
            ("Why are triangles used in chassis construction?", ["They are cheaper", "They are naturally rigid and prevent flexing", "They weigh more", "To fit more logos"], "They are naturally rigid and prevent flexing"),
            ("What is the 'Impact Attenuator' designed to protect?", ["The engine", "The driver's feet during a crash", "The tires", "The radio"], "The driver's feet during a crash"),
            ("What is a typical exit-time requirement for FSAE cockpits?", ["5 seconds", "30 seconds", "1 minute", "No requirement"], "5 seconds"),
            ("What does a high 'Torsional Rigidity' number indicate?", ["A flexible car", "A stiff and stable chassis", "A heavy interior", "A fast engine"], "A stiff and stable chassis")
        ]
    },
    5: {
        "title": "Tire Thermodynamics: The Magic Formula",
        "intro": "A cold tire is a useless tire in motorsport.",
        "p1": "Tires are the only component of a car that touches the track. Grip is not just 'rubber meeting road'; it is a complex chemical bond. Tires have a 'Thermal Window'—usually between 90°C and 110°C—where the rubber reaches a visco-elastic state, physically interlocking with the microscopic craters in the asphalt.",
        "p2": "Hans B. Pacejka developed the 'Magic Formula' (P.M.F) to calculate exactly how much force a tire can produce. It shows that tires are actually fastest when they are slightly sliding—about 2 to 6 degrees of 'Slip Angle'. If the angle is 0, you aren't turning; if it's 15, you are spinning out.",
        "p3": "Overheating is the enemy. If a tire gets too hot, the rubber 'blisters'—chunks of it literally melt and tear away. This happens because of 'Shear Stress' during high-speed cornering. To cool the tires, drivers will often drive onto the 'dirty' (cooler) part of the track or into wet patches.",
        "p4": "Conversely, 'Graining' happens when the tire is too cold. The rubber is brittle and peels off in little balls, like a pencil eraser. A driver must find the 'Sweet Spot' and stay there for 20+ laps. This is what we call 'Tire Management'.",
        "p5": "Tire air pressure also plays a role. As the air inside heats up, it expands, making the tire harder (higher PSI) and changing the shape of the 'Contact Patch'. Engineers monitor this in real-time using infrared sensors.",
        "qs": [
            ("What is the optimal 'Slip Angle' for maximum tire grip?", ["0 degrees", "2-6 degrees", "20 degrees", "No slip"], "2-6 degrees"),
            ("What happens to tires if they drop below the 'Thermal Window'?", ["They melt", "They become brittle and 'Grain'", "They get stickier", "They turn blue"], "They become brittle and 'Grain'"),
            ("Who created the 'Magic Formula' for tire modeling?", ["Isaac Newton", "Hans B. Pacejka", "Adrian Newey", "Enzo Ferrari"], "Hans B. Pacejka"),
            ("What is 'Blistering' caused by?", ["Too much cooling", "Overheating and melting of the internal rubber", "Low oil", "Rain"], "Overheating and melting of the internal rubber")
        ]
    },
    6: {
        "title": "Ballistics & Reliability: The Halo Shield",
        "intro": "Safety in F1 is automotive bulletproofing.",
        "p1": "Modern F1 reliability isn't just about the engine lasting—it's about the driver surviving. The Halo is a Grade 5 Titanium structure that can withstand 12.5 tons of force. That's like putting a double-decker bus on top of the cockpit without the Halo cracking.",
        "p2": "Underneath the car is the 'Plank'. This is made of Jabroc (processed wood) or composite. Its job is to ensure the car isn't running too low to the ground. If the plank wears away by more than 1mm, the car is disqualified. It ensures a level playing field and consistent floor aerodynamics.",
        "p3": "We also use Zylon panels on the sides of the cockpit. Zylon has a tensile strength 1.6 times higher than Kevlar. Its job is to prevent loose debris—like a flying tire or a shard of carbon fiber—from penetrating the cockpit walls and striking the driver.",
        "p4": "The 'Survival Cell' or Monocoque is designed to be indestructible. In a massive impact, the engine and gearbox are designed to break *away* from the cell, taking their massive kinetic energy with them and leaving the driver safe inside a rigid 'egg'.",
        "p5": "Finally, the Fire Suppression System. If a car detects a fire, it automatically floods the engine bay and cockpit with Novec gas—a high-tech fire extinguisher that is safe for the driver to breathe but instantly kills the flames.",
        "qs": [
            ("What material is the F1 Halo primarily made of?", ["Carbon Fiber", "Grade 5 Titanium", "Steel", "Aluminum"], "Grade 5 Titanium"),
            ("Why is Zylon used in cockpit construction?", ["It's heavy", "It's 1.6x stronger than Kevlar and prevents penetration", "It's transparent", "It's cheaper"], "It's 1.6x stronger than Kevlar and prevents penetration"),
            ("How much wear is allowed on the underbody 'Plank'?", ["None", "Up to 1mm", "10mm", "Unlimited"], "Up to 1mm"),
            ("What is the purpose of the 'Survival Cell'?", ["To store fuel", "To protect the driver as an indestructible rigid box", "To make the car lighter", "To look fast"], "To protect the driver as an indestructible rigid box")
        ]
    },
    7: {
        "title": "Composite Mastery: The Carbon Autoclave",
        "intro": "F1 parts aren't built; they are baked in a high-pressure oven.",
        "p1": "Every F1 car is made of Carbon Fiber, but not all carbon is equal. We use 'Pre-Preg' carbon fiber—the resin is already carefully soaked into the fabric. These layers are meticulously placed by hand into a mold in a 'Clean Room' where even a single speck of dust can cause a part to fail.",
        "p2": "Once laid, the mold is vacuum-sealed and placed into an Autoclave. This is a giant pressure cooker. It uses high heat (135°C+) and high pressure (6-10 bar) to bond the fibers. The pressure is critical—it squeezes out every tiny air bubble (a 'void') between the layers.",
        "p3": "If a part had an air bubble inside, that would be a 'Stress Point'. Under the massive loads of F1 (up to 5G), that bubble would cause the part to snap like a cracker. We aim for 'Zero Voids' for maximum reliability and a strength-to-weight ratio that beats steel by 10 times.",
        "p4": "There are different 'Weaves' of carbon. Twill weaves are flexible for complex curves like the nosecone, while Plain weaves are stiff for flat structural floors. We also use 'Nomex Honeycomb'—a paper-like material that acts as a core, making parts incredibly thick and strong without adding weight.",
        "p5": "Finally, the finish. A raw carbon part is painted with ultra-thin layers to save weight. Every gram counts in F1. Some teams even skip paint on certain areas to save a few hundred grams—that's the obsession with performance.",
        "qs": [
            ("What is an 'Autoclave' used for?", ["Generating electricity", "Curing carbon fiber under heat and pressure", "Mixing fuel", "Washing the car"], "Curing carbon fiber under heat and pressure"),
            ("Why are air bubbles (voids) dangerous in carbon parts?", ["They make it too heavy", "They act as stress points and cause the part to snap", "They look ugly", "They make it slower"], "They act as stress points and cause the part to snap"),
            ("What is 'Pre-Preg' carbon fiber?", ["Raw carbon fabric", "Carbon fiber with resin already soaked in", "Recycled carbon", "Carbon that has been painted"], "Carbon fiber with resin already soaked in"),
            ("Which material is used in the core of carbon panels for extra strength?", ["Wood", "Nomex Honeycomb", "Solid lead", "Plastic foam"], "Nomex Honeycomb")
        ]
    },
    8: {
        "title": "Impact Structures: The Art of Crushing",
        "intro": "A crash is just energy looking for somewhere to go.",
        "p1": "In a crash, the goal is not to stay rigid—it’s to 'shatter' correctly. F1 cars have 'Crush Structures' (Impact Attenuators) at the front and sides. These are designed to crumble like a drink can in a controlled way, absorbing the massive kinetic energy of a crash so the driver doesn't have to.",
        "p2": "Every piece of carbon fiber that shatters and flies away is taking a little bit of that energy with it. This is 'Energy Attenuation'. Modern F1 nosecones can absorb a 50 G impact and keep the driver's feet completely untouched.",
        "p3": "Side Impact Spars are also critical. If a car hits you from the side (like at a T-junction), these spars splinter and crush. They are tested to ensure they don't penetrate the driver's cockpit, acting like a soft pillow made of breaking glass.",
        "p4": "The steering column is also an impact structure. It collapses forward away from the driver during a front-on crash, ensuring it doesn't become a spear. This is why F1 drivers can walk away from 200 mph crashes with barely a scratch.",
        "p5": "Finally, the HANS device (Head and Neck Support). It is a carbon collar that tether's the driver's helmet to the seat. It prevents the head from snapping forward during a crash, which is the leading cause of neck injuries in racing.",
        "qs": [
            ("How does a 'Crush Structure' protect the driver?", ["It stays solid", "It shatters in a controlled way to absorb energy", "It bounces back", "It speeds up"], "It shatters in a controlled way to absorb energy"),
            ("What is the HANS device used for?", ["Radio communication", "Protecting the head and neck during a crash", "Controlling the engine", "Drinking water"], "Protecting the head and neck during a crash"),
            ("What happens to energy when carbon fiber delaminates (splinters)?", ["It gets stronger", "It is absorbed and carried away from the driver", "It turns into fire", "It disappears"], "It is absorbed and carried away from the driver"),
            ("Where are the primary impact structures located on an F1 car?", ["The tires", "Front (nosecone) and sides (spars)", "In the engine", "The radio antenna"], "Front (nosecone) and sides (spars)")
        ]
    },
    9: {
        "title": "Race Strategy: Undercut & Overcut Math",
        "intro": "F1 is a game of chess played at 200 mph.",
        "p1": "Strategy is the art of passing people without ever being near them on track. The 'Undercut' is the most famous move. If you are stuck behind a car and can't pass, you pit 1 lap early. Your new tires are much stickier and faster. Your 'Out Lap' will be 2 seconds faster than the car in front. When they pit 1 lap later, you've already passed them!.",
        "p2": "The 'Overcut' is the opposite—and much rarer. You stay out on old tires while the car in front pits. This only works if your old tires are still fast and the track is getting better. By staying out, you gain 'Clean Air' and can set fast laps while the other car is struggling to warm up their new tires.",
        "p3": "Fuel management is now less critical than battery management. In 2026, drivers must decide when to 'Deploy' and when to 'Harvest'. If you harvest too much, you lose speed. If you deploy too much, you run out of juice (Clipping). It's a constant balancing act on the steering wheel.",
        "p4": "Weather strategy is also a gamble. We look at the 'Crossover Point'—the exact second when a wet track becomes dry enough for Slick tires. Pitting 1 lap too early can mean you spin off; pitting 1 lap too late means you've lost 15 seconds. Engineers use high-res radar to predict rain down to the minute.",
        "p5": "Finally, the Pit Stop. 20 people must work in perfect sync to change 4 tires in under 2 seconds. A mistake of just 0.5 seconds can ruin an entire weekend of strategy. In F1, human performance is just as important as machine performance.",
        "qs": [
            ("What is the 'Undercut' strategy?", ["Pitting early for fresh tires to gain a time advantage", "Driving very close to the car in front", "Pitting late", "Using more fuel"], "Pitting early for fresh tires to gain a time advantage"),
            ("What is the 'Crossover Point' in weather strategy?", ["When the driver switches teams", "When a wet track becomes dry enough for slick tires", "When the race ends", "A pit lane crossing"], "When a wet track becomes dry enough for slick tires"),
            ("Why is the 'Out Lap' so critical in an Undercut?", ["Because it's the last lap", "Because fresh tires provide a significant speed boost", "Because the fuel is heavy", "Because the pits are closed"], "Because fresh tires provide a significant speed boost"),
            ("What is a typical F1 pit stop duration for tires?", ["10 seconds", "Under 2 seconds", "1 minute", "No limit"], "Under 2 seconds")
        ]
    },
    10: {
        "title": "Telemetry Mastery: The V-Graph Diagnostic",
        "intro": "Telemetry is the car's heartbeat on a computer screen.",
        "p1": "Engineers spend their lives looking at 'V-Graphs'—charts showing Speed vs. Distance. A corner looks like a deep 'V'. The bottom point of that V is the 'Apex' speed—the slowest point of the corner. If the V is too shallow, the driver is braking too early; if it's too deep, they are probably missing the exit.",
        "p2": "We also look at the 'Brake Trace'. A 'Threshold Braking' driver will show a steep, near-vertical line up to 100% pressure, followed by a gradual release known as 'Trail Braking'. This helps the car pivot into the corner. If the brake trace looks jagged, the driver is 'pumping' the brakes and losing stability.",
        "p3": "G-Force logs show how hard the driver is working. F1 drivers experience 5G in corners—that means their head feels 5 times heavier than normal. By looking at the lateral G-log, we can see if the car is 'washing out' (understeering) or 'snapping' (oversteering) at the limit of grip.",
        "p4": "Ride Height sensors are the most secret data. With ground-effect cars, kept as low as possible without 'stalling' the floor. If we see a sudden drop in downforce on the sensors, we know the car is floor-stalling, and we have to raise the car by 1mm—even if it makes it slightly slower.",
        "p5": "Finally, Engine Health. We monitor 'Oil Pressure' and 'Exhaust Gas Temperatures' (EGT). If an engineer sees EGTs rising too fast, they will tell the driver to 'Lift and Coast'—take their foot off the gas early on straights—to cool the engine and survive to the finish line.",
        "qs": [
            ("What does the bottom point of a 'V' on a speed graph represent?", ["Top speed", "The Apex (minimum corner speed)", "Pit stop", "Start line"], "The Apex (minimum corner speed)"),
            ("What is 'Trail Braking'?", ["Braking in a straight line", "Gradually releasing the brakes as you turn into a corner", "Braking after the corner", "Using the handbrake"], "Gradually releasing the brakes as you turn into a corner"),
            ("How many 'Gs' do F1 drivers typically experience in corners?", ["1G", "5G", "100G", "0G"], "5G"),
            ("What does 'Lift and Coast' mean?", ["Going faster", "Lifting off the gas early to cool the car or save fuel", "Driving on two wheels", "Pitting early"], "Lifting off the gas early to cool the car or save fuel")
        ]
    },
    11: {
        "title": "Aero coefficients: Barn Doors vs Razors",
        "intro": "Aerodynamics is the art of the trade-off.",
        "p1": "F1 wings are not designed to be as 'big' as possible—they are designed for an 'L/D Ratio' (Lift over Drag). Downforce pushes the car down (Lift), but it also pulls it back (Drag). The more wing you have, the more you are pulled back.",
        "p2": "At Monza (the fastest track), we use 'Razor' wings. They are tiny, thin, and almost flat. Why? Because the straights are so long that drag is the enemy. At Monaco (the slowest track), we use 'Barn Door' wings. They are huge and steep because you need every gram of grip for the tight corners, and the straights are too short for drag to matter.",
        "p3": "The 'Front Wing' is the most important part because it directs the air to the rest of the car. If the front wing is damaged, the 'Flow Structure' of the entire car is ruined. Air will arrive at the sidepods and rear wing in a 'messy' (turbulent) state, losing almost 50% of the total downforce.",
        "p4": "Cooling Ducts also create drag. Every time you open a hole in the car to cool the engine, you are creating 'Internal Drag'. Engineers are constantly closing these holes with tape during qualifying (when it’s cold) and opening them for the race to prevent the engine from melting.",
        "p5": "DRS (Drag Reduction System) is the ultimate aero trick. By flipping the top flap of the rear wing open, we 'stall' the wing. This destroys the downforce but also destroys the drag, allowing the car to gain 10-15 km/h instantly on a straight. It's like a 'Turbo Boost' made of air.",
        "qs": [
            ("What is the 'L/D Ratio' in aerodynamics?", ["Long vs Deep", "Lift over Drag", "Left vs Right", "Light vs Dark"], "Lift over Drag"),
            ("Why do teams use thin 'Razor' wings at Monza?", ["To look cool", "To minimize drag on the long straights", "Because they are cheaper", "Because of the rain"], "To minimize drag on the long straights"),
            ("What happens to total downforce if the front wing is damaged?", ["It increases", "It is significantly reduced due to turbulent air", "Nothing happens", "The engine gets more power"], "It is significantly reduced due to turbulent air"),
            ("What is the main goal of using DRS?", ["More downforce", "Reducing drag to gain top speed", "Cooling the engine", "Braking faster"], "Reducing drag to gain top speed")
        ]
    },
    12: {
        "title": "Future: 2026 X-Mode and Z-Mode",
        "intro": "The wings of 2026 will move while the car is driving.",
        "p1": "As we move to 2026, F1 is introducing 'Active Aerodynamics'. Because the engines are half-electric, the cars need less drag to prevent the batteries from draining. So, the car will have two modes: X-Mode and Z-Mode.",
        "p2": "X-Mode is the 'Straight Line' mode. Both the front and rear wing flaps will flatten out (low drag). This allows the car to reach high top speeds with less engine power. Think of it like a swimmer tucking their head in to be more streamlined.",
        "p3": "Z-Mode is the 'Cornering' mode. The wings will automatically 'pop up' to a steep angle as soon as the driver enters a braking zone. This provides the massive downforce needed to grip the corners. This transformation happens hundreds of times during a race.",
        "p4": "Active aero also helps with 'Followability'. Currently, cars lose grip when they follow another car in its 'Dirty Air'. In 2026, the active wings can adjust themselves to compensate for this lost air, making overtaking much easier and closer.",
        "p5": "Finally, the Cockpit Safety. The 2026 regulations include even stricter impact tests and a mandatory 15% increase in the strength of the survival cell. We are entering an era where cars are faster, cleaner, and the safest in human history.",
        "qs": [
            ("What is 'X-Mode' in the 2026 regulations?", ["A reverse gear", "A low-drag mode for straights", "A high-downforce mode for corners", "A pit lane limiter"], "A low-drag mode for straights"),
            ("Why is active aero being introduced in 2026?", ["To make the cars heavier", "To save battery energy and prevent 'clipping'", "To make it more expensive", "To slow the cars down"], "To save battery energy and prevent 'clipping'"),
            ("What is 'Z-Mode' specifically used for?", ["Speed on straights", "Downforce in corners", "Cooling the engine", "Launching the car"], "Downforce in corners"),
            ("How does active aero help with 'Dirty Air'?", ["It makes the air cleaner", "It adjusts to compensate for lost downforce when following", "It blows the air away", "It has no effect"], "It adjusts to compensate for lost downforce when following")
        ]
    }
}

lessons_to_insert = []
questions_to_insert = []

for cid, data in ELITE_DATA.items():
    slug = f"module-{cid}-elite-lesson"
    content_json = json.dumps({
        "sections": [
            {"title": data['title'], "content": data['intro']},
            {"title": "Phase 1: Structural Theory", "content": data['p1']},
            {"title": "Phase 2: Technical Dynamics", "content": data['p2']},
            {"title": "Phase 3: Formula Student / SAE Context", "content": data['p3']},
            {"title": "Phase 4: Expert Engineering Insights", "content": data['p4']},
            {"title": "Final Summary: The 2026 Paradigm", "content": data.get('p5', "Engineers must adapt.")}
        ]
    })
    lesson_id = cid * 10
    lessons_to_insert.append((lesson_id, cid, data['title'], slug, content_json, 1))
    
    for q_idx, (q_text, q_opts, q_corr) in enumerate(data['qs']):
        questions_to_insert.append((
            lesson_id * 100 + q_idx, lesson_id, "multiple_choice", q_text,
            json.dumps(q_opts), q_corr,
            f"Correct! '{q_corr}' is a fundamental peak-level fact.",
            None, 400
        ))

cursor.executemany("INSERT INTO academy_courses (id, title, difficulty, slug, description, icon, order_num) VALUES (?,?,?,?,?,?,?)", COURSES)
cursor.executemany("INSERT INTO academy_lessons (id, course_id, title, slug, content_json, order_num) VALUES (?,?,?,?,?,?)", lessons_to_insert)
cursor.executemany("INSERT INTO academy_questions (id, lesson_id, question_type, question, options_json, correct_answer, explanation, image_url, xp_reward) VALUES (?,?,?,?,?,?,?,?,?)", questions_to_insert)

db.commit()
print("Academy V4.5.1 PEAK ELITE (Complete 1-12) synced.")
db.close()
