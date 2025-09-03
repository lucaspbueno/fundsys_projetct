from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logging_config import logger
from app.controllers.file import file_routes
from app.config import get_settings
import app.config.db

app = FastAPI(debug=get_settings().DEBUG)

logger.info("🚀 API inicializada com sucesso.")

# Middleware CORS totalmente liberado (não recomendado para produção)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # permite qualquer origem
    allow_credentials=True,
    allow_methods=["*"],  # permite todos os métodos: GET, POST, PUT, DELETE, etc
    allow_headers=["*"],  # permite qualquer cabeçalho
)

# Rotas
app.include_router(file_routes)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.middleware("http")
async def log_requests(request, call_next):
    print("Requisição recebida:", request.method, request.url)
    response = await call_next(request)
    return response
