from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from projects.models import Project
from user.mixins import AccessMixinView
from user.models import User
from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from payments.models import CustomerModel
import stripe

class ProjectPaymentPage(AccessMixinView):
    only_role = "Employer"

    def get(self, request,id):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        project= get_object_or_404(Project,id=id)
        user=request.user
        # customer =stripe.Customer.create(
        #     email=request.user.email,
        #         name=user.display_name,
        #         metadata={"email":user.email,"userId":user.id,"username":user.username}
        #         )
        # CustomerModel.objects.create(user=request.user,stripe_customer_id=customer["id"])
        context={"project":project}
        customer = user.stripe_customer
        if not project.employer_payment_status == "Paid":
            intent = stripe.PaymentIntent.create(
                    amount=int(project.price) *100,
                    currency='usd',
                    payment_method_types=['card'],
                    customer=customer.stripe_customer_id,
                    metadata={
                        'userId':request.user.id,
                        'productId':project.id,
                        'type':'project_payment'
                        },
                    receipt_email="fanime492@gmail.com"
                    )
            context['client_secret']=intent.client_secret
        return render(request, "payments/employer/ProjectPayment.html", context)



class ProjectPaymentIntentAPI(APIView):

    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        pk =request.data.get("project_id")
        project= get_object_or_404(Project,id=pk)
        customer = request.user.stripe_customer
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(project.price) *100,
                currency='usd',
                payment_method_types=['card'],
                customer=customer.stripe_customer_id,
                metadata={'userId':request.user.id,'productId':project.id},
                receipt_email="fanime492@gmail.com"
                )
            return Response({"paymentIntent":intent})

        except Exception as e:
            return Response({"error":str(e)},status=HTTP_400_BAD_REQUEST)




