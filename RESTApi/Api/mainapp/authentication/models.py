from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):

    def create_user(self, EmailId, FullName, MobileNumber, password):
        if not EmailId:
            raise ValueError("Users must have an EmailId")

        user = self.model(EmailId=self.normalize_email(EmailId),
                          FullName=FullName,
                          MobileNumber=MobileNumber,
                          )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, EmailId, FullName, MobileNumber, password):
        user = self.create_user(
            EmailId=self.normalize_email(EmailId),
            FullName=FullName,
            MobileNumber=MobileNumber,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class Account(models.Model):
    AccountName = models.TextField(max_length=100, blank=False, null=False)


class User(AbstractBaseUser):

    EmailId = models.EmailField(max_length=128, unique=True, blank=False, null=False)
    FullName = models.TextField(max_length=200, blank=False, null=False)
    MobileNumber = models.TextField(max_length=20, blank=False, null=False)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    auth_change_failures = models.IntegerField(default=0)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'EmailId'
    REQUIRED_FIELDS = ['FullName', 'MobileNumber']

    def __str__(self):
        return self.EmailId

    def has_perm(self, perm, obj=None):
        """ Does the user have a specific permission? """
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def has_max_auth_change_failures(self):
        return self.auth_change_failures >= 5

    objects = MyAccountManager()


class User_Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    acc = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)

# I can store another table for storing the owners for the accounts
