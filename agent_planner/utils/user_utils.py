from fastapi import Header, HTTPException
from supabase import create_client, Client
import os

# Initialize your supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"), 
    os.getenv("SUPABASE_ANON_KEY")
)

async def get_current_user(authorization: str = Header(...)):
    try:
        # Extract the token from "Bearer <token>"
        token = authorization.split(" ")[1]
        
        # Ask Supabase to verify the token and return the user
        response = supabase.auth.get_user(token)
        
        if not response.user:
            raise HTTPException(status_code=401, detail="User not found")
            
        return response.user.id  # Returns the UUID string
    except Exception as e:
        print(f"Supabase Auth Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid Session or Token")