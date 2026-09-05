import base64
import json
import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.schemas.user import UserLogin, UserResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def decode_jwt_payload(credential: str) -> Optional[dict]:
    try:
        parts = credential.split(".")
        if len(parts) >= 2:
            payload_b64 = parts[1]
            # Add padding
            payload_b64 += "=" * ((4 - len(payload_b64) % 4) % 4)
            decoded_bytes = base64.b64decode(payload_b64)
            return json.loads(decoded_bytes.decode("utf-8"))
    except Exception as exc:
        logger.warning(f"Failed to decode credential JWT payload: {exc}")
    return None


@router.post(
    "/google",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
def google_auth(
    payload: UserLogin,
    db: Session = Depends(get_db)
):
    email = payload.email
    name = payload.name
    picture = payload.picture
    google_id = payload.google_id

    # If raw Google JWT credential is sent, decode it
    if payload.credential:
        jwt_data = decode_jwt_payload(payload.credential)
        if jwt_data:
            email = jwt_data.get("email") or email
            name = jwt_data.get("name") or jwt_data.get("given_name") or name
            picture = jwt_data.get("picture") or picture
            google_id = jwt_data.get("sub") or google_id

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Valid email address is required"
        )

    # Check if user already exists
    existing_user = (
        db.query(User)
        .filter((User.email == email) | (User.google_id == google_id if google_id else False))
        .first()
    )

    if existing_user:
        # Update details if changed
        if name:
            existing_user.name = name
        if picture:
            existing_user.picture = picture
        if google_id:
            existing_user.google_id = google_id
        db.commit()
        db.refresh(existing_user)
        return existing_user

    # Create new Gmail / Google user
    new_user = User(
        email=email,
        name=name or email.split("@")[0].capitalize(),
        picture=picture or f"https://api.dicebear.com/7.x/bottts/svg?seed={email}",
        google_id=google_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get(
    "/me/{user_id}",
    response_model=UserResponse
)
def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
