from django.db import models
from ..authentication.models import User, Account


def user_directory_path(instance, filename):
    if instance.IsSigned != True:
    #     return 'user_{0}/signed/{1}'.format(instance.User.id, filename)
    # else:
        return 'user_{0}/unsigned/{1}'.format(instance.User.id, filename)
    

class FilesModel(models.Model):
    User = models.ForeignKey(User,
                             default=1,
                             null=True,
                             on_delete=models.SET_NULL)
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)

    File = models.FileField(upload_to = user_directory_path ,blank=False, null=False)

    # Filter Properties
    IsSigned = models.BooleanField(default=False)
    Date = models.DateField(auto_now_add=True, blank=True, null=False)
    DateTime = models.DateTimeField(auto_now_add=True)
