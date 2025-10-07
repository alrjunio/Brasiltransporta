from fastapi import APIRouter, Depends, HTTPException, status, Request
from datetime import datetime

# Import dos schemas
from brasiltransporta.presentation.api.models.requests.auth_request import (
    LoginRequest, RefreshTokenRequest
)
from brasiltransporta.presentation.api.models.responses.auth_responses import Token

# Import das dependências CORRETAS
from brasiltransporta.infrastructure.dependencies import (
    get_user_service, 
    get_refresh_token_service,
    get_jwt_service,
    get_send_phone_verification_use_case,
    get_verify_phone_code_use_case, 
    get_phone_login_use_case
)

from brasiltransporta.application.auth.use_case.phone_login_use_case import PhoneLoginUseCase

from brasiltransporta.application.auth.use_case.phone_auth_inputs import (
    SendPhoneVerificationCodeCommand,
    VerifyPhoneCodeCommand,
    PhoneLoginCommand
)

from brasiltransporta.application.auth.use_case.phone_auth_use_cases import (
    SendPhoneVerificationUseCase, 
    VerifyPhoneCodeUseCase
)

from brasiltransporta.infrastructure.security.refresh_token_service import RefreshTokenService
from brasiltransporta.infrastructure.security.jwt_service import JWTService
from brasiltransporta.application.service.user_service import UserService
from brasiltransporta.domain.errors.errors import SecurityAlertError
from brasiltransporta.presentation.api.models.requests.phone_auth_request import SendPhoneCodeRequest, VerifyPhoneCodeRequest, PhoneLoginRequest

router = APIRouter(prefix="/auth", tags=["authentication"])

# Fallback para get_current_user se não existir
try:
    from brasiltransporta.presentation.api.dependencies.authz import get_current_user
except ImportError:
    # Mock para desenvolvimento
    async def get_current_user():
        class MockUser:
            id = "mock-user-id"
            email = "mock@example.com"
        return MockUser()

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    request: Request,
    jwt_service: JWTService = Depends(get_jwt_service),
    user_service: UserService = Depends(get_user_service),
    refresh_service: RefreshTokenService = Depends(get_refresh_token_service)
):
    """Refresh access token using refresh token with rotation"""
    try:
        print("🔄 Iniciando refresh token...")
        
        # Verify refresh token signature first
        payload = jwt_service.verify_refresh_token(refresh_data.refresh_token)
        if not payload:
            print("❌ Refresh token signature inválida")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token signature"
            )
        
        user_id = payload.get("sub")
        if not user_id:
            print("❌ Payload do refresh token inválido")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token payload"
            )
        
        print(f"🔍 Verificando refresh token para usuário: {user_id}")
        
        # Verify and rotate refresh token in Redis
        is_valid, token_family, error = refresh_service.verify_and_rotate(
            user_id, refresh_data.refresh_token
        )
        
        if not is_valid:
            print(f"❌ Refresh token inválido: {error}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error or "Invalid refresh token"
            )
        
        print("✅ Refresh token válido, gerando novos tokens...")
        
        # Generate new tokens
        access_token = jwt_service.create_access_token(
            claims={"sub": user_id, "email": payload.get("email", "unknown")}
        )
        
        new_refresh_token = jwt_service.create_refresh_token(
            claims={"sub": user_id}
        )
        
        # Store new refresh token with same token family
        if token_family:
            refresh_service.store_refresh_token(user_id, new_refresh_token, token_family)
        else:
            # Fallback: criar nova família de tokens
            refresh_service.store_refresh_token(user_id, new_refresh_token)
        
        print("✅ Novos tokens gerados e armazenados")
        
        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )
        
    except SecurityAlertError as e:
        print(f"🚨 Alerta de segurança: {e}")
        raise
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro durante refresh token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during token refresh"
        )

@router.post("/login")
async def login(
    login_data: LoginRequest,
    request: Request,
    user_service: UserService = Depends(get_user_service),
    jwt_service: JWTService = Depends(get_jwt_service),
    refresh_service: RefreshTokenService = Depends(get_refresh_token_service)
):
    """Login user and generate tokens with refresh token storage"""
    try:
        print(f"🔐 Tentando login para: {login_data.email}")
        
        user = await user_service.authenticate_user(
            login_data.email, login_data.password
        )
        
        if not user:
            print("❌ Credenciais inválidas")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        print(f"✅ Login bem-sucedido para usuário: {user.id}")
        
        # Generate tokens
        user_id = str(getattr(user, 'id', 'unknown'))
        user_email = getattr(user, 'email', 'unknown')
        
        access_token = jwt_service.create_access_token(
            claims={"sub": user_id, "email": user_email}
        )
        refresh_token = jwt_service.create_refresh_token(
            claims={"sub": user_id}
        )
        
        # Store refresh token in Redis
        success = refresh_service.store_refresh_token(user_id, refresh_token)
        
        if not success:
            print("⚠️  Aviso: Falha ao armazenar refresh token no Redis")
        else:
            print("✅ Refresh token armazenado no Redis")
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro durante login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )

@router.post("/logout")
async def logout(
    request: Request,
    refresh_service: RefreshTokenService = Depends(get_refresh_token_service),
    current_user = Depends(get_current_user)
):
    """Logout user by revoking all refresh tokens"""
    try:
        user_id = str(getattr(current_user, 'id', 'unknown'))
        print(f"🚪 Logout solicitado para usuário: {user_id}")
        
        success = refresh_service.revoke_all_tokens(user_id)
        
        if success:
            print("✅ Logout bem-sucedido - tokens revogados")
            return {"message": "Successfully logged out"}
        else:
            print("⚠️  Logout parcial - alguns tokens podem não ter sido revogados")
            return {"message": "Logged out (some tokens may not have been revoked)"}
            
    except Exception as e:
        print(f"❌ Erro durante logout: {e}")
        return {"message": "Logged out"}

@router.get("/sessions")
async def get_sessions(
    request: Request,
    refresh_service: RefreshTokenService = Depends(get_refresh_token_service),
    current_user = Depends(get_current_user)
):
    """Get active sessions for current user"""
    try:
        user_id = str(getattr(current_user, 'id', 'unknown'))
        print(f"📋 Solicitando sessões para usuário: {user_id}")
        
        sessions = refresh_service.get_active_sessions(user_id)
        return {"sessions": sessions}
        
    except Exception as e:
        print(f"❌ Erro ao obter sessões: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get sessions: {str(e)}"
        )

@router.get("/health")
async def auth_health():
    """Health check para autenticação"""
    return {
        "status": "healthy", 
        "service": "authentication",
        "timestamp": datetime.utcnow().isoformat()
    }
    
# ATUALIZAR brasiltransporta/presentation/api/controllers/auth.py

# Adicionar imports dos use cases


# ATUALIZAR OS ENDPOINTS COMENTADOS:

@router.post("/phone/send-code")
async def send_phone_verification_code(
    request: SendPhoneCodeRequest,
    send_code_use_case: SendPhoneVerificationUseCase = Depends(get_send_phone_verification_use_case)
):
    """Envia código de verificação para celular"""
    try:
        command = SendPhoneVerificationCodeCommand(phone=request.phone)
        success = await send_code_use_case.execute(command)
        
        if success:
            return {"message": "Código enviado com sucesso"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Falha ao enviar código"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/phone/verify")
async def verify_phone_code(
    request: VerifyPhoneCodeRequest,
    verify_code_use_case: VerifyPhoneCodeUseCase = Depends(get_verify_phone_code_use_case)
):
    """Verifica código de celular"""
    try:
        command = VerifyPhoneCodeCommand(phone=request.phone, code=request.code)
        is_valid, user = await verify_code_use_case.execute(command)
        
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Código inválido ou expirado"
            )
            
        return {"valid": True, "user_exists": user is not None}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/phone/login", response_model=Token)
async def phone_login(
    request: PhoneLoginRequest,
    phone_login_use_case: PhoneLoginUseCase = Depends(get_phone_login_use_case),
    jwt_service: JWTService = Depends(get_jwt_service),
    refresh_service: RefreshTokenService = Depends(get_refresh_token_service)
):
    """Login completo com celular"""
    try:
        command = PhoneLoginCommand(phone=request.phone, code=request.code)
        user, error = await phone_login_use_case.execute(command)
        
        if error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error
            )
        
        # Gera tokens (mesmo padrão do login por email)
        user_id = str(user.id)
        user_email = str(user.email)
        
        access_token = jwt_service.create_access_token(
            claims={"sub": user_id, "email": user_email}
        )
        refresh_token = jwt_service.create_refresh_token(
            claims={"sub": user_id}
        )
        
        # Armazena refresh token
        refresh_service.store_refresh_token(user_id, refresh_token)
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )