class DomainError(Exception):
    """Base para todos os erros de domínio"""
    pass

class ValidationError(DomainError):
    """Erro de validação de domínio / aplicação."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        
class DomainError(Exception):
    """Base domain error"""
    pass

class ValidationError(DomainError):
    """Validation error"""
    pass

class SecurityAlertError(DomainError):
    """Security alert - potential token theft detected"""
    pass

# Adicione esta linha se SecurityAlertError não existir