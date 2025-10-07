from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import redis # type: ignore

from brasiltransporta.presentation.api.controllers.users import router as users_router
from brasiltransporta.presentation.api.controllers.vehicles import router as vehicles_router 
from brasiltransporta.presentation.api.controllers.stores import router as stores_router
from brasiltransporta.presentation.api.controllers.transactions import router as transactions_router
from brasiltransporta.presentation.api.controllers.plans import router as plans_router
from brasiltransporta.presentation.api.controllers.advertisements import router as advertisements_router
from brasiltransporta.presentation.api.controllers.auth import router as auth_router

from brasiltransporta.domain.errors.errors import ValidationError, DomainError, SecurityAlertError
from brasiltransporta.infrastructure.security.refresh_token_service import RefreshTokenService
from brasiltransporta.infrastructure.config.settings import AppSettings

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
    
    @app.on_event("startup")
    async def startup_event():
        """Initialize services on startup"""
        settings = AppSettings()
        
        # Configura Redis client
        try:
            redis_client = redis.Redis.from_url(
                settings.redis.url,
                decode_responses=True  # Para trabalhar com strings ao invés de bytes
            )
            
            # Test Redis connection
            redis_client.ping()
            print("✅ Redis connected successfully")
            
            # Inicializa serviço de refresh tokens
            app.state.refresh_token_service = RefreshTokenService(redis_client)
            print("✅ RefreshTokenService initialized")
            
        except redis.ConnectionError as e:
            print(f"❌ Failed to connect to Redis: {e}")
            # Em desenvolvimento, podemos continuar sem Redis por enquanto
            if settings.environment == "production":
                raise
            else:
                print("⚠️  Continuing without Redis (development mode)")
                app.state.refresh_token_service = None
        except Exception as e:
            print(f"❌ Error initializing Redis: {e}")
            app.state.refresh_token_service = None

    # Exception mapping (Domínio → HTTP)
    @app.exception_handler(ValidationError)
    async def handle_validation_error(_: Request, exc: ValidationError):
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    @app.exception_handler(DomainError)
    async def handle_domain_error(_: Request, exc: DomainError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(SecurityAlertError)
    async def handle_security_alert_error(_: Request, exc: SecurityAlertError):
        """Handle security alerts - return 401 with security flag"""
        return JSONResponse(
            status_code=401,
            content={
                "detail": str(exc),
                "security_alert": True
            }
        )

    # Routers
    app.include_router(users_router)
    app.include_router(vehicles_router)
    app.include_router(stores_router)
    app.include_router(transactions_router)
    app.include_router(plans_router)
    app.include_router(advertisements_router)   
    app.include_router(auth_router)  
    
    return app

app = create_app()