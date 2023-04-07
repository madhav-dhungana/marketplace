from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save
from .models import HiredModel, InviteModel, Project, Proposal, Reviews
from user.models import User
from allauth.socialaccount.signals import social_account_added


@receiver(post_save, sender=HiredModel)
def addHired(sender, instance, created, *args, **kwargs):
    if created:
        instance.project.hired = instance.got_hired
        instance.project.save()
        instance.activities.create(
            action_by=instance.hired_by,
            action="hired",
            detail=f"{instance.hired_by} hired {instance.got_hired} for project {instance.project.id}",
        )
        instance.project.notify.create(
            action_by=instance.hired_by,
            action_to=instance.got_hired,
            action="hired",
            title=f"{instance.hired_by} hired you for project.",
        )


# freelancer can only bid if project status is active
@receiver(post_save, sender=Project)
def ProjectSignal(sender, instance, created, *args, **kwargs):
    if instance.status == "Active":
        Project.objects.filter(id=instance.id).update(can_apply=True)
    else:
        Project.objects.filter(id=instance.id).update(can_apply=False)
    if created:
        instance.activities.create(action_by=instance.posted_by, action="created")


@receiver(post_save, sender=Proposal)
def createProposalSignal(sender, instance, created, *args, **kwargs):
    if created:
        action_to =instance.project.posted_by
        instance.activities.create(action_by=instance.user, action="created")
        instance.project.notify.create(
            action_by=instance.user,
            action_to=action_to,
            action="created",
            title=f"{instance.user} created proposal for your project.",
        )


@receiver(post_save, sender=InviteModel)
def createInviteSignal(sender, instance, created, *args, **kwargs):
    if created:

        instance.activities.create(
            action_by=instance.sent_by,
            action="created",
            detail=f"{instance.sent_by} invited {instance.sent_to} for project",
        )
        instance.notify.create(
            action_by=instance.sent_by,
            action_to=instance.sent_to,
            action="invited",
            title=f"{instance.sent_by} invited you for project.",
        )


@receiver(post_save, sender=Reviews)
def createReviewSignal(sender, instance, created, *args, **kwargs):
    if created:
        instance.activities.create(
            action_by=instance.review_by,
            action="review",
            detail=f"{instance.review_by} added review for {instance.review_to}",
        )
        instance.for_project.notify.create(
            action_by=instance.review_by,
            action_to=instance.review_to,
            action="review",
            title=f"{instance.review_by} gave you a review .",
        )
        to_user =instance.review_to
        to_user.user_ratings=to_user.get_rating
        to_user.user_ratings_floor=to_user.get_rating_floor
        to_user.save()
