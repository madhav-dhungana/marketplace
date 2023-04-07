from django.db import models
from chat.models import BaseModel
from projects.models import Project
from user.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from notification.models import Notification
from django.core.validators import MaxValueValidator, MinValueValidator

class ConnectedFreelancer(BaseModel):
    """This will represent stripe connected account which links with django user model """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="stripe_connect_account")
    stripe_account_id = models.CharField( max_length=100,null=True)
    enabled = models.BooleanField(default=False) #check if account is authorized with stripe


class CustomerModel(BaseModel):
    """This will represent stripe customer account which links with django user model """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="stripe_customer")
    stripe_customer_id = models.CharField( max_length=100,null=True)

class TransactionModel(BaseModel):
    transaction_type = [
        ('Transfer','Transfer'),
        ('Withdraw','Withdraw'),
        ('Payment','Payment'),
        ('Refund','Refund'),
    ]
    transaction_status = [
       ( "success","success"),
       ( "rejected","rejected")
    ]
    price=models.FloatField(null=True)
    transaction_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    transaction_to = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name="transaction_to")
    stripe_transaction_id = models.CharField( max_length=100,null=True) #link stripe's id
    types = models.CharField(max_length=100, choices= transaction_type)
    status =models.CharField(max_length=100, choices= transaction_status)

    class Meta:
        ordering=['-id']




class DepositModel(BaseModel):

    """
    This stores the payment done by employer for a project
    using this admin will release/transfer money to freelancer stripe account
    This will also track if money is released or not
    """

    deposit_status = [
       ( "Released","Released"),
       ( "On Hold","On Hold"),
       ("Refunded","Refunded")
    ]
    transaction = models.OneToOneField(TransactionModel, on_delete=models.CASCADE, related_name="transaction")
    status =models.CharField(max_length=100, choices= deposit_status,default="On Hold")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name="my_deposits")
    for_project = models.OneToOneField(Project, on_delete=models.CASCADE,null=True)
    notify = GenericRelation(Notification)

    def get_absolute_url(self):
        return reverse('freelancer_payment')
    
    class Meta:
        ordering=['-id']

    @property
    def can_release(self):
        if  self.for_project.hired == None or self.status != "On Hold":
            return False

    @property
    def can_refund(self):
        if self.status != "On Hold":
            return False
    


    
class TaxModel(BaseModel):
    name = models.CharField(max_length=50,unique=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2,validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])
    
    def __str__(self) -> str:
        return self.name


class FeeModel(BaseModel):
    name = models.CharField(max_length=50,unique=True)
    percentage = models.DecimalField(null=True,blank=True,max_digits=5, decimal_places=2,validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])
    
    def __str__(self) -> str:
        return self.name


