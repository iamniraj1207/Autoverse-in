# AUTOVERSE — The Ultimate Automotive & F1 Enthusiast Platform

#### Video Demo: https://youtu.be/5MEH26eyQmA

## Description

**AutoVerse** is a premium, high-performance web application designed for car enthusiasts and Formula One fans. Built with a focus on cinematic aesthetics and interactive experiences, it combines a massive car database with a futuristic F1 Hub, an educational Academy, and personalized garage management.

The platform leverages modern web technologies to deliver a "WOW" factor through glassmorphism, dynamic video backgrounds, and smooth scroll animations (AOS).

### Key Features

#### 1. Cinematic Home & Discovery
- **Hero Video Background**: High-interpolation (60fps) automotive visuals that set a premium tone.
- **Dynamic AOS Animations**: Elements reveal themselves elegantly as the user scrolls, creating a sense of depth and quality.

#### 2. Virtual Car Explorer & Comparison
- **Virtual Scroll Gallery**: Optimized performance for browsing hundreds of car models with real-time filtering by brand, fuel type, and category.
- **Comparison Engine**: A side-by-side spec comparison tool that allows users to analyze up to 4 cars simultaneously, highlighting power, speed, and pricing.
- **3D Viewer Integration**: Support for interactive car models to give users a 360-degree look at featured vehicles.

#### 3. F1 Hub: The 2026 Grid & History
- **2026 Grid Integration**: Real-time data for future F1 constructors and driver lineups.
- **Interactive Timelines**: Aceternity-style vertical timelines for drivers and teams, documenting career milestones and championship wins.
- **Hall of Fame**: A dedicated section for F1 legends with high-quality imagery and career statistics.

#### 4. AutoVerse Academy (Gamified Learning)
- **XP & Leveling System**: Users earn Experience Points (XP) by completing interactive lessons and quizzes.
- **Course Dashboard**: Track progress across multiple automotive engineering and history modules.
- **Global Leaderboard**: Compete with other enthusiasts to become the ultimate automotive expert.

#### 5. User Personalization
- **Digital Garage**: Authenticated users can save their favorite cars to a private garage for quick access.
- **User Dashboard**: Displays XP rank, current level, and learning streaks.

### Technical Stack
- **Backend**: Flask (Python)
- **Database**: SQLite with CS50 SQL for robust query handling.
- **Frontend**: Vanilla HTML5, CSS3 (Glassmorphism), and JavaScript.
- **Animations**: AOS (Animate on Scroll) for cinematic transitions.
- **Media**: Optimized MP4 backgrounds and custom-sliced F1 assets.

### File Structure Highlights
- `app.py`: The core Flask application managing all routes (Auth, Cars, F1, Academy).
- `static/js/`: Modular JavaScript for features like virtual scrolling, 360 views, and timelines.
- `templates/`: Cinematic Jinja2 templates organized by feature modules (F1, Academy, Car Details).
- `autoverse.db`: The master relational database containing car specs, F1 history, and user progress.

---

### Installation & Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Initialize the database: `python init_db.py` and `python seed_f1_complete.py`.
4. Run the server: `python app.py`.
5. Open `http://127.0.0.1:5000` in your browser.

---
*AutoVerse — Where Car Culture Lives.*
