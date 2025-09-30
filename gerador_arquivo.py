#!/usr/bin/env python3
"""
Script para criar o arquivo pytest.ini que faltou
Execute: python create_pytest_ini.py
"""

import os

def create_file(file_path, content):
    """Cria um arquivo com o conteúdo especificado"""
    # Verifica se o caminho tem diretórios
    dir_path = os.path.dirname(file_path)
    if dir_path:  # Só cria diretórios se o caminho não for vazio
        os.makedirs(dir_path, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Criado: {file_path}")

def main():
    print("🚀 Criando arquivo pytest.ini...")
    print("=" * 60)
    
    # PYTEST CONFIGURATION
    pytest_config = '''[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --strict-config
    --disable-warnings
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
'''

    # REQUIREMENTS FOR TESTS
    test_requirements = '''pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
httpx>=0.24.0
freezegun>=1.2.0
factory_boy>=3.2.0
Faker>=15.0.0
'''

    # Criar apenas os arquivos que faltaram
    files = [
        ("pytest.ini", pytest_config),
        ("requirements-test.txt", test_requirements),
    ]

    for file_path, content in files:
        create_file(file_path, content)

    print("\n" + "=" * 60)
    print(f"🎉 Arquivos criados com sucesso!")
    print("\n📁 ARQUIVOS CRIADOS:")
    print("  ├── pytest.ini")
    print("  └── requirements-test.txt")
    print("\n🔥 COMO EXECUTAR OS TESTES:")
    print("1. Instale as dependências de teste:")
    print("   pip install -r requirements-test.txt")
    print("\n2. Execute todos os testes:")
    print("   pytest")
    print("\n3. Execute testes com cobertura:")
    print("   pytest --cov=brasiltransporta")
    print("\n4. Execute testes específicos:")
    print("   pytest tests/domain/entities/test_advertisement.py -v")

if __name__ == "__main__":
    main()