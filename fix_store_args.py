with open('tests/application/advertisements/test_advertisement_use_cases.py', 'r') as f:
    content = f.read()

# Corrige o número de argumentos do Store.create()
content = content.replace('store = Store.create(\"Minha Loja\", \"user-123\", \"owner-123\")', 'store = Store.create(\"Minha Loja\", \"user-123\")')

with open('tests/application/advertisements/test_advertisement_use_cases.py', 'w') as f:
    f.write(content)

print('Argumentos do Store.create() corrigidos!')
