import stripe

from miniblog import settings
from miniblog.settings import STRIPE_PRICE_ID, ALLOWED_HOSTS


class Stripe:
    domain_url = 'https://' + ALLOWED_HOSTS[-1] + '/payments/'
    stripe.api_key = settings.STRIPE_SECRET_KEY

    def __init__(self, user=None):
        self.user = user

    @staticmethod
    def stripe_api():
        return stripe

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

    def create_source(self, token, ):
        cus_id = self.user.memberaccount.customer_id
        customer = stripe.Customer.retrieve(cus_id)

        old_card = stripe.Customer.list_sources(cus_id, object='card').get('data')[0]
        card = customer.create_source(self.user.memberaccount.customer_id, source=token.get('id'))

        customer.default_source = card.id
        customer.save()

        self.user.memberaccount.card_id = card.last4
        self.user.memberaccount.save()

        self.delete_source(old_card)

    def update_source(self, card, name=''):
        stripe.Customer.modify_source(
            self.user.memberaccount.customer_id,
            card.id,
            name=name,
        )
        self.user.memberaccount.card_id = card.last4
        self.user.memberaccount.save()

    def delete_source(self, card):
        stripe.Customer.delete_source(
            self.user.memberaccount.customer_id,
            card.id,
        )
