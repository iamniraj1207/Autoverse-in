import urllib.parse

# AutoVerse Monetization Engine V2.0
# Centralized control for Amazon Associate tracking and strategic product placement.

AMAZON_TAG = "autoverse7-21"
REGION_DOMAIN = "amazon.in"

def get_amazon_link(keyword, category=None):
    """
    Generates a high-fidelity, tracked Amazon Associate search link.
    This is the primary revenue driver for AutoVerse.
    """
    clean_keyword = urllib.parse.quote(keyword)
    params = {
        "tag": AMAZON_TAG,
        "ref": "as_li_ss_tl",
        "linkCode": "ll2"
    }
    query_string = urllib.parse.urlencode(params)
    return f"https://www.{REGION_DOMAIN}/s?k={clean_keyword}&{query_string}"

def get_fanatics_link(team_name):
    """
    SAFE ROUTE: Redirects to Amazon search for team gear until Fanatics is registered.
    Ensures no revenue leakage for the CEO.
    """
    return get_amazon_link(f"Official {team_name} F1 merchandise apparel")

def get_ticket_link(race_name="monaco"):
    """
    SAFE ROUTE: Redirects to Amazon search for race gear/memorabilia until Ticket provider is registered.
    """
    return get_amazon_link(f"F1 {race_name} grand prix memorabilia and tickets")

def get_featured_products(count=3):
    """Returns a list of high-priority featured product keywords."""
    return [
        {"title": "F1 Engineering Masterclass", "link": "https://amzn.to/4mQHPvK", "tag": "LITERATURE"},
        {"title": "2026 Team Gear", "link": get_amazon_link("official f1 team jerseys"), "tag": "APPAREL"},
        {"title": "F1 Race Essentials", "link": get_amazon_link("f1 race day gear"), "tag": "GEAR"}
    ][:count]
