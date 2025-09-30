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
from brasiltransporta.domain.errors import ValidationError

class TestCreateTransactionUseCase:
    def test_execute_success(self):
        """Testa criação bem-sucedida de transação"""
        # Mocks
        mock_transaction_repo = Mock()
        mock_user_repo = Mock()
        mock_plan_repo = Mock()
        
        # Setup
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
        mock_transaction_repo.add = Mock()
        
        # Use Case
        use_case = CreateTransactionUseCase(mock_transaction_repo, mock_user_repo, mock_plan_repo)
        input_data = CreateTransactionInput(
            user_id=user.id,
            plan_id=plan.id,
            amount=199.90,
            payment_method=PaymentMethod.CREDIT_CARD,
            metadata={"card_last_digits": "1234"}
        )
        
        # Execute
        result = use_case.execute(input_data)
        
        # Assert
        assert result.transaction_id is not None
        mock_user_repo.get_by_id.assert_called_once_with(user.id)
        mock_plan_repo.get_by_id.assert_called_once_with(plan.id)
        mock_transaction_repo.add.assert_called_once()

    def test_execute_user_not_found(self):
        """Testa criação com usuário não encontrado"""
        mock_transaction_repo = Mock()
        mock_user_repo = Mock()
        mock_plan_repo = Mock()
        
        mock_user_repo.get_by_id.return_value = None
        
        use_case = CreateTransactionUseCase(mock_transaction_repo, mock_user_repo, mock_plan_repo)
        input_data = CreateTransactionInput(
            user_id="user-123",
            plan_id="plan-456",
            amount=199.90,
            payment_method=PaymentMethod.CREDIT_CARD
        )
        
        with pytest.raises(ValidationError, match="Usuário não encontrado"):
            use_case.execute(input_data)

    def test_execute_plan_not_found(self):
        """Testa criação com plano não encontrado"""
        mock_transaction_repo = Mock()
        mock_user_repo = Mock()
        mock_plan_repo = Mock()
        
        user = User.create("João Silva", "joao@email.com", "hashed_password")
        mock_user_repo.get_by_id.return_value = user
        mock_plan_repo.get_by_id.return_value = None
        
        use_case = CreateTransactionUseCase(mock_transaction_repo, mock_user_repo, mock_plan_repo)
        input_data = CreateTransactionInput(
            user_id=user.id,
            plan_id="plan-456",
            amount=199.90,
            payment_method=PaymentMethod.CREDIT_CARD
        )
        
        with pytest.raises(ValidationError, match="Plano não encontrado ou inativo"):
            use_case.execute(input_data)

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
