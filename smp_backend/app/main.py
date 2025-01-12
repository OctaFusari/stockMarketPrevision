
from fastapi import FastAPI, WebSocket
from app.routes import example  # Importa il file delle rotte


from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Origini consentite (frontend)
    allow_credentials=True,
    allow_methods=["*"],  # Permetti tutti i metodi (GET, POST, ecc.)
    allow_headers=["*"],  # Permetti tutti gli header
)

@app.get("/")
def read_root():
    return {"message": "Prova iniziale"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")


# Includi le rotte
app.include_router(example.router)