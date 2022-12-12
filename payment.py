import stripe
import os

stripe_keys = {
    'secret_key': os.environ.get('STRIPE_SECRET_KEY'),
    'publishable_key': os.environ.get('STRIPE_PUBLISHABLE_KEY')
}


class PaymentAPI:
    def __init__(self):
        stripe.api_key = stripe_keys['secret_key']

    def process(self, tier, email):
        # get Stripe customer info
        customer = self.get_customer_info(email)

        # get payment tier
        amount = self.get_payment_tier(tier)

        # create a Stripe Charge
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='OpenAI API subscription'
        )

        return charge.status

    def get_payment_tier(self, tier):
        if tier == 1:
            return 50
        elif tier == 2:
            return 100
        elif tier == 3:
            return 200
        else:
            return 0

    def get_customer_info(self, email):
        # if customer exists, retrieve customer info, else create customer
        try:
            customer = stripe.Customer.retrieve(email)
        except stripe.error.InvalidRequestError:
            customer = stripe.Customer.create(
                email=email
            )

        return customer
