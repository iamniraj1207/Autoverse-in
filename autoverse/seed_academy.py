import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'autoverse.db')
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def seed_academy():
    print("📚 Seeding Content-Heavy Academy...")

    # Courses
    courses = [
        ('1', 'Automotive Engineering 101', 'Master the fundamental physics and mechanical engineering behind modern performance cars.', 'beginner', '/static/img/academy/engine_101.jpg'),
        ('2', 'Aero & Fluid Dynamics', 'Explore how air flows over, under, and through a vehicle to create downforce and stability.', 'intermediate', '/static/img/academy/aero_101.jpg'),
        ('3', 'Formula 1 Technical Analysis', 'A deep dive into the most advanced racing series on Earth: F1 engines, ERS, and chassis design.', 'advanced', '/static/img/academy/f1_tech.jpg'),
    ]

    cursor.execute("DELETE FROM courses")
    cursor.executemany("INSERT INTO courses (id, title, description, level, image_url) VALUES (?,?,?,?,?)", courses)

    # Lessons
    lessons = [
        # Course 1 Lessons
        ('1', '1', 'The Internal Combustion Engine', 'learn', 'Learn how chemical energy is converted into mechanical work using the four-stroke cycle.', 1, 10),
        ('2', '1', 'Force Induction: Turbos & Blowers', 'learn', 'Understand how turbochargers and superchargers compress air to extract massive power from small displacements.', 2, 15),
        ('3', '1', 'Drivetrain & Power Delivery', 'learn', 'How power moves from the crank to the wheels: Front, Rear, and All-Wheel Drive systems explained.', 3, 10),
        ('4', '1', 'Engine Quiz', 'quiz', 'Test your knowledge on piston physics and forced induction.', 4, 20),

        # Course 2 Lessons
        ('5', '2', 'The Venturi Effect & Underbody Aero', 'learn', 'Discover how ground effect generates suction to glue a car to the track without the drag of a wing.', 1, 25),
        ('6', '2', 'Drag Reduction Systems (DRS)', 'learn', 'A technical study on how movable aerodynamic elements reduce drag and increase top speed.', 2, 10),
    ]

    cursor.execute("DELETE FROM lessons")
    cursor.executemany("INSERT INTO lessons (id, course_id, title, type, description, order_num, xp_reward) VALUES (?,?,?,?,?,?,?)", lessons)

    # Lesson Content (The user wants HEAVY content)
    lesson_contents = [
        ('1', """
### ⚙️ The Heart of the Machine: The Internal Combustion Engine

The Internal Combustion Engine (ICE) is a masterpiece of thermodynamic engineering. At its core, it is a heat engine that converts the energy released by Burning fuel into pressurized gas, which then moves mechanical components.

#### 🏁 The Four-Stroke Cycle (The Otto Cycle)
Modern petrol engines follow four distinct phases:

1. **Intake (Induction):** The intake valve opens, and the piston moves down, sucking a mixture of air and atomized fuel into the cylinder. In modern direct-injection engines, only air is sucked in, and fuel is sprayed later.
2. **Compression:** The valves close, and the piston moves back up, compressing the mixture to a fraction of its original volume. This increases the temperature and prepares the mixture for rapid combustion.
3. **Power (Combustion):** A spark plug creates a high-voltage arc, igniting the compressed mixture. The resulting explosion forces the piston down with thousands of pounds of force. This is the **only stroke** that produces power.
4. **Exhaust:** The exhaust valve opens, and the piston moves up again, pushing the spent gases out through the exhaust manifold.

#### 💡 Displacement vs. Horsepower
*   **Displacement:** The total volume of all cylinders. A 5.0L V8 has 5 liters of internal volume. Generally, more displacement = more air = more fuel = more torque.
*   **Horsepower:** The rate at which work is done. It is a mathematical calculation: `(Torque x RPM) / 5252`. Higher revving engines can produce more horsepower even with lower torque.
"""),
        ('2', """
### 🐌 Forced Induction: Entering the Boost Zone

Forced induction is the process of forcing more air into the engine's cylinders than it could normally suck in on its own (Atmospheric Pressure). More air means you can burn more fuel, leading to a much larger "Power Stroke."

#### 🌀 Turbochargers: The Free Energy Loop
A turbocharger uses the **kinetic energy of exhaust gases** to spin a turbine. That turbine is connected to a compressor that jams fresh air into the intake.
*   **Pros:** Massive power gains, increased efficiency (uses waste heat).
*   **Cons:** "Turbo Lag" (time needed for exhaust pressure to build), high heat soak.

#### 🔩 Superchargers: Instant Response
Unlike a turbo, a supercharger is **driven by a belt** connected directly to the engine's crankshaft. This means there is no lag—power is available the moment you touch the throttle.
*   **Pros:** Linear power delivery, instant torque.
*   **Cons:** "Parasitic Loss" (takes power from the engine to make power), less efficient at high RPMs.

#### 🧊 The Intercooler
Compressing air makes it hot. Hot air is less dense and can cause "knock" (pre-ignition). An intercooler sits between the compressor and the engine to chill the air, making it dense and safe for combustion.
"""),
        ('5', """
### 💨 Mastering the Wind: The Venturi Effect

In high-performance automotive design, aerodynamics isn't just about "slipping through the air"—it's about using the air to create **Downforce**.

#### 🧪 Bernoulli’s Principle
In simple terms: *Faster moving air has lower pressure than slower moving air.* By creating a shape that forces air to move faster under the car than over it, we create a vacuum that pulls the car toward the asphalt.

#### 🏎️ The Ground Effect & Diffusers
The **Diffuser** is the most critical part of an F1 or GT3 car's floor. It is an upswept section at the rear that allows the fast air under the car to expand and slow down. This expansion creates a "suction" effect at the exit, pulling air through the narrow channels under the car even faster.

#### ⚖️ The Drag vs. Downforce Tradeoff
Every wing that generates downforce also generates **Induced Drag**. Racing engineers must find the "Sweet Spot":
*   **Low Downforce (Monza):** Small wings, low drag, high top speeds (350km/h+).
*   **High Downforce (Monaco):** Massive wings, high drag, incredible cornering speeds but lower top speeds.
"""),
    ]

    cursor.execute("DELETE FROM lesson_contents")
    cursor.executemany("INSERT INTO lesson_contents (lesson_id, content) VALUES (?,?)", lesson_contents)

    conn.commit()
    conn.close()
    print("✅ Academy Seeding Complete (Rich Content Added).")

if __name__ == "__main__":
    seed_academy()
