import news_engine
import f1_engine
import academy_engine
import json

print("--- Testing News Engine ---")
news = news_engine.get_daily_briefings()
print(f"Count: {len(news)}")
if news: print(f"First: {news[0]['title']}")

print("\n--- Testing F1 Engine ---")
live = f1_engine.get_live_session_data()
print(f"Live Data: {bool(live)}")

print("\n--- Testing Academy Engine ---")
fact = academy_engine.get_daily_intel_fact()
print(f"Fact: {fact['fact']}")
