# tests/application/plans/test_use_cases.py
import pytest
from unittest.mock import Mock
from brasiltransporta.application.plans.use_cases.create_plan import (
    CreatePlanUseCase, CreatePlanInput
)
from brasiltransporta.application.plans.use_cases.get_plan_by_id import (
    GetPlanByIdUseCase
)
from brasiltransporta.application.plans.use_cases.list_active_plans import (
    ListActivePlansUseCase
)
from brasiltransporta.domain.entities.plan import Plan, PlanType, BillingCycle
from brasiltransporta.domain.errors import ValidationError

class TestCreatePlanUseCase:
    def test_execute_success(self):
        """Testa criação bem-sucedida de plano"""
        mock_plan_repo = Mock()
        mock_plan_repo.get_by_type_and_cycle.return_value = None
        mock_plan_repo.add = Mock()
        
        use_case = CreatePlanUseCase(mock_plan_repo)
        input_data = CreatePlanInput(
            name="Plano Premium",
            description="Plano completo para grandes empresas",
            plan_type=PlanType.PREMIUM,
            billing_cycle=BillingCycle.MONTHLY,
            price_amount=499.90,
            max_ads=50,
            max_featured_ads=5,
            features=["Suporte prioritário", "Analytics avançado"]
        )
        
        result = use_case.execute(input_data)
        
        assert result.plan_id is not None
        mock_plan_repo.add.assert_called_once()

    def test_execute_duplicate_plan(self):
        """Testa criação de plano duplicado"""
        mock_plan_repo = Mock()
        existing_plan = Plan.create(
            name="Plano Existente",
            description="Plano já existente",
            plan_type=PlanType.PREMIUM,
            billing_cycle=BillingCycle.MONTHLY,
            price_amount=499.90
        )
        mock_plan_repo.get_by_type_and_cycle.return_value = existing_plan
        
        use_case = CreatePlanUseCase(mock_plan_repo)
        input_data = CreatePlanInput(
            name="Plano Premium",
            description="Plano completo para grandes empresas",
            plan_type=PlanType.PREMIUM,
            billing_cycle=BillingCycle.MONTHLY,
            price_amount=499.90
        )
        
        with pytest.raises(ValidationError, match="Já existe um plano com este tipo e ciclo de cobrança"):
            use_case.execute(input_data)

class TestGetPlanByIdUseCase:
    def test_execute_success(self):
        """Testa busca bem-sucedida de plano por ID"""
        mock_plan_repo = Mock()
        plan = Plan.create(
            name="Plano Básico",
            description="Plano ideal para pequenas empresas",
            plan_type=PlanType.BASIC,
            billing_cycle=BillingCycle.MONTHLY,
            price_amount=199.90
        )
        mock_plan_repo.get_by_id.return_value = plan
        
        use_case = GetPlanByIdUseCase(mock_plan_repo)
        result = use_case.execute(plan.id)
        
        assert result is not None
        assert result.id == plan.id
        assert result.name == "Plano Básico"
        mock_plan_repo.get_by_id.assert_called_once_with(plan.id)

    def test_execute_not_found(self):
        """Testa busca de plano não encontrado"""
        mock_plan_repo = Mock()
        mock_plan_repo.get_by_id.return_value = None
        
        use_case = GetPlanByIdUseCase(mock_plan_repo)
        result = use_case.execute("non-existent-id")
        
        assert result is None

class TestListActivePlansUseCase:
    def test_execute_success(self):
        """Testa listagem bem-sucedida de planos ativos"""
        mock_plan_repo = Mock()
        plan1 = Plan.create(
            name="Plano Básico",
            description="Plano básico",
            plan_type=PlanType.BASIC,
            billing_cycle=BillingCycle.MONTHLY,
            price_amount=199.90
        )
        plan2 = Plan.create(
            name="Plano Premium",
            description="Plano premium",
            plan_type=PlanType.PREMIUM,
            billing_cycle=BillingCycle.MONTHLY,
            price_amount=499.90
        )
        mock_plan_repo.list_active.return_value = [plan1, plan2]
        
        use_case = ListActivePlansUseCase(mock_plan_repo)
        result = use_case.execute()
        
        assert len(result.plans) == 2
        assert result.plans[0].name == "Plano Básico"
        assert result.plans[1].name == "Plano Premium"
        mock_plan_repo.list_active.assert_called_once()

    def test_execute_empty_list(self):
        """Testa listagem quando não há planos ativos"""
        mock_plan_repo = Mock()
        mock_plan_repo.list_active.return_value = []
        
        use_case = ListActivePlansUseCase(mock_plan_repo)
        result = use_case.execute()
        
        assert len(result.plans) == 0
