from django.shortcuts import render, get_object_or_404,     reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms  import MakePaymentForm, DonateForm
from .models import DonateLineItem
from django.conf import settings 
from django.utils import timezone
from contrabutions.models import Donations
import stripe

stripe.api_key = settings.STRIPE_SECRET

@login_required()
def payment (request):
    if request.method=="POST":
        donate_form = DonateForm(request.POST)
        payment_form = MakePaymentForm(request.POST)
        
        if donate_form.is_valid() and payment_form.is_valid():
            donate = donate_form.save(commit=False)
            donate.full_name = request.user
            donate.date = timezone.now()
            donate.save()
            
            cart = request.session.get('cart', {})
            total = 0
            for id, amount in cart.items():
                donations = get_object_or_404(Donations, pk=id)
                total += amount * donations.donation
                donate_line_item = DonateLineItem(
                    full_name = donate,
                    donations = donations,
                    amount = amount
                )
            donate_line_item.save()
            
            try:
                customer = stripe.Charge.create(
                    amount = int(total * 100),
                    currency = "EUR",
                    description = request.user.email,
                    card = payment_form.cleaned_data['stripe_id'],
                )
            except stripe.error.CardError:
                messages.error(request, "Sorry, your car was Declined!")
                
            if customer.paid:
                messages.error(request, "You have successfully Paid!")
                request.session['cart'] = {}
                return redirect(reverse('donation'))
            else:
                messages.error(request, "Unable to take payment")
        else:
            print(donate_form.is_valid)
            print(payment_form.is_valid)
            print(payment_form.errors)
            messages.error(request, "We were unable to take payment with that card!")
    else:
        payment_form = MakePaymentForm()
        donate_form = DonateForm()
        
    return render(request, "payment.html", {'donate_form': donate_form, 'payment_form': payment_form, 'publishable': settings.STRIPE_PUBLISHABLE})