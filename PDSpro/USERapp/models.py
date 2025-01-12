from django.db import models as m
from django.contrib.auth.hashers import make_password
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Base Model for Shared Fields
class BaseModel(m.Model):
    created_at = m.DateTimeField(auto_now_add=True)
    updated_at = m.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Admin Model (Government Officials)
class Admin_model(BaseModel):
    """
    Represents a government administrator in the system.
    """
    admin_id = m.AutoField(primary_key=True)  # Custom primary key
    admin_name = m.CharField(max_length=20, blank=False, null=False)  # Full name of the admin
    admin_email = m.EmailField(
        max_length=50,
        unique=True,
        blank=False,
        null=False,
        validators=[EmailValidator(message="Enter a valid email address.")]
    )
    admin_password = m.CharField(max_length=128, blank=False, null=False)

    def save(self, *args, **kwargs):
        if not self.pk:  # Hash the password only during creation
            self.admin_password = make_password(self.admin_password)
        super().save(*args, **kwargs)

    def _str_(self):
        return f"Admin({self.admin_id}, {self.admin_name})"

    class Meta:
        db_table = "admin_table"



# FPS Model (Fair Price Shops/Owners)
class FPS_model(BaseModel):
    """
    Represents Fair Price Shops and their owners.
    """
    fps_id = m.AutoField(primary_key=True)
    fps_name = m.CharField(max_length=20, blank=False, null=False)
    fps_email = m.EmailField(
        max_length=50,
        unique=True,
        blank=False,
        null=False,
        validators=[EmailValidator(message="Enter a valid email address.")]
    )
    fps_password = m.CharField(max_length=128, blank=False, null=False)
    fps_phone = m.CharField(
        max_length=13,
        unique=True,
        blank=False,
        null=False,
        validators=[RegexValidator(r'^\d{10,13}$', message="Enter a valid phone number.")]
    )
    owner_image = m.ImageField(upload_to="fps_owners/", blank=False)

    def save(self, *args, **kwargs):
        if not self.pk:  # Hash the password only during creation
            self.fps_password = make_password(self.fps_password)
        super().save(*args, **kwargs)

    def _str_(self):
        return f"FPS({self.fps_id}, {self.fps_name})"

    class Meta:
        db_table = "fps_table"

class RationCardManager(BaseUserManager):
    def create_user(self, ration_card_beneficiary_name, password=None, **extra_fields):
        if not ration_card_beneficiary_name:
            raise ValueError('The Beneficiary Name field must be set')
        user = self.model(ration_card_beneficiary_name=ration_card_beneficiary_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, ration_card_beneficiary_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(ration_card_beneficiary_name, password, **extra_fields)
# Ration Card Model
class Ration_card(AbstractBaseUser):
    """
    Represents ration cards for beneficiaries.
    """
    r_id = m.AutoField(primary_key=True)
    email = m.EmailField(unique=True , default = str)
    beneficiary_card_no = m.CharField(max_length=15, null=False, default=str)
    ration_card_beneficiary_name = m.CharField(max_length=20, blank=False, null=False, default=str)
    b_ration_address = m.CharField(max_length=100, blank=False, null=False, default=str)
    b_ration_aadhaar = m.CharField(max_length=10, blank=False, null=False, default=str)
    b_ration_state = m.CharField(max_length=20, blank=False, null=False, default=str)
    b_ration_pincode = m.CharField(max_length=6, blank=False, null=False, default=str)
    password = m.CharField(max_length=10 , default=str)
    b_ration_family_size = m.IntegerField(blank=False, null=False, default=1)
    b_ration_family = m.JSONField(blank=False, null=False, default=list)  # Default to an empty list

    # Set up custom manager
    objects = RationCardManager()

    USERNAME_FIELD = 'email'  # Set this as the username field
    REQUIRED_FIELDS = ['beneficiary_card_no', 'b_ration_address', 'b_ration_aadhaar', 'b_ration_state' , "b_ration_pincode" , "b_ration_family_size"]  # Add other required fields

    def _str_(self):
        return f"RationCard({self.ration_card_beneficiary_name})"

    class Meta:
        db_table = "ration_card_table"



# Beneficiaries Model
class Beneficiaries(BaseModel):
    beneficiary_id = m.AutoField(primary_key=True)
    r_id = m.ForeignKey(Ration_card, on_delete=m.CASCADE, related_name="beneficiaries")
    beneficiary_card_no = m.CharField(max_length=15, default=str , null=False)
    beneficiary_name = m.CharField(max_length=20, blank=False, null=False)
    beneficiary_email = m.EmailField(
        max_length=50,
        blank=False,
        null=False,
        validators=[EmailValidator(message="Enter a valid email address.")]
    )
    beneficiary_phone = m.CharField(
        max_length=13,
        blank=False,
        null=False,
        validators=[RegexValidator(r'^\d{10,13}$', message="Enter a valid phone number.")]
    )
    beneficiary_address = m.CharField(max_length=100,default=str, blank=False, null=False)
    beneficiary_aadhaar = m.CharField(max_length=10, blank=False,default=str, null=False)
    beneficiary_state = m.CharField(max_length=20, blank=False,default=str, null=False)
    beneficiary_pincode = m.CharField(max_length=6, blank=False, default=str,null=False)
    beneficiary_family_size = m.IntegerField(blank=False, null=False , default=int)
    beneficiary_family = m.JSONField(blank=False, null=False, default=list)  # Store family as a list
    beneficiary_otp = m.CharField(max_length=6, blank=False, null=False, default=None)
    beneficiary_password = m.CharField(max_length=128, blank=False, default=str)
    def save(self, *args, **kwargs):
        if not self.pk:  # Hash the password only during creation
            self.beneficiary_password = make_password(self.beneficiary_password)
        super().save(*args, **kwargs)

    def _str_(self):
        return f"Beneficiary({self.beneficiary_id}, {self.beneficiary_name})"

    class Meta:
        db_table = "beneficiaries_table"

    class BeneficiaryCardChoices(m.TextChoices):
        SELECT = "select", "Select"
        YELLOW = "yellow", "Yellow"
        WHITE = "white", "White"
        SAFFRON = "saffron", "Saffron"
        GREEN = "green", "Green"

    beneficiary_card = m.CharField(
        max_length=20,
        choices=BeneficiaryCardChoices.choices,
        default=BeneficiaryCardChoices.SELECT
    )
    class BeneficiaryTypeChoices(m.TextChoices):
        SELECT = "select", "Select"
        SUPERUSER = "superuser", "Superuser"
        FPS = "fps", "Fair Price Shop"
        USER = "user", "User"

    beneficiary_type = m.CharField(
        max_length=20,
        choices=BeneficiaryTypeChoices.choices,
        default=BeneficiaryTypeChoices.SELECT,
        null=True,
    )

    def save(self, *args, **kwargs):
        if not self.pk:  # Hash the password only during creation
            self.beneficiary_password = make_password(self.beneficiary_password)
        super().save(*args, **kwargs)

    def _str_(self):
        return f"Beneficiary:({self.beneficiary_id}, {self.beneficiary_name})"

    class Meta:
        db_table = "beneficiaries_table"
    