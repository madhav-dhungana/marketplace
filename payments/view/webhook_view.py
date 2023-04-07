
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from ..models import TransactionModel
from payments.models import ConnectedFreelancer,DepositModel
from django.shortcuts import get_object_or_404, render
from user.models import User
from projects.models import Project


@csrf_exempt
def my_webhook_view(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, 'whsec_fba0ade10d1959bc13305ec0e97d3f2939ff47642fe7718eecc5264e3a68e890'
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == "account.updated":
        obj = event.data.object
        if obj["charges_enabled"] and obj["payouts_enabled"]:
            acnt =ConnectedFreelancer.objects.get(stripe_account_id=obj["id"])
            acnt.enabled = True
            acnt.save()
    
    
    if event['type'] == "payment_intent.succeeded":
        obj = event.data.object
        # print('obj is ',obj)
        if obj["status"]=="succeeded":
            project_id = obj.metadata.productId
            userId = obj.metadata.userId
            intent_type = obj.metadata.type
            project = get_object_or_404(Project,id=project_id)
            user = get_object_or_404(User,id=userId)
            project.employer_payment_status="Paid"
            project.status="Active"
            project.save()
            transaction = TransactionModel.objects.create(
                type="Payment",
                price=obj["amount_received"]/100,
                stripe_transaction_id=obj["id"],
                transaction_by=user,
                status="success"
                )
            print("inten",obj)
            if intent_type == "project_payment":
                DepositModel.objects.create(user=user,for_project=project,transaction=transaction)

        
         
        
    if event['type'] == "transfer.created":
        obj = event.data.object
        deposit_id = obj.metadata.deposit_id
        send_by_id = obj.metadata.send_by
        send_by = get_object_or_404(User,id=send_by_id)
        deposit_model = get_object_or_404(DepositModel,id=deposit_id)
        deposit_model.status = "Released"
        deposit_model.save()
        deposit_model.notify.create(
            action_to=deposit_model.for_project.hired,
            action="released",
            title=f"${deposit_model.transaction.price} is transferred to your stripe account.",
        )
        transaction = TransactionModel.objects.create(
                type="Transfer",
                price=obj["amount"]/100,
                stripe_transaction_id=obj["id"],
                transaction_by=send_by,
                status="success"
                )
                
    if event['type'] == "charge.refunded":
        obj = event.data.object
        refund_to_id = obj.metadata.userId
        refund_to = get_object_or_404(User,id=refund_to_id)
        deposit = DepositModel.objects.filter(transaction__stripe_transaction_id=obj["payment_intent"]).first()
        deposit.status ="Refunded"
        deposit.save()
        deposit.for_project.employer_payment_status="Refunded"
        deposit.for_project.status="CAN" #cancel project once refunded
        deposit.for_project.save()
        deposit.notify.create(
            action_to=deposit.user,
            action="refunded",
            title=f"${deposit.transaction.price} is refunded to your account.",
        )

    if event['type'] == "payout.paid":
        obj = event.data.object
        user_id = obj.metadata.userId
        user = get_object_or_404(User,id=user_id)
        transaction = TransactionModel.objects.create(
                type="Withdraw",
                price=obj["amount"]/100,
                stripe_transaction_id=obj["id"],
                transaction_by=user,
                status="success"
                )
        

    return HttpResponse(status=200)
