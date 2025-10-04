from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from brasiltransporta.presentation.api.controllers.users import router as users_router
from brasiltransporta.presentation.api.controllers.vehicles import router as vehicles_router 
from brasiltransporta.presentation.api.controllers.stores import router as stores_router
from brasiltransporta.presentation.api.controllers.transactions import router as transactions_router
from brasiltransporta.presentation.api.controllers.plans import router as plans_router
from brasiltransporta.presentation.api.controllers.advertisements import router as advertisements_router

from brasiltransporta.domain.errors.errors import ValidationError, DomainError


def create_app() -> FastAPI:
    app = FastAPI(title="BrasilTransporta API", version="0.1.0")

    # CORS básico (ajuste conforme seus frontends)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    # Healthcheck
    @app.get("/health")
    def health():
        return {"status": "ok"}

    # Exception mapping (Domínio → HTTP)
    @app.exception_handler(ValidationError)
    async def handle_validation_error(_: Request, exc: ValidationError):
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    @app.exception_handler(DomainError)
    async def handle_domain_error(_: Request, exc: DomainError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    # Routers
    app.include_router(users_router)
    app.include_router(vehicles_router)
    app.include_router(stores_router)
    app.include_router(transactions_router)
    app.include_router(plans_router)
    app.include_router(advertisements_router)   
    return app


app = create_app()      
