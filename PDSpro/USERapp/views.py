from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from USERapp import *
from USERapp.forms import Ration_admin
from .models import *
from django.contrib import messages
import random
import http.client
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login
from django.contrib import messages


def send_otp(request, mobile, otp):
    conn = http.client.HTTPSConnection("control.msg91.com")
    authkey = settings.AUTH_KEY
    headers = {'Content-Type': "application/json"}  

    message = f"Your OTP is {otp}"
    encoded_message = urllib.parse.quote(message)  # URL encoding

    url = f"/api/sendotp.php?otp={otp}&sender=ABC&message={encoded_message}&mobile={mobile}&authkey={authkey}&country=91"
    
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(url)
    return None


def home(request):
    return render(request,'home.html')

def signup_view(request):
    if request.method == 'POST':  # Handle POST requests for form submission
        name = request.POST.get("beneficiary_name")
        email = request.POST.get("beneficiary_email")
        phone = request.POST.get("beneficiary_phone")
        password = request.POST.get("beneficiary_password")
        card_no = request.POST.get("beneficiary_card_no")
        aadhaar = request.POST.get("beneficiary_aadhaar")
        

        # Check if the user is already registered using the correct field name
        check_user = Beneficiaries.objects.filter(beneficiary_phone=phone).first()
        if check_user:
            context = {
                "message": "Mobile number already registered",
                "class": "danger"
            }
            return render(request, 'signup.html', context)

        # Fetch the corresponding Ration card data based on the provided card number
        ration_card = Ration_card.objects.filter(beneficiary_card_no=card_no).first()

        if not ration_card:
            context = {
                "message": "Ration card not found. Please verify your details.",
                "class": "danger"
            }
            return render(request, 'signup.html', context)

        # Generate OTP before saving
        otp = str(random.randint(1000, 9999))
        

        # Create and save a new beneficiary
        beneficiaries = Beneficiaries(
            beneficiary_name=name,
            beneficiary_email=email,
            beneficiary_phone=phone,
            beneficiary_password=password,
            beneficiary_card_no=card_no,
            beneficiary_aadhaar=aadhaar,
            beneficiary_address=ration_card.b_ration_address,
            beneficiary_state=ration_card.b_ration_state,
            beneficiary_pincode=ration_card.b_ration_pincode,
            beneficiary_family_size=ration_card.b_ration_family_size,
            beneficiary_family=ration_card.b_ration_family,
            r_id=ration_card,
            beneficiary_otp=otp,  # Assign the OTP here
        )
        beneficiaries.save()
        


        # Send OTP
        # send_otp(request, phone, otp)

        # Store OTP and phone in session
        request.session['phone'] = phone
        request.session['otp'] = otp

        return redirect('User:otp')

    # Render signup page for GET requests
    return render(request, 'signup.html')
    


def otp_new_view(request):
    phone = request.session.get('phone')  # Retrieve phone from session
    if not phone:
        context = {
                "message": "Session expired. Please sign up again.",
                "class": "danger"
            }
        
        return redirect('User:signup')
    

    context = {'mobile': phone}

    if request.method == 'POST':
        otp_entered = request.POST.get("otp")
        user = Beneficiaries.objects.filter(beneficiary_phone=phone).first()

        if user and str(otp_entered) == str(user.beneficiary_otp):
            context = {
                "message": "OTP verified successfully! Please log in.",
                "class": "danger"
            }
            return redirect('User:login')  # Redirect to login page after verification
        else:
            # Delete user if OTP is incorrect
            user = Beneficiaries.objects.filter(beneficiary_phone=phone).first()
            if user:
                user.delete()
            
            context = {
                "message": "Invalid OTP. Please sign up again.",
                "class": "danger"
            }
            return redirect('User:signup')  # Redirect to signup page

    return render(request, 'otp.html', context)

        

    # if request.method == 'POST':
    #     form = Registration(request.POST)
    #     if form.is_valid():
    #         Name = form.cleaned_data.get("beneficiary_name")
    #         form.save()
    #         messages.success(request,f'Welcome {Name}')
    #         return redirect('User:otp')
    
    # else:
    #     form = Registration(None)
    
    # context = {
    #     'form': form
    # }

    # return render(request, 'signup.html',context)


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")  # Use 'email' instead of 'username'
        password = request.POST.get("password")
        
        # Authenticate using email and password
        user = authenticate(request, email=email, password=password)

        if user is None:
            messages.error(request, "Invalid Login! Please try again...")
            return redirect("User:login")  

        # If the user is authenticated, login
        login(request, user)
        
        # Customize the message based on user type
        if user.is_superuser:
            messages.success(request, f"Hello superuser {user.username}, you have been successfully logged in!")
        else:
            messages.success(request, f"Hello {user.username}, you have been successfully logged in!")
        
        return redirect("User:home")

    return render(request, "login.html")

def logout_view(request):
    if request.method == "POST":
        username = request.user.username
        logout(request)
        messages.success(
            request,
            "{}, you have been successfully logged out!".format(username)
        )
        return redirect("User:home")
    return render(request, "logout.html")

def forgot_p(request):
    return render(request, 'forgot_p.html')

def create_pass(request):
    return render(request, 'create_pass.html')

def otp_view(request):
    return render(request, 'otp.html')



def ration_card_view(request) : 
    if request.method == "POST":
        form = Ration_admin(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ration detail successfully added!")
            return redirect("User:home")  # Adjust the URL name to your login page
        else:
            messages.error(request, "Unable to add ration details try again")
    else:
        form = Ration_admin()

    context = { 
        "form": form
    }
    return render(request, "ration_card_details.html", context)




# def user_role_context(request):
#     role = None
#     if request.user.is_authenticated:
#         try:
#             # Fetch the user's role from the Beneficiaries model
#             beneficiary = Beneficiaries.objects.get(beneficiary_email=request.user.email)
#             role = beneficiary.beneficiary_type
#         except Beneficiaries.DoesNotExist:
#             role = 'unknown'
#     return {
#         'user_role': role,
#     }