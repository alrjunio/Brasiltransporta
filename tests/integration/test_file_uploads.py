import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from brasiltransporta.presentation.api.app import create_app as create_application

class TestFileUploads:
    def setup_method(self):
        self.app = create_application()
        self.client = TestClient(self.app)
        
        # Mock do JWT para testes
        self.auth_headers = {"Authorization": "Bearer mock_jwt_token"}
    
    @patch('presentation.api.controllers.file_uploads.get_current_user')
    @patch('presentation.api.controllers.file_uploads.get_upload_use_case')
    def test_upload_image_success(self, mock_use_case, mock_auth):
        # Configurar mocks
        mock_auth.return_value = {"user_id": "test-user", "email": "test@example.com"}
        
        mock_result = Mock()
        mock_result.success = True
        mock_result.file_url = "https://example.com/image.jpg"
        mock_result.file_key = "ads/123/images/test.jpg"
        mock_result.file_size = 1024000
        
        mock_use_case_instance = Mock()
        mock_use_case_instance.execute.return_value = mock_result
        mock_use_case.return_value = mock_use_case_instance
        
        # Fazer requisição
        files = {"file": ("test.jpg", b"fake image content", "image/jpeg")}
        response = self.client.post(
            "/api/v1/storage/ads/123/images",
            files=files,
            headers=self.auth_headers
        )
        
        # Verificar resultado
        assert response.status_code == 201
        data = response.json()
        assert data["success"] == True
        assert data["file_url"] == "https://example.com/image.jpg"
    
    @patch('presentation.api.controllers.file_uploads.get_current_user')
    def test_upload_image_unauthorized(self, mock_auth):
        # Testar sem autenticação
        files = {"file": ("test.jpg", b"fake image content", "image/jpeg")}
        response = self.client.post("/api/v1/storage/ads/123/images", files=files)
        
        assert response.status_code == 401
    
    @patch('presentation.api.controllers.file_uploads.get_current_user')
    @patch('presentation.api.controllers.file_uploads.get_presigned_url_use_case')
    def test_generate_presigned_url(self, mock_use_case, mock_auth):
        # Configurar mocks
        mock_auth.return_value = {"user_id": "test-user"}
        
        mock_result = Mock()
        mock_result.success = True
        mock_result.url = "https://s3.amazonaws.com/presigned-url"
        
        mock_use_case_instance = Mock()
        mock_use_case_instance.execute.return_value = mock_result
        mock_use_case.return_value = mock_use_case_instance
        
        # Fazer requisição
        payload = {
            "file_key": "ads/123/images/test.jpg",
            "operation": "get_object",
            "expires_in": 3600
        }
        response = self.client.post(
            "/api/v1/storage/presigned-url",
            json=payload,
            headers=self.auth_headers
        )
        
        # Verificar resultado
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "presigned-url" in data["url"]