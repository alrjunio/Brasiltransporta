class DomainError(Exception):
    """Base para todos os erros de domínio"""
    pass

class ValidationError(DomainError):
    """Erro de validação de domínio / aplicação."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)