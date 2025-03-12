import csv
import os
import django
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "als_monitoring.settings")

# Setup Django
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import KioskOperatorProfile


User = get_user_model()

CSV_FILE_PATH = "tracklist.csv"


# def generate_kiosk_id():
#     """Generates a random kiosk ID."""
#     return f"KIOSK-{random.randint(10000, 99999)}"


def create_users_from_csv(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        # Create the dictionary from STATE_CHOICES
        state_mapping = {name: code for code, name in KioskOperatorProfile.STATE_CHOICES}

        reader = csv.DictReader(file)

        for row in reader:
            email = row["Email"].strip()
            full_name = row["Kiosk Operator"].strip()
            # To get the short form representation
            state = state_mapping.get(row["State"].strip())
            location = row["Location"].strip()
            phone_no = f"0{row["Phone Number"].strip()}"
            kiosk_id = row["Serial Number"].strip()

            # Extract first and name (first and second words in full name)
            first_name = full_name.split()[0]
            last_name = full_name.split()[1] if len(
                full_name.split()) > 1 else "N/A"

            # Generate password (e.g., Philip_Zamfara)
            password = f"{first_name}_{state}"

            # Create user if not exists
            user, created = User.objects.get_or_create(email=email, defaults={
                "first_name": first_name,
                "last_name": last_name,
            })

            if created:
                user.set_password(password)
                user.save()
                print(f"Created user: {email}")
            else:
                print(f"User already exists: {email}")

            # Create or update the kiosk profile
            profile, profile_created = KioskOperatorProfile.objects.get_or_create(user=user, defaults={
                "kiosk_location": location,
                # "kiosk_id": generate_kiosk_id(),
                "kiosk_id": kiosk_id,
                "phone_number": phone_no,
                "operating_hours": "5:00am to 8:00pm",
                "is_available": True,
                "state": state
            })

            if not profile_created:
                profile.kiosk_location = location
                # You might not want to overwrite this in production!
                # profile.kiosk_id = generate_kiosk_id()
                profile.kiosk_id = kiosk_id
                profile.state = state
                profile.phone_number = phone_no
                profile.operating_hours = "5:00am to 8:00pm"
                profile.is_available = True
                profile.save()

            print(
                f"✅ Profile set up for: {email} | Kiosk ID: {profile.kiosk_id}")


create_users_from_csv(CSV_FILE_PATH)
