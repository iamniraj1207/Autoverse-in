import os

# Ensure the directory exists
logo_dir = os.path.join('static', 'img', 'teams')
os.makedirs(logo_dir, exist_ok=True)

TEAM_LOGOS = {
  'red_bull': {
    'name': 'RED BULL RACING', 'abbr': 'RBR',
    'bg': '#0A1831', 'accent': '#CC1E1E', 'text': '#3671C6'
  },
  'ferrari': {
    'name': 'SCUDERIA FERRARI', 'abbr': 'SF',
    'bg': '#8B0000', 'accent': '#FFD700', 'text': '#ffffff'
  },
  'mercedes': {
    'name': 'MERCEDES AMG', 'abbr': 'AMG',
    'bg': '#00413B', 'accent': '#00D2BE', 'text': '#ffffff'
  },
  'mclaren': {
    'name': 'MCLAREN F1', 'abbr': 'MCL',
    'bg': '#4A2400', 'accent': '#FF8000', 'text': '#ffffff'
  },
  'aston_martin': {
    'name': 'ASTON MARTIN', 'abbr': 'AM',
    'bg': '#003830', 'accent': '#CEDC00', 'text': '#ffffff'
  },
  'alpine': {
    'name': 'ALPINE F1', 'abbr': 'ALP',
    'bg': '#001A4A', 'accent': '#0090FF', 'text': '#ffffff'
  },
  'haas': {
    'name': 'HAAS F1 TEAM', 'abbr': 'HAA',
    'bg': '#1A0000', 'accent': '#E8002D', 'text': '#ffffff'
  },
  'racing_bulls': {
    'name': 'RACING BULLS', 'abbr': 'RB',
    'bg': '#0A0F40', 'accent': '#1434CB', 'text': '#ffffff'
  },
  'williams': {
    'name': 'WILLIAMS RACING', 'abbr': 'WIL',
    'bg': '#001A70', 'accent': '#005AFF', 'text': '#ffffff'
  },
  'sauber': {
    'name': 'STAKE SAUBER', 'abbr': 'SAU',
    'bg': '#0A2A0A', 'accent': '#52E252', 'text': '#ffffff'
  },
}

for slug, data in TEAM_LOGOS.items():
  svg = f'''<svg xmlns="http://www.w3.org/2000/svg" 
    viewBox="0 0 220 90" width="220" height="90">
  <defs>
    <linearGradient id="grad_{slug}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{data['bg']};stop-opacity:1"/>
      <stop offset="100%" style="stop-color:{data['bg']}dd;stop-opacity:1"/>
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="220" height="90" rx="6" 
        fill="url(#grad_{slug})"/>
  
  <!-- Left accent bar -->
  <rect x="0" y="0" width="4" height="90" rx="2"
        fill="{data['accent']}"/>
  
  <!-- Top accent line -->
  <rect x="4" y="0" width="216" height="2"
        fill="{data['accent']}" opacity="0.4"/>
  
  <!-- Abbreviation — large -->
  <text x="110" y="52" 
        font-family="Arial Black, sans-serif"
        font-size="28" font-weight="900"
        fill="{data['accent']}"
        text-anchor="middle"
        letter-spacing="3">{data['abbr']}</text>
  
  <!-- Full name — small -->
  <text x="110" y="72"
        font-family="Arial, monospace"
        font-size="8" font-weight="400"
        fill="{data['text']}"
        text-anchor="middle"
        letter-spacing="2"
        opacity="0.7">{data['name']}</text>
  
  <!-- Corner decoration -->
  <rect x="190" y="10" width="16" height="2"
        fill="{data['accent']}" opacity="0.5"/>
  <rect x="190" y="16" width="10" height="2"
        fill="{data['accent']}" opacity="0.3"/>
</svg>'''
  
  path = os.path.join(logo_dir, f"{slug}_logo.svg")
  with open(path, 'w') as f:
    f.write(svg)
  print(f"Created: {path}")

print("All 10 team SVG logos generated")
