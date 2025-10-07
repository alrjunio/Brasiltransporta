# tests/unit/security/test_refresh_token_service.py
from __future__ import annotations

import pytest
import json
import uuid
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from typing import Optional

from brasiltransporta.infrastructure.security.refresh_token_service import RefreshTokenService
from brasiltransporta.domain.errors.errors import SecurityAlertError


class TestRefreshTokenService:
    """Testes unitários para RefreshTokenService"""
    
    @pytest.fixture
    def mock_redis(self):
        """Mock do cliente Redis"""
        redis_mock = Mock()
        redis_mock.setex = Mock(return_value=True)
        redis_mock.keys = Mock(return_value=[])
        redis_mock.get = Mock(return_value=None)
        redis_mock.delete = Mock(return_value=1)
        return redis_mock
    
    @pytest.fixture
    def mock_settings(self):
        """Mock das configurações"""
        settings_mock = Mock()
        settings_mock.redis.refresh_token_namespace = "rt"
        settings_mock.redis.refresh_token_ttl = 86400
        return settings_mock
    
    @pytest.fixture
    def refresh_token_service(self, mock_redis, mock_settings):
        """Instância do serviço com mocks"""
        with patch('brasiltransporta.infrastructure.security.refresh_token_service.AppSettings') as mock_app_settings:
            mock_app_settings.return_value = mock_settings
            service = RefreshTokenService(redis_client=mock_redis)
        return service
    
    @pytest.fixture
    def sample_token_data(self):
        """Dados de exemplo para token"""
        return {
            "token": "refresh-token-123",
            "created_at": datetime.utcnow().isoformat(),
            "used": False,
            "token_family": "family-123"
        }
    
    def test_get_key_without_family(self, refresh_token_service):
        """Testa geração de chave Redis sem token family"""
        # Arrange
        user_id = "user-123"
        
        # Act
        key = refresh_token_service._get_key(user_id)
        
        # Assert
        assert key == "rt:user-123"
    
    def test_get_key_with_family(self, refresh_token_service):
        """Testa geração de chave Redis com token family"""
        # Arrange
        user_id = "user-123"
        token_family = "family-456"
        
        # Act
        key = refresh_token_service._get_key(user_id, token_family)
        
        # Assert
        assert key == "rt:user-123:family-456"
    
    def test_store_refresh_token_success_with_family(self, refresh_token_service, mock_redis):
        """Testa armazenamento bem-sucedido com token family fornecido"""
        # Arrange
        user_id = "user-123"
        refresh_token = "refresh-token-abc"
        token_family = "provided-family"
        
        mock_redis.setex.return_value = True
        
        # Act
        result = refresh_token_service.store_refresh_token(user_id, refresh_token, token_family)
        
        # Assert
        assert result is True
        mock_redis.setex.assert_called_once()
        
        # Verificar que a chave e dados estão corretos
        call_args = mock_redis.setex.call_args
        assert call_args[0][0] == "rt:user-123:provided-family"
        assert call_args[0][1] == 86400
        
        stored_data = json.loads(call_args[0][2])
        assert stored_data["token"] == "refresh-token-abc"
        assert stored_data["token_family"] == "provided-family"
        assert stored_data["used"] is False
        assert "created_at" in stored_data
    
    def test_store_refresh_token_success_generate_family(self, refresh_token_service, mock_redis):
        """Testa armazenamento bem-sucedido com geração de token family"""
        # Arrange
        user_id = "user-123"
        refresh_token = "refresh-token-abc"
        
        mock_redis.setex.return_value = True
        
        # Act
        with patch('uuid.uuid4') as mock_uuid:
            mock_uuid.return_value = uuid.UUID('12345678-1234-5678-1234-567812345678')
            result = refresh_token_service.store_refresh_token(user_id, refresh_token)
        
        # Assert
        assert result is True
        mock_redis.setex.assert_called_once()
        
        call_args = mock_redis.setex.call_args
        assert call_args[0][0] == "rt:user-123:12345678-1234-5678-1234-567812345678"
        
        stored_data = json.loads(call_args[0][2])
        assert stored_data["token_family"] == "12345678-1234-5678-1234-567812345678"
    
    def test_store_refresh_token_failure(self, refresh_token_service, mock_redis):
        """Testa falha no armazenamento do token"""
        # Arrange
        user_id = "user-123"
        refresh_token = "refresh-token-abc"
        
        mock_redis.setex.return_value = False
        
        # Act
        result = refresh_token_service.store_refresh_token(user_id, refresh_token)
        
        # Assert
        assert result is False
    
    def test_store_refresh_token_exception(self, refresh_token_service, mock_redis):
        """Testa exceção durante armazenamento"""
        # Arrange
        user_id = "user-123"
        refresh_token = "refresh-token-abc"
        
        mock_redis.setex.side_effect = Exception("Redis error")
        
        # Act
        result = refresh_token_service.store_refresh_token(user_id, refresh_token)
        
        # Assert
        assert result is False
    
    def test_verify_and_rotate_success(self, refresh_token_service, mock_redis, sample_token_data):
        """Testa verificação e rotação bem-sucedidas"""
        # Arrange
        user_id = "user-123"
        old_refresh_token = "refresh-token-123"
        
        # Mock Redis para retornar token válido
        mock_redis.keys.return_value = ["rt:user-123:family-123"]
        mock_redis.get.return_value = json.dumps(sample_token_data)
        mock_redis.setex.return_value = True
        
        # Act
        result, token_family, error = refresh_token_service.verify_and_rotate(user_id, old_refresh_token)
        
        # Assert
        assert result is True
        assert token_family == "family-123"
        assert error is None
        
        # Verificar que o token foi marcado como usado
        mock_redis.setex.assert_called_once()
        updated_data = json.loads(mock_redis.setex.call_args[0][2])
        assert updated_data["used"] is True
        assert "used_at" in updated_data
    
    def test_verify_and_rotate_token_not_found(self, refresh_token_service, mock_redis):
        """Testa verificação com token não encontrado"""
        # Arrange
        user_id = "user-123"
        old_refresh_token = "invalid-token"
        
        mock_redis.keys.return_value = ["rt:user-123:family-123"]
        mock_redis.get.return_value = json.dumps({
            "token": "different-token",
            "used": False,
            "token_family": "family-123"
        })
        
        # Act
        result, token_family, error = refresh_token_service.verify_and_rotate(user_id, old_refresh_token)
        
        # Assert
        assert result is False
        assert token_family is None
        assert error == "Invalid refresh token"
    
    def test_verify_and_rotate_no_tokens(self, refresh_token_service, mock_redis):
        """Testa verificação quando usuário não tem tokens"""
        # Arrange
        user_id = "user-123"
        old_refresh_token = "any-token"
        
        mock_redis.keys.return_value = []
        
        # Act
        result, token_family, error = refresh_token_service.verify_and_rotate(user_id, old_refresh_token)
        
        # Assert
        assert result is False
        assert token_family is None
        assert error == "Invalid refresh token"
    
    def test_verify_and_rotate_token_reuse_detected(self, refresh_token_service, mock_redis):
        """Testa detecção de reuso de token (security alert)"""
        # Arrange
        user_id = "user-123"
        old_refresh_token = "reused-token"
        
        mock_redis.keys.return_value = ["rt:user-123:family-123"]
        mock_redis.get.return_value = json.dumps({
            "token": "reused-token",
            "used": True,  # Token já foi usado!
            "token_family": "family-123"
        })
        
        # Act & Assert
        with pytest.raises(SecurityAlertError, match="Refresh token reuse detected"):
            refresh_token_service.verify_and_rotate(user_id, old_refresh_token)
    
    def test_verify_and_rotate_exception(self, refresh_token_service, mock_redis):
        """Testa exceção durante verificação"""
        # Arrange
        user_id = "user-123"
        old_refresh_token = "any-token"
        
        mock_redis.keys.side_effect = Exception("Redis connection error")
        
        # Act
        result, token_family, error = refresh_token_service.verify_and_rotate(user_id, old_refresh_token)
        
        # Assert
        assert result is False
        assert token_family is None
        assert "Redis connection error" in error
    
    def test_revoke_all_tokens_success(self, refresh_token_service, mock_redis):
        """Testa revogação bem-sucedida de todos os tokens"""
        # Arrange
        user_id = "user-123"
        
        mock_redis.keys.return_value = [
            "rt:user-123:family-1",
            "rt:user-123:family-2",
            "rt:user-123:family-3"
        ]
        mock_redis.delete.return_value = 1
        
        # Act
        result = refresh_token_service.revoke_all_tokens(user_id)
        
        # Assert
        assert result is True
        assert mock_redis.delete.call_count == 3
    
    def test_revoke_all_tokens_no_tokens(self, refresh_token_service, mock_redis):
        """Testa revogação quando não há tokens"""
        # Arrange
        user_id = "user-123"
        
        mock_redis.keys.return_value = []
        
        # Act
        result = refresh_token_service.revoke_all_tokens(user_id)
        
        # Assert
        assert result is False
    
    def test_revoke_all_tokens_failure(self, refresh_token_service, mock_redis):
        """Testa falha na revogação de tokens"""
        # Arrange
        user_id = "user-123"
        
        mock_redis.keys.return_value = ["rt:user-123:family-1"]
        mock_redis.delete.return_value = 0  # Delete falhou
        
        # Act
        result = refresh_token_service.revoke_all_tokens(user_id)
        
        # Assert
        assert result is False
    
    def test_revoke_all_tokens_exception(self, refresh_token_service, mock_redis):
        """Testa exceção durante revogação"""
        # Arrange
        user_id = "user-123"
        
        mock_redis.keys.side_effect = Exception("Redis error")
        
        # Act
        result = refresh_token_service.revoke_all_tokens(user_id)
        
        # Assert
        assert result is False
    
    def test_get_active_sessions_success(self, refresh_token_service, mock_redis):
        """Testa obtenção bem-sucedida de sessões ativas - VERSÃO CORRIGIDA"""
        # Arrange
        user_id = "user-123"
        
        # Mock multiple sessions com dados CONSISTENTES
        mock_redis.keys.return_value = [b"rt:user-123:family-123", b"rt:user-123:family-456"]
        
        token_data_1 = {
            "token": "refresh-token-123",
            "created_at": "2024-01-01T10:00:00",
            "used": False,
            "token_family": "family-123"  # CORRIGIDO para match
        }
        
        token_data_2 = {
            "token": "refresh-token-456",
            "created_at": "2024-01-01T11:00:00",
            "used": True,
            "used_at": "2024-01-01T11:00:00",
            "token_family": "family-456"  # CORRIGIDO para match
        }
        
        mock_redis.get.side_effect = [
            json.dumps(token_data_1),
            json.dumps(token_data_2)
        ]
        
        # Act
        sessions = refresh_token_service.get_active_sessions(user_id)
        
        # Assert
        assert len(sessions) == 2
        # Ordenar por created_at para garantir ordem
        sessions_sorted = sorted(sessions, key=lambda x: x["created_at"])
        assert sessions_sorted[0]["token_family"] == "family-123"
        assert sessions_sorted[1]["token_family"] == "family-456"
    
    def test_get_active_sessions_empty(self, refresh_token_service, mock_redis):
        """Testa obtenção de sessões quando não há tokens"""
        # Arrange
        user_id = "user-123"
        
        mock_redis.keys.return_value = []
        
        # Act
        sessions = refresh_token_service.get_active_sessions(user_id)
        
        # Assert
        assert sessions == []
    
    def test_get_active_sessions_exception(self, refresh_token_service, mock_redis):
        """Testa exceção durante obtenção de sessões"""
        # Arrange
        user_id = "user-123"
        
        mock_redis.keys.side_effect = Exception("Redis error")
        
        # Act
        sessions = refresh_token_service.get_active_sessions(user_id)
        
        # Assert
        assert sessions == []
    
    def test_cleanup_expired_tokens(self, refresh_token_service):
        """Testa limpeza de tokens expirados (apenas placeholder)"""
        # Act
        result = refresh_token_service.cleanup_expired_tokens()
        
        # Assert
        assert result == 0  # Método sempre retorna 0 conforme implementação
    
    def test_verify_and_rotate_with_multiple_tokens(self, refresh_token_service, mock_redis):
        """Testa verificação com múltiplos tokens do mesmo usuário"""
        # Arrange
        user_id = "user-123"
        target_token = "target-refresh-token"
        
        # Mock multiple token families
        mock_redis.keys.return_value = [
            "rt:user-123:family-1",
            "rt:user-123:family-2",  # Este contém o token alvo
            "rt:user-123:family-3"
        ]
        
        # Primeiros dois retornam tokens diferentes
        mock_redis.get.side_effect = [
            json.dumps({"token": "wrong-token-1", "used": False, "token_family": "family-1"}),
            json.dumps({"token": target_token, "used": False, "token_family": "family-2"}),
            # Terceiro não deve ser chamado pois já encontramos
        ]
        
        mock_redis.setex.return_value = True
        
        # Act
        result, token_family, error = refresh_token_service.verify_and_rotate(user_id, target_token)
        
        # Assert
        assert result is True
        assert token_family == "family-2"
        assert error is None
        
        # Verificar que apenas o token correto foi marcado como usado
        assert mock_redis.setex.call_count == 1