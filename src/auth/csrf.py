import hmac
import secrets

from fastapi import HTTPException, Request

from src.config import config


def ensure_csrf_token(request: Request) -> str:
    token = request.session.get(config.CSRF_SESSION_KEY)
    if not token:
        token = secrets.token_urlsafe(32)
        request.session[config.CSRF_SESSION_KEY] = token
    return token


def validate_csrf(request: Request, token_from_form: str) -> None:
    token_in_session = request.session.get(config.CSRF_SESSION_KEY)
    if not token_in_session or not token_from_form:
        raise HTTPException(status_code=403, detail="CSRF token отсутсвует")

    if not hmac.compare_digest(str(token_in_session), str(token_from_form)):
        raise HTTPException(status_code=403, detail="Неправильный CSRF token")
