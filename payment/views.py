from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView

from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from product.models import Product

import stripe

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'payment/home.html'

class SuccessView(TemplateView):
    template_name = 'payment/success.html'

class CancelledView(TemplateView):
    template_name = 'payment/cancelled.html'


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
@login_required
def create_checkout_session(request, product_pk):
    
    product = get_object_or_404(Product, pk=product_pk)

    if request.method == 'GET':
        domain_url = 'http://127.0.0.1:8000/payment/'
        stripe.api_key = settings.STRIPE_SECRET_KEY

        if not product.is_reserved and not product.is_sold:
            try:
                checkout_session = stripe.checkout.Session.create(
                    client_reference_id=product.pk if request.user.is_authenticated else None,
                    success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=domain_url + 'cancelled/',
                    payment_method_types=['card'],
                    mode='payment',
                    line_items=[{
                        "price_data": {
                            "currency": 'usd',
                            "product_data": { "name": product.name,},
                            "unit_amount": int(product.price * 100),
                        },
                        "quantity": 1,
                    }]
                )
                # reserve the product
                product.reserve(request.user)
                print('Product is reserved')

                return JsonResponse({'sessionId': checkout_session['id']})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'error': 'Product is already sold or reserved by another customer. Please refresh your page!'})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")

        # Get the Checkout session ID from the event
        session_id = event['data']['object']['id']

        # Find the product associated with this session
        
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        product_pk = checkout_session.get('client_reference_id')
        
        if product_pk:
            # Mark the product as sold here
            product = Product.objects.get(pk=product_pk)
            product.is_reserved = False
            product.is_sold = True
            product.save()
            print("Product marked as sold.")
            print('Sold', product.is_sold)
            print('Reserved', product.is_reserved)

    return HttpResponse(status=200)

