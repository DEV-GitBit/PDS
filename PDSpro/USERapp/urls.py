
from django.urls import path
from . import views as v
from django.conf import settings
from django.conf.urls.static import static
app_name = 'User'

urlpatterns = [
    path('',v.home, name='home'),
    path('signup/',v.signup_view, name='signup'),
    path('login/',v.login_view, name='login'),
    path('logout/',v.logout_view, name='logout'),
    # path('profile/',v.profile_view, name='profile'),
    path('forgot_pass/',v.forgot_p, name='f_p'),
    path('create_pass/',v.create_pass, name='c_p'),
    path('otp/',v.otp_view, name='otp'),
    path('ration_card_details/' , v.ration_card_view, name="add_ration_details"),
]

urlpatterns +=[]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
