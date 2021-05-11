import stripe

from miniblog import settings
from miniblog.settings import STRIPE_PRICE_ID


class Stripe:
    domain_url = 'https://8175bda9da0b.ngrok.io/payments/'
    stripe.api_key = settings.STRIPE_SECRET_KEY

    def __init__(self, user=None):
        self.user = user

    @staticmethod
    def stripe_api():
        return stripe.api_key

    def get_success_url_domain(self):
        return self.domain_url + 'success?session_id={CHECKOUT_SESSION_ID}'

    def get_cancel_url_domain(self):
        return self.domain_url + 'cancelled/'

    def create_session(self):
        try:
            subscription_data = {
                'items': [{
                    'plan': STRIPE_PRICE_ID
                }]
            }
            session = stripe.checkout.Session.create(
                client_reference_id=self.user,
                success_url=self.get_success_url_domain(),
                cancel_url=self.get_cancel_url_domain(),
                payment_method_types=['card'],
                mode='subscription',
                customer=self.user.memberaccount.customer_id,
                subscription_data=subscription_data,
            )
            return session.id
        except Exception as e:
            print(e)
            return None
