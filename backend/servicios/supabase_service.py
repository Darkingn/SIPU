from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("https://wigmurzhkogmzgdczjmb.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpZ211cnpoa29nbXpnZGN6am1iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAxMTA0NDgsImV4cCI6MjA3NTY4NjQ0OH0.l0Gj1iJ3COqMXMgOPVmnVJhr01YkORw6Q3-hjAbtCEg")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
