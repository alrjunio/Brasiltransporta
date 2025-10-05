import pytest
from unittest.mock import Mock
from brasiltransporta.domain.entities.transaction import Transaction, PaymentMethod
from brasiltransporta.domain.entities.plan import Plan, PlanType, BillingCycle
from brasiltransporta.application.transactions.use_cases.create_transaction import CreateTransactionUseCase, CreateTransactionInput
from brasiltransporta.application.transactions.use_cases.get_transaction_by_id import GetTransactionByIdUseCase, GetTransactionByIdInput

class TestCreateTransactionUseCase:
    def test_create_transaction_success(self):
        # Arrange
        mock_transaction_repo = Mock()
        mock_user_repo = Mock()
        mock_plan_repo = Mock()
        
        user_id = "user-123"
        plan = Plan.create(
            name="Plano Básico",
            description="Plano básico de anúncios",
            plan_type=PlanType.PREMIUM,
            billing_cycle=BillingCycle.MONTHLY,
            price_amount=100.0
        )
        
        mock_plan_repo.get_by_id.return_value = plan
        mock_user_repo.get_by_id.return_value = Mock()
        
        use_case = CreateTransactionUseCase(
            transaction_repo=mock_transaction_repo,
            user_repo=mock_user_repo,
            plan_repo=mock_plan_repo
        )
        
        # Act
        input_data = CreateTransactionInput(
            user_id=user_id,
            plan_id=plan.id,
            amount=100.0,
            currency="BRL",
            payment_method=PaymentMethod.CREDIT_CARD,
            metadata={"some_data": "value"}
        )
        result = use_case.execute(input_data)
        
        # Assert
        assert result.transaction_id is not None
        assert len(result.transaction_id) > 0
        mock_transaction_repo.add.assert_called_once()

    def test_create_transaction_plan_not_found(self):
        # Arrange
        mock_transaction_repo = Mock()
        mock_user_repo = Mock()
        mock_plan_repo = Mock()
        mock_plan_repo.get_by_id.return_value = None
        
        use_case = CreateTransactionUseCase(
            transaction_repo=mock_transaction_repo,
            user_repo=mock_user_repo,
            plan_repo=mock_plan_repo
        )
        
        # Act & Assert
        input_data = CreateTransactionInput(
            user_id="user-123",
            plan_id="non-existent-plan-id",
            amount=100.0,
            payment_method=PaymentMethod.CREDIT_CARD
        )
        
        with pytest.raises(Exception) as exc_info:
            use_case.execute(input_data)
        
        assert "Plano não encontrado" in str(exc_info.value)

class TestGetTransactionByIdUseCase:
    def test_execute_success(self):
        # Arrange
        mock_repo = Mock()
        
        transaction = Transaction.create(
            user_id="user-123",
            plan_id="plan-123",
            amount=100.0,
            payment_method=PaymentMethod.CREDIT_CARD
        )
        
        mock_repo.get_by_id.return_value = transaction
        use_case = GetTransactionByIdUseCase(mock_repo)
        
        # Act
        input_data = GetTransactionByIdInput(transaction_id=transaction.id)
        result = use_case.execute(input_data)
        
        # Assert
        assert result is not None
        assert result.id == transaction.id
        assert result.user_id == "user-123"
        assert result.amount.amount == 100.0
        mock_repo.get_by_id.assert_called_once_with(transaction.id)

    def test_execute_not_found(self):
        # Arrange
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None
        use_case = GetTransactionByIdUseCase(mock_repo)
        
        # Act
        input_data = GetTransactionByIdInput(transaction_id="non-existent-id")
        result = use_case.execute(input_data)
        
        # Assert
        assert result is None
        mock_repo.get_by_id.assert_called_once_with("non-existent-id")