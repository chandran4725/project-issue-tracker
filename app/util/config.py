import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CLERK_SECRET_KEY: str = os.getenv("CLERK_SECRET_KEY","")
    CLERK_PUBLISHABLE_KEY: str = os.getenv("CLERK_PUBLISHABLE_KEY","")
    CLERK_JWKS_URL: str = os.getenv("CLERK_JWKS_URL","")
    
    DATABASE_URL:str = os.getenv("DATABASE_URL","")
    FRONTEND_URL:str = os.getenv("FRONTEND_URL","")
    
    CLERK_SIGN_UP_URL:str = os.getenv("CLERK_SIGN_UP_URL","")
    
settings = Config()