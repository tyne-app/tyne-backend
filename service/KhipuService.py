from khipupy import Khipupy

from configuration.Settings import Settings
from dto.internal.KhipuResponse import KhipuResponse


class KhipuService:
    _settings_ = Settings()

    def create_link(self, amount: int, payer_email: str):
        api = Khipupy(receiver_id=self._settings_.KHIPU_RECEIVER_ID, secret=self._settings_.KHIPU_SECRET_ID)

        result = api.payments({
            'subject': 'Asunto',
            'body': 'Descripcion',
            'amount': str(amount),
            'payer_email': payer_email,
            'bank_id': '',
            'transaction_id': 'T-1000',
            'custom': '',
            'notify_url': self._settings_.KHIPU_NOTIFY_URL,
            'return_url': self._settings_.KHIPU_RETURN_URL,
            'cancel_url': self._settings_.KHIPU_CANCEL_URL,
            'picture_url': self._settings_.KHIPU_PICTURE_URL,
            'currency': 'CLP'
        })

        response = KhipuResponse(payment_id=result["response"].get("payment_id"),
                                 url=result["response"].get("payment_url"), status=result["status"])

        return response
