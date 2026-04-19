"""
telemetry_engine.py — AutoVerse Race Intelligence Engine
Uses FastF1 for real historical F1 telemetry data.
Falls back to rich simulation when session data is unavailable.
"""
try:
    import fastf1
    from fastf1 import plotting
    FASTF1_AVAILABLE = True
except ImportError:
    FASTF1_AVAILABLE = False

import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import json

# FastF1 Cache
CACHE_DIR = os.path.join(os.getcwd(), ".tmp", "fastf1_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

if FASTF1_AVAILABLE:
    fastf1.Cache.enable_cache(CACHE_DIR)

# Full 2024 F1 Calendar mapped to FastF1 round identifiers
F1_2024_CALENDAR = [
    {"name": "Bahrain Grand Prix",        "round": 1,  "identifier": "Bahrain"},
    {"name": "Saudi Arabian Grand Prix",  "round": 2,  "identifier": "Saudi Arabia"},
    {"name": "Australian Grand Prix",     "round": 3,  "identifier": "Australia"},
    {"name": "Japanese Grand Prix",       "round": 4,  "identifier": "Japan"},
    {"name": "Chinese Grand Prix",        "round": 5,  "identifier": "China"},
    {"name": "Miami Grand Prix",          "round": 6,  "identifier": "Miami"},
    {"name": "Monaco Grand Prix",         "round": 8,  "identifier": "Monaco"},
    {"name": "Canadian Grand Prix",       "round": 9,  "identifier": "Canada"},
    {"name": "Spanish Grand Prix",        "round": 10, "identifier": "Spain"},
    {"name": "British Grand Prix",        "round": 12, "identifier": "Great Britain"},
    {"name": "Hungarian Grand Prix",      "round": 13, "identifier": "Hungary"},
    {"name": "Belgian Grand Prix",        "round": 14, "identifier": "Belgium"},
    {"name": "Dutch Grand Prix",          "round": 15, "identifier": "Netherlands"},
    {"name": "Italian Grand Prix",        "round": 16, "identifier": "Italy"},
    {"name": "Singapore Grand Prix",      "round": 18, "identifier": "Singapore"},
    {"name": "United States Grand Prix",  "round": 19, "identifier": "USA"},
    {"name": "Mexico City Grand Prix",    "round": 20, "identifier": "Mexico"},
    {"name": "Las Vegas Grand Prix",      "round": 22, "identifier": "Las Vegas"},
    {"name": "Abu Dhabi Grand Prix",      "round": 24, "identifier": "Abu Dhabi"},
]

# Driver colors for consistent charting
DRIVER_COLORS = {
    'VER': '#3671C6', 'NOR': '#FF8000', 'LEC': '#E8002D', 'SAI': '#E8002D',
    'HAM': '#27F4D2', 'RUS': '#27F4D2', 'PIA': '#FF8000', 'ALO': '#358C75',
    'STR': '#358C75', 'PER': '#3671C6', 'GAS': '#B6BABD', 'OCO': '#B6BABD',
    'TSU': '#6692FF', 'RIC': '#6692FF', 'HUL': '#B6BABD', 'MAG': '#B6BABD',
    'BOT': '#52E252', 'ZHO': '#52E252', 'ALB': '#64C4FF', 'SAR': '#64C4FF',
    'BEA': '#B6BABD',
}

def get_driver_color(driver):
    return DRIVER_COLORS.get(driver.upper(), '#e83a3a')

def get_calendar():
    """Returns the full 2024 F1 calendar for the frontend."""
    return F1_2024_CALENDAR

def generate_multi_overlay(gp_identifier, drivers, year=2024, session_type='R'):
    """
    Fetches real FastF1 telemetry and builds a premium multi-panel Plotly chart.
    Panels: Speed Profile | Throttle/Brake | Gear | Delta Time
    Falls back to rich simulation on error.
    """
    if not FASTF1_AVAILABLE or not drivers:
        return _simulated(gp_identifier, drivers or ['VER', 'HAM'])

    try:
        session = fastf1.get_session(year, gp_identifier, session_type)
        session.load(telemetry=True, laps=True, weather=False, messages=False)

        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.04,
            subplot_titles=(
                "SPEED  (KM/H)",
                "THROTTLE %  |  BRAKE %",
                "GEAR"
            ),
            row_heights=[0.5, 0.3, 0.2]
        )

        lap_summaries = []
        ref_distance = None

        for driver in drivers:
            try:
                drv_laps = session.laps.pick_driver(driver.upper())
                if drv_laps.empty:
                    continue
                fastest = drv_laps.pick_fastest()
                tel = fastest.get_telemetry().add_distance()

                color = get_driver_color(driver)
                lap_time = str(fastest['LapTime']).split(' ')[-1][:10] if fastest['LapTime'] is not None else 'N/A'
                lap_summaries.append({
                    'driver': driver.upper(),
                    'lap_time': lap_time,
                    'color': color
                })

                kw = dict(x=tel['Distance'], mode='lines', line=dict(color=color, width=2.5))

                # Row 1: Speed
                fig.add_trace(go.Scatter(y=tel['Speed'], name=driver.upper(), **kw), row=1, col=1)
                # Row 2: Throttle (solid), Brake (dashed)
                fig.add_trace(go.Scatter(y=tel['Throttle'], name=f"{driver.upper()} THR", showlegend=False,
                                         line=dict(color=color, width=1.5), x=tel['Distance'], mode='lines'), row=2, col=1)
                if 'Brake' in tel.columns:
                    brake_pct = tel['Brake'].astype(float) * 100
                    fig.add_trace(go.Scatter(y=brake_pct, name=f"{driver.upper()} BRK", showlegend=False,
                                             line=dict(color=color, width=1, dash='dot'), x=tel['Distance'], mode='lines'), row=2, col=1)
                # Row 3: Gear
                if 'nGear' in tel.columns:
                    fig.add_trace(go.Scatter(y=tel['nGear'], name=f"{driver.upper()} GEAR", showlegend=False,
                                             line=dict(color=color, width=2, shape='hv'), x=tel['Distance'], mode='lines'), row=3, col=1)

                if ref_distance is None:
                    ref_distance = tel['Distance'].max()

            except Exception as driver_err:
                print(f"Driver {driver} telemetry error: {driver_err}")
                continue

        if not lap_summaries:
            return _simulated(gp_identifier, drivers)

        _style_figure(fig, f"{gp_identifier.upper()} {year} — FASTEST LAP TELEMETRY")
        return fig.to_json(), lap_summaries

    except Exception as e:
        print(f"FastF1 session error for {gp_identifier}: {e}")
        return _simulated(gp_identifier, drivers)


def _style_figure(fig, title):
    """Apply premium dark theme to Plotly figure."""
    fig.update_layout(
        template="plotly_dark",
        title=dict(text=title, font=dict(family="'Bebas Neue', sans-serif", size=26), x=0.02),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.04,
            xanchor="right", x=1,
            font=dict(family="'DM Mono', monospace", size=12)
        ),
        height=780,
        margin=dict(l=60, r=20, t=90, b=50),
        hovermode='x unified',
        font=dict(family="'DM Mono', monospace", color="rgba(255,255,255,0.7)")
    )
    fig.update_xaxes(
        showgrid=True, gridcolor='rgba(255,255,255,0.04)',
        showline=True, linecolor='rgba(255,255,255,0.1)',
        title_text="DISTANCE (M)",
        row=3, col=1
    )
    fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.04)')


def _simulated(gp_name, drivers):
    """Rich simulated telemetry with mini-sector phases."""
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        vertical_spacing=0.06,
        subplot_titles=("SIMULATED SPEED (KM/H)", "SIMULATED G-FORCE")
    )

    dist = list(range(0, 5200, 15))

    for idx, driver in enumerate(drivers):
        color = get_driver_color(driver)
        speed, gforce = [], []
        curr = random.uniform(220, 260)
        for d in dist:
            # Simulate straights and corners
            phase = (d // 300) % 4
            if phase == 0: target = random.uniform(280, 330)
            elif phase == 1: target = random.uniform(100, 160)
            elif phase == 2: target = random.uniform(200, 250)
            else: target = random.uniform(160, 220)
            curr = curr * 0.85 + target * 0.15
            speed.append(round(curr, 1))
            gforce.append(round(abs(curr - 200) / 50 + random.uniform(0, 1.5), 2))

        fig.add_trace(go.Scatter(x=dist, y=speed, name=driver.upper(), mode='lines',
                                  line=dict(color=color, width=2.5)), row=1, col=1)
        fig.add_trace(go.Scatter(x=dist, y=gforce, name=driver.upper(), showlegend=False, mode='lines',
                                  line=dict(color=color, width=1.5, dash='dot')), row=2, col=1)

    _style_figure(fig, f"SIMULATION — {gp_name.upper()} GRID OVERLAY")
    lap_summaries = [{'driver': d.upper(), 'lap_time': 'SIMULATED', 'color': get_driver_color(d)} for d in drivers]
    return fig.to_json(), lap_summaries


# Legacy wrappers
def get_telemetry_data(year, gp, session_type, d1, d2=None):
    drivers = [d for d in [d1, d2] if d]
    result = generate_multi_overlay(gp, drivers, year, session_type)
    if isinstance(result, tuple):
        return result[0], None
    return result, None

def create_telemetry_chart(data, drivers): return data
def generate_simulated_telemetry(gp_name, drivers):
    result = _simulated(gp_name, drivers)
    return result[0] if isinstance(result, tuple) else result
