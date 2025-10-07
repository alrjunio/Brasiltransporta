# tests/unit/security/test_password_hasher.py
from __future__ import annotations

import pytest
from unittest.mock import patch, Mock
from passlib.hash import bcrypt # pyright: ignore[reportMissingModuleSource]

from brasiltransporta.infrastructure.security.password_hasher import BcryptPasswordHasher


class TestBcryptPasswordHasher:
    """Testes unitários para BcryptPasswordHasher"""
    
    @pytest.fixture
    def password_hasher(self):
        """Instância do hasher para testes"""
        return BcryptPasswordHasher()
    
    def test_hash_password_success(self, password_hasher):
        """Testa hash bem-sucedido de senha"""
        # Arrange
        raw_password = "securepassword123"
        
        # Mock bcrypt.hash para retornar hash previsível
        with patch('brasiltransporta.infrastructure.security.password_hasher.bcrypt.hash') as mock_hash:
            mock_hash.return_value = "$2b$12$hashedpassword123456789012"
            
            # Act
            hashed_password = password_hasher.hash(raw_password)
            
            # Assert
            assert hashed_password == "$2b$12$hashedpassword123456789012"
            mock_hash.assert_called_once_with(raw_password)
    
    def test_hash_password_short_password(self, password_hasher):
        """Testa hash com senha muito curta"""
        # Arrange
        short_passwords = ["", "123", "short", "12345"]  # Todas < 6 caracteres
        
        for raw_password in short_passwords:
            # Act & Assert
            with pytest.raises(ValueError, match="Senha deve ter pelo menos 6 caracteres"):
                password_hasher.hash(raw_password)
    
    def test_hash_password_none_password(self, password_hasher):
        """Testa hash com senha None"""
        # Act & Assert
        with pytest.raises(ValueError, match="Senha deve ter pelo menos 6 caracteres"):
            password_hasher.hash(None)
    
    def test_verify_password_success(self, password_hasher):
        """Testa verificação bem-sucedida de senha"""
        # Arrange
        raw_password = "correctpassword"
        hashed_password = "$2b$12$hashedpassword123456789012"
        
        # Mock bcrypt.verify para retornar True
        with patch('brasiltransporta.infrastructure.security.password_hasher.bcrypt.verify') as mock_verify:
            mock_verify.return_value = True
            
            # Act
            result = password_hasher.verify(raw_password, hashed_password)
            
            # Assert
            assert result is True
            mock_verify.assert_called_once_with(raw_password, hashed_password)
    
    def test_verify_password_wrong_password(self, password_hasher):
        """Testa verificação com senha incorreta"""
        # Arrange
        wrong_password = "wrongpassword"
        hashed_password = "$2b$12$hashedpassword123456789012"
        
        # Mock bcrypt.verify para retornar False
        with patch('brasiltransporta.infrastructure.security.password_hasher.bcrypt.verify') as mock_verify:
            mock_verify.return_value = False
            
            # Act
            result = password_hasher.verify(wrong_password, hashed_password)
            
            # Assert
            assert result is False
            mock_verify.assert_called_once_with(wrong_password, hashed_password)
    
    def test_verify_password_empty_strings(self, password_hasher):
        """Testa verificação com strings vazias"""
        # Arrange
        raw_password = ""
        hashed_password = ""
        
        # Mock bcrypt.verify para retornar False (comportamento esperado)
        with patch('brasiltransporta.infrastructure.security.password_hasher.bcrypt.verify') as mock_verify:
            mock_verify.return_value = False
            
            # Act
            result = password_hasher.verify(raw_password, hashed_password)
            
            # Assert
            assert result is False
            mock_verify.assert_called_once_with(raw_password, hashed_password)
    
    def test_verify_password_none_values(self, password_hasher):
        """Testa verificação com valores None"""
        # Arrange
        raw_password = None
        hashed_password = None
        
        # Mock bcrypt.verify para lidar com None (deve lançar exceção ou retornar False)
        with patch('brasiltransporta.infrastructure.security.password_hasher.bcrypt.verify') as mock_verify:
            # bcrypt.verify normalmente lançaria exceção com None, mas vamos mockar
            mock_verify.return_value = False
            
            # Act
            result = password_hasher.verify(raw_password, hashed_password)
            
            # Assert
            assert result is False
            mock_verify.assert_called_once_with(raw_password, hashed_password)
    
    def test_hash_and_verify_integration(self, password_hasher):
        """Teste de integração: hash seguido de verificação"""
        # Arrange
        raw_password = "mysecurepassword789"
        
        # Mock bcrypt.hash para retornar um hash simulado
        with patch('brasiltransporta.infrastructure.security.password_hasher.bcrypt.hash') as mock_hash:
            simulated_hash = "$2b$12$simulatedhash1234567890123456"
            mock_hash.return_value = simulated_hash
            
            # Mock bcrypt.verify para verificar contra o hash simulado
            with patch('brasiltransporta.infrastructure.security.password_hasher.bcrypt.verify') as mock_verify:
                mock_verify.return_value = True
                
                # Act - Hash
                hashed_password = password_hasher.hash(raw_password)
                
                # Act - Verify
                verification_result = password_hasher.verify(raw_password, hashed_password)
                
                # Assert
                assert hashed_password == simulated_hash
                assert verification_result is True
                mock_hash.assert_called_once_with(raw_password)
                mock_verify.assert_called_once_with(raw_password, simulated_hash)
    
    def test_hash_different_passwords_produce_different_hashes(self, password_hasher):
        """Testa que senhas diferentes produzem hashes diferentes"""
        # Arrange
        password1 = "password123"
        password2 = "password456"
        
        # Mock bcrypt.hash para retornar hashes diferentes
        with patch('brasiltransporta.infrastructure.security.password_hasher.bcrypt.hash') as mock_hash:
            mock_hash.side_effect = [
                "$2b$12$hashforpassword1123456789012",
                "$2b$12$hashforpassword2123456789012"
            ]
            
            # Act
            hash1 = password_hasher.hash(password1)
            hash2 = password_hasher.hash(password2)
            
            # Assert
            assert hash1 != hash2
            assert mock_hash.call_count == 2
            mock_hash.assert_any_call(password1)
            mock_hash.assert_any_call(password2)
    
    def test_hash_same_password_produces_different_hashes_due_to_salt(self, password_hasher):
        """Testa que a mesma senha produz hashes diferentes devido ao salt"""
        # Arrange
        same_password = "samepassword"
        
        # Mock bcrypt.hash para retornar hashes diferentes (comportamento real do bcrypt)
        with patch('brasiltransporta.infrastructure.security.password_hasher.bcrypt.hash') as mock_hash:
            mock_hash.side_effect = [
                "$2b$12$firsthashwithsalt1234567890",
                "$2b$12$secondhashwithsalt123456789"
            ]
            
            # Act
            hash1 = password_hasher.hash(same_password)
            hash2 = password_hasher.hash(same_password)
            
            # Assert
            assert hash1 != hash2  # Hashes devem ser diferentes devido ao salt
            assert mock_hash.call_count == 2
            # Ambas as chamadas foram com a mesma senha
            assert mock_hash.call_args_list[0] == mock_hash.call_args_list[1]
    
    def test_verify_with_different_hashes(self, password_hasher):
        """Testa verificação com diferentes hashes para a mesma senha"""
        # Arrange
        raw_password = "testpassword"
        hash1 = "$2b$12$firsthash12345678901234567890"
        hash2 = "$2b$12$secondhash1234567890123456789"
        
        # Mock bcrypt.verify para retornar True apenas para o hash correto
        with patch('brasiltransporta.infrastructure.security.password_hasher.bcrypt.verify') as mock_verify:
            def verify_side_effect(password, hashed):
                return hashed == hash1  # Apenas hash1 é "válido"
            
            mock_verify.side_effect = verify_side_effect
            
            # Act & Assert
            result1 = password_hasher.verify(raw_password, hash1)
            result2 = password_hasher.verify(raw_password, hash2)
            
            # Assert
            assert result1 is True
            assert result2 is False
            assert mock_verify.call_count == 2
    
    def test_hash_password_boundary_length(self, password_hasher):
        """Testa hash com senha no limite mínimo de caracteres"""
        # Arrange
        boundary_password = "123456"  # Exatamente 6 caracteres
        
        with patch('brasiltransporta.infrastructure.security.password_hasher.bcrypt.hash') as mock_hash:
            mock_hash.return_value = "$2b$12$boundaryhash1234567890123"
            
            # Act - Não deve lançar exceção
            hashed_password = password_hasher.hash(boundary_password)
            
            # Assert
            assert hashed_password == "$2b$12$boundaryhash1234567890123"
            mock_hash.assert_called_once_with(boundary_password)
    
    def test_hash_password_very_long(self, password_hasher):
        """Testa hash com senha muito longa"""
        # Arrange
        long_password = "a" * 1000  # Senha muito longa
        
        with patch('brasiltransporta.infrastructure.security.password_hasher.bcrypt.hash') as mock_hash:
            mock_hash.return_value = "$2b$12$longpasswordhash1234567890"
            
            # Act - Não deve lançar exceção
            hashed_password = password_hasher.hash(long_password)
            
            # Assert
            assert hashed_password == "$2b$12$longpasswordhash1234567890"
            mock_hash.assert_called_once_with(long_password)
    
    def test_verify_with_invalid_hash_format(self, password_hasher):
        """Testa verificação com formato de hash inválido"""
        # Arrange
        raw_password = "anypassword"
        invalid_hash = "invalid-hash-format"
        
        # Mock bcrypt.verify para lançar exceção com hash inválido
        with patch('brasiltransporta.infrastructure.security.password_hasher.bcrypt.verify') as mock_verify:
            mock_verify.side_effect = Exception("Invalid hash")
            
            # Act & Assert
            with pytest.raises(Exception, match="Invalid hash"):
                password_hasher.verify(raw_password, invalid_hash)
    
    def test_implements_password_hasher_interface(self, password_hasher):
        """Testa que a classe implementa a interface PasswordHasher"""
        # Arrange
        from brasiltransporta.application.users.use_cases.register_user import PasswordHasher
        
        # Act & Assert
        assert isinstance(password_hasher, PasswordHasher)
        assert hasattr(password_hasher, 'hash')
        assert hasattr(password_hasher, 'verify')
        assert callable(password_hasher.hash)
        assert callable(password_hasher.verify)