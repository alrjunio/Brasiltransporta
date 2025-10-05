import re

with open("tests/application/advertisements/test_advertisement_use_cases.py", "r") as f:
    content = f.read()

# Encontra o teste problemático
pattern = r'(def test_execute_vehicle_not_found\(self\):.*?)(result = use_case\.execute\(input_data\))'

def replacement(match):
    test_body = match.group(1)
    # Substitui a linha problemática pelo código correto
    new_body = test_body + '        with pytest.raises(ValidationError, match="Veículo não encontrado"):\n            use_case.execute(input_data)\n'
    return new_body

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open("tests/application/advertisements/test_advertisement_use_cases.py", "w") as f:
    f.write(new_content)

print("Arquivo corrigido!")
