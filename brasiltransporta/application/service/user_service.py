from typing import Optional
from datetime import datetime

from brasiltransporta.domain.entities.user import User
from brasiltransporta.application.users.use_cases.login_user import LoginUserUseCase, LoginUserInput
from brasiltransporta.domain.repositories.user_repository import UserRepository
from brasiltransporta.infrastructure.security.password_hasher import BcryptPasswordHasher
from brasiltransporta.infrastructure.security.jwt_service import JWTService
from brasiltransporta.domain.errors.errors import ValidationError


class UserService:
    """
    Service como facade para coordenar Use Cases e fornecer interface
    compatível com os controllers FastAPI
    
    Abordagem híbrida: mantém Use Cases existentes + interface simples para controllers
    """

    def __init__(
        self, 
        user_repository: UserRepository,
        password_hasher: BcryptPasswordHasher,
        jwt_service: JWTService
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._jwt_service = jwt_service
        
        # Inicializa o Use Case existente
        self._login_use_case = LoginUserUseCase(
            users=user_repository,
            hasher=password_hasher,
            jwt_service=jwt_service
        )

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Autentica usuário - compatível com auth.py
        Retorna a entidade User se válido, None se inválido
        """
        try:
            # Verificar se usuário existe primeiro
            user = await self.get_user_by_email(email)
            if not user:
                return None
            
            # Verificar senha
            if not await self.verify_password(user, password):
                return None
            
            # Verificar se usuário está ativo
            if not user.is_active:
                return None
                
            # Atualizar último login
            await self.update_last_login(str(user.id))
            
            return user
                
        except ValidationError:
            # Credenciais inválidas - retorna None conforme esperado pelo auth.py
            return None
        except Exception as e:
            # Log para outros tipos de erro
            print(f"Erro inesperado na autenticação: {e}")
            return None
        
    async def verify_password(self, user: User, password: str) -> bool:
        """Verifica se a senha está correta para o usuário"""
        return self._password_hasher.verify(password, user.password_hash)
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Busca usuário pelo ID - compatível com auth.py
        
        Args:
            user_id: ID do usuário
            
        Returns:
            User entity se encontrado, None se não existir
        """
        try:
            return self._user_repository.get_by_id(user_id)
        except Exception as e:
            print(f"Erro ao buscar usuário por ID {user_id}: {e}")
            return None

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Busca usuário por email
        
        Args:
            email: Email do usuário
            
        Returns:
            User entity se encontrado, None se não existir
        """
        try:
            return self._user_repository.get_by_email(email)
        except Exception as e:
            print(f"Erro ao buscar usuário por email {email}: {e}")
            return None

    async def create_user(self, user_data: dict) -> Optional[User]:
        """
        Cria novo usuário - método direto sem Use Case específico
        Para casos simples, o Service pode conter a lógica diretamente
        
        Args:
            user_data: Dict com dados do usuário
                - name: Nome completo (obrigatório)
                - email: Email (obrigatório)
                - password: Senha em texto puro (obrigatório)
                - phone: Telefone (opcional)
                - birth_date: Data nascimento (opcional)
                - profession: Profissão (opcional)
                - region: Região (opcional)
                - roles: Lista de roles (opcional)
                
        Returns:
            User entity criada ou None em caso de erro
        """
        try:
            # Validações básicas
            if not user_data.get('name') or not user_data.get('email') or not user_data.get('password'):
                raise ValidationError("Nome, email e senha são obrigatórios")

            # Verifica se email já existe
            existing_user = await self.get_user_by_email(user_data['email'])
            if existing_user:
                raise ValidationError("Email já cadastrado")

            # Hash da senha
            password_hash = self._password_hasher.hash(user_data['password'])
            
            # Cria a entidade User usando o factory method existente
            user = User.create(
                name=user_data['name'],
                email=user_data['email'],
                password_hash=password_hash,
                phone=user_data.get('phone'),
                birth_date=user_data.get('birth_date'),
                profession=user_data.get('profession'),
                region=user_data.get('region'),
                roles=user_data.get('roles', ['buyer'])  # Role padrão
            )
            
            # Salva no repositório
            return self._user_repository.save(user)
            
        except ValidationError as e:
            print(f"Erro de validação ao criar usuário: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao criar usuário: {e}")
            return None

    async def update_user(self, user_id: str, update_data: dict) -> Optional[User]:
        """
        Atualiza usuário existente
        
        Args:
            user_id: ID do usuário
            update_data: Dict com campos para atualizar
            
        Returns:
            User entity atualizada ou None se usuário não existir
        """
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return None
                
            # Aplica as atualizações permitidas
            if 'name' in update_data and update_data['name']:
                user.name = update_data['name']
                
            if 'phone' in update_data:
                from brasiltransporta.domain.value_objects.phone_number import PhoneNumber
                user.phone = PhoneNumber(update_data['phone']) if update_data['phone'] else None
                
            if 'profession' in update_data:
                user.profession = update_data['profession']
                
            if 'region' in update_data:
                user.region = update_data['region']
                
            if 'birth_date' in update_data:
                user.birth_date = update_data['birth_date']
            
            # Atualiza timestamp
            user.updated_at = datetime.utcnow()
            
            return self._user_repository.save(user)
            
        except Exception as e:
            print(f"Erro ao atualizar usuário {user_id}: {e}")
            return None

    # Métodos auxiliares para auth.py e outros controllers
    async def user_exists(self, email: str) -> bool:
        """Verifica se usuário existe pelo email"""
        user = await self.get_user_by_email(email)
        return user is not None

    async def verify_password(self, user: User, password: str) -> bool:
        """Verifica se a senha está correta para o usuário"""
        return self._password_hasher.verify(password, user.password_hash)

    async def update_last_login(self, user_id: str) -> Optional[User]:
        """Atualiza o último login do usuário"""
        try:
            user = await self.get_user_by_id(user_id)
            if user:
                user.update_last_login()
                return self._user_repository.update(user)
            return None
        except Exception as e:
            print(f"Erro ao atualizar último login: {e}")
            return None

    async def deactivate_user(self, user_id: str) -> bool:
        """Desativa usuário"""
        try:
            user = await self.get_user_by_id(user_id)
            if user:
                user.deactivate()
                self._user_repository.save(user)
                return True
            return False
        except Exception as e:
            print(f"Erro ao desativar usuário: {e}")
            return False

    async def activate_user(self, user_id: str) -> bool:
        """Ativa usuário"""
        try:
            user = await self.get_user_by_id(user_id)
            if user:
                user.activate()
                self._user_repository.save(user)
                return True
            return False
        except Exception as e:
            print(f"Erro ao ativar usuário: {e}")
            return False