import time
from datetime import time
from loguru import logger
from starlette import status
from src.configuration.Settings import Settings
from src.dto.internal.MercadoPagoResponse import MercadoPagoResponse
from src.exception.exceptions import CustomError
import mercadopago


class MercadoPagoService:
    _settings_ = Settings()

    def create_link(self, amount: int, payer_email: str, transaction_id: str):
        api = mercadopago.SDK(self._settings_.MP_ACCESS_TOKEN)
        preference_data = {
            "items": [
                {
                    "title": "Pago de reserva - Tyne",
                    "quantity": 1,
                    "unit_price": int(amount),
                }
            ],
            "back_urls": {
                "success": self._settings_.MP_SUCCESS_URL,
                "failure": self._settings_.MP_REJECTED_URL,
            },
            "binary_mode": True,
            "auto_return": "approved",
            "payment_methods": {
                "installments": 3
            },
            "statement_descriptor": "Pago de reserva - Tyne",
            "external_reference": transaction_id
        }

        preference_response = api.preference().create(preference_data)
        logger.info("result preference_response Mercado Pago: {}", preference_response)

        # response = MercadoPagoResponse(payment_id=preference_response["response"].get("id"),
        #                               url=preference_response["response"].get("init_point"),
        #                               status=preference_response["status"])

        logger.info("result response Mercado Pago: {}", preference_response["response"])

        response = MercadoPagoResponse(payment_id=preference_response["response"].get("id"),
                                       url=preference_response["response"].get("sandbox_init_point"),
                                       status=preference_response["status"])
        return response

    def verify_payment(self, payment_id: str):
        try:
            api = mercadopago.SDK(self._settings_.MP_ACCESS_TOKEN)
            for x in range(3):  # TODO: Analizar más esta lógica para refactorizarla
                mp_payment = api.payment().get(payment_id)
                logger.info("payment: {}", mp_payment["response"])

                if mp_payment["response"].get("status") == "approved":
                    return mp_payment["response"]
                elif mp_payment["response"].get("status") == "pending":
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
