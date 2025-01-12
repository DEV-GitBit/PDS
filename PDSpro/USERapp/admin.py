from django.contrib import admin

from USERapp.forms import Registration
from .models import *

admin.site.register(Admin_model)
admin.site.register(FPS_model)
admin.site.register(Ration_card)
admin.site.register(Beneficiaries)