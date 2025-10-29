from dotenv import load_dotenv
import os

load_dotenv()

# Database configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
# Prefer explicit SUPABASE_KEY, fallback to service role key or anon key if present
SUPABASE_KEY = os.getenv('SUPABASE_KEY') or os.getenv('SUPABASE_SERVICE_ROLE_KEY') or os.getenv('SUPABASE_ANON_KEY')

# Application configuration
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ENV = os.getenv('ENV', 'development')

# Security configuration
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')