import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(URL, KEY) if URL and KEY else None

def get_supabase():
    return supabase

# Auth Wrappers
def signup_user(email, password, username):
    if not supabase: return None, "Supabase not configured"
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"username": username}}
        })
        return res, None
    except Exception as e:
        return None, str(e)

def login_user(email, password):
    if not supabase: return None, "Supabase not configured"
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return res, None
    except Exception as e:
        return None, str(e)
def get_oauth_url(provider, redirect_url):
    """Dynamically generates an OAuth redirect URL for Google, Github, Discord etc."""
    if not supabase: return None, "Supabase not configured"
    try:
        # Using PKCE (flow_type='pkce') which is more secure for modern apps
        res = supabase.auth.sign_in_with_oauth({
            "provider": provider,
            "options": {
                "redirect_to": redirect_url,
                "skip_browser_redirect": True
            }
        })
        return res.url, None
    except Exception as e:
        return None, str(e)

def exchange_code_for_session(code):
    """Exchanges a PKCE code for a proper session."""
    if not supabase: return None, "Supabase not configured"
    try:
        res = supabase.auth.exchange_code_for_session({"auth_code": code})
        return res, None
    except Exception as e:
        return None, str(e)

def get_user_xp(user_id):
    if not supabase: return {"user_id": user_id, "level": 1, "total_xp": 0, "role": "user"}
    try:
        res = supabase.table("user_xp").select("*").eq("user_id", user_id).execute()
        if res.data:
            return res.data[0]
        # Initialize if not found
        new_xp = {"user_id": user_id, "level": 1, "total_xp": 0, "role": "user"}
        supabase.table("user_xp").insert(new_xp).execute()
        return new_xp
    except Exception as e:
        print(f"Supabase XP Error: {e}")
        return {"user_id": user_id, "level": 1, "total_xp": 0, "role": "user"}

def is_elite_member(user_id):
    """Lead Architect check for premium membership status."""
    data = get_user_xp(user_id)
    return data.get('role') == 'elite'

def update_xp(user_id, xp_amount):
    if not supabase: return
    current = get_user_xp(user_id)
    new_total = current['total_xp'] + xp_amount
    new_level = (new_total // 1000) + 1
    supabase.table("user_xp").update({"total_xp": new_total, "level": new_level}).eq("user_id", user_id).execute()

def get_user_garage(user_id):
    if not supabase: return []
    try:
        res = supabase.table("garage").select("car_id").eq("user_id", user_id).execute()
        return [item['car_id'] for item in res.data]
    except Exception as e:
        print(f"Supabase Garage Error: {e}")
        return []

def add_to_garage(user_id, car_id):
    if not supabase: return False, "Supabase not configured"
    try:
        # Check if already exists to avoid duplicates
        existing = supabase.table("garage").select("*").eq("user_id", user_id).eq("car_id", car_id).execute()
        if existing.data:
            return True, "Car already in garage"
            
        res = supabase.table("garage").insert({"user_id": user_id, "car_id": car_id}).execute()
        return True, "Added to garage"
    except Exception as e:
        return False, str(e)

def remove_from_garage(user_id, car_id):
    if not supabase: return False, "Supabase not configured"
    try:
        supabase.table("garage").delete().eq("user_id", user_id).eq("car_id", car_id).execute()
        return True, "Removed from garage"
    except Exception as e:
        return False, str(e)

def save_quiz_response(user_id, question_id, answer, is_correct):
    """Architectural persistence for Academy learning metrics."""
    if not supabase: return
    try:
        supabase.table("quiz_responses").insert({
            "user_id": user_id,
            "question_id": question_id,
            "answer_provided": str(answer),
            "is_correct": is_correct
        }).execute()
    except Exception as e:
        print(f"Supabase Quiz Tracking Error: {e}")
