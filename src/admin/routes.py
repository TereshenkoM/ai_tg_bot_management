from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.auth.admin_backend import AdminAuthBackend
from src.auth.csrf import ensure_csrf_token, validate_csrf

admin_router = APIRouter()


def get_templates() -> Jinja2Templates:
    templates = Jinja2Templates(directory="src/templates")

    templates.env.globals["csrf_token"] = lambda request: ensure_csrf_token(request)
    return templates


@admin_router.get("/admin/login", response_class=HTMLResponse)
async def admin_login_get(
    request: Request,
):
    auth: AdminAuthBackend = request.app.state.admin_auth

    if await auth.authenticate(request):
        return RedirectResponse(url="/admin", status_code=302)

    templates = get_templates()
    return templates.TemplateResponse(
        "login_admin.html",
        {"request": request, "error": None},
    )


@admin_router.post("/admin/login", response_class=HTMLResponse)
async def admin_login_post(
    request: Request,
    csrf_token: str = Form(...),
):
    validate_csrf(request, csrf_token)

    auth: AdminAuthBackend = request.app.state.admin_auth

    ok = await auth.login(request)
    if ok:
        return RedirectResponse("/admin/", status_code=303)

    templates = get_templates()
    return templates.TemplateResponse(
        "login_admin.html",
        {"request": request, "error": "Неверный логин или пароль"},
        status_code=401,
    )
