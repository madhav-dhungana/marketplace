from django.template.loader import render_to_string
from .tasks import background_email_send

""" Mixin for API"""
class SendEmailMixin:
    email_template_name = None
    mail_subject = None

    def send_email_temp(self, email_data, action_to):
        message = render_to_string(self.email_template_name, email_data)
        background_email_send.delay(self.mail_subject, message, [action_to])
