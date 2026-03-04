"""
app.py — AutoVerse Flask Application
All routes live here. Page routes use Jinja2, API routes return JSON.
"""
import os
import json

from cs50 import SQL
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import error_response, login_required, success_response

# ── App Setup ──────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")

# CS50 SQL wrapper — uses SQLite under the hood
db = SQL("sqlite:///autoverse.db")

# Add helper functions to Jinja
app.jinja_env.globals.update(min=min, max=max, int=int, str=str, json=json)

@app.context_processor
def inject_user_data():
    if session.get('user_id'):
        xp_data = db.execute("SELECT * FROM user_xp WHERE user_id=?", session['user_id'])
        if not xp_data:
            db.execute("INSERT OR IGNORE INTO user_xp (user_id, level) VALUES (?, 1)", session['user_id'])
            xp_data = db.execute("SELECT * FROM user_xp WHERE user_id=?", session['user_id'])
        return {
            'user_xp': xp_data[0] if xp_data else None,
            'username': session.get('username')
        }
    return {'user_xp': None, 'username': None}


# ╔══════════════════════════════════════════════════════════════╗
# ║  AUTH ROUTES — No login required                            ║
# ╚══════════════════════════════════════════════════════════════╝

@app.route("/")
def index():
    """Landing page with featured content."""
    featured_cars = db.execute("SELECT * FROM cars ORDER BY horsepower DESC LIMIT 3")
    return render_template("index.html", featured_cars=featured_cars)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm", "")

        if not username or not password:
            return render_template("register.html", error="Username and password required.")
        if password != confirm:
            return render_template("register.html", error="Passwords do not match.")

        # Check username not already taken
        existing = db.execute("SELECT id FROM users WHERE username = ?", username)
        if existing:
            return render_template("register.html", error="Username already taken.")

        hash_ = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_)
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return render_template("login.html", error="Invalid username or password.")

        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ╔══════════════════════════════════════════════════════════════╗
# ║  CAR EXPLORER — Public pages                                ║
# ╚══════════════════════════════════════════════════════════════╝

@app.route("/cars")
def cars():
    """Browse all cars. Supports ?brand= and ?fuel= query filters."""
    brand     = request.args.get("brand", "")
    fuel_type = request.args.get("fuel", "")
    category  = request.args.get("category", "")

    query  = "SELECT * FROM cars WHERE 1=1"
    params = []
    if brand:
        query += " AND brand = ?"
        params.append(brand)
    if fuel_type:
        query += " AND fuel_type = ?"
        params.append(fuel_type)
    if category:
        query += " AND category = ?"
        params.append(category)
        
    query += " ORDER BY CASE WHEN category='Hypercar' THEN 1 WHEN category='Supercar' THEN 2 ELSE 3 END, brand, model"

    all_cars = db.execute(query, *params)
    brands   = db.execute("SELECT DISTINCT brand FROM cars WHERE brand IS NOT NULL ORDER BY brand")
    fuels    = db.execute("SELECT DISTINCT fuel_type FROM cars WHERE fuel_type IS NOT NULL ORDER BY fuel_type")
    categories = db.execute("SELECT DISTINCT category FROM cars WHERE category IS NOT NULL ORDER BY category")

    brand_logos = {
        "Ferrari": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d1/Ferrari-Logo.svg/100px-Ferrari-Logo.svg.png",
        "Lamborghini": "https://upload.wikimedia.org/wikipedia/en/thumb/d/df/Lamborghini_Logo.svg/100px-Lamborghini_Logo.svg.png",
        "Mercedes-Benz": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Mercedes-Benz_logo_2011.svg/100px-Mercedes-Benz_logo_2011.svg.png",
        "BMW": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/BMW.svg/100px-BMW.svg.png",
        "Porsche": "https://upload.wikimedia.org/wikipedia/en/thumb/b/be/Porsche_logo.svg/100px-Porsche_logo.svg.png",
        "Aston Martin": "https://upload.wikimedia.org/wikipedia/en/thumb/b/bd/Aston_Martin_logo.svg/100px-Aston_Martin_logo.svg.png",
        "Bugatti": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Bugatti_logo.svg/100px-Bugatti_logo.svg.png",
        "Pagani": "https://upload.wikimedia.org/wikipedia/en/thumb/8/87/Pagani_Automobili_Logo.svg/100px-Pagani_Automobili_Logo.svg.png",
        "Koenigsegg": "https://upload.wikimedia.org/wikipedia/en/thumb/c/ca/Koenigsegg_logo.svg/100px-Koenigsegg_logo.svg.png",
        "Mahindra": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Mahindra_logo.svg/100px-Mahindra_logo.svg.png",
        "Tata": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Tata_logo.svg/100px-Tata_logo.svg.png",
        "Tesla": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Tesla_logo.svg/100px-Tesla_logo.svg.png"
    }

    return render_template("cars.html", cars=all_cars, brands=brands, fuels=fuels, categories=categories,
                           selected_brand=brand, selected_fuel=fuel_type, selected_category=category, brand_logos=brand_logos)


@app.route("/cars/<int:car_id>")
def car_detail(car_id):
    """Single car detail page."""
    car = db.execute("SELECT * FROM cars WHERE id = ?", car_id)
    if not car:
        return render_template("404.html"), 404
        
    # Get similar cars (same brand or category)
    similar = db.execute(
        "SELECT * FROM cars WHERE (brand = ? OR category = ?) AND id != ? LIMIT 3", 
        car[0]['brand'], car[0]['category'], car_id
    )
    
    return render_template("car.html", car=car[0], similar=similar)


@app.route("/compare")
def compare():
    """Comparison engine page supporting up to 4 cars."""
    ids_param = request.args.get('ids', '')
    if not ids_param:
        return render_template("compare.html", cars=[])

    # Parse IDs then limit to 4 (split avoids slice-on-list lint)
    parsed = [int(i.strip()) for i in ids_param.split(',') if i.strip().isdigit()]
    ids = parsed[:4]
    if not ids:
        return render_template("compare.html", cars=[])

    placeholders = ','.join(['?' for _ in ids])
    cars = db.execute(f"SELECT * FROM cars WHERE id IN ({placeholders})", *ids)

    return render_template('compare.html', cars=cars)


# ╔══════════════════════════════════════════════════════════════╗
# ║  ACADEMY — Login required                                   ║
# ╚══════════════════════════════════════════════════════════════╝

@app.route("/academy")
@login_required
def academy():
    courses = db.execute("SELECT * FROM academy_courses ORDER BY order_num")
    user_id = session['user_id']
    
    # Get user progress for each course
    for course in courses:
        total_lessons = db.execute("SELECT count(*) as count FROM academy_lessons WHERE course_id=?", course['id'])[0]['count']
        completed_lessons = db.execute("""
            SELECT count(DISTINCT lesson_id) as count FROM user_progress 
            WHERE user_id=? AND completed=1 AND lesson_id IN (
                SELECT id FROM academy_lessons WHERE course_id=?
            )
        """, user_id, course['id'])[0]['count']
        
        course['total_lessons'] = total_lessons
        course['completed_lessons'] = completed_lessons
        course['progress_percent'] = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        
    return render_template("academy/index.html", courses=courses)

@app.route("/academy/course/<slug>")
@login_required
def academy_course(slug):
    course = db.execute("SELECT * FROM academy_courses WHERE slug=?", slug)
    if not course:
        return render_template("404.html"), 404
    
    lessons = db.execute("SELECT * FROM academy_lessons WHERE course_id=? ORDER BY order_num", course[0]['id'])
    user_id = session['user_id']
    
    for lesson in lessons:
        progress = db.execute("SELECT completed FROM user_progress WHERE user_id=? AND lesson_id=?", user_id, lesson['id'])
        lesson['completed'] = progress[0]['completed'] if progress else 0
        
    return render_template("academy/course.html", course=course[0], lessons=lessons)

@app.route("/academy/lesson/<int:lesson_id>")
@login_required
def academy_lesson(lesson_id):
    lesson = db.execute("""
        SELECT l.*, c.content 
        FROM academy_lessons l
        LEFT JOIN lesson_contents c ON l.id = c.lesson_id
        WHERE l.id = ?
    """, lesson_id)
    if not lesson:
        return render_template("404.html"), 404
    
    course = db.execute("SELECT * FROM academy_courses WHERE id = ?", lesson[0]['course_id'])[0]
    
    if lesson[0]['lesson_type'] == 'quiz':
        questions = db.execute("SELECT * FROM academy_questions WHERE lesson_id=? ORDER BY RANDOM()", lesson_id)
        return render_template("academy/lesson_quiz.html", lesson=lesson[0], course=course, questions=questions)
    else:
        return render_template("academy/lesson_learn.html", lesson=lesson[0], course=course)

@app.route("/academy/leaderboard")
@login_required
def academy_leaderboard():
    users = db.execute("""
        SELECT u.username, x.total_xp, x.level, x.current_streak 
        FROM user_xp x
        JOIN users u ON x.user_id = u.id
        ORDER BY x.total_xp DESC LIMIT 100
    """)
    return render_template("academy/leaderboard.html", users=users)


# ╔══════════════════════════════════════════════════════════════╗
# ║  GARAGE — Login required                                    ║
# ╚══════════════════════════════════════════════════════════════╝

@app.route("/garage")
@login_required
def garage():
    """User's personal garage page with proper sorting."""
    user_id = session["user_id"]
    user_cars = db.execute(
        """SELECT cars.*, garage.added_at FROM cars
           JOIN garage ON cars.id = garage.car_id
           WHERE garage.user_id = ?
           ORDER BY garage.added_at DESC""",
        user_id
    )
    return render_template("garage.html", cars=user_cars)


# ╔══════════════════════════════════════════════════════════════╗
# ║  F1 HUB — Public pages                                     ║
# ╚══════════════════════════════════════════════════════════════╝

@app.route("/f1")
def f1_hub():
    """Cinematic F1 Hub landing page."""
    # Featured 2026 teams
    teams = db.execute("SELECT * FROM teams WHERE is_active_2026 = 1 LIMIT 4")
    # Hall of Fame (Now higher prominence)
    legends = db.execute("SELECT * FROM drivers WHERE championships >= 3 ORDER BY championships DESC LIMIT 3")
    # Top speed record
    top_lap = db.execute(
        """SELECT l.*, d.name as driver_name, d.image_url as driver_img 
           FROM f1_fastest_laps l 
           JOIN drivers d ON l.driver_id = d.id 
           ORDER BY l.speed_kmh DESC LIMIT 1"""
    )
    return render_template("f1/f1.html", 
                         teams=teams, 
                         legends=legends, 
                         top_lap=top_lap[0] if top_lap else None)


@app.route('/f1/drivers')
def f1_drivers():
    # ONLY 2026 active drivers
    drivers = db.execute("""
        SELECT d.*, t.name as team_name,
               t.primary_color, t.logo_url as team_logo_url
        FROM drivers d
        LEFT JOIN teams t ON d.team_id = t.id
        WHERE d.is_active_2026 = 1
        ORDER BY d.championships DESC, d.wins DESC
    """)
    return render_template('f1/drivers.html', drivers=drivers)

@app.route('/f1/legends')
def f1_legends():
    # Hall of Fame — retired legends only
    legends = db.execute("""
        SELECT * FROM drivers
        WHERE is_active_2026 = 0
        AND championships > 0
        ORDER BY championships DESC
    """)
    return render_template('f1/legends.html', legends=legends)


@app.route('/f1/hall-of-fame')
def f1_hall_of_fame():
    """Hall of Fame — the GOATs of Formula One."""
    legends = db.execute("""
        SELECT * FROM drivers
        WHERE is_active_2026 = 0
        AND championships > 0
        ORDER BY championships DESC, wins DESC
    """)
    return render_template('f1/hall_of_fame.html', legends=legends)


@app.route('/f1/driver/<int:driver_id>')
def f1_driver_profile(driver_id):
    driver = db.execute("""
        SELECT d.*, t.name as team_name, t.primary_color,
               t.id as team_id
        FROM drivers d
        LEFT JOIN teams t ON d.team_id = t.id
        WHERE d.id = ?
    """, driver_id)
    if not driver:
        return "Driver not found", 404
    return render_template(
      'f1/driver_profile.html', driver=driver[0]
    )


@app.route("/f1/teams")
def f1_teams():
    """Constructor gallery split into 2026 Grid and All-Time History."""
    # 2026 Active Constructors
    active_teams = db.execute("SELECT * FROM teams WHERE is_active_2026 = 1 ORDER BY name ASC")
    # All-Time / Historical Constructors
    legacy_teams = db.execute("SELECT * FROM teams WHERE is_active_2026 = 0 ORDER BY championships DESC")
    
    # Attach driver chips for all
    for team in (active_teams + legacy_teams):
        team['drivers'] = db.execute("SELECT id, name FROM drivers WHERE team_id = ?", team['id'])
        
    return render_template("f1/teams.html", active_teams=active_teams, legacy_teams=legacy_teams)


@app.route("/f1/team/<int:team_id>")
def f1_team(team_id):
    """Cinematic team profile."""
    team = db.execute("SELECT * FROM teams WHERE id = ?", team_id)
    if not team:
        return render_template("404.html"), 404
    
    drivers = db.execute("SELECT * FROM drivers WHERE team_id = ?", team_id)
    return render_template("f1/team.html", team=team[0], drivers=drivers)


@app.route("/f1/records")
def f1_records():
    """Hall of Fame and speed database."""
    laps = db.execute(
        """SELECT l.*, d.name as driver_name, d.image_url as driver_img, t.name as team_name
           FROM f1_fastest_laps l
           JOIN drivers d ON l.driver_id = d.id
           JOIN teams t ON l.team_id = t.id
           ORDER BY l.speed_kmh DESC"""
    )
    legends = db.execute("SELECT * FROM drivers WHERE championships >= 3 ORDER BY championships DESC")
    return render_template("f1/records.html", laps=laps, legends=legends)


# ╔══════════════════════════════════════════════════════════════╗
# ║  API ROUTES — Return JSON                                   ║
# ╚══════════════════════════════════════════════════════════════╝

@app.route("/api/cars")
def api_cars():
    """Returns all cars as JSON — used by virtual scroll explorer."""
    all_cars = db.execute("SELECT id, brand, model, year, image_exterior, horsepower, acceleration, price_usd, category FROM cars ORDER BY brand, model")
    return jsonify(all_cars)


@app.route("/api/compare", methods=["POST"])
def api_compare():
    """POST {ids: [1, 2, 3]} → returns full car specs as JSON."""
    data = request.get_json(silent=True)
    if not data or "ids" not in data:
        return error_response("ids array required")
    ids = data["ids"]
    if not isinstance(ids, list) or len(ids) < 2 or len(ids) > 4:
        return error_response("Provide 2–4 car IDs")

    placeholders = ",".join("?" * len(ids))
    cars = db.execute(f"SELECT * FROM cars WHERE id IN ({placeholders})", *ids)
    return jsonify(cars)


@app.route("/api/garage/add", methods=["POST"])
@login_required
def api_garage_add():
    """POST {car_id} → persists car to garage DB and returns success."""
    data = request.get_json(silent=True)
    car_id = data.get("car_id") if data else None
    user_id = session.get("user_id")

    if not car_id:
        return error_response("car_id required")

    # Validate car exists
    car = db.execute("SELECT id FROM cars WHERE id = ?", car_id)
    if not car:
        return error_response("Car not found", 404)

    try:
        # Insert or ignore duplicate
        db.execute("""
            INSERT OR IGNORE INTO garage (user_id, car_id, added_at) 
            VALUES (?, ?, datetime('now'))
        """, user_id, car_id)
        return jsonify({"success": True, "message": "Added to garage"})
    except Exception as e:
        return error_response(f"Database error: {str(e)}", 500)


@app.route("/api/garage/remove", methods=["DELETE"])
@login_required
def api_garage_remove():
    """DELETE {car_id} → removes car from user's garage."""
    data   = request.get_json(silent=True)
    car_id = data.get("car_id") if data else None
    if not car_id:
        return error_response("car_id required")

    db.execute(
        "DELETE FROM garage WHERE user_id = ? AND car_id = ?",
        session["user_id"], car_id
    )
    return success_response(message="removed")


@app.route("/api/f1/drivers")
def api_f1_drivers():
    drivers = db.execute("SELECT * FROM drivers ORDER BY wins DESC")
    return jsonify(drivers)


@app.route("/api/f1/driver/<int:driver_id>")
def api_f1_driver(driver_id):
    driver = db.execute("SELECT * FROM drivers WHERE id = ?", driver_id)
    return jsonify(driver[0]) if driver else error_response("Not found", 404)


@app.route('/api/timeline/<entity_type>/<int:entity_id>')
def api_timeline(entity_type, entity_id):
    events = db.execute("""
        SELECT year, title, description, milestone_type
        FROM f1_timeline
        WHERE entity_type = ? AND entity_id = ?
        ORDER BY year ASC
    """, entity_type, entity_id)
    return jsonify(events)


@app.route("/api/f1/fastest-laps")
def api_fastest_laps():
    laps = db.execute("SELECT * FROM f1_fastest_laps ORDER BY speed_kmh DESC")
    return jsonify(laps)

# The academy routes originally here were duplicated and thus removed to prevent AssertionError on startup.

@app.route("/api/academy/answer", methods=["POST"])
@login_required
def api_academy_answer():
    data = request.get_json()
    question_id = data.get('question_id')
    answer = data.get('answer')
    
    question = db.execute("SELECT * FROM academy_questions WHERE id=?", question_id)
    if not question:
        return error_response("Question not found", 404)
    
    is_correct = str(answer).strip().lower() == str(question[0]['correct_answer']).strip().lower()
    
    if is_correct:
        user_id = session['user_id']
        xp_reward = question[0]['xp_reward']
        db.execute("UPDATE user_xp SET total_xp = total_xp + ? WHERE user_id = ?", xp_reward, user_id)
        
        # Check for level up
        xp_data = db.execute("SELECT total_xp, level FROM user_xp WHERE user_id=?", user_id)[0]
        new_level = 1
        xp = xp_data['total_xp']
        if xp >= 15000: new_level = 10
        elif xp >= 10000: new_level = 9
        elif xp >= 7500: new_level = 8
        elif xp >= 5000: new_level = 7
        elif xp >= 3500: new_level = 6
        elif xp >= 2000: new_level = 5
        elif xp >= 1000: new_level = 4
        elif xp >= 500: new_level = 3
        elif xp >= 200: new_level = 2
        
        if new_level > xp_data['level']:
            db.execute("UPDATE user_xp SET level = ? WHERE user_id = ?", new_level, user_id)
            
        return jsonify({
            "correct": True, 
            "explanation": question[0]['explanation'],
            "xp_earned": xp_reward,
            "new_level": new_level if new_level > xp_data['level'] else None
        })
    
    return jsonify({"correct": False, "explanation": question[0]['explanation']})

@app.route("/api/academy/complete", methods=["POST"])
@login_required
def api_academy_complete():
    data = request.get_json()
    lesson_id = data.get('lesson_id')
    score = data.get('score', 0)
    
    user_id = session['user_id']
    lesson = db.execute("SELECT * FROM academy_lessons WHERE id=?", lesson_id)
    
    if not lesson:
        return error_response("Lesson not found", 404)
        
    db.execute("""
        INSERT INTO user_progress (user_id, lesson_id, completed, score, xp_earned, completed_at)
        VALUES (?, ?, 1, ?, ?, datetime('now'))
        ON CONFLICT(user_id, lesson_id) DO UPDATE SET
        completed=1, score=max(score, excluded.score), completed_at=datetime('now')
    """, user_id, lesson_id, score, lesson[0]['xp_reward'])
    
    # Update streak (simplified)
    db.execute("UPDATE user_xp SET current_streak = current_streak + 1, last_activity = date('now') WHERE user_id = ?", user_id)
    
    return jsonify({"success": True, "xp_bonus": lesson[0]['xp_reward']})

@app.route("/api/academy/daily-challenge")
@login_required
def api_daily_challenge():
    import random, datetime
    # Use date as seed for daily consistency
    random.seed(str(datetime.date.today()))
    questions = db.execute("SELECT * FROM academy_questions ORDER BY RANDOM() LIMIT 5")
    return jsonify(questions)

# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import json
    app.run(debug=True)
