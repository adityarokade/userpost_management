from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Post

@receiver(post_save, sender=Post)
def send_post_creation_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'New Post Created'
        plain_message = f"The Use Created the New Post - "
        author_email = instance.author.email

        send_mail(subject, plain_message, None, [author_email])