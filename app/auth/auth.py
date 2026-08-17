from clerk_backend_api.security import AuthenticateRequestOptions
from fastapi import Request,HTTPException,status
import httpx
from app.auth.clerk import clerk
from app.util.config import settings


class CurrentUser:
    def __init__(self, user_id: str, email: str | None = None):
        self.user_id = user_id
        self.email = email
        
# Your Clerk user ID
TEST_CLERK_USER_ID = "user_3Hp12nXKcB45Li0jmcw0c2FL3rr"


def get_current_user(request: Request) -> CurrentUser:
    user_email = request.headers.get("X-User-Email")
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        try:
            httpx_request = convert_to_httpx_request(request)
            authorized_parties = ["http://localhost:3000", "http://localhost:5173"]
            if settings.FRONTEND_URL and settings.FRONTEND_URL not in authorized_parties:
                authorized_parties.append(settings.FRONTEND_URL)
            
            request_state = clerk.authenticate_request(
                httpx_request,
                AuthenticateRequestOptions(authorized_parties=authorized_parties)
            )
            if request_state.is_signed_in and request_state.payload:
                payload = request_state.payload
                user_id = payload.get("sub")
                email = user_email or payload.get("email") or payload.get("primary_email") or payload.get("email_address")
                if user_id:
                    return CurrentUser(user_id=user_id, email=email)
        except Exception as e:
            print("Clerk token verification error:", e)

    return CurrentUser(user_id=TEST_CLERK_USER_ID, email=user_email)
        
def convert_to_httpx_request(fastapi_request: Request) -> httpx.Request:
    return httpx.Request(
        method=fastapi_request.method,
        url=str(fastapi_request.url),
        headers=dict(fastapi_request.headers)
    )
    
def get_current_user1(request: Request) -> CurrentUser:
    httpx_request = convert_to_httpx_request(request)
    
    request_state = clerk.authenticate_request(
        httpx_request,
        AuthenticateRequestOptions(authorized_parties=[settings.FRONTEND_URL])
    )
    
    if not request_state.is_signed_in:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="From Clerk Not Authenticated"
        )
    
    claims = request_state.payload
    
    user_id = claims.get("sub")
    
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authenticated"
        )
    
    return CurrentUser(user_id=user_id)