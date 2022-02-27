import time
from datetime import time
from loguru import logger
from khipupy import Khipupy
from starlette import status
from pykhipu.client import Client as KhipuClient
from src.configuration.Settings import Settings
from src.dto.internal.KhipuResponse import KhipuResponse
from src.exception.exceptions import CustomError


class KhipuService:
    _settings_ = Settings()

    def create_link(self, amount: int, payer_email: str, transaction_id: str):
        api = Khipupy(receiver_id=self._settings_.KHIPU_RECEIVER_ID, secret=self._settings_.KHIPU_SECRET_ID)

        # d = (datetime.now() + timedelta(minutes=30)).replace(microsecond=0).timestamp()

        result = api.payments({
            'subject': 'Pago de reserva - Tyne',
            'body': 'Descripcion',
            'amount': str(amount),
            'payer_email': payer_email,
            'bank_id': '',
            'transaction_id': transaction_id,
            'custom': '',
            # 'notify_url': 'http://localhost:4200/estado-pago/exitoso',#self._settings_.KHIPU_NOTIFY_URL,
            'return_url': 'http://localhost:4200/estado-pago/exitoso', #self._settings_.KHIPU_RETURN_URL,
            'cancel_url': 'http://localhost:4200/estado-pago/cancelado',#self._settings_.KHIPU_CANCEL_URL,
            'picture_url': self._settings_.KHIPU_PICTURE_URL,
            'currency': 'CLP',
            'notify_api_version': '1.3'
        })
        # 'expires_date': str((datetime.now() + timedelta(minutes=30)).isoformat())
        logger.info("result: {}", result)

        response = KhipuResponse(payment_id=result["response"].get("payment_id"),
                                 url=result["response"].get("payment_url"), status=result["status"])
        logger.info("response: {}", response.__dict__)
        return response

    def verify_payment(self, payment_id: str):
        try:
            for x in range(3):  # TODO: Analizar más esta lógica para refactorizarla
                khipu_client = KhipuClient(receiver_id=self._settings_.KHIPU_RECEIVER_ID, secret=self._settings_.KHIPU_SECRET_ID)
                payment = khipu_client.payments.get_id(id=payment_id)

                print(payment.status)

                if payment.status == "done":
                    return payment
                elif payment.status == "pending":
                    raise CustomError(name="Pago aún está pendiente",
                                      detail="Pago aún está pendiente",
                                      status_code=status.HTTP_400_BAD_REQUEST)

                time.sleep(10)

        except CustomError as ex:
            raise ex
        except Exception:
            raise CustomError(name="Pago no encontrado",
                              detail="El pago no fue encontrado",
                              status_code=status.HTTP_400_BAD_REQUEST)
