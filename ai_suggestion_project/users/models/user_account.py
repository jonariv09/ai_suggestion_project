from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.utils.translation import gettext_lazy

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=gettext_lazy("created_at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=gettext_lazy("updated_at"))
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True

class UserAccount(PermissionsMixin, BaseModel, AbstractBaseUser):
    email = models.EmailField(verbose_name=gettext_lazy("email address"), unique=True)
    first_name = models.CharField(verbose_name=gettext_lazy("first name"), max_length=150, blank=True)
    last_name = models.CharField(verbose_name=gettext_lazy("last name"), max_length=150, blank=True)
    is_active = models.BooleanField(
        gettext_lazy("active"),
        default=True,
        help_text=gettext_lazy(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []