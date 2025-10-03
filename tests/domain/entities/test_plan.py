# tests/domain/entities/test_plan.py
import pytest
from brasiltransporta.domain.entities.plan import Plan, PlanType, BillingCycle


class TestPlan:
    def test_create_plan_success(self):
        """Testa criação bem-sucedida de plano"""
        plan = Plan.create(
            name="Plano Básico",
            description="Plano ideal para pequenas empresas",
            plan_type=PlanType.BASIC,
            billing_cycle=BillingCycle.MONTHLY,
            price_amount=199.90,
            max_ads=10,
            max_featured_ads=1,
            features=["Suporte por email", "5 anúncios ativos"]
        )
        
        assert plan.id is not None
        assert plan.name == "Plano Básico"
        assert plan.plan_type == PlanType.BASIC
        assert plan.billing_cycle == BillingCycle.MONTHLY
        assert plan.price_amount == 199.90
        assert plan.max_ads == 10
        assert plan.max_featured_ads == 1
        assert plan.is_active == True
        assert "Suporte por email" in plan.features

    def test_create_plan_invalid_name(self):
        """Testa criação com nome inválido"""
        with pytest.raises(ValueError, match="Nome do plano deve ter pelo menos 3 caracteres"):
            Plan.create(
                name="A",
                description="Descrição válida",
                plan_type=PlanType.BASIC,
                billing_cycle=BillingCycle.MONTHLY,
                price_amount=199.90
            )

    def test_create_plan_negative_price(self):
        """Testa criação com preço negativo"""
        with pytest.raises(ValueError, match="Preço não pode ser negativo"):
            Plan.create(
                name="Plano Válido",
                description="Descrição válida",
                plan_type=PlanType.BASIC,
                billing_cycle=BillingCycle.MONTHLY,
                price_amount=-10.00
            )

    def test_create_plan_negative_max_ads(self):
        """Testa criação com número negativo de anúncios"""
        with pytest.raises(ValueError, match="Número máximo de anúncios não pode ser negativo"):
            Plan.create(
                name="Plano Válido",
                description="Descrição válida",
                plan_type=PlanType.BASIC,
                billing_cycle=BillingCycle.MONTHLY,
                price_amount=199.90,
                max_ads=-5
            )

    def test_deactivate_plan(self):
        """Testa desativação de plano"""
        plan = Plan.create(
            name="Plano Básico",
            description="Plano ideal para pequenas empresas",
            plan_type=PlanType.BASIC,
            billing_cycle=BillingCycle.MONTHLY,
            price_amount=199.90
        )
        
        plan.deactivate()
        
        assert plan.is_active == False

    def test_activate_plan(self):
        """Testa ativação de plano"""
        plan = Plan.create(
            name="Plano Básico",
            description="Plano ideal para pequenas empresas",
            plan_type=PlanType.BASIC,
            billing_cycle=BillingCycle.MONTHLY,
            price_amount=199.90
        )
        
        plan.deactivate()
        plan.activate()
        
        assert plan.is_active == True
