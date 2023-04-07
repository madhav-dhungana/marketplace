from django.urls import path

from .view.admin_view import *
from .view.employer_view import *
from .view.freelancer_view import *
from .view.webhook_view import my_webhook_view

freelancer_urls = [
   path('',FreelancerPayment.as_view(), name='freelancer_payment'),
   path('my-transaction/',FreelancerTranscation.as_view(), name='freelancer_transaction'),
   path('my-invoices/',FreelancerInvoices.as_view(), name='freelancer_invoices'),
   path('connect-account/',OnBoardUser, name='connect_account'),
   path('withdraw-money/',WithdrawMoney.as_view(), name='withdraw_money'),
   path('webhook-stripe/',my_webhook_view ,name="webhook"),  
]


employer_urls = [
   path('project-payment/<int:id>/',ProjectPaymentPage.as_view() , name="project_payment"),
   path('project-payment-intent/',ProjectPaymentIntentAPI.as_view() , name="project_payment_intent")
]


admin_urls =[
      path('transactions/',TransactionPage.as_view() , name="transactions"),
      path('deposits/',DepositPage.as_view() , name="deposits"),
      path('fee-list/',FeePage.as_view() , name="fee_list"),
      path('tax-list/',TaxPage.as_view() , name="tax_list"),
      path('release-money/',ReleaseMoneyAPI.as_view() , name="release_money"),
      path('refund-money/',RefundMoneyAPI.as_view() , name="refund_money"),

]

urlpatterns =freelancer_urls+employer_urls+admin_urls