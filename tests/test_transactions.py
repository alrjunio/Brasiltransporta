# tests/domain/entities/test_transaction.py
import pytest
from brasiltransporta.domain.entities.transaction import Transaction, TransactionStatus, PaymentMethod
from brasiltransporta.domain.errors.errors import ValidationError

class TestTransaction:
    def test_create_transaction_success(self):
        """Testa criação bem-sucedida de transação"""
        transaction = Transaction.create(
            user_id="user-123",
            plan_id="plan-456",
            amount=199.90,
            payment_method=PaymentMethod.CREDIT_CARD,
            metadata={"card_last_digits": "1234"}
        )
        
        assert transaction.id is not None
        assert transaction.user_id == "user-123"
        assert transaction.plan_id == "plan-456"
        assert transaction.amount.amount == 199.90
        assert transaction.payment_method == PaymentMethod.CREDIT_CARD
        assert transaction.status == TransactionStatus.PENDING
        assert transaction.external_payment_id is None
        assert transaction.metadata["card_last_digits"] == "1234"

    def test_create_transaction_invalid_amount(self):
        """Testa criação com valor inválido"""
        with pytest.raises(ValidationError, match="Valor da transação deve ser maior que zero"):
            Transaction.create(
                user_id="user-123",
                plan_id="plan-456",
                amount=0,
                payment_method=PaymentMethod.CREDIT_CARD
            )

    def test_mark_completed(self):
        """Testa marcação de transação como completada"""
        transaction = Transaction.create(
            user_id="user-123",
            plan_id="plan-456",
            amount=199.90,
            payment_method=PaymentMethod.CREDIT_CARD
        )
        
        transaction.mark_completed("ext_payment_123")
        
        assert transaction.status == TransactionStatus.COMPLETED
        assert transaction.external_payment_id == "ext_payment_123"

    def test_mark_failed(self):
        """Testa marcação de transação como falha"""
        transaction = Transaction.create(
            user_id="user-123",
            plan_id="plan-456",
            amount=199.90,
            payment_method=PaymentMethod.CREDIT_CARD
        )
        
        transaction.mark_failed()
        
        assert transaction.status == TransactionStatus.FAILED

    def test_refund_completed_transaction(self):
        """Testa reembolso de transação completada"""
        transaction = Transaction.create(
            user_id="user-123",
            plan_id="plan-456",
            amount=199.90,
            payment_method=PaymentMethod.CREDIT_CARD
        )
        
        transaction.mark_completed("ext_payment_123")
        transaction.refund()
        
        assert transaction.status == TransactionStatus.REFUNDED

    def test_refund_pending_transaction(self):
        """Testa tentativa de reembolso de transação pendente"""
        transaction = Transaction.create(
            user_id="user-123",
            plan_id="plan-456",
            amount=199.90,
            payment_method=PaymentMethod.CREDIT_CARD
        )
        
        with pytest.raises(ValidationError, match="Apenas transações completadas podem ser reembolsadas"):
            transaction.refund()
