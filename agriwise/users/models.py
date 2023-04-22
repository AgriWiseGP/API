from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models import BooleanField, CharField, EmailField, ImageField
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise TypeError("user must have username")
        if not email:
            raise TypeError("user must have email")
        if not password:
            raise TypeError("user must have password")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if not username:
            raise TypeError("superuser must have username")
        if not email:
            raise TypeError("superuser must have email")
        if not password:
            raise TypeError("superuser must have password")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user


class User(AbstractUser):
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None
    last_name = None
    email = EmailField(
        max_length=254,
        verbose_name="email address",
        unique=True,
    )
    is_active = BooleanField(default=False)
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    is_agriculture_specialist = BooleanField(null=True, blank=True)
    image = ImageField(null=True, blank=True, upload_to="user/profile/images/")
    objects = UserManager()
