from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request) -> HTMLResponse:
    html = request.app.state.templates.get_template("dashboard.html").render()
    return HTMLResponse(html)

@router.websocket("/ws/metrics")
async def ws_metrics(ws: WebSocket) -> None:
    manager = ws.app.state.ws_manager
    hub = ws.app.state.metrics_hub

    await manager.connect(ws)
    try:
        snapshot = await hub.snapshot()
        await ws.send_json({"type": "metrics", **snapshot})
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        await manager.disconnect(ws)
