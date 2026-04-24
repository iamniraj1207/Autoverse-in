import requests
import logging
import os
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Load from environment eventually, currently using generic F1 query
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "") # User should add this to .env

def get_f1_headlines():
    """Fetches F1 news from NewsAPI."""
    if not NEWS_API_KEY:
        # Fallback with mixed F1 and Car news
        return [
            {
                'title': "The 2026 Ferrari F80 Hypercar revealed in Maranello",
                'url': "https://www.ferrari.com",
                'summary': "Ferrari unveils their latest pinnacle of performance featuring a hybrid V6 powertrain and active F1-derived aero...",
                'date': datetime.now().strftime("%Y-%m-%d"),
                'source': 'AutoVerse Intelligence'
            },
            {
                'title': "2026 Regulation Changes: What we know so far",
                'url': "https://www.formula1.com",
                'summary': "The FIA has released new details regarding the 2026 power units and aero rules...",
                'date': datetime.now().strftime("%Y-%m-%d"),
                'source': 'F1 Official'
            },
            {
                'title': "Porsche Mission X: The future of electric performance",
                'url': "https://newsroom.porsche.com",
                'summary': "Porsche explores the limits of electric hypercars with a focus on power-to-weight ratios and high-speed cornering stability...",
                'date': datetime.now().strftime("%Y-%m-%d"),
                'source': 'Stuttgart Feed'
            },
            {
                'title': "Adrian Newey joins Aston Martin for 2026 technical development",
                'url': "https://www.astonmartinf1.com",
                'summary': "The legendary designer shifts focus to the 2026 regulations, aiming to master the active-aero paradigm shift...",
                'date': datetime.now().strftime("%Y-%m-%d"),
                'source': 'F1 Insider'
            },
            {
                'title': "Lamborghini Temerario: The 10,000 RPM V8 Hybrid Debut",
                'url': "https://www.lamborghini.com",
                'summary': "Lamborghini replaces the Huracán with a high-revving twin-turbo V8 hybrid, marking a new era of emotional electrification...",
                'date': datetime.now().strftime("%Y-%m-%d"),
                'source': 'Maranello Feed'
            }
        ]

    try:
        # Querying NewsAPI for a mix of F1 and Luxury Automotive
        q = '("Formula 1" OR F1 OR Ferrari OR Porsche OR Lamborghini OR supercar OR hypercar)'
        url = f"https://newsapi.org/v2/everything?q={q}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        articles = data.get('articles', [])[:9]
        news = []
        for art in articles:
            news.append({
                'title': art.get('title'),
                'url': art.get('url'),
                'summary': art.get('description', "Check full article for details."),
                'date': art.get('publishedAt', "")[:10],
                'source': art.get('source', {}).get('name', 'News')
            })
        return news
    except Exception as e:
        logger.error(f"Error fetching NewsAPI: {e}")
        return []

def get_daily_briefings():
    """Wrapper for news logic to maintain compatibility with app.py"""
    return get_f1_headlines()
