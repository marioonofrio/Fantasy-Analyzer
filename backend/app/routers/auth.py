from fastapi import APIRouter
from sqlmodel import select
from database import get_session
from models import User
from auth import verify_google_token, create_access_token
from schemas import GoogleAuthRequest, AuthResponse

router = APIRouter()


@router.post("/auth/google", response_model=AuthResponse)
def google_login(payload: GoogleAuthRequest):
    info = verify_google_token(payload.credential)

    with get_session() as session:
        user = session.exec(select(User).where(User.google_id == info["sub"])).first()
        if not user:
            user = User(google_id=info["sub"], email=info["email"], name=info.get("name", info["email"]))
        else:
            user.email = info["email"]
            user.name = info.get("name", user.name)
        session.add(user)
        session.commit()
        session.refresh(user)

        token = create_access_token(user.id)
        return AuthResponse(access_token=token, user_id=user.id, email=user.email, name=user.name)