from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import strip_tags
from notifications.signals import notify
from .models import LikeRecord

@receiver(post_save, sender=LikeRecord)
def send_notification(sender, instance, **kwargs):
    if instance.content_type.model == 'bbs':
        bbs = instance.content_object
        verb = '{0} 点赞了你的帖子《{1}》'.format(instance.user.get_nickname_or_username(), bbs.title)
    elif instance.content_type.model == 'barter':
        barter = instance.content_object
        verb = '{0} 点赞了你的换品《{1}》'.format(instance.user.get_nickname_or_username(), barter.name)
    elif instance.content_type.model == 'comment':
        comment = instance.content_object
        verb = '{0} 点赞了你的评论 "{1}"'.format(instance.user.get_nickname_or_username(), strip_tags(comment.text))

    recipient = instance.content_object.get_user()
    url = instance.content_object.get_url()
    notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance, url=url)