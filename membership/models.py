from django.db import models
from django.template.defaultfilters import slugify
from user.models import User


class Plan(models.Model):
    title = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} --> {self.is_available}"

class Membership(models.Model):
    MEMBERSHIP_CHOICES = (
        ('Premium', 'Premium'),
        ('Free', 'Free')
    )
    PERIOD_DURATION = (
        ('Days', 'Days'),
        ('Weeks', 'Weeks'),
        ('Months', 'Months'),
    )
    plans = models.ManyToManyField(Plan)
    title = models.CharField(max_length=255)
    slogan = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES, default='Free', max_length=30)
    duration = models.PositiveIntegerField(default=7)
    duration_period = models.CharField(max_length=100, default='Days', choices=PERIOD_DURATION)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
 
    def __str__(self):
       return f"{self.membership_type}--> {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class PaymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_for = models.ForeignKey(Membership, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} --> {self.payment_for.membership_type}"


class UserMembership(models.Model):
    user = models.OneToOneField(User, related_name='user_membership', on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, related_name='user_membership', on_delete=models.SET_NULL, null=True)
 
    def __str__(self):
       return self.user.username


class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, related_name='subscription', on_delete=models.CASCADE)
    expires_in = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
 
    def __str__(self):
      return self.user_membership.user.username