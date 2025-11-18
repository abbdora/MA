from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..services.auth_service import AuthService, get_auth_service
from ..models.user import User, UserCreate, UserLogin, Token

auth_router = APIRouter(prefix='/auth', tags=['Auth'])
security = HTTPBearer()

@auth_router.post('/register', response_model=User)
def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        return auth_service.register_user(user_data)
    except ValueError as e:
        raise HTTPException(400, str(e))

@auth_router.post('/login', response_model=Token)
def login(
    login_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.login_user(login_data)

@auth_router.get('/me', response_model=User)
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    token = credentials.credentials
    return auth_service.get_current_user(token)