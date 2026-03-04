import sqlite3
import requests
import time

conn = sqlite3.connect('autoverse.db')
db = conn.cursor()

WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"

def get_wiki_image(page_title):
    """Get main image URL from Wikipedia page"""
    params = {
        'action': 'query',
        'titles': page_title,
        'prop': 'pageimages',
        'format': 'json',
        'pithumbsize': 500,
        'pilicense': 'any'
    }
    try:
        r = requests.get(WIKIPEDIA_API, params=params, timeout=5)
        data = r.json()
        pages = data['query']['pages']
        for page in pages.values():
            if 'thumbnail' in page:
                return page['thumbnail']['source']
    except Exception as e:
        print(f"  Error fetching {page_title}: {e}")
    return None

# Wikipedia page titles for each driver
DRIVER_WIKI_PAGES = {
    'Max Verstappen':     'Max Verstappen',
    'Lewis Hamilton':     'Lewis Hamilton',
    'Charles Leclerc':    'Charles Leclerc',
    'Lando Norris':       'Lando Norris',
    'Carlos Sainz':       'Carlos Sainz Jr.',
    'George Russell':     'George Russell (racing driver)',
    'Oscar Piastri':      'Oscar Piastri',
    'Fernando Alonso':    'Fernando Alonso',
    'Lance Stroll':       'Lance Stroll',
    'Pierre Gasly':       'Pierre Gasly',
    'Alexander Albon':    'Alexander Albon',
    'Nico Hulkenberg':    'Nico Hülkenberg',
    'Esteban Ocon':       'Esteban Ocon',
    'Guanyu Zhou':        'Zhou Guanyu',
    'Valtteri Bottas':    'Valtteri Bottas',
    'Kimi Antonelli':     'Andrea Kimi Antonelli',
    'Jack Doohan':        'Jack Doohan',
    'Liam Lawson':        'Liam Lawson',
    'Oliver Bearman':     'Oliver Bearman',
    'Isack Hadjar':       'Isack Hadjar',
    'Gabriel Bortoleto':  'Gabriel Bortoleto',
    # Legends
    'Ayrton Senna':       'Ayrton Senna',
    'Michael Schumacher': 'Michael Schumacher',
    'Alain Prost':        'Alain Prost',
    'Niki Lauda':         'Niki Lauda',
    'Juan Manuel Fangio': 'Juan Manuel Fangio',
    'Jim Clark':          'Jim Clark',
    'Jackie Stewart':     'Jackie Stewart',
    'Nigel Mansell':      'Nigel Mansell',
    'Sebastian Vettel':   'Sebastian Vettel',
    'Jenson Button':      'Jenson Button',
    'Kimi Raikkonen':     'Kimi Räikkönen',
    'Mika Hakkinen':      'Mika Häkkinen',
    'Damon Hill':         'Damon Hill',
}

# Fallback avatar
def avatar_url(name, bg='1a1a2e', fg='e83a3a'):
    return (f"https://ui-avatars.com/api/?name="
            f"{name.replace(' ','+')}&size=400"
            f"&background={bg}&color={fg}"
            f"&bold=true&font-size=0.28&format=png")

for driver_name, wiki_page in DRIVER_WIKI_PAGES.items():
    print(f"Fetching: {driver_name}...")
    url = get_wiki_image(wiki_page)
    
    if url:
        print(f"  ✓ Got Wikipedia image")
    else:
        print(f"  ✗ Using avatar fallback")
        url = avatar_url(driver_name)
    
    db.execute(
        "UPDATE drivers SET image_url=? WHERE name=?",
        (url, driver_name)
    )
    time.sleep(0.3)  # Be nice to Wikipedia API

conn.commit()
conn.close()
print("Driver images updated via Wikipedia.")
