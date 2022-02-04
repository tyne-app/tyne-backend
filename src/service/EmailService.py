import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.util.EmailSubject import EmailSubject
from loguru import logger
from src.util.Constants import Constants

class EmailService:
    port: int = 465
    password: str = "Tyneserarentable2022"
    sender_email: str = "tyne2023@gmail.com"
    READ: str = 'r'
    ENCODING: str = 'utf-8'

    def send_email(self, user: str, subject: str, receiver_email: str) -> None:
        logger.info('Subject: {}, receiver_email: {}, user: {}', subject, receiver_email, user)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=context) as server:

            template_name: str = self.get_template_name(user=user, subject=subject)
            template: str = self.read_email_template(user=user, template_name=template_name)

            plain_text: str = "Texto plano de prueba para ver si funciona" # TODO: Reemplazarlo con la alternativa oficial por cada template

            message: MIMEMultipart = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = receiver_email

            alternative_message = MIMEText(plain_text, "plain")
            main_message = MIMEText(template, "html")

            message.attach(alternative_message)
            message.attach(main_message)

            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, message.as_string())

    def read_email_template(self, user: str, template_name: str) -> str:
        logger.info('user: {}, template_name: {}', user, template_name)

        template_path: str = os.path.abspath('src/util/email_template/%s/%s' % (user, template_name))
        logger.info('template_path: {}', template_path)

        with open(template_path, self.READ, encoding=self.ENCODING) as file:
            return file.read()

    def get_template_name(self, user: str, subject: str) -> str:
        # TODO: Agregar los demás casos para todos los match
        if user is Constants.CLIENT:
            match subject:
                case EmailSubject.CLIENT_WELCOME:
                    return 'welcome.html'

        if user is Constants.LOCAL:
            match subject:
                case EmailSubject.LOCAL_WELCOME:
                    return 'welcome.html'

        if user is Constants.USER:
            return 'forgotten_password.html'
