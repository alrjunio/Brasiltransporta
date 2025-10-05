with open('tests/application/advertisements/test_advertisement_use_cases.py', 'r') as f:
    content = f.read()

# Corrige o teste store_not_found
store_test = '''    def test_execute_store_not_found(self):
        \"\"\"Testa criação com loja não encontrada\"\"\"
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()

        mock_store_repo.get_by_id.return_value = None

        use_case = CreateAdvertisementUseCase(mock_ad_repo, mock_store_repo, mock_vehicle_repo)
        input_data = CreateAdvertisementInput(
            store_id=\"store-123\",
            vehicle_id=\"vehicle-456\",
            title=\"Caminhão Volvo 2022\",
            description=\"Caminhão em excelente estado\",
            price_amount=150000.00
        )

        with pytest.raises(ValidationError, match=\"Loja não encontrada\"):
            use_case.execute(input_data)'''

# Corrige o teste vehicle_not_found
vehicle_test = '''    def test_execute_vehicle_not_found(self):
        \"\"\"Testa criação com veículo não encontrado\"\"\"
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()

        store = Store.create(\"Minha Loja\", \"user-123\", \"owner-123\")
        mock_store_repo.get_by_id.return_value = store

        mock_vehicle_repo.get_by_id.return_value = None

        use_case = CreateAdvertisementUseCase(mock_ad_repo, mock_store_repo, mock_vehicle_repo)
        input_data = CreateAdvertisementInput(
            store_id=\"store-123\",
            vehicle_id=\"vehicle-456\",
            title=\"Caminhão Volvo 2022\",
            description=\"Caminhão em excelente estado\",
            price_amount=150000.00
        )

        with pytest.raises(ValidationError, match=\"Veículo não encontrado\"):
            use_case.execute(input_data)'''

import re

# Substitui os testes
content = re.sub(r'def test_execute_store_not_found\(self\):.*?assert True', store_test, content, flags=re.DOTALL)
content = re.sub(r'def test_execute_vehicle_not_found\(self\):.*?assert True', vehicle_test, content, flags=re.DOTALL)

with open('tests/application/advertisements/test_advertisement_use_cases.py', 'w') as f:
    f.write(content)

print('Testes corrigidos!')
