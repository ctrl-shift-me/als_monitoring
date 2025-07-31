from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
# from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier for auth, instead of username
    """

    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class UserType(models.TextChoices):
        KIOSK_OPERATOR = 'KO', 'Kiosk Operator'
        SUPER_AGENT = 'SA', 'Super Agent'

    username = None
    email = models.EmailField(
        verbose_name="email address", blank=True, unique=True)
    user_type = models.CharField(
        max_length=2,
        choices=UserType.choices,
        default=UserType.KIOSK_OPERATOR
    )
    profile_completed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class KioskOperatorProfile(models.Model):

    STATE_CHOICES = (
        ('AB', 'Abia'),
        ('FC', 'Abuja'),
        ('AD', 'Adamawa'),
        ('AK', 'Akwa Ibom'),
        ('AN', 'Anambra'),
        ('BA', 'Bauchi'),
        ('BY', 'Bayelsa'),
        ('BE', 'Benue'),
        ('BO', 'Borno'),
        ('CR', 'Cross River'),
        ('DE', 'Delta'),
        ('EB', 'Ebonyi'),
        ('ED', 'Edo'),
        ('EK', 'Ekiti'),
        ('EN', 'Enugu'),
        ('GO', 'Gombe'),
        ('IM', 'Imo'),
        ('JI', 'Jigawa'),
        ('KD', 'Kaduna'),
        ('KN', 'Kano'),
        ('KT', 'Katsina'),
        ('KE', 'Kebbi'),
        ('KO', 'Kogi'),
        ('KW', 'Kwara'),
        ('LA', 'Lagos'),
        ('NA', 'Nasarawa'),
        ('NI', 'Niger'),
        ('OG', 'Ogun'),
        ('ON', 'Ondo'),
        ('OS', 'Osun'),
        ('OY', 'Oyo'),
        ('PL', 'Plateau'),
        ('RI', 'Rivers'),
        ('SO', 'Sokoto'),
        ('TA', 'Taraba'),
        ('YO', 'Yobe'),
        ('ZA', 'Zamfara'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Perhaps use Postgres text search to find places based on location stored
    kiosk_location = models.CharField(max_length=255)
    # Possibly have extra details about the shop
    # Optionally have provision for images
    kiosk_id = models.CharField(max_length=50)
    # Should probably take in states too but as an enum
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    operating_hours = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    is_available = models.BooleanField(default=False)

    def __str__(self):
        return f"Kiosk Operator Profile - {self.user.email}"

    def get_full_name(self):
        last_name = self.user.last_name if self.user.last_name != "N/A" else ""
        return f"{self.user.first_name} {last_name}"


class SuperAgentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=100)
    # Should probably take in states too but as an enum
    state = models.CharField(
        max_length=2, choices=KioskOperatorProfile.STATE_CHOICES)
    # Todo: Add kiosks managed
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Super Agent Profile - {self.user.email}"

    def get_full_name(self):
        last_name = self.user.last_name if self.user.last_name != "N/A" else ""
        return f"{self.user.first_name} {last_name}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == User.UserType.KIOSK_OPERATOR:
            KioskOperatorProfile.objects.create(user=instance)
        elif instance.user_type == User.UserType.SUPER_AGENT:
            SuperAgentProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    if instance.user_type == User.UserType.KIOSK_OPERATOR:
        instance.kioskoperatorprofile.save()
    if instance.user_type == User.UserType.SUPER_AGENT:
        instance.superagentprofile.save()


@receiver(pre_save, sender=KioskOperatorProfile)
def fetch_coordinates(sender, instance, **kwargs):
    if instance.kiosk_location:
        geolocator = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)
        try:
            location = geolocator.geocode(instance.kiosk_location)
            if location:
                instance.latitude = location.latitude
                instance.longitude = location.longitude
        except GeocoderTimedOut:
            pass
