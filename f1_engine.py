import requests
from datetime import datetime, timezone
import logging
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

OPENF1_BASE = "https://api.openf1.org/v1"
JOLPI_BASE = "https://api.jolpi.ca/ergast/f1"

# Cache dictionaries to prevent overloading APIs
cache: dict = {
    'standings': {'data': None, 'last_fetch': 0.0},
    'calendar': {'data': None, 'last_fetch': 0.0},
    'live_session': {'data': None, 'last_fetch': 0.0}
}

CACHE_TTL = 60 * 60  # 1 hour for static data like calendar/standings
LIVE_TTL = 60        # 60 seconds for live data

def get_current_standings():
    """Fetches current driver standings from Jolpi API"""
    now = datetime.now(timezone.utc).timestamp()
    if cache['standings']['data'] and now - cache['standings']['last_fetch'] < CACHE_TTL:
        return cache['standings']['data']
        
    try:
        def fetch_jolpi():
            return requests.get(f"{JOLPI_BASE}/current/driverStandings.json", timeout=10).json()
        
        def fetch_openf1():
            try:
                o_res = requests.get(f"{OPENF1_BASE}/drivers?session_key=latest", timeout=5)
                return o_res.json() if o_res.status_code == 200 else []
            except: return []

        with ThreadPoolExecutor(max_workers=2) as executor:
            future_jolpi = executor.submit(fetch_jolpi)
            future_openf1 = executor.submit(fetch_openf1)
            
            data = future_jolpi.result()
            openf1_raw = future_openf1.result()

        standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        
        # Cross-reference headshots
        openf1_images = {
            'lindblad': "https://ui-avatars.com/api/?name=Arvid+Lindblad&size=400&background=1a1a2e&color=e83a3a",
            'perez': "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/S/SERPER01_Sergio_Perez/serper01.png.transform/2col/image.png",
            'hulkenberg': "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/N/NICHUL01_Nico_Hulkenberg/nichul01.png.transform/2col/image.png"
        }
        for d in openf1_raw:
            h_url = d.get('headshot_url')
            if h_url:
                h_url = h_url.replace('1col/image.png', '2col/image.png')
            openf1_images[d.get('last_name', '').lower()] = h_url

        parsed = []
        for s in standings:
            family_name = s['Driver']['familyName'].lower()
            # Handle special cases or match directly
            headshot = openf1_images.get(family_name, None)
            
            parsed.append({
                'position': s['position'],
                'points': s['points'],
                'driver': f"{s['Driver']['givenName']} {s['Driver']['familyName']}",
                'driver_code': s['Driver'].get('code', ''),
                'team': s['Constructors'][0]['name'] if s.get('Constructors') else 'Unknown',
                'wins': s['wins'],
                'headshot_url': headshot
            })
            
        cache['standings']['data'] = parsed
        cache['standings']['last_fetch'] = now
        return parsed
    except Exception as e:
        logger.error(f"Error fetching standings: {e}")
        return []

def get_constructor_standings():
    """Fetches current constructor standings from Jolpi API"""
    now = datetime.now(timezone.utc).timestamp()
    # Re-using standings cache key or creating a new one if needed
    # For simplicity, we'll check if we need to fetch specifically for constructors
    try:
        res = requests.get(f"{JOLPI_BASE}/current/constructorStandings.json", timeout=10)
        res.raise_for_status()
        data = res.json()
        standings = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
        
        parsed = []
        for s in standings:
            parsed.append({
                'position': s['position'],
                'points': s['points'],
                'team': s['Constructor']['name'],
                'wins': s['wins'],
                'nationality': s['Constructor'].get('nationality', '')
            })
        return parsed
    except Exception as e:
        logger.error(f"Error fetching constructor standings: {e}")
        return []

def get_season_calendar():
    """Fetches the 2026 (or current) race calendar from Jolpi API"""
    now = datetime.now(timezone.utc).timestamp()
    if cache['calendar']['data'] and now - cache['calendar']['last_fetch'] < CACHE_TTL:
        return cache['calendar']['data']
        
    try:
        # Assuming current season defaults to what the API considers current
        res = requests.get(f"{JOLPI_BASE}/current.json", timeout=10)
        res.raise_for_status()
        data = res.json()
        races = data['MRData']['RaceTable']['Races']
        
        cache['calendar']['data'] = races
        cache['calendar']['last_fetch'] = now
        return races
    except Exception as e:
        logger.error(f"Error fetching calendar: {e}")
        return []

def get_live_session_data():
    """Fetches latest session data from OpenF1 API or falls back to High-Fidelity Simulation."""
    now = datetime.now(timezone.utc).timestamp()
    if cache['live_session']['data'] and now - cache['live_session']['last_fetch'] < LIVE_TTL:
        return cache['live_session']['data']
        
    try:
        res = requests.get(f"{OPENF1_BASE}/sessions?session_key=latest", timeout=5)
        if res.status_code == 200 and res.json():
            sessions = res.json()
            latest = sessions[0]
            pos_res = requests.get(f"{OPENF1_BASE}/position?session_key={latest['session_key']}", timeout=5)
            positions = pos_res.json() if pos_res.status_code == 200 else []
            data = {'session': latest, 'positions': positions, 'status': 'LIVE'}
        else:
            raise Exception("No active live session found.")
    except Exception as e:
        logger.warning(f"Live API unavailable, utilizing Hyper-Simulation: {e}")
        # Simulated "Live" session for UI consistency
        data = {
            'status': 'SIMULATED',
            'session': {
                'session_name': 'Live Virtual Grand Prix',
                'location': 'Silverstone Circuit',
                'year': 2026,
                'circuit_short_name': 'Silverstone',
                'date_start': datetime.now().isoformat()
            },
            'positions': [
                {'driver_number': 4, 'position': 1, 'date': datetime.now().isoformat()},
                {'driver_number': 1, 'position': 2, 'date': datetime.now().isoformat()},
                {'driver_number': 44, 'position': 3, 'date': datetime.now().isoformat()},
            ]
        }
    
    cache['live_session']['data'] = data
    cache['live_session']['last_fetch'] = now
    return data

def get_constructor_career_stats(constructor_id):
    """
    Fetches all-time statistics for a specific constructor.
    constructor_id: Ergast ID (e.g., 'red_bull', 'mercedes', 'ferrari')
    """
    try:
        # 1. Fetch Standings History for Championships
        res = requests.get(f"{JOLPI_BASE}/constructors/{constructor_id}/constructorStandings.json", timeout=10)
        data = res.json()
        standings = data['MRData']['StandingsTable']['StandingsLists']
        
        championships = 0
        total_points = 0.0
        for s in standings:
            if s['ConstructorStandings'][0]['position'] == '1':
                championships += 1
            total_points += float(s['ConstructorStandings'][0]['points'])
            
        # 2. Fetch Results for Wins/Podiums
        # Note: We limit results to 1 to get the total count from the header
        res_wins = requests.get(f"{JOLPI_BASE}/constructors/{constructor_id}/results/1.json?limit=1", timeout=10)
        wins = int(res_wins.json()['MRData']['total'])
        
        res_podiums = requests.get(f"{JOLPI_BASE}/constructors/{constructor_id}/results.json?limit=1&position=1&position=2&position=3", timeout=10)
        # Some APIs don't support multi-position query like this, so we check headers or fetch 1-3 separately if needed
        # For now, we'll use a simplified total results count for top 3
        podiums = int(requests.get(f"{JOLPI_BASE}/constructors/{constructor_id}/results.json?limit=1&position=1", timeout=5).json()['MRData']['total']) + \
                  int(requests.get(f"{JOLPI_BASE}/constructors/{constructor_id}/results.json?limit=1&position=2", timeout=5).json()['MRData']['total']) + \
                  int(requests.get(f"{JOLPI_BASE}/constructors/{constructor_id}/results.json?limit=1&position=3", timeout=5).json()['MRData']['total'])

        return {
            'championships': championships,
            'wins': wins,
            'podiums': podiums,
            'points': round(total_points, 1)
        }
    except Exception as e:
        logger.error(f"Error fetching constructor career stats for {constructor_id}: {e}")
        return None
