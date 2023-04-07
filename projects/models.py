from django.db import models
from django.utils.functional import cached_property
from django_countries.fields import CountryField
from datetime import date
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from notification.models import Notification
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Portfolio(models.Model):
    user = models.ForeignKey(
        "user.User", related_name="portfolios", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    detail = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title


class PortfolioFile(models.Model):
    portfolio_of = models.ForeignKey(Portfolio,  on_delete=models.CASCADE)
    files = models.FileField(upload_to='portfolio_files')

    @cached_property
    def get_file_name(self):
        return self.files.url.split("/")[-1]


class ProjectCategory(models.Model):
    name = models.CharField(max_length=50)
    created_on = models.DateField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.name


class DesiredExpertise(models.Model):
    skill_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.skill_name


class ProjectManager(models.Manager):
    def available(self):
        return Project.objects.filter(can_apply=True, expires_on__gte=date.today())


class Project(models.Model):
    pricing_types = [
        ("F", "Fixed Budget Price"),
        ("H", "Hourly Pricing"),
        ("B", "Biding Price"),
    ]
    pricing_types = [
        ("F", "Fixed Budget Price"),
        ("H", "Hourly Pricing"),
        ("B", "Biding Price"),
    ]

    project_status = [
        ("PEN", "Pending"),
        # approved by admin/ freelancer can only bid or apply in this status
        ("Active", "Active"),
        ("ON", "Ongoing"),
        ("COM", "Completed"),
        ("CAN", "Cancelled"),
    ]

    price_stats = [
        ("FIXED", "FIXED"),
        ("NEGOTIATE", "Can Negotiate"),
    ]

    deposit_status = [
        ("Unpaid", "Unpaid"),
        ("Paid", "Paid"),
        ("Refunded", "Refunded")
    ]

    posted_by = models.ForeignKey(
        "user.User", related_name="my_projects", null=True, on_delete=models.CASCADE)
    hired = models.ForeignKey("user.User", related_name="hired_projects",
                              null=True, on_delete=models.SET_NULL, blank=True)
    category = models.ForeignKey(
        "projects.ProjectCategory", null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=250)
    pricing_type = models.CharField(max_length=250, choices=pricing_types)
    detail = RichTextUploadingField(null=True, blank=True)
    status = models.CharField(
        max_length=250, choices=project_status, default="PEN", blank=True)
    price_status = models.CharField(
        max_length=250, choices=price_stats, default="NEGOTIATE")
    expires_on = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
    start_time = models.TimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    end_time = models.TimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    posted_on = models.DateField(auto_now_add=True, blank=True, null=True)
    desired_skills = models.ManyToManyField(
        "projects.DesiredExpertise", blank=True)
    interviewing = models.ManyToManyField("user.User", blank=True)
    price = models.FloatField(null=True, blank=True)
    location = CountryField()
    address = models.CharField(max_length=50, null=True, blank=True)
    experience_needed = models.IntegerField(null=True, blank=True)
    can_apply = models.BooleanField(default=False)
    # if employer paid the the platform project price
    employer_payment_status = models.CharField(
        max_length=20, choices=deposit_status, blank=True, default="Unpaid")

    activities = GenericRelation("user.ActivityLog")
    notify = GenericRelation(Notification)
    objects = ProjectManager()

    def __str__(self) -> str:
        return self.title[:30]

    @property
    def get_skills(self):
        return self.desired_skills.all()

    @property
    def get_documents(self):
        return self.projectdocument_set.all()

    @property
    def get_skills_in_comma(self):
        return ','.join([i.skill_name for i in self.get_skills])

    @property
    def no_of_proposals(self):
        return self.proposals.count()

    @property
    def total_invites(self):
        return self.project_invites.count()

    @property
    def total_answered_invites(self):
        return self.project_invites.filter(answered=False).count()

    @property
    def no_of_interviewing(self):
        return self.interviewing.all().count()

    @property
    def has_hired(self):
        return True if self.hired else False

    @cached_property
    def hired_date(self):
        b = HiredModel.objects.get(project=self)
        return b.hired_date

    @property
    def get_expiry_days(self):
        today = date.today()
        l_date = self.expires_on
        delta = l_date - today
        return delta.days

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Projects"

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'id': int(self.id)})

    # based on uesr detail url is different

    def get_absolute_for_freelancer(self):
        return reverse('free_project_detail', kwargs={'id': int(self.id)})


class HiredModel(models.Model):
    """Model to track hire information"""
    project = models.ForeignKey(
        "projects.Project", related_name="project_hires", null=True, on_delete=models.CASCADE)
    hired_by = models.ForeignKey(
        "user.User", related_name="hired", null=True, on_delete=models.CASCADE)
    got_hired = models.ForeignKey(
        "user.User", related_name="got_hired", null=True, on_delete=models.SET_NULL)
    hired_date = models.DateField(auto_now_add=True)
    activities = GenericRelation("user.ActivityLog")
    notify = GenericRelation(Notification)


class InviteModel(models.Model):
    project = models.ForeignKey(
        "projects.Project", related_name="project_invites", null=True, on_delete=models.CASCADE)
    sent_by = models.ForeignKey(
        "user.User", related_name="invites_sent", null=True, on_delete=models.CASCADE)
    sent_to = models.ForeignKey(
        "user.User", related_name="invites_got", null=True, on_delete=models.SET_NULL)
    detail = models.TextField()
    answered = models.BooleanField(default=False)
    posted_on = models.DateField(auto_now_add=True)
    estimated_duration = models.CharField(max_length=100)
    estimated_price = models.FloatField()
    activities = GenericRelation("user.ActivityLog")
    accepted = models.BooleanField(null=True, blank=True)
    notify = GenericRelation(Notification)

    def __str__(self) -> str:
        return f'Invite from {self.sent_by} to {self.sent_to}'

    def get_absolute_url(self):
        return reverse('invite_list')

    def get_absolute_for_freelancer(self):
        return reverse('free_invite_list')

    def answer_invite(self, accepted, user):
        self.accepted = accepted
        self.answered = True
        self.save()
        answer = "accepted" if self.accepted else "rejected"
        self.notify.create(
            action_by=user,
            action_to=self.sent_by,
            action="hired",
            title=f"{self.sent_to} {answer} your invitation.",
        )
        if accepted:
            HiredModel.objects.create(
                project=self.project, hired_by=self.sent_by, got_hired=user)


class ProjectLinks(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    link = models.URLField(max_length=200)


class ProjectDocument(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    documents = models.FileField(upload_to='project_files')

    @cached_property
    def get_file_name(self):
        return self.documents.url.split("/")[-1]


class Proposal(models.Model):
    user = models.ForeignKey(
        "user.User", related_name="proposals", on_delete=models.CASCADE)
    project = models.ForeignKey(
        "projects.Project", related_name="proposals", on_delete=models.CASCADE)
    detail = models.TextField()
    price = models.FloatField()
    created_on = models.DateField(null=True, auto_now_add=True)
    activities = GenericRelation("user.ActivityLog")
    notify = GenericRelation(Notification)


class Reviews(models.Model):
    review_by = models.ForeignKey(
        "user.User", related_name="reviews_given", on_delete=models.CASCADE)
    review_to = models.ForeignKey(
        "user.User", related_name="reviews_got", on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField()
    for_project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE)
    activities = GenericRelation("user.ActivityLog")
    notify = GenericRelation(Notification)
    is_approved = models.BooleanField(default=False)
    is_trash = models.BooleanField(default=False)

    class Meta:
        ordering = ["-id"]

    @property
    def rating_star(self):
        return list(range(0, self.rating))

    @property
    def rating_unstar(self):
        return list(range(0, 5-self.rating))
