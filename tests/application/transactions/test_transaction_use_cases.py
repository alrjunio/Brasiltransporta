# tests/application/transactions/test_use_cases.py
import pytest
from unittest.mock import Mock
from brasiltransporta.application.transactions.use_cases.create_transaction import (
    CreateTransactionUseCase, CreateTransactionInput
)
from brasiltransporta.application.transactions.use_cases.get_transaction_by_id import (
    GetTransactionByIdUseCase
)
from brasiltransporta.domain.entities.transaction import Transaction, PaymentMethod
from brasiltransporta.domain.entities.user import User
from brasiltransporta.domain.entities.plan import Plan, PlanType, BillingCycle
from brasiltransporta.domain.errors.errors import ValidationError

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient

class TestAdvertisementRoutes:
    
    def test_get_advertisement_success(self, client):
        """Testa busca bem-sucedida de anúncio via API"""
        with patch('brasiltransporta.presentation.api.di.dependencies.get_get_advertisement_by_id_uc') as mock_uc:
            mock_use_case = Mock()
            valid_uuid = "123e4567-e89b-12d3-a456-426614174999"
            
            # Mock mais realista do retorno
            mock_result = Mock()
            mock_result.id = valid_uuid
            mock_result.store_id = "123e4567-e89b-12d3-a456-426614174000"
            mock_result.vehicle_id = "123e4567-e89b-12d3-a456-426614174001"
            mock_result.title = "Caminhão Volvo 2022"
            mock_result.description = "Caminhão em excelente estado"
            mock_result.price_amount = 150000.00
            mock_result.price_currency = "BRL"
            mock_result.status = "draft"
            mock_result.is_featured = False
            mock_result.views = 0
            mock_result.created_at = "2023-01-01T00:00:00"
            mock_result.updated_at = "2023-01-01T00:00:00"
            
            mock_use_case.execute.return_value = mock_result
            mock_uc.return_value = mock_use_case

            response = client.get(f"/advertisements/{valid_uuid}")
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == valid_uuid
            assert data["title"] == "Caminhão Volvo 2022"
            assert data["description"] == "Caminhão em excelente estado"
            assert data["price_amount"] == 150000.00
            mock_uc.assert_called_once()
            mock_use_case.execute.assert_called_once_with(valid_uuid)

    def test_get_advertisement_not_found(self, client):
        """Testa busca de anúncio não encontrado"""
        with patch('brasiltransporta.presentation.api.di.dependencies.get_get_advertisement_by_id_uc') as mock_uc:
            mock_use_case = Mock()
            mock_use_case.execute.return_value = None
            mock_uc.return_value = mock_use_case

            invalid_uuid = "00000000-0000-0000-0000-000000000000"
            response = client.get(f"/advertisements/{invalid_uuid}")
            
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert "not found" in data["detail"].lower()

    def test_create_advertisement_success(self, client):
        """Testa criação bem-sucedida de anúncio"""
        with patch('brasiltransporta.presentation.api.di.dependencies.get_create_advertisement_uc') as mock_uc:
            mock_use_case = Mock()
            mock_use_case.execute.return_value = Mock(advertisement_id="123e4567-e89b-12d3-a456-426614174999")
            mock_uc.return_value = mock_use_case

            payload = {
                "store_id": "123e4567-e89b-12d3-a456-426614174000",
                "vehicle_id": "123e4567-e89b-12d3-a456-426614174001",
                "title": "Novo Caminhão",
                "description": "Descrição do anúncio",
                "price_amount": 200000.00
            }

            response = client.post("/advertisements/", json=payload)
            
            assert response.status_code == 201
            data = response.json()
            assert "advertisement_id" in data
            mock_uc.assert_called_once()

    def test_execute_inactive_plan(self):
        """Testa criação com plano inativo"""
        mock_transaction_repo = Mock()
        mock_user_repo = Mock()
        mock_plan_repo = Mock()
        
        user = User.create("João Silva", "joao@email.com", "hashed_password")
        plan = Plan.create(
            name="Plano Básico",
            description="Plano básico",
            plan_type=PlanType.BASIC,
            billing_cycle=BillingCycle.MONTHLY,
            price_amount=199.90
        )
        plan.deactivate()
        
        mock_user_repo.get_by_id.return_value = user
        mock_plan_repo.get_by_id.return_value = plan
        
        use_case = CreateTransactionUseCase(mock_transaction_repo, mock_user_repo, mock_plan_repo)
        input_data = CreateTransactionInput(
            user_id=user.id,
            plan_id=plan.id,
            amount=199.90,
            payment_method=PaymentMethod.CREDIT_CARD
        )
        
        with pytest.raises(ValidationError, match="Plano não encontrado ou inativo"):
            use_case.execute(input_data)

    def test_execute_amount_mismatch(self):
        """Testa criação com valor incorreto"""
        mock_transaction_repo = Mock()
        mock_user_repo = Mock()
        mock_plan_repo = Mock()
        
        user = User.create("João Silva", "joao@email.com", "hashed_password")
        plan = Plan.create(
            name="Plano Básico",
            description="Plano básico",
            plan_type=PlanType.BASIC,
            billing_cycle=BillingCycle.MONTHLY,
            price_amount=199.90
        )
        
        mock_user_repo.get_by_id.return_value = user
        mock_plan_repo.get_by_id.return_value = plan
        
        use_case = CreateTransactionUseCase(mock_transaction_repo, mock_user_repo, mock_plan_repo)
        input_data = CreateTransactionInput(
            user_id=user.id,
            plan_id=plan.id,
            amount=150.00,  # Diferente do preço do plano
            payment_method=PaymentMethod.CREDIT_CARD
        )
        
        with pytest.raises(ValidationError, match="Valor da transação não corresponde ao preço do plano"):
            use_case.execute(input_data)

class TestGetTransactionByIdUseCase:
    def test_execute_success(self):
        """Testa busca bem-sucedida de transação por ID"""
        mock_transaction_repo = Mock()
        transaction = Transaction.create(
            user_id="user-123",
            plan_id="plan-456",
            amount=199.90,
            payment_method=PaymentMethod.CREDIT_CARD
        )
        mock_transaction_repo.get_by_id.return_value = transaction
        
        use_case = GetTransactionByIdUseCase(mock_transaction_repo)
        result = use_case.execute(transaction.id)
        
        assert result is not None
        assert result.id == transaction.id
        assert result.amount == 199.90
        mock_transaction_repo.get_by_id.assert_called_once_with(transaction.id)

    def test_execute_not_found(self):
        """Testa busca de transação não encontrada"""
        mock_transaction_repo = Mock()
        mock_transaction_repo.get_by_id.return_value = None
        
        use_case = GetTransactionByIdUseCase(mock_transaction_repo)
        result = use_case.execute("non-existent-id")
        
        assert result is None
