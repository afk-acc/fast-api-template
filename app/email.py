from fastapi_mail import ConnectionConfig, MessageSchema, FastMail, MessageType
from starlette.background import BackgroundTasks

from app.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_email_async(subject: str, email_to: str, text: str, files: list = []):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=text,
        subtype=MessageType.html,
        # attachments=files
    )
    fm = FastMail(conf)
    await fm.send_message(message)


def send_email_background(
    background_tasks: BackgroundTasks,
    subject: str,
    email_to: str,
    text: str,
    files: list = [],
):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=text,
        subtype=MessageType.html,
        attachments=files,
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)
