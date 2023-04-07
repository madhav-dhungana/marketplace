from email import message
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from projects.models import Project
from ..models import TransactionModel
from user.mixins import AccessMixinView
from user.models import User
from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from payments.models import ConnectedFreelancer,DepositModel
import stripe

class FreelancerPayment(AccessMixinView):
    only_role = "Freelancer"
    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        user=request.user
        
        #create account in stripe if not
        if not hasattr(user, 'stripe_connect_account'):
            acnt = stripe.Account.create(
                type="express",
                country="US",
                email=user.email,
                metadata={
                    "user_id":request.user.id,
                    "username":request.user.username
                })
            ConnectedFreelancer.objects.create(user=request.user,stripe_account_id=acnt["id"])
        connected_account = request.user.stripe_connect_account
        stripe_balance = stripe.Balance.retrieve(stripe_account=connected_account.stripe_account_id)
        context = {
            "connected_account":connected_account,
            "stripe_balance":stripe_balance,
            "available":(stripe_balance["available"][0]["amount"])/100,
            "pending":(stripe_balance["pending"][0]["amount"])/100,
            "instant_available":(stripe_balance["instant_available"][0]["amount"])/100,
        }
        return render(request, "payments/freelancer/payments.html", context)


def OnBoardUser(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user = request.user.stripe_connect_account
    domain =request.scheme+'://'+request.get_host()

    link =stripe.AccountLink.create(
        account=user.stripe_account_id,
        refresh_url=f"{domain}/payments/",
        return_url=f"{domain}/payments/",
        type="account_onboarding",
        )

    return HttpResponseRedirect(link["url"])
  
class WithdrawMoney(APIView):
    def post(self,request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        connected_account = request.user.stripe_connect_account
        withdraw_amount = int(request.POST.get("withdraw_amount"))
        try:
            payout = stripe.Payout.create(
                amount=withdraw_amount*100,
                currency='usd',
                stripe_account=connected_account.stripe_account_id,
                metadata={
                    "userId":request.user.id
                }
                )
            return Response({"detail":"Payout was successful."})
        except Exception as e:
            return Response({"detail":str(e)},status=HTTP_400_BAD_REQUEST)
            
    
class FreelancerInvoices(AccessMixinView):
    only_role = "Freelancer"

    def get(self,request):
        context={}
        return render(request, "payments/freelancer/freelancer_invoices.html", context)


class FreelancerTranscation(AccessMixinView):
    only_role = "Freelancer"

    def get(self,request):
        context={}
        return render(request, "payments/freelancer/transaction_history.html", context)

