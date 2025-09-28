from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.routes import api_router
from backend.app.database.database import engine, Base

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BrasilTransporta API",
    description="Marketplace para veículos pesados",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "BrasilTransporta API está funcionando!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Registrar rotas
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)