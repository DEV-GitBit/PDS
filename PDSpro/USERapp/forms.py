from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class Registration(forms.ModelForm):
    class Meta:
        model = Beneficiaries
        fields = [
            "beneficiary_name",
            "beneficiary_phone",
            "beneficiary_card_no",
            "beneficiary_email",
            "beneficiary_aadhaar",
        ]

class Ration_admin(UserCreationForm):
    class Meta:
        model = Ration_card
        fields = [
            "beneficiary_card_no",
            "ration_card_beneficiary_name",
            "b_ration_address",
            "b_ration_state",
            "b_ration_pincode",
            "b_ration_family_size",
            "b_ration_family",
        ]

class Admin_registration(UserCreationForm):
    class Meta:
        model = Admin_model
        fields = [
            "admin_name",
            "admin_email",
            "admin_password",
        ]