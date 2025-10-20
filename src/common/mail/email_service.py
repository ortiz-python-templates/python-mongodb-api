from typing import Dict
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from src.common.config.env_config import EnvConfig
from src.common.config.template_config import TemplateConfig


class EmailService:

    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=EnvConfig.MAIL_USERNAME,
            MAIL_PASSWORD=EnvConfig.MAIL_PASSWORD,
            MAIL_FROM=EnvConfig.MAIL_FROM,
            MAIL_PORT=EnvConfig.MAIL_PORT,
            MAIL_SERVER=EnvConfig.MAIL_SERVER,
            MAIL_STARTTLS=True, 
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )

    async def send_email(self, subject: str, email_to: str, template_name: str, context: Dict):
        html = TemplateConfig.templates.get_template(template_name).render(context)
        
        message = MessageSchema(
            subject=subject,
            recipients=[email_to],
            body=html,
            subtype="html"
        )
        try:
            await FastMail(self.conf).send_message(message)
        except Exception as e:
            print(f"Error while sending email: {str(e)}")

         
