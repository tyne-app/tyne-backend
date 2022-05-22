import os
import smtplib, ssl
from jinja2 import Environment, FileSystemLoader, Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.util.EmailSubject import EmailSubject
from loguru import logger
from src.util.Constants import Constants
from src.configuration.Settings import Settings


class EmailService:
    _HOST: str = Settings.EMAIL_HOST
    _PORT: int = Settings.EMAIL_PORT
    _PASSWORD: str = Settings.EMAIL_PASSWORD
    _SENDER_EMAIL: str = Settings.EMAIL_USERNAME
    _ENCODING: str = Settings.EMAIL_ENCODING
    _READ: str = 'r'

    def send_email(self, user: str, subject: str, receiver_email: str, data=None) -> None:
        logger.info('Subject: {}, receiver_email: {}, data: {}', subject, receiver_email, data)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self._HOST, self._PORT, context=context) as server:

            template_name: str = self._get_template_name(user=user, subject=subject)
            template: Template = self._get_template(user=user, template_name=template_name)
            body_message: str = template.render(data=data)

            message: MIMEMultipart = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self._SENDER_EMAIL
            message["To"] = receiver_email
            logger.info("Detail message done")

            message_template = MIMEText(body_message, "html")

            message.attach(message_template)
            logger.info("Message attach done")

            try:
                server.login(self._SENDER_EMAIL, self._PASSWORD)
                server.sendmail(self._SENDER_EMAIL, receiver_email, message.as_string())
                logger.info("Email sent!")
            except Exception as e:
                logger.error("Error sending email: {}", e)

    def _get_template(self, user: str, template_name: str) -> Template:
        logger.info('user: {}, template_name: {}', user, template_name)
        env: Environment = Environment(loader=FileSystemLoader(os.path.abspath('src/util/email_template/%s' % user)))
        logger.info('env template: {}', env)
        template: Template = env.get_template(template_name)
        logger.info('template: {}', template)
        return template

    def _get_template_name(self, user: str, subject: str) -> str:
        # TODO: Agregar los demás casos para todos los match
        if user is Constants.CLIENT:
            match subject:
                case EmailSubject.CLIENT_WELCOME:
                    return 'welcome.html'
                case EmailSubject.SUCCESSFUL_PAYMENT:
                    return 'successful_payment.html'
                case EmailSubject.LOCAL_NO_CONFIRMATION_TO_CLIENT:
                    return 'local_no_confirmation.html'
                case EmailSubject.CANCELLATION_BY_LOCAL:
                    return 'cancellation_by_local.html'
                case EmailSubject.CONFIRMATION_TO_CLIENT:
                    return 'confirmation.html'
                case EmailSubject.REMINDER_TO_CLIENT:
                    return 'reminder.html'
                case EmailSubject.REFUND_CANCELLATION:
                    return 'refund_cancellation.html'

        if user is Constants.BRANCH:
            match subject:
                case EmailSubject.LOCAL_WELCOME:
                    return 'welcome.html'
                case EmailSubject.LOCAL_NO_CONFIRMATION_TO_LOCAL:
                    return 'local_no_confirmation.html'
                case EmailSubject.REMINDER_TO_LOCAL:
                    return 'reminder.html'
                case EmailSubject.CANCELLATION_BY_CLIENT:
                    return 'cancellation_by_client.html'
                case EmailSubject.CONFIRMATION_TO_LOCAL:
                    return 'confirmation.html'
                case EmailSubject.REFUND_CANCELLATION_TO_BRANCH:
                    return 'refund_by_client.html'

        if user is Constants.USER:
            match subject:
                case EmailSubject.FORGOTTEN_PASSWORD:
                    return 'forgotten_password.html'
                case EmailSubject.RETRY_ACTIVATION:
                    return 'retry_activation.html'
