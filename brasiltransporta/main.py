try:
    # usa o app já criado se existir
    from brasiltransporta.presentation.api.app import app  # type: ignore
except Exception:
    # fallback: cria a app
    from brasiltransporta.presentation.api.app import create_app  # type: ignore
    app = create_app()
