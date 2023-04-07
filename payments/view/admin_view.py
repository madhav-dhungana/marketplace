from importlib.metadata import metadata
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from projects.models import Project
from user.mixins import AdminOnlyView, PaginateView
from ..models import DepositModel, FeeModel, TaxModel, TransactionModel
from rest_framework.response import Response
from user.api.permissions import IsBatuwaAdminOnly

import stripe


class TransactionPage(AdminOnlyView):
    def get(self, request):
        user = request.user
        transactions = TransactionModel.objects.all()
        res = PaginateView()
        page = self.request.GET.get("page")
        response = res.give_paginated_response(page, transactions, 10)
        context = {"page_obj": response}
        return render(request, "payments/admin/transaction_list.html", context)


class TaxPage(AdminOnlyView):
    def get(self, request):
        taxes = TaxModel.objects.all()
        context = {"page_obj": taxes}
        return render(request, "payments/admin/tax_list.html", context)


class FeePage(AdminOnlyView):
    def get(self, request):
        fees = FeeModel.objects.all()
        context = {"page_obj": fees}
        return render(request, "payments/admin/fee_list.html", context)


class DepositPage(AdminOnlyView):
    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        deposits = DepositModel.objects.all()
        res = PaginateView()
        page = self.request.GET.get("page")
        response = res.give_paginated_response(page, deposits, 10)
        context = {"page_obj": response}
        return render(request, "payments/admin/deposit_list.html", context)


class ReleaseMoneyAPI(APIView):
    permission_classes=[IsBatuwaAdminOnly]

    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        data = request.data
        project = get_object_or_404(Project, id=data.get("project_id"))
        deposited = DepositModel.objects.get(for_project=project)

        if  deposited.can_release ==False:
            raise APIException("Payment Release condition not satisfied !")

        for_user = project.hired
        connected_account = for_user.stripe_connect_account
        amount = int(deposited.transaction.price) * 100
        
        try:
            transfer = stripe.Transfer.create(
                amount=amount,
                currency="usd",
                destination=connected_account.stripe_account_id,
                transfer_group=f"{for_user.username}_transfer",
                metadata={
                    "send_to": for_user.id,
                    "deposit_id": deposited.id,
                    "send_by": request.user.id,
                },
            )
            return Response(
                {
                    "deposit_id": deposited.id,
                    "detail": "Successful released money to freelancer {for_user}.",
                    "transfer": transfer,
                    "amount": deposited.transaction.price,
                    "type": "release",
                }
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=HTTP_400_BAD_REQUEST)

class RefundMoneyAPI(APIView):
    """
    Refund money back to customer (eg. when project is cancelled)
    """
    permission_classes=[IsBatuwaAdminOnly]

    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        data = request.data
        s_id = data.get("stripe_transaction_id")
        deposit_id = data.get("deposit_id")
        get_object_or_404(TransactionModel, stripe_transaction_id=s_id)
        deposited = DepositModel.objects.get(id=deposit_id)

        if  deposited.can_refund == False:
            raise APIException("Payment Refund condition not satisfied !")
      
        try:
            refund = stripe.Refund.create(
                payment_intent=s_id,
                metadata={
                    "refund_to": deposited.user.id,
                    "deposit_id": deposited.id,
                    "send_by": request.user.id,
                },
            )
            return Response(
                {
                    "deposit_id": deposited.id,
                    "type": "refund",
                    "detail": f"Successful refunded money to {deposited.user}.",
                    "refund": refund,
                    "amount": deposited.transaction.price,
                }
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=HTTP_400_BAD_REQUEST)
