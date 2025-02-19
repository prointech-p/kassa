import os
from dotenv import load_dotenv
import requests


PAYKASSA_CURRENCIES = ["BTC", "ETH", "LTC", "DOGE", "DASH", "BCH", "ETC", "XRP", "TRX", "XLM", 
                       "BNB", "USDT", "BUSD", "USDC", "ADA", "EOS", "SHIB"]


load_dotenv()  # Загружает переменные из .env

PAYKASSA_SCI_ID = os.environ.get('PAYKASSA_SCI_ID', 'ID123456')
PAYKASSA_SCI_KEY = os.environ.get('PAYKASSA_SCI_KEY', 'KEY123456')
PAYKASSA_DOMAIN = os.environ.get('PAYKASSA_DOMAIN', 'DOMAIN123456')


class PayKassa:
    SCI_URL = 'https://paykassa.app/sci/0.4/index.php'

    def __init__(self, sci_id, sci_key, domain, test=False):
        self.sci_id = sci_id
        self.sci_key = sci_key
        self.domain = domain
        self.test = 'true' if test else 'false'

    def sci_create_order(self, order_id, amount, currency, system, comment="", phone="false", paid_commission="shop"):
        """
        Creates a deposit payment link for the user.
        :param order_id: Unique payment ID in your system
        :param amount: Amount to be received
        :param currency: Currency (e.g., USD, RUB, BTC, etc.)
        :param system: ID of the payment system (e.g., 11 for BTC, 12 for ETH)
        :param comment: Optional comment for transaction history
        :param phone: Must be "false" (required by PayKassa)
        :param paid_commission: Who pays the commission (default: "shop")
        :return: JSON response with payment link
        """
        return self.make_request({
            'func': 'sci_create_order',
            'order_id': order_id,
            'amount': amount,
            'currency': currency,
            'system': system,
            'comment': comment,
            'phone': phone,
            'paid_commission': paid_commission
        })

    def sci_confirm_order(self, private_hash):
        """
        Confirms an incoming payment.
        :param private_hash: The hash received in the IPN request
        :return: JSON response with payment confirmation status
        """
        return self.make_request({
            'func': 'sci_confirm_order',
            'private_hash': private_hash
        })

    def make_request(self, params):
        """
        Sends a request to PayKassa API.
        :param params: Dictionary with request parameters
        :return: JSON response from the API
        """
        fields = {
            'sci_id': self.sci_id,
            'sci_key': self.sci_key,
            'domain': self.domain,
            'test': self.test
        }
        fields.update(params)

        try:
            response = requests.post(self.SCI_URL, data=fields, headers={'Content-Type': 'application/x-www-form-urlencoded'})
            response.raise_for_status()  # Raise error if response is not 200
            return response.json()  # Convert response to JSON
        except requests.RequestException as e:
            return {'error': str(e)}