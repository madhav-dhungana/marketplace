from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from notification.models import Notification
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from dateutil import relativedelta
from django_countries.fields import CountryField
from django.db.models.aggregates import Sum
from django.utils.functional import cached_property


class ActivityLog(models.Model):
    action = models.CharField(max_length=100)
    action_date = models.DateTimeField(auto_now_add=True)
    action_by = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name='activities')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    detail = models.CharField(max_length=100, null=True, blank=True)

    @property
    def get_description(self):
        if self.detail:
            return self.detail
        return f'{self.action_by} {self.action}  {self.content_object.__class__.__name__}'

    class Meta:
        ordering = ['-id']


class CustomUserManager(BaseUserManager):

    def create_user(self, email, username, password, **extra_fields):
        """
          Create and save a SuperUser with the given email,username, password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_('Username must be set'))
        if not password:
            raise ValueError(_('Password must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email,username, password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        b = self.create_user(email, username, password, **extra_fields)
        b.role = "Admin"
        b.save()
        return b


class User(AbstractUser):
    """
        Main User Model which has basic information
    """

    # using employer and freelancer since it is easy to understand the role
    # rather than batuwa or traveller (sounds same)
    # we will use employer or freelancer behind the scene
    # but show batuwa and traveller in front side
    role = [
        ('Admin', 'Admin'),
        ('Employer', 'Employer'),  # someone who post projects and hire freelancer
        # someone who take project by sending propposal
        ('Freelancer', 'Freelancer'),
    ]

    gender_types = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
        ('Not Specify', 'Not Specify'),
    ]

    role = models.CharField(max_length=200, choices=role)
    email = models.CharField(max_length=200, unique=True)
    username = models.CharField(max_length=200, unique=True)
    display_name = models.CharField(max_length=200, null=True, blank=True)
    overview = models.TextField(blank=True, null=True)
    avatar = models.ImageField(default='default.png', upload_to='avatars')
    banner_image = models.ImageField(default='banner.jpg', upload_to='avatars')
    gender = models.CharField(
        max_length=100, choices=gender_types, default='Male')
    language_one = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    state = models.CharField(max_length=150, null=True, blank=True)
    country = CountryField(default='AF')
    zipcode = models.IntegerField(null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    hourly_rate = models.FloatField(null=True, blank=True, default=5)
    skills = models.ManyToManyField("projects.DesiredExpertise", blank=True)
    bookmarked_projects = models.ManyToManyField(
        "projects.Project", related_name="bookmared_projects")
    bookmarked_people = models.ManyToManyField("self")
    verified = models.BooleanField(default=False)
    user_ratings = models.FloatField(null=True, blank=True)
    user_ratings_floor = models.FloatField(null=True, blank=True)

    availability = models.BooleanField(default=False)
    activities = GenericRelation(ActivityLog)
    notify = GenericRelation(Notification)

    # freelancer rating based on completed projects rating by client

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['-date_joined']
        verbose_name_plural = "Custom Users"

    def __str__(self):
        return f'{self.username}'

    @cached_property
    def get_rating(self):
        count = self.reviews_got.count()
        if self.role != "Freelancer" or count < 1:
            return None
        total_rate = self.reviews_got.aggregate(sum=Sum("rating"))
        return total_rate["sum"]/count

    @cached_property
    def get_rating_floor(self):
        from math import floor
        if not self.get_rating:
            return None
        return floor(self.get_rating)

    @property
    def no_of_reviews_got(self):
        return self.reviews_got.count()

    @property
    def get_skills(self):
        return self.skills.all()

    @property
    def get_awards(self):
        return self.awards.all()

    @property
    def get_langs(self):
        return self.many_languages.all()

    @property
    def get_bookmarked_projects(self):
        return self.bookmarked_projects.all()

    @property
    def get_bookmarked_users(self):
        return self.bookmarked_people.all()

    @property
    def get_project_posted(self):
        return self.my_projects.count()

    @property
    def get_project_hired(self):
        return self.hired.count()

    @property
    def get_open_job(self):
        return self.my_projects.filter(can_apply=True, expires_on__gte=datetime.today()).count()

    @property
    def get_finished_jobs(self):
        return self.hired_projects.filter(status="COM").count()

    @property
    def get_hired_rate(self):
        if self.get_project_hired == 0:
            return 0
        return (self.get_project_hired/self.get_project_posted)*100

    @property
    def profile_complete_percentage(self):
        count = 0
        if self.is_active:
            count += 1

        if self.email:
            count += 1

        if self.username:
            count += 1

        if self.display_name:
            count += 1

        if self.avatar:
            count += 1

        if self.overview:
            count += 1

        if self.gender:
            count += 1

        if self.address:
            count += 1

        if self.country:
            count += 1

        if self.contact:
            count += 1

        if self.hourly_rate:
            count += 1

        if self.skills:
            count += 1

        if self.zipcode:
            count += 1

        if self.verified:
            count += 1

        if self.title:
            count += 1

        percent = count/15 * 100

        return int(percent)

    @property
    def total_payment(self):
        total_payment = 0
        for i in self.my_deposits.filter(transaction__types='Transfer', transaction__status='success'):
            total_payment += i.transaction.price
        return total_payment

    @property
    def follower_count(self):
        return self.user_follow_to.all().count()

    @property
    def following_count(self):
        return self.user_follow_by.all().count()

    @property
    def active_proposal(self):
        count = 0
        for i in self.proposals.all():
            if i.project.status == 'Active':
                count += 1
        return count

    @property
    def applied_proposal(self):
        return self.proposals.all().count()

    @property
    def hired_jobs(self):
        return self.hired.all().count()


class WeekDayAvailable(models.Model):
    """
        This gives the weekly availabilty of freelancer
        Eg: Sunday (1am to 5pm)
            Monday (2am to 6am)
    """
    weekday = [
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),

    ]
    name = models.CharField(max_length=10, choices=weekday)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    available_from = models.TimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    available_to = models.TimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name} {self.id}"


class Languages(models.Model):
    user = models.ForeignKey(
        "user.User", related_name="many_languages", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150)
    fluency = models.PositiveSmallIntegerField(default=50, validators=[
        MaxValueValidator(100),
        MinValueValidator(1)
    ]
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Languages"


class Experience(models.Model):
    user = models.ForeignKey(
        "user.User", related_name="experiences", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150)
    start_date = models.DateField(auto_now=False)
    end_date = models.DateField(auto_now=False, null=True, blank=True)
    currently_working = models.BooleanField(default=False)
    summary = models.TextField(_("Summary "), null=True)
    activities = GenericRelation(ActivityLog)

    def __str__(self):
        return self.company_name

    def clean(self):
        if self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError('Start date is after end date')

    @property
    def calculate_experience(self):
        currently_working = self.currently_working
        today = datetime.today()
        start_date = self.start_date
        end_date = self.end_date
        if currently_working:
            total_date = relativedelta.relativedelta(start_date, today)
        else:
            total_date = relativedelta.relativedelta(end_date, start_date)
        return total_date

    class Meta:
        verbose_name_plural = "Experience"


class Education(models.Model):
    user = models.ForeignKey(
        "user.User", related_name="education", on_delete=models.CASCADE)
    degree_title = models.CharField(max_length=150)
    uni_name = models.CharField(max_length=150)
    start_year = models.DateField(auto_now=False)
    end_year = models.DateField(auto_now=False, null=True, blank=True)
    currently_working = models.BooleanField(default=False)
    summary = models.TextField(_("Summary "), null=True)
    activities = GenericRelation(ActivityLog)

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_year > self.end_year:
            raise ValidationError('Start year is after end year')

    class Meta:
        verbose_name_plural = "Education"


class Awards(models.Model):
    user = models.ForeignKey(
        "user.User", related_name="awards", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    date = models.DateField(auto_now=False)
    activities = GenericRelation(ActivityLog)


class SocialLink(models.Model):
    user = models.OneToOneField("user.User", on_delete=models.CASCADE)
    facebook = models.URLField(max_length=200, null=True, blank=True)
    linkedin = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return 'Social Link'


class IdentityForm(models.Model):
    status_type = [
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('On Review', 'On Review'),
    ]
    user = models.OneToOneField("user.User", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    contact_number = models.CharField(max_length=150)
    identiy_num = models.CharField(verbose_name=_(
        "CNIC / Passport / NIN / SSN"), max_length=150)
    document = models.FileField(upload_to='identity_files')
    address = models.CharField(max_length=150)
    answered = models.BooleanField(default=False)
    status = models.CharField(
        max_length=200, choices=status_type, default='On Review', blank=True)
    notify = GenericRelation(Notification)

    def __str__(self) -> str:
        return f'Identity form of {self.user}'

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('verify_identity')

    def accept_or_reject_user(self, val):
        status = "Accepted" if val else "Rejected"
        self.status = status
        self.user.verified = val
        self.user.save()
        self.answered = True
        self.save()
        self.notify.create(
            action_to=self.user,
            action="verified" if val else "rejected",
            title=f"Your identity form has been {status}.",
        )


class UserDeleteRecords(models.Model):
    """docstring for UserDeleteRecords"""
    reason = models.CharField(max_length=250)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.email


class Followers(models.Model):
    follow_by = models.ForeignKey(
        User, related_name='user_follow_by', on_delete=models.CASCADE)
    follow_to = models.ForeignKey(
        User, related_name='user_follow_to', on_delete=models.CASCADE)

    @classmethod
    def get_follow_status(cls, follow_by, follow_to):
        if cls.objects.filter(follow_by_id=follow_by, follow_to_id=follow_to).exists():
            return True
        return False


class PortfolioDocument(models.Model):
    file = models.FileField(upload_to='freelancer/portfolio/')
    is_banner = models.BooleanField(default=False)


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)
    file = models.ManyToManyField(PortfolioDocument)

    def __str__(self):
        return self.title
