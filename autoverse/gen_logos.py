import os

teams = [
    ('red_bull_logo.svg', '#1E3A5F', '#CC1E1E', 'RBR', 'RED BULL RACING'),
    ('ferrari_logo.svg', '#DC143C', '#FFD700', 'SF', 'SCUDERIA FERRARI'),
    ('mercedes_logo.svg', '#00D2BE', '#000000', 'MGP', 'MERCEDES-AMG'),
    ('mclaren_logo.svg', '#FF8000', '#000000', 'MCL', 'MCLAREN F1'),
    ('aston_martin_logo.svg', '#006F62', '#CEDC00', 'AMF', 'ASTON MARTIN'),
    ('alpine_logo.svg', '#0090FF', '#FF0000', 'ALP', 'ALPINE F1'),
    ('haas_logo.svg', '#E8002D', '#FFFFFF', 'HAS', 'HAAS F1'),
    ('racing_bulls_logo.svg', '#1434CB', '#FFFFFF', 'VCARB', 'RACING BULLS'),
    ('williams_logo.svg', '#005AFF', '#FFFFFF', 'WIL', 'WILLIAMS RACING'),
    ('sauber_logo.svg', '#52E252', '#000000', 'KICK', 'SAUBER F1'),
    ('audi_logo.svg', '#000000', '#F1F1F1', 'AUDI', 'AUDI F1 TEAM'),
    ('cadillac_logo.svg', '#C4CED4', '#000000', 'GM', 'CADILLAC F1')
]

template = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 80" width="200" height="80">
  <rect width="200" height="80" fill="transparent"/>
  <rect x="4" y="4" width="192" height="72" rx="8" fill="{bg_color}"/>
  <text x="100" y="48" font-family="'Arial Black', sans-serif" font-size="32" font-weight="900" fill="{text_color}" text-anchor="middle" letter-spacing="2">{abbr}</text>
  <text x="100" y="65" font-family="monospace" font-size="9" fill="#8892a4" text-anchor="middle" letter-spacing="3">{full_name}</text>
</svg>"""

os.makedirs('static/img/teams', exist_ok=True)

for filename, bg, text, abbr, full in teams:
    with open(f'static/img/teams/{filename}', 'w') as f:
        f.write(template.format(bg_color=bg, text_color=text, abbr=abbr, full_name=full))

print("Created 10 team logos.")
