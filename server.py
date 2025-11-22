import socketio
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

# 1. Setup Server & Socket
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/socket.io", socketio.ASGIApp(sio, socketio_path=""))
templates = Jinja2Templates(directory="templates")

# Variabel global untuk menyimpan data statis dari Agent
agent_metadata = {}

# HTTP REST API
@app.get("/")
async def index(request: Request):
    """Serve halaman Dashboard HTML"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/register")
async def register_agent(data: dict):
    """API untuk Agent mendaftarkan spesifikasi OS (Data Statis)"""
    global agent_metadata
    agent_metadata = data
    print(f"[API LOG] Agent Registered: {data}")
    return {"status": "success", "message": "Agent registered"}

@app.get("/api/agent-info")
async def get_agent_info():
    """API untuk Dashboard mengambil info OS Agent"""
    return JSONResponse(content=agent_metadata)

# WEBSOCKET
@sio.event
async def connect(sid, environ):
    print(f"[SOCKET LOG] Client Connected: {sid}")

@sio.event
async def telemetry_data(sid, data):
    """
    Menerima data live dari Agent, lalu mem-broadcast ke Dashboard.
    Ini adalah konsep 'Relay' atau 'Broker'.
    """
    # Broadcast ke semua client yang membuka web ('dashboard')
    await sio.emit('update_dashboard', data)

@sio.event
async def disconnect(sid):
    print(f"[SOCKET LOG] Client Disconnected: {sid}")

# Cara menjalankan: uvicorn server:app --reload