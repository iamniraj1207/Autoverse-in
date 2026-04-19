import sqlite3
import json

def seed_academy():
    conn = sqlite3.connect('autoverse.db')
    db = conn.cursor()

    # Clear old dummy data
    db.execute("DELETE FROM academy_courses")
    db.execute("DELETE FROM academy_lessons")
    db.execute("DELETE FROM academy_questions")

    # DB Schemas:
    # academy_courses: id, title, slug, description, category, difficulty, total_xp, icon, color, order_num
    # academy_lessons: id, course_id, title, slug, lesson_type, content_json, xp_reward, order_num
    # academy_questions: id, lesson_id, question_type, question, options_json, correct_answer, explanation, image_url, xp_reward

    # 1. Internal Combustion Mastery
    db.execute('''INSERT INTO academy_courses (id, title, slug, description, category, difficulty, total_xp, icon, color, order_num)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
               (1, 'Internal Combustion Mastery', 'engine-mastery', 
                'Dive deep into how 4-stroke engines generate power, covering intake, compression, combustion, and exhaust phases.', 
                'Engineering', 'Intermediate', 500, '⚙️', '#e83a3a', 1))
    
    # 2. Aerodynamics 101
    db.execute('''INSERT INTO academy_courses (id, title, slug, description, category, difficulty, total_xp, icon, color, order_num)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
               (2, 'Aerodynamics 101', 'aero-101', 
                'Understand downforce, drag coefficients, ground effect, and how F1 cars manipulate air to stick to the track.', 
                'Aerodynamics', 'Advanced', 750, '🌬️', '#0090FF', 2))
    
    # 3. Hybrid Power Units (F1)
    db.execute('''INSERT INTO academy_courses (id, title, slug, description, category, difficulty, total_xp, icon, color, order_num)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
               (3, 'Hybrid Power Units', 'f1-hybrid-pu', 
                'Explore the pinnacle of engineering: the MGU-K, MGU-H, and turbo-hybrid systems that deliver 1000+ HP.', 
                'F1 Tech', 'Expert', 1000, '⚡', '#52E252', 3))

    # Lessons for Internal Combustion
    l1_content = {
      "slides": [
        {
          "type": "intro",
          "heading": "The 4-Stroke Cycle",
          "body": "ICE (Internal Combustion Engines) rely on thousands of controlled explosions per minute. The standard cycle contains four specific strokes: Intake, Compression, Power, and Exhaust.",
          "image_url": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=1200&h=700&fit=crop"
        },
        {
          "type": "concept",
          "heading": "Stroke 1: Intake",
          "body": "The piston travels downward, creating a vacuum. The intake valve opens, allowing a precise mixture of air and fuel to be drawn into the cylinder."
        },
        {
          "type": "concept",
          "heading": "Stroke 2: Compression",
          "body": "Valves close. The piston travels upward, compressing the air-fuel mixture into a highly volatile, highly pressurized state called the combustion chamber."
        }
      ]
    }
    db.execute('''INSERT INTO academy_lessons (course_id, title, slug, lesson_type, content_json, xp_reward, order_num)
                  VALUES (?, ?, ?, ?, ?, ?, ?)''',
               (1, 'The 4-Stroke Cycle', '4-stroke-cycle', 'Interactive', json.dumps(l1_content), 50, 1))
    
    lesson1_id = db.execute("SELECT id FROM academy_lessons WHERE slug='4-stroke-cycle'").fetchone()[0]

    # Questions for Lesson 1
    db.execute('''INSERT INTO academy_questions (lesson_id, question_type, question, options_json, correct_answer, explanation, xp_reward)
                  VALUES (?, ?, ?, ?, ?, ?, ?)''',
               (lesson1_id, 'multiple-choice', 'Which stroke creates the actual horsepower in an engine?', 
                json.dumps(['Intake', 'Compression', 'Power', 'Exhaust']), 'Power', 
                'The Power (or Combustion) stroke is when the spark plug ignites the mixture, forcing the piston down. This creates the rotational force (torque) that drives the car.', 20))
                
    db.execute('''INSERT INTO academy_questions (lesson_id, question_type, question, options_json, correct_answer, explanation, xp_reward)
                  VALUES (?, ?, ?, ?, ?, ?, ?)''',
               (lesson1_id, 'multiple-choice', 'What happens during the Intake stroke?', 
                json.dumps(['Valves close and piston moves up', 'Spark plug fires', 'Piston moves down and draws in air/fuel', 'Burnt gases are pushed out']), 'Piston moves down and draws in air/fuel', 
                'The piston drops, acting like a syringe to pull the fresh air and fuel mixture through the open intake valve into the cylinder.', 20))

    # Lessons for Aerodynamics
    l2_content = {
      "slides": [
        {
          "type": "intro",
          "heading": "Downforce vs. Drag",
          "body": "Aerodynamics is a balancing act. Downforce pushes the car into the track for grip, but creating downforce usually creates drag, which slows the car down on straights.",
          "image_url": "https://images.unsplash.com/photo-1541773079-82de5b9e4e4a?w=1200&h=700&fit=crop"
        },
        {
          "type": "concept",
          "heading": "The Bernoulli Principle",
          "body": "Fast moving air creates low pressure. By shaping the floor of the car like an inverted airplane wing, it accelerates air underneath the car, creating a low pressure zone that sucks the car into the ground (Ground Effect)."
        }
      ]
    }
    db.execute('''INSERT INTO academy_lessons (course_id, title, slug, lesson_type, content_json, xp_reward, order_num)
                  VALUES (?, ?, ?, ?, ?, ?, ?)''',
               (2, 'Downforce & Drag', 'downforce-drag', 'Interactive', json.dumps(l2_content), 75, 1))

    lesson2_id = db.execute("SELECT id FROM academy_lessons WHERE slug='downforce-drag'").fetchone()[0]

    db.execute('''INSERT INTO academy_questions (lesson_id, question_type, question, options_json, correct_answer, explanation, xp_reward)
                  VALUES (?, ?, ?, ?, ?, ?, ?)''',
               (lesson2_id, 'multiple-choice', 'Which principle explains how fast-moving air under a car creates lower pressure and sucks the car to the track?', 
                json.dumps(['Newton''s Third Law', 'The Bernoulli Principle', 'Thermodynamics', 'Centrifugal Force']), 'The Bernoulli Principle', 
                'The Bernoulli Principle states an increase in the speed of a fluid (or air) occurs simultaneously with a decrease in pressure.', 25))

    # Lessons for Hybrid PUs
    l3_content = {
      "slides": [
        {
          "type": "intro",
          "heading": "The 1,000 HP Formula",
          "body": "Modern F1 Power Units are the most efficient engines on earth, achieving thermal efficiency over 50%. A V6 Turbo is assisted by two electric motors: the MGU-K and MGU-H.",
          "image_url": "https://images.unsplash.com/photo-1536611593361-bba6eb00a4b8?w=1200&h=700&fit=crop"
        },
        {
          "type": "concept",
          "heading": "MGU-K (Kinetic)",
          "body": "It acts as a generator under braking, recovering kinetic energy that would be lost as heat in the brakes. It stores this in the battery, then deploys it as electric horsepower during acceleration."
        }
      ]
    }
    db.execute('''INSERT INTO academy_lessons (course_id, title, slug, lesson_type, content_json, xp_reward, order_num)
                  VALUES (?, ?, ?, ?, ?, ?, ?)''',
               (3, 'Inside the Power Unit', 'inside-pu', 'Interactive', json.dumps(l3_content), 100, 1))
               
    lesson3_id = db.execute("SELECT id FROM academy_lessons WHERE slug='inside-pu'").fetchone()[0]

    db.execute('''INSERT INTO academy_questions (lesson_id, question_type, question, options_json, correct_answer, explanation, xp_reward)
                  VALUES (?, ?, ?, ?, ?, ?, ?)''',
               (lesson3_id, 'multiple-choice', 'What is the primary function of the MGU-K under braking?', 
                json.dumps(['To cool the brakes', 'To recover kinetic energy into the battery', 'To prevent wheel lockup', 'To spin the turbocharger']), 'To recover kinetic energy into the battery', 
                'The Motor Generator Unit - Kinetic captures the energy normally lost as heat during braking and stores it electrically for later deployment as horsepower.', 30))

    conn.commit()
    conn.close()
    print("✓ Academy fully seeded with authentic automotive and F1 engineering content.")

if __name__ == "__main__":
    seed_academy()
