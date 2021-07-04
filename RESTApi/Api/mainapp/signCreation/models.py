from django.db import models
from ..authentication.models import User
from django.utils.translation import gettext_lazy as _

def user_directory_path(instance, filename):
    return 'user_{0}/SigImage/{1}'.format(instance.User.id, filename)


class UserSign(models.Model):

    class Position(models.TextChoices):
        TOPLEFT = 'TL', _('TopLeft')
        TOPRIGHT = 'TR', _('TopRight')
        BOTTOMLEFT = 'BL', _('BottomLeft')
        BOTTOMRIGHT = 'BR', _('BottomRight')

    FriendlyName = models.TextField( max_length=200, blank=False, null=False)
    SignPage = models.IntegerField(default=1)
    # SignPage = models.CharField(max_length = 10 , blank = False, null=False,  default="Last")
    SignPosition = models.CharField(
        max_length=250,
        choices=Position.choices,
        default=Position.BOTTOMRIGHT,
        )


class UserSignText(models.Model):
    User = models.ForeignKey(User,
                            default=1,
                            null=True,
                            on_delete=models.SET_NULL)
    Sign = models.ForeignKey(UserSign, on_delete=models.CASCADE, null=False, related_name='usersigntext',)
    VisText = models.TextField(max_length=500, blank=False, null=False)


class UserSignImage(models.Model):
    User = models.ForeignKey(User,
                            default=1,
                            null=True,
                            on_delete=models.SET_NULL)
    Sign = models.ForeignKey(UserSign, on_delete=models.CASCADE, null=True, related_name='usersignimage',)
    VisImage = models.ImageField(upload_to = "signature/" ,blank=False, null=False)