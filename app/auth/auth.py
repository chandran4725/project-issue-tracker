from clerk_backend_api.security import AuthenticateRequestOptions
from fastapi import Request,HTTPException,status
import httpx
from app.auth.clerk import clerk
from app.util.config import settings


class CurrentUser:
    def __init__(self,user_id: str):
        self.user_id = user_id
        
# Your Clerk user ID
TEST_CLERK_USER_ID = "user_3Hp12nXKcB45Li0jmcw0c2FL3rr"


def get_current_user(request: Request) -> CurrentUser:
    # TEMPORARY: bypass Clerk authentication
    return CurrentUser(user_id=TEST_CLERK_USER_ID)
        
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