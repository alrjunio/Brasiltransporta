with open('brasiltransporta/application/advertisements/use_cases/create_advertisement.py', 'r') as f:
    content = f.read()

# Remove os comentários das validações
content = content.replace('# store = self._stores.get_by_id(inp.store_id) if self._stores else None', 'store = self._stores.get_by_id(inp.store_id) if self._stores else None')
content = content.replace('# if store is None:', 'if store is None:')
content = content.replace('#     raise ValidationError(\"Loja não encontrada\")', '    raise ValidationError(\"Loja não encontrada\")')
content = content.replace('# vehicle = self._vehicles.get_by_id(inp.vehicle_id) if self._vehicles else None', 'vehicle = self._vehicles.get_by_id(inp.vehicle_id) if self._vehicles else None')
content = content.replace('# if vehicle is None:', 'if vehicle is None:')
content = content.replace('#     raise ValidationError(\"Veículo não encontrado\")', '    raise ValidationError(\"Veículo não encontrado\")')

with open('brasiltransporta/application/advertisements/use_cases/create_advertisement.py', 'w') as f:
    f.write(content)

print('Validações ativadas no use case!')
