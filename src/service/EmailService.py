import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.util.EmailSubject import EmailSubject
from loguru import logger
from src.util.Constants import Constants
from src.configuration.Settings import Settings


class EmailService:
    __PORT: int = Settings.PORT_EMAIL
    __PASSWORD: str = Settings.PASSWORD_EMAIL
    __SENDER_EMAIL: str = Settings.SENDER_EMAIL
    __ENCODING: str = Settings.ENCODING_EMAIL
    __READ: str = 'r'

    def send_email(self, user: str, subject: str, receiver_email: str) -> None:
        logger.info('Subject: {}, receiver_email: {}, user: {}', subject, receiver_email, user)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", self.__PORT, context=context) as server:

            template_name: str = self._get_template_name(user=user, subject=subject)
            template: str = self._read_email_template(user=user, template_name=template_name)
            logger.info("template: {}", template)

            plain_text: str = "Texto plano de prueba para ver si funciona" # TODO: Reemplazarlo con la alternativa oficial por cada template

            message: MIMEMultipart = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.__SENDER_EMAIL
            message["To"] = receiver_email
            logger.info("Detail message done")

            alternative_message = MIMEText(plain_text, "plain")
            main_message = MIMEText(template, "html")

            message.attach(alternative_message)
            message.attach(main_message)
            logger.info("Message attach done")

            server.login(self.__SENDER_EMAIL, self.__PASSWORD)
            server.sendmail(self.__SENDER_EMAIL, receiver_email, message.as_string())
            logger.info("Email sent!")

    def _read_email_template(self, user: str, template_name: str) -> str:
        logger.info('user: {}, template_name: {}', user, template_name)

        template_path: str = os.path.abspath('src/util/email_template/%s/%s' % (user, template_name))
        logger.info('template_path: {}', template_path)

        with open(template_path, self.__READ, encoding=self.__ENCODING) as file:
            return file.read()

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

        if user is Constants.BRANCH:
            match subject:
                case EmailSubject.LOCAL_WELCOME:
                    return 'welcome.html'
                case EmailSubject.LOCAL_NO_CONFIRMATION_TO_LOCAL:
                    return 'local_no_confirmation.html'
                case EmailSubject.REMINDER_TO_LOCAL:
                    return 'reminder.html'

        if user is Constants.USER:
            return 'forgotten_password.html'
