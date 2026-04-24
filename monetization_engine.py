import urllib.parse

# AutoVerse Monetization Engine V2.0
# Centralized control for Amazon Associate tracking and strategic product placement.

AMAZON_TAG = "autoverse7-21"
REGION_DOMAIN = "amazon.in" # Targeted at India as requested, can be expanded.

PRODUCT_CATEGORIES = {
    "f1_merch": "F1 Official Merchandise, Team Caps, Jerseys",
    "diecast": "F1 Diecast Models, 1:18 Scale Cars, Bburago",
    "apparel": "Automotive Hoodies, Racing Apparel, Motorsport Clothing",
    "lifestyle": "Racing Shoes, Driving Gloves, Tech Gear",
    "maintenance": "Car Cleaning Kit, Detailing Gear, Ceramic Coating",
    "literature": "Automotive Engineering Books, Adrian Newey, F1 History"
}

def get_amazon_link(keyword, category=None):
    """
    Generates a high-fidelity, tracked Amazon Associate search link.
    Strategically appends tracking parameters to maximize conversion registration.
    """
    clean_keyword = urllib.parse.quote(keyword)
    base_url = f"https://www.{REGION_DOMAIN}/s?k={clean_keyword}"
    
    # Tracking parameters
    params = {
        "tag": AMAZON_TAG,
        "ref": "as_li_ss_tl",  # Standard referral tag
        "linkCode": "ll2",     # High-conversion link code
        "linkId": "autoverse_engine_v2" # Custom internal tracking ID
    }
    
    query_string = urllib.parse.urlencode(params)
    return f"{base_url}&{query_string}"

def get_featured_products(count=3):
    """Returns a list of high-priority featured product keywords for the homepage intel cards."""
    return [
        {"title": "F1 Engineering Masterclass", "keyword": "How to Build a Car Adrian Newey", "tag": "LITERATURE"},
        {"title": "2026 Team Gear", "keyword": "Official F1 Team Merchandise 2024", "tag": "APPAREL"},
        {"title": "Precision Diecast", "keyword": "1:18 scale F1 diecast bburago", "tag": "GEAR"}
    ][:count]
