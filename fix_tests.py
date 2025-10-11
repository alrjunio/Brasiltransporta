import os
import re

# Corrigir Store.create nos testes
def fix_store_create(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Adicionar cnpj nos Store.create
    pattern = r'Store\.create\(([^)]+)\)'
    replacement = r'Store.create(\1, cnpj="12.345.678/0001-90")'
    content = re.sub(pattern, replacement, content)
    
    with open(filepath, 'w') as f:
        f.write(content)

# Corrigir JWTService nos testes  
def fix_jwt_service(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Adicionar secret_key no JWTService
    content = content.replace('JWTService()', 'JWTService(secret_key="test-key")')
    
    with open(filepath, 'w') as f:
        f.write(content)

# Aplicar correções
for root, dirs, files in os.walk('tests'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            fix_store_create(filepath)
            fix_jwt_service(filepath)

print("Testes corrigidos!")
