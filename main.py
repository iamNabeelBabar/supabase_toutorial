from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("SUPABASE_URL")
api = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, api)

try:
    response = supabase.table("users").select("*").execute()
    print(response)
    
except Exception as e:
    print("An error occurred:", e)
    
    