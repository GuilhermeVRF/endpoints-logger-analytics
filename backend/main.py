from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.auth import router as auth_router
from api.routers.logs import router as logs_router

app = FastAPI(title="Techbiz Dashboard API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Permite todas as origens (domínios)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(logs_router)
