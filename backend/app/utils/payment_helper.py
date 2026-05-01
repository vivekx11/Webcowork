"""
Payment processing helper (Stripe integration)
"""
import os
import stripe

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

class PaymentHelper:
    """Helper class for payment processing"""
    
    @staticmethod
    def create_payment_intent(amount, currency='usd', metadata=None):
        """
        Create a Stripe payment intent
        
        Args:
            amount: Amount in cents (e.g., 1000 for $10.00)
            currency: Currency code (default: 'usd')
            metadata: Additional metadata dictionary
        
        Returns:
            dict: Payment intent response
        """
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency=currency,
                metadata=metadata or {},
                automatic_payment_methods={'enabled': True}
            )
            
            return {
                'success': True,
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def confirm_payment(payment_intent_id):
        """
        Confirm a payment intent
        
        Args:
            payment_intent_id: Stripe payment intent ID
        
        Returns:
            dict: Confirmation response
        """
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            return {
                'success': True,
                'status': intent.status,
                'amount': intent.amount / 100,  # Convert from cents
                'currency': intent.currency
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def refund_payment(payment_intent_id, amount=None):
        """
        Refund a payment
        
        Args:
            payment_intent_id: Stripe payment intent ID
            amount: Amount to refund in cents (None for full refund)
        
        Returns:
            dict: Refund response
        """
        try:
            refund_data = {'payment_intent': payment_intent_id}
            if amount:
                refund_data['amount'] = int(amount * 100)
            
            refund = stripe.Refund.create(**refund_data)
            
            return {
                'success': True,
                'refund_id': refund.id,
                'status': refund.status,
                'amount': refund.amount / 100
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }

# Create a singleton instance
payment_helper = PaymentHelper()
