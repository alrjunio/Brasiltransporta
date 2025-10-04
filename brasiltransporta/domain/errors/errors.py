class DomainError(Exception):
    ...
class ValidationError(DomainError): 
    ...
class ValidationError(Exception):
    """Erro de validação de domínio / aplicação."""
    pass
