import os
import json
import time
import sqlite3
import warnings

# Silencing deprecation warnings from older libraries on Python 3.12
warnings.filterwarnings("ignore", category=DeprecationWarning)

# --- CLOUD-NATIVE HEADLESS OVERRIDE ---
try:
    import matplotlib
    matplotlib.use('Agg')
except: pass

from cs50 import SQL
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_compress import Compress
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import error_response, login_required, success_response
import f1_engine
import news_engine
import academy_engine
import supabase_engine
import telemetry_engine
import ai_engine
from security_engine import SecurityManager, role_required
from flask_talisman import Talisman
from flask_seasurf import SeaSurf
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_compress import Compress
from dotenv import load_dotenv

load_dotenv()
from monetization_engine import get_amazon_link, get_featured_products

# --- Vercel Cloud Compatibility ---
IS_VERCEL = os.environ.get('VERCEL') == '1'
basedir = os.path.abspath(os.path.dirname(__file__))

# ── App Setup ──────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod-security-ultra-long-key")

# Security Layer
talisman = Talisman(app, 
    force_https=IS_VERCEL, 
    strict_transport_security=IS_VERCEL,
    session_cookie_secure=False, # Disable to prevent session drops on certain networks
    session_cookie_http_only=True,
    content_security_policy={
        'default-src': ["'self'", "https://*", "http://*"],
        'script-src': [
            "'self'", 
            "https://unpkg.com", 
            "https://cdn.plot.ly", 
            "https://cdn.jsdelivr.net", 
            "https://accounts.google.com", 
            "https://cdnjs.cloudflare.com", 
            "'unsafe-inline'", 
            "'unsafe-eval'" # Required for Plotly.js charts
        ],
        'style-src': [
            "'self'", 
            "'unsafe-inline'", 
            "https://fonts.googleapis.com", 
            "https://use.fontawesome.com", 
            "https://cdnjs.cloudflare.com", 
            "https://unpkg.com"
        ],
        'font-src': ["'self'", "https://fonts.gstatic.com", "https://use.fontawesome.com", "https://cdnjs.cloudflare.com"],
        'img-src': ["'self'", "data:", "https://*", "http://*"],
        'connect-src': ["'self'", "https://*", "ws://*", "wss://*"],
        'frame-src': ["'self'", "https://*", "http://*"]
    }
)
csrf = SeaSurf(app)
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

# Performance Layer (Cache & Compression)
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 300})
Compress(app)

if not IS_VERCEL:
    # Only boot background threads on local/persistent servers
    SecurityManager.init_background_threads()

db_path = os.path.join(basedir, "autoverse.db")
db = SQL(f"sqlite:///{db_path}")
app.jinja_env.globals.update(min=min, max=max, int=int, str=str, json=json)

@app.context_processor
def inject_user_data():
    try:
        if session.get('user_id'):
            # Fetch with timeout/error protection
            xp_data = supabase_engine.get_user_xp(session['user_id'])
            return {'user_xp': xp_data, 'username': session.get('username'), 'get_amazon_link': get_amazon_link, 'featured_products': get_featured_products(), 'tag': 'autoverse7-21'}
    except Exception as e:
        print(f"Global Context Error: {e}")
    return {'user_xp': None, 'username': None, 'get_amazon_link': get_amazon_link, 'featured_products': get_featured_products(), 'tag': 'autoverse7-21'}

import threading
import car_auto_update
import os

# --- Vercel Cloud Compatibility ---
IS_VERCEL = os.environ.get('VERCEL') == '1'

if not IS_VERCEL:
    # Background Maintenance Engine (Local Development Only)
    def run_maintenance():
        """Periodically updates the car library and safety systems."""
        while True:
            try:
                car_auto_update.update_library()
            except: pass
            time.sleep(3600 * 24)

    maintenance_thread = threading.Thread(target=run_maintenance, daemon=True)
    maintenance_thread.start()
else:
    # On Vercel, ensure FastF1 cache is in /tmp
    try:
        import fastf1
        if not os.path.exists('/tmp/ff1_cache'):
            os.makedirs('/tmp/ff1_cache')
        fastf1.Cache.enable_cache('/tmp/ff1_cache')
    except: pass

@app.before_request
def enforce_login():
    """Global Security Gate: Enforce login for all high-value content."""
    # Architectural decision: Privacy, Terms, and About are public documents
    exempt = ['index', 'login', 'register', 'auth_oauth', 'auth_callback', 'static', 'about', 'contact', 'privacy', 'terms', 'elite', 'guides', 'guide_diecast', 'guide_cleaning', 'guide_books', 'guide_merch']
    if request.endpoint not in exempt:
        # Prevent loop/error on internal requests or missing endpoints
        if request.endpoint and not request.endpoint.startswith('static'):
            if 'user_id' not in session:
                return redirect(url_for('login'))

@app.route("/favicon.ico")
def favicon():
    # Attempt to serve from root first, then static
    if os.path.exists(os.path.join(app.root_path, 'favicon.ico')):
        from flask import send_from_directory
        return send_from_directory(app.root_path, 'favicon.ico')
    return app.send_static_file("favicon.ico")

@app.route("/")
@cache.cached(timeout=600) # Increased cache for home page shell
def index():
    featured_cars = db.execute("SELECT * FROM cars ORDER BY horsepower DESC LIMIT 3")
    daily_fact = academy_engine.get_daily_intel_fact()
    # News is now fetched asynchronously via /api/news to speed up initial load
    return render_template("index.html", featured_cars=featured_cars, daily_fact=daily_fact)

@app.route("/about")
def about(): return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # In real app, send mail here
        return render_template("contact.html", success="Message transmitted successfully.")
    return render_template("contact.html")

@app.route("/privacy")
def privacy(): return render_template("privacy.html")

@app.route("/terms")
def terms(): return render_template("terms.html")

@app.route("/elite")
def elite_portal():
    """Elite Membership Portal: High-value revenue channel."""
    return render_template("elite.html")

@app.route("/guides")
def guides_hub():
    """Content hub for affiliate-driven Buyer's Guides."""
    return render_template("guides/index.html")

@app.route("/guides/f1-diecast")
def guide_diecast(): return render_template("guides/f1_diecast.html", tag="autoverse7-21")

@app.route("/guides/cleaning-kit")
def guide_cleaning(): return render_template("guides/cleaning_kit.html", tag="autoverse7-21")

@app.route("/guides/f1-books")
def guide_books(): return render_template("guides/f1_books.html", tag="autoverse7-21")

@app.route("/guides/f1-merch")
def guide_merch(): return render_template("guides/f1_merch.html", tag="autoverse7-21")

@app.route("/maintenance/expand-academy")
def maintenance_expand():
    """Hidden Co-Founder utility to generate 360+ technical lessons."""
    try:
        COURSES = [
            (101, "The Engine Masterclass", "beginner", "engine-masterclass", "Complete internal combustion theory.", "⚙️", 101),
            (102, "Drivetrain Dynamics", "intermediate", "drivetrain-mastery", "Transmission, Differentials, and Torque.", "🔗", 102),
            (103, "Electrical Architecture", "expert", "electrical-architecture", "Modern sensors, ECU, and CAN-bus.", "⚡", 103),
            (104, "Chassis & Suspension", "expert", "chassis-suspension", "Geometry, Dampers, and Handling.", "🏎️", 104),
            (105, "Fuel & Induction", "intermediate", "fuel-induction", "Turbocharging and Fuel Delivery.", "⛽", 105),
            (106, "Braking & Safety", "beginner", "braking-mastery", "Hydraulics and ABS Logic.", "🛑", 106)
        ]
        
        conn = sqlite3.connect("autoverse.db")
        cursor = conn.cursor()
        cursor.executemany("INSERT OR REPLACE INTO academy_courses VALUES (?,?,?,?,?,?,?)", COURSES)
        
        lessons = []
        questions = []
        TOPICS = {
            101: ["Cylinder Blocks", "Pistons", "Crankshafts", "Camshafts", "Valvetrain", "Gaskets", "Timing Belts", "Oil Pumps", "Cooling Jackets", "Flywheels"],
            102: ["Manual Gearboxes", "Automatic Transmissions", "Torque Converters", "Clutches", "Differentials", "Driveshafts", "CV Joints", "Transfer Cases", "Syncromesh", "Flywheel Interfacing"],
            103: ["Battery Chemistry", "Alternators", "ECU Mapping", "Spark Plugs", "Sensors", "Wiring Looms", "CAN-bus", "Fuses & Relays", "Ignition Timing", "Diagnostic Port (OBD)"],
            104: ["Coil Springs", "Dampers", "Anti-roll Bars", "Control Arms", "Steering Rack", "Power Steering", "Alignment Geometry", "Camber & Toe", "Strut Braces", "Bushings"],
            105: ["Fuel Pumps", "Injectors", "Intake Manifolds", "Air Filters", "Turbochargers", "Intercoolers", "Superchargers", "Wastegates", "Blow-off Valves", "Fuel Pressure Regulators"],
            106: ["Brake Pads", "Rotors/Discs", "Calipers", "Master Cylinders", "Brake Lines", "ABS Modules", "Brake Fluid", "Handbrakes", "Drum Brakes", "Regenerative Braking"]
        }

        for c_id, topic_list in TOPICS.items():
            for i in range(1, 61):
                lesson_id = (c_id * 1000) + i
                topic = topic_list[(i-1) % len(topic_list)]
                title = f"{topic}: Advanced Lesson {i}"
                content = json.dumps({
                    "sections": [
                        {"title": "Introduction", "content": f"The {topic} is a critical component of the {c_id} ecosystem. Understanding its thermal and mechanical limits is key to performance."},
                        {"title": "Engineering Physics", "content": f"Analyzing the frictional coefficients and load bearing capacity of {topic} during high-stress operations."},
                        {"title": "Industrial Standards", "content": "Referencing SAE J-Series technical standards for tolerance and material specification."},
                        {"title": "Summary", "content": "Modern engineering requires zero-defect manufacturing for this unit."}
                    ]
                })
                lessons.append((lesson_id, c_id, title, f"{topic.lower().replace(' ', '-')}-{i}", content, i))
                questions.append((lesson_id * 10, lesson_id, "multiple_choice", f"What is the primary technical function of the {topic}?", json.dumps(["Structural Support", "Thermal Management", "Torque Transfer", "Energy Storage"]), "Structural Support", "Correct based on standard automotive theory.", None, 300))

        cursor.executemany("INSERT OR REPLACE INTO academy_lessons (id, course_id, title, slug, content_json, order_num) VALUES (?,?,?,?,?,?)", lessons)
        cursor.executemany("INSERT OR REPLACE INTO academy_questions (id, lesson_id, question_type, question, options_json, correct_answer, explanation, image_url, xp_reward) VALUES (?,?,?,?,?,?,?,?,?)", questions)
        conn.commit()
        conn.close()
        return jsonify({"status": "Success", "lessons_generated": len(lessons)})
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u, e, p, c = request.form.get("username", "").strip(), request.form.get("email", "").strip(), request.form.get("password", ""), request.form.get("confirm", "")
        if not u or not e or not p: return render_template("register.html", error="All fields required.")
        if p != c: return render_template("register.html", error="Passwords mismatch.")
        
        res, err = supabase_engine.signup_user(e, p, u)
        if err: return render_template("register.html", error=err)
        
        # Architect's Choice: Auto-login if session provided (Immediate Gratification)
        if hasattr(res, 'session') and res.session:
            session["user_id"] = res.user.id
            session["username"] = u
            return redirect(url_for("index"))
            
        return redirect(url_for("login", message="Account created. Please login."))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        e, p = request.form.get("email", "").strip(), request.form.get("password", "")
        res, err = supabase_engine.login_user(e, p)
        if err: return render_template("login.html", error="Invalid credentials.")
        
        session["user_id"] = res.user.id
        session["username"] = res.user.user_metadata.get("username", "Pilot")
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/auth/<provider>")
def auth_oauth(provider):
    if provider not in ['google', 'github', 'discord']:
        return redirect(url_for("login", error="Invalid Provider"))
        
    auth_url, err = supabase_engine.get_oauth_url(provider, url_for('auth_callback', _external=True))
    if err or not auth_url:
        return redirect(url_for("login", error="OAuth configuration error."))
    return redirect(auth_url)

@app.route("/auth/callback")
def auth_callback():
    code = request.args.get('code')
    if code:
        # Standard PKCE Flow
        res, err = supabase_engine.exchange_code_for_session(code)
        if not err and res.user:
            session["user_id"] = res.user.id
            session["username"] = res.user.user_metadata.get("username", res.user.email.split('@')[0])
            return redirect(url_for('index'))
        return redirect(url_for('login', error=err or "Auth Failed"))

    # Fallback to Implicit Flow (Handled in JS for hash fragments)
    return render_template("auth_callback.html")

@app.route("/auth/session", methods=["POST"])
def auth_session():
    data = request.get_json()
    acc = data.get('access_token')
    ref = data.get('refresh_token')
    
    if acc and ref:
        try:
            res = supabase_engine.get_supabase().auth.set_session(acc, ref)
            if res.user:
                session["user_id"] = res.user.id
                session["username"] = res.user.user_metadata.get("username", res.user.email.split('@')[0])
                return jsonify({"status": "success"})
        except Exception as e:
            print(f"Session Error: {e}")
            return jsonify({"status": "error", "message": str(e)}), 400
            
    return jsonify({"status": "error"}), 400

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# ── CAR EXPLORER ───────────────────────────────────────────────────────────────
@app.route("/cars")
def cars():
    brand, fuel, cat = request.args.get("brand", ""), request.args.get("fuel", ""), request.args.get("category", "")
    q = "SELECT * FROM cars WHERE 1=1"
    params = []
    if brand: q += " AND brand = ?"; params.append(brand)
    if fuel: q += " AND fuel_type = ?"; params.append(fuel)
    if cat: q += " AND category = ?"; params.append(cat)
    return render_template("cars.html", cars=db.execute(q + " ORDER BY category, brand", *params))

@app.route("/cars/<int:car_id>")
def car_detail(car_id):
    car = db.execute("SELECT * FROM cars WHERE id = ?", car_id)
    if not car:
        return redirect(url_for('index'))
    
    car = car[0]
    # Synthetic variation for acquisition channels if not in DB
    raw_price = car['price_usd'] or "1.5 Cr" 
    if isinstance(raw_price, (int, float)):
        dealer_price = f"₹{raw_price} Cr" if raw_price < 1000 else f"₹{round(raw_price/100, 2)} Cr"
    else:
        dealer_price = str(raw_price) if "₹" in str(raw_price) else f"₹{raw_price}"
    
    if "NaN" in str(dealer_price): dealer_price = "₹1.50 Cr" # Hard fallback

    # Calculate Luxury Premium (8-12% variance)
    try:
        # Extract number from "₹3.51 Cr" or "3.51"
        clean_val = str(dealer_price).replace('₹', '').replace(',', '').replace('Cr', '').strip()
        val = float(clean_val)
        luxury_price = f"₹{round(val * 1.09, 2)} Cr"
    except Exception as e:
        luxury_price = dealer_price

    similar = db.execute("SELECT * FROM cars WHERE (brand=? OR category=?) AND id != ? LIMIT 3", car['brand'], car['category'], car_id)
    return render_template("car.html", car=car, dealer_price=dealer_price, luxury_price=luxury_price, similar=similar)

@app.route("/compare")
@login_required
def compare():
    ids_param = request.args.get('ids', '')
    if not ids_param: return render_template("compare.html", cars=[])
    ids = [int(i) for i in ids_param.split(',') if i.strip().isdigit()][:4]
    placeholders = ",".join("?" * len(ids))
    cars = db.execute(f"SELECT * FROM cars WHERE id IN ({placeholders})", *ids) if ids else []
    return render_template("compare.html", cars=cars)

# ── ACADEMY ───────────────────────────────────────────────────────────────────
@app.route("/academy")
@login_required
def academy():
    courses = db.execute("SELECT * FROM academy_courses ORDER BY order_num")
    # Group by difficulty for Phase display
    phases = {
        "beginner": [c for c in courses if c['difficulty'] == 'beginner'],
        "intermediate": [c for c in courses if c['difficulty'] == 'intermediate'],
        "expert": [c for c in courses if c['difficulty'] == 'expert']
    }
    return render_template("academy.html", phases=phases)

@app.route("/academy/course/<slug>")
@login_required
def academy_course(slug):
    course = db.execute("SELECT * FROM academy_courses WHERE slug = ?", slug)
    if not course: return render_template("404.html"), 404
    lessons = db.execute("SELECT * FROM academy_lessons WHERE course_id = ? ORDER BY order_num", course[0]['id'])
    return render_template("academy/course.html", course=course[0], lessons=lessons)

@app.route("/academy/lesson/<identifier>")
@login_required
def academy_lesson(identifier):
    # Try ID first, then slug
    if identifier.isdigit():
        lesson = db.execute("SELECT * FROM academy_lessons WHERE id = ?", int(identifier))
    else:
        lesson = db.execute("SELECT * FROM academy_lessons WHERE slug = ?", identifier)
        
    if not lesson: return render_template("404.html"), 404
    
    # --- Elite Access Gate ---
    if lesson[0]['is_premium'] == 1 and session.get('user_role') != 'elite':
        return render_template("academy/elite_preview.html", lesson=lesson[0])

    course = db.execute("SELECT * FROM academy_courses WHERE id = ?", lesson[0]['course_id'])[0]
    content = json.loads(lesson[0]['content_json'])
    questions = db.execute("SELECT * FROM academy_questions WHERE lesson_id = ?", lesson[0]['id'])
    return render_template("academy/lesson.html", lesson=lesson[0], course=course, content=content, questions=questions)

@app.route("/academy/anatomy")
@login_required
def academy_anatomy(): return render_template("academy/anatomy.html")

@app.route("/academy/wind-tunnel")
@login_required
def academy_wind_tunnel(): return render_template("academy/wind_tunnel.html")

@app.route("/academy/strategy")
@login_required
def academy_strategy(): return render_template("academy/strategy.html")

# ── F1 HUB ────────────────────────────────────────────────────────────────────
@app.route("/f1")
@cache.cached(timeout=300)
def f1_hub():
    teams = db.execute("SELECT * FROM teams WHERE is_active_2026 = 1 LIMIT 4")
    legends = db.execute("SELECT * FROM drivers WHERE championships >= 3 ORDER BY championships DESC LIMIT 3")
    top_lap = db.execute("SELECT l.*, d.name as driver_name FROM f1_fastest_laps l JOIN drivers d ON l.driver_id = d.id ORDER BY l.speed_kmh DESC LIMIT 1")
    return render_template("f1/f1.html", teams=teams, legends=legends, top_lap=top_lap[0] if top_lap else None)

@app.route("/f1/live-hub")
@login_required
def f1_live_hub(): return render_template("f1/live.html")

@app.route("/f1/history")
def f1_history(): return render_template("f1/history.html")

@app.route("/f1/news")
@cache.cached(timeout=300)
def f1_news():
    news = news_engine.get_daily_briefings()
    return render_template("f1/news.html", news=news)

@app.route("/f1/drivers")
@cache.cached(timeout=600)
def f1_drivers():
    drivers = db.execute("SELECT d.*, t.name as team_name FROM drivers d LEFT JOIN teams t ON d.team_id = t.id WHERE d.is_active_2026 = 1 ORDER BY d.wins DESC")
    return render_template("f1/drivers.html", drivers=drivers)

@app.route("/f1/driver/<int:driver_id>")
def f1_driver(driver_id):
    driver = db.execute("SELECT d.*, t.name as team_name, t.primary_color FROM drivers d LEFT JOIN teams t ON d.team_id = t.id WHERE d.id = ?", driver_id)
    if not driver: return render_template("404.html"), 404
    return render_template("f1/driver_profile.html", driver=driver[0])

@app.route("/f1/teams")
@cache.cached(timeout=600)
def f1_teams():
    active = db.execute("SELECT * FROM teams WHERE is_active_2026 = 1")
    legacy = db.execute("SELECT * FROM teams WHERE is_active_2026 = 0")
    
    # Attach drivers to each active team
    for team in active:
        team['drivers'] = db.execute("SELECT name, image_url, number FROM drivers WHERE team_id = ? ORDER BY id", team['id'])
        
    return render_template("f1/teams.html", active_teams=active, legacy_teams=legacy)

@app.route("/f1/team/<int:team_id>")
@cache.cached(timeout=600)
def f1_team_profile(team_id):
    team = db.execute("SELECT * FROM teams WHERE id = ?", team_id)
    if not team: return render_template("404.html"), 404
    drivers = db.execute("SELECT * FROM drivers WHERE team_id = ? ORDER BY id", team_id)
    
    # ── Live Career Stats (Research Mode) ───────────────────────────────────
    career_stats = None
    if team[0].get('ergast_id'):
        career_stats = f1_engine.get_constructor_career_stats(team[0]['ergast_id'])
    
    # Use live data if available, fallback to DB
    stats = {
        'championships': career_stats['championships'] if career_stats else team[0]['championships'],
        'wins': career_stats['wins'] if career_stats else team[0]['wins'],
        'podiums': career_stats['podiums'] if career_stats else team[0]['podiums'],
        'points': career_stats['points'] if career_stats else 0
    }

    # Live Standing Data
    standings = f1_engine.get_constructor_standings()
    live_stat = next((s for s in standings if s['team'].lower() in team[0]['name'].lower()), None)
    
    # Live Telemetry Teaser
    drv_codes = [d['name'].split(' ')[-1].upper()[:3] for d in drivers]
    teaser_data = telemetry_engine._simulated("Active Teaser", drv_codes[:2])
    teaser_json = teaser_data[0] if isinstance(teaser_data, tuple) else teaser_data
    
    return render_template("f1/team.html", team=team[0], drivers=drivers, live_stat=live_stat, teaser_json=teaser_json, stats=stats)

@app.route("/api/timeline/<type>/<int:id>")
def api_timeline(type, id):
    """Unified API for driver and team timelines."""
    events = db.execute("SELECT * FROM f1_timeline WHERE entity_type = ? AND entity_id = ? ORDER BY year ASC", type, id)
    return jsonify(events)

@app.route("/f1/hall-of-fame")
def f1_hall_of_fame():
    legends = db.execute("SELECT * FROM drivers WHERE championships > 0 AND is_active_2026 = 0 ORDER BY championships DESC")
    return render_template("f1/hall_of_fame.html", legends=legends)

@app.route("/f1/legends")
def f1_legends(): return redirect(url_for('f1_hall_of_fame'))

@app.route("/f1/records")
def f1_records():
    laps = db.execute("SELECT l.*, d.name as driver_name, t.name as team_name FROM f1_fastest_laps l JOIN drivers d ON l.driver_id = d.id JOIN teams t ON l.team_id = t.id ORDER BY l.speed_kmh DESC")
    return render_template("f1/records.html", laps=laps)

@app.route("/garage")
@login_required
def garage():
    car_ids = supabase_engine.get_user_garage(session['user_id'])
    if not car_ids: return render_template("garage.html", cars=[])
    placeholders = ",".join("?" * len(car_ids))
    user_cars = db.execute(f"SELECT * FROM cars WHERE id IN ({placeholders})", *car_ids)
    return render_template("garage.html", cars=user_cars)

@app.route("/api/garage/add", methods=["POST"])
@login_required
def api_garage_add():
    data = request.get_json()
    car_id = data.get('car_id')
    if not car_id: return jsonify({"status": "error", "message": "Car ID required"}), 400
    
    success, msg = supabase_engine.add_to_garage(session['user_id'], car_id)
    if success:
        return jsonify({"status": "success", "message": msg})
    return jsonify({"status": "error", "message": msg}), 400

@app.route("/api/garage/remove", methods=["DELETE"])
@login_required
def api_garage_remove():
    data = request.get_json()
    car_id = data.get('car_id')
    if not car_id: return jsonify({"status": "error", "message": "Car ID required"}), 400
    
    success, msg = supabase_engine.remove_from_garage(session['user_id'], car_id)
    if success:
        return jsonify({"status": "success", "message": msg})
    return jsonify({"status": "error", "message": msg}), 400

# ── TELEMETRY LAB ─────────────────────────────────────────────────────────────
@app.route("/f1/telemetry")
@login_required
def f1_telemetry_hub():
    return render_template("f1/telemetry.html")

@app.route("/f1/telemetry/analysis")
@login_required
@role_required(required_role="elite")
def telemetry_analysis():
    gp = request.args.get("gp", "Bahrain")
    year = int(request.args.get("year", 2024))
    session_type = request.args.get("session_type", "R")
    drivers = request.args.getlist("drivers")
    if not drivers:
        drivers = [d for d in [request.args.get("d1"), request.args.get("d2")] if d]
    if not drivers:
        return redirect(url_for('f1_telemetry_hub', error="Please select at least one driver."))

    try:
        result = telemetry_engine.generate_multi_overlay(gp, drivers, year, session_type)
        chart_json, lap_summaries = result if isinstance(result, tuple) else (result, [])
        
        if not chart_json:
            return render_template("f1/telemetry_results.html", error="No real telemetry data available for this selection.")

        # Vercel Edge Caching: Cache the real data globally for 1 hour to ensure sub-5s speed for other users
        from flask import make_response
        resp = make_response(render_template("f1/telemetry_results.html",
                                chart_json=chart_json,
                                session_info={"name": gp, "year": year, "session": session_type},
                                drivers=drivers,
                                lap_summaries=lap_summaries))
        resp.headers['Cache-Control'] = 'public, s-maxage=3600, stale-while-revalidate=86400'
        return resp

    except Exception as e:
        print(f"Telemetry route error: {e}")
        sim_result = telemetry_engine._simulated(gp, drivers)
        chart_json, lap_summaries = sim_result if isinstance(sim_result, tuple) else (sim_result, [])
        return render_template("f1/telemetry_results.html",
                               chart_json=chart_json,
                               session_info={"name": gp, "year": year},
                               drivers=drivers,
                               lap_summaries=lap_summaries,
                               simulated=True)

# ── APIs ──────────────────────────────────────────────────────────────────────
@app.route("/api/news")
def api_news(): return jsonify(news_engine.get_daily_briefings())
@app.route("/api/f1/live")
def api_f1_live(): return jsonify(f1_engine.get_live_session_data())
@app.route("/api/f1/standings")
def api_f1_standings(): return jsonify(f1_engine.get_current_standings())
@app.route("/api/cars")
def api_cars(): return jsonify(db.execute("SELECT * FROM cars ORDER BY brand"))
@app.route("/api/cron/keepalive", methods=["GET"])
def api_cron_keepalive():
    try:
        # Ping SQLite DB
        db.execute("SELECT 1 FROM cars LIMIT 1")
        # Ping Supabase to keep it warm
        if supabase_engine.get_supabase():
            supabase_engine.get_supabase().table("garage").select("car_id").limit(1).execute()
        return jsonify({"status": "awake", "time": time.time()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/compare", methods=["POST"])
def api_compare():
    ids = request.get_json().get('ids', [])
    if not ids: return error_response("IDs required")
    placeholders = ",".join("?" * len(ids))
    return jsonify(db.execute(f"SELECT * FROM cars WHERE id IN ({placeholders})", *ids))

@app.route("/api/academy/answer", methods=["POST"])
@login_required
@role_required(required_role="user")
def api_academy_answer():
    data = request.get_json()
    q_id, ans = data.get('question_id'), data.get('answer')
    q = db.execute("SELECT * FROM academy_questions WHERE id=?", q_id)
    if not q: return error_response("Not found")
    
    correct = str(ans).lower() == str(q[0]['correct_answer']).lower()
    
    # Architect's Persistence Layer
    supabase_engine.save_quiz_response(session['user_id'], q_id, ans, correct)
    
    if correct:
        supabase_engine.update_xp(session['user_id'], q[0]['xp_reward'])
        
    return jsonify({"correct": correct, "explanation": q[0]['explanation']})

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """Handles communications with the Free AI Guide."""
    data = request.get_json()
    user_msg = data.get('message', '')
    history = data.get('history', [])
    
    if not user_msg:
        return jsonify({"error": "No message provided"}), 400
    
    ai_response = ai_engine.generate_ai_response(user_msg, history)
    return jsonify({"reply": ai_response})

# ── SEO & RELIABILITY ─────────────────────────────────────────────────────────
@app.route("/sitemap.xml")
def sitemap():
    """Dynamic sitemap generation for Google Search Console."""
    from flask import Response
    base = "https://autoverse-seven.vercel.app"
    pages = [
        "/", "/about", "/contact", "/privacy", "/terms", "/cars", "/academy",
        "/f1", "/f1/drivers", "/f1/teams", "/f1/history", "/f1/news",
        "/f1/hall-of-fame", "/f1/records", "/f1/telemetry", "/f1/live-hub",
    ]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for page in pages:
        priority = "1.0" if page == "/" else "0.8"
        xml += f'  <url><loc>{base}{page}</loc><priority>{priority}</priority><changefreq>weekly</changefreq></url>\n'
    
    # Add dynamic car pages
    try:
        cars = db.execute("SELECT id FROM cars")
        for car in cars:
            xml += f'  <url><loc>{base}/cars/{car["id"]}</loc><priority>0.6</priority><changefreq>monthly</changefreq></url>\n'
    except: pass
    
    xml += '</urlset>'
    return Response(xml, mimetype='application/xml')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('404.html'), 500

@app.after_request
def add_header(response):
    """Performance Engineering: Vercel Edge Caching & Browser Headers."""
    if 'Cache-Control' not in response.headers:
        if request.path.startswith('/static'):
            response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
        else:
            response.headers['Cache-Control'] = 'public, s-maxage=600, stale-while-revalidate=3600'
    return response

if __name__ == "__main__":
    app.run(debug=True)
