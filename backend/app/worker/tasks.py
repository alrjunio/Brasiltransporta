from app.worker.celery_app import celery_app

@celery_app.task
def process_image_upload(image_path: str):
    """Task para processar upload de imagens"""
    # Implementar processamento de imagem
    return f"Processed image: {image_path}"

@celery_app.task
def send_notification(email: str, message: str):
    """Task para enviar notificações"""
    # Implementar envio de email
    return f"Notification sent to {email}"