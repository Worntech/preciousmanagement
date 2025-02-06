from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from django.contrib.auth.models import User, auth
from . models import *
from . forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import transaction
from decimal import Decimal

from django.contrib.auth import get_user_model

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.core.mail import send_mail

from django.shortcuts import get_object_or_404

from django.conf import settings

from django.http import HttpResponse, Http404
from django.urls import reverse_lazy

from django.http import FileResponse
from .forms import QRCodeForm
from .models import QRCode
import os

from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)


@login_required(login_url='signin')
def signup(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    if request.method == 'POST':
        # Collect user inputs
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        village = request.POST.get('village')
        ward = request.POST.get('ward')
        district = request.POST.get('district')
        region = request.POST.get('region')
        designation = request.POST.get('designation')
        mobile_number = request.POST.get('mobile')
        nin_number = request.POST.get('nin_number')
        postal_code = request.POST.get('postal_code')
        profile_picture = request.FILES.get('profile_picture')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Validate passwords
        if password == password2:
            if MyUser.objects.filter(email=email).exists():
                messages.error(request, f"Email {email} is already taken")
                return redirect('signup')
            elif MyUser.objects.filter(username=username).exists():
                messages.error(request, f"Username {username} is already taken")
                return redirect('signup')
            else:
                try:
                    with transaction.atomic():
                        user = MyUser.objects.create_user(
                            username=username,
                            email=email,
                            password=password
                        )

                        Staff.objects.create(
                            first_name=first_name,
                            middle_name=middle_name,
                            last_name=last_name,
                            gender=gender,
                            village=village,
                            ward=ward,
                            district=district,
                            region=region,
                            designation=designation,
                            mobile_number=mobile_number,
                            nin_number=nin_number,
                            postal_code=postal_code,
                            email=email,
                            username=username,
                            profile_picture=profile_picture,
                            user = request.user,
                        )

                        messages.success(request, 'Registered successfully.')
                        return redirect('signup')

                except Exception as e:
                    messages.error(request, f"An error occurred: {str(e)}")
                    return redirect('signup')
        else:
            messages.success(request, 'Passwords do not match')
            return redirect('signup')
        
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
    }

    return render(request, 'web/signup.html', context)

@login_required(login_url='signin')
def registervendors(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    if request.method == 'POST':
        # Collect user inputs
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        village = request.POST.get('village')
        ward = request.POST.get('ward')
        district = request.POST.get('district')
        region = request.POST.get('region')
        designation = request.POST.get('designation')
        mobile_number = request.POST.get('mobile')
        nin_number = request.POST.get('nin_number')
        postal_code = request.POST.get('postal_code')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Validate passwords
        if password == password2:
            if MyUser.objects.filter(email=email).exists():
                messages.error(request, f"Email {email} is already taken")
                return redirect('registervendors')
            elif MyUser.objects.filter(username=username).exists():
                messages.error(request, f"Username {username} is already taken")
                return redirect('registervendors')
            else:
                try:
                    with transaction.atomic():
                        user = MyUser.objects.create_user(
                            username=username,
                            email=email,
                            password=password
                        )

                        Staff.objects.create(
                            first_name=first_name,
                            middle_name=middle_name,
                            last_name=last_name,
                            gender=gender,
                            village=village,
                            ward=ward,
                            district=district,
                            region=region,
                            designation=designation,
                            mobile_number=mobile_number,
                            nin_number=nin_number,
                            postal_code=postal_code,
                            email=email,
                            username=username,
                            user = request.user,
                        )

                        messages.success(request, 'Registered successfully.')
                        return redirect('registervendors')

                except Exception as e:
                    messages.error(request, f"An error occurred: {str(e)}")
                    return redirect('registervendors')
        else:
            messages.success(request, 'Passwords do not match')
            return redirect('registervendors')
        
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
    }

    return render(request, 'web/registervendors.html', context)



def signin(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.info(request, 'Loged in succesefull.')
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
            return redirect('signin')

    else:
        return render(request, 'web/signin.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'Loged out succesefull.')
    return redirect('signin')

@login_required(login_url='signin')
def change_password(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    if request.method == 'POST':
        passwordchange = PasswordChangeForm(request.user, request.POST)
        if passwordchange.is_valid():
            user = passwordchange.save()
            
            
            subject = "PRECIOUS HONEY"
            message = f"Hellow {request.user.username} You have changed your password in worntech online services, if not you please contact us through whatsapp +255 710 891 288"
            #from_email = settings.EMAIL_HOST_USER
            from_email = 'worntechservices@gmail.com'
            recipient_list = [user.request.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)
                
            # This is to keep the user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('signin')  # Redirect to the same page after successful password change
        else:
            messages.error(request, 'Please inseart correct information.')
    else:
        passwordchange = PasswordChangeForm(request.user)
    context = {
        'passwordchange': passwordchange,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
    }
    return render(request, 'web/change_password.html', context)

# Custom Password Reset View
class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')

# Custom Password Reset Done View
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

# Custom Password Reset Confirm View
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

# Custom Password Reset Complete View
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
    
def base(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)

    # Pass only the designation to the template
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
    }

    return render(request, 'web/base.html', context)

@login_required(login_url='signin')
def home(request):
    farmers = Farmer.objects.all().count()
    staff = Staff.objects.all().count()
    asset = Asset.objects.all().count()
    masteramount = get_object_or_404(MasterAmount, unique_code='welcomemasterofus')
    
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    allstaff = Staff.objects.all().count()
    vendors = Staff.objects.filter(designation="Vendors").count()
    
    Collection = Staff.objects.filter(designation="Collection Officer").count()
    Store = Staff.objects.filter(designation="Store Keeper").count()
    Finance = Staff.objects.filter(designation="Finance Officer").count()
    Marketing = Staff.objects.filter(designation="Marketing Officer").count()
    Factory = Staff.objects.filter(designation="Factory Manager").count()
    Customer = Staff.objects.filter(designation="Customer").count()
    CEO = Staff.objects.filter(designation="CEO").count()
    farmers = Farmer.objects.all().count()
    productp = MasterProduct.objects.all()
    
    assetsum = AllAsset.objects.filter(unique_code='allasset').first()

    if assetsum:  # Check to avoid potential NoneType errors
        allasset = assetsum.Tables + assetsum.Chairs + assetsum.Computers + assetsum.Motocycles + assetsum.Beehives + assetsum.Packages + assetsum.Labels + assetsum.Buckets + assetsum.Bee_suit + assetsum.Gloves + assetsum.Hire_tools + assetsum.Bee_smoker + assetsum.Honey_press + assetsum.Honey_strainer + assetsum.Sandles + assetsum.Apron
    else:
        allasset = 0
    
    
    context={
        "farmers":farmers,
        "staff":staff,
        "asset":asset,
        "masteramount":masteramount,
        
        "allstaff":allstaff,
        "vendors":vendors,
        "Collection":Collection,
        "Store":Store,
        "Finance":Finance,
        "Marketing":Marketing,
        "Factory":Factory,
        "Customer":Customer,
        "CEO":CEO,
        "farmers":farmers,
        "allasset":allasset,
        "productp":productp,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "gender": staff.gender,
    }
    return render(request, 'web/home.html', context)

def aboutus(request):
    return render(request, 'web/aboutus.html')
def base(request):
    return render(request, 'web/base.html')
def contactus(request):
    return render(request, 'web/contactus.html')
def contactpost(request):
    contactpost = ContactForm()
    if request.method == "POST":
        Full_Name = request.POST.get('Full_Name')
        Email = request.POST.get('Email')
        Message = request.POST.get('Message')
        Phone = request.POST.get('Phone')
        contactpost = ContactForm(request.POST, files=request.FILES)
        if contactpost.is_valid():
            contactpost.save()
            return redirect('contactpost')
    context={
        "contactpost":contactpost
    }
    return render(request, 'web/contactpost.html',context)
@login_required(login_url='signin')
def contactlist(request):
    contactlist = Contact.objects.all()
    countmessage= Contact.objects.all().count()
    context={
        "contactlist":contactlist,
        "countmessage":countmessage
    }
    return render(request, 'web/contactlist.html', context)
@login_required(login_url='signin')
def viewcontact(request, id):
    contact = Contact.objects.get(id=id)
    
    context = {"contact":contact}
    return render(request, 'web/viewcontact.html', context)
@login_required(login_url='signin')
def deletecontact(request, id):
    contact = Contact.objects.get(id=id)
    if request.method == "POST":
        contact.delete()
        return redirect('contactlist')
    
    context = {"contact":contact}
    return render(request, 'web/deletecontact.html', context)


@login_required(login_url='signin')
def dashboard(request):
    return render(request, 'web/dashboard.html')

def services(request):
    return render(request, 'web/services.html')

def shop(request):
    return render(request, 'web/shop.html')

# @login_required(login_url='signin')
# def add_farmers(request):
#     return render(request, 'web/add_farmers.html')

@login_required(login_url='signin')
def add_farmers(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        village = request.POST.get('village')
        ward = request.POST.get('ward')
        district = request.POST.get('district')
        region = request.POST.get('region')
        mobile_number = request.POST.get('mobile')
        nin_number = request.POST.get('nin_number')
        postal_code = request.POST.get('postal_code')
        total_beehives = request.POST.get('total_beehives')
        ttb_beehives = request.POST.get('ttb_beehives')
        top_bar_beehives = request.POST.get('top_bar_beehives')
        tch_beehives = request.POST.get('tch_beehives')
        ktbh_beehives = request.POST.get('ktbh_beehives')
        local_beehives = request.POST.get('local_beehives')
        colonized_beehives = request.POST.get('colonized_beehives')
        uncolonized_beehives = request.POST.get('uncolonized_beehives')
        farmer_background = request.POST.get('farmer_background')
        
        Farmer.objects.create(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            gender=gender,
            village=village,
            ward=ward,
            district=district,
            region=region,
            mobile_number=mobile_number,
            nin_number=nin_number,
            postal_code=postal_code,
            total_beehives=total_beehives,
            ttb_beehives=ttb_beehives,
            top_bar_beehives=top_bar_beehives,
            tch_beehives=tch_beehives,
            ktbh_beehives=ktbh_beehives,
            local_beehives=local_beehives,
            colonized_beehives=colonized_beehives,
            uncolonized_beehives=uncolonized_beehives,
            farmer_background=farmer_background,
            user = request.user,
            )

        messages.success(request, 'Registered successfully.')
        return redirect('add_farmers')
    
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
    }

    return render(request, 'web/add_farmers.html', context)

@login_required(login_url='signin')
def add_asset(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    if request.method == 'POST':
        allasset = AllAsset.objects.filter(unique_code='allasset').first()
        
        asset_name = request.POST.get('asset_name')
        quantity = request.POST.get('quantity')
        
        Asset.objects.create(
            asset_name=asset_name,
            quantity=quantity,
            user = request.user
            )
        
        if not allasset:
            # If the record does not exist, create it
            allasset = AllAsset.objects.create(
            Tables=int(0),
            Chairs=int(0),
            Computers=int(0),
            Motocycles=int(0),
            Beehives=int(0),
            Packages=int(0),
            Labels=int(0),
            Buckets=int(0),
            Bee_suit=int(0),
            Gloves=int(0),
            Hire_tools=int(0),
            Bee_smoker=int(0),
            Honey_press=int(0),
            Honey_strainer=int(0),
            Sandles=int(0),
            Apron=int(0),
            unique_code = 'allasset',
        )
        elif asset_name == "Tables":
            allasset.Tables += int(quantity)
            allasset.Chairs += int(0)
            allasset.Computers += int(0)
            allasset.Motocycles += int(0)
            allasset.Beehives += int(0)
            allasset.Packages += int(0)
            allasset.Labels += int(0)
            allasset.Buckets += int(0)
            allasset.Bee_suit += int(0)
            allasset.Gloves += int(0)
            allasset.Hire_tools += int(0)
            allasset.Bee_smoker += int(0)
            allasset.Honey_press += int(0)
            allasset.Honey_strainer += int(0)
            allasset.Sandles += int(0)
            allasset.Apron += int(0)
            allasset.save()
            
        elif asset_name == "Chairs":
            allasset.Tables += int(0)
            allasset.Chairs += int(quantity)
            allasset.Computers += int(0)
            allasset.Motocycles += int(0)
            allasset.Beehives += int(0)
            allasset.Packages += int(0)
            allasset.Labels += int(0)
            allasset.Buckets += int(0)
            allasset.Bee_suit += int(0)
            allasset.Gloves += int(0)
            allasset.Hire_tools += int(0)
            allasset.Bee_smoker += int(0)
            allasset.Honey_press += int(0)
            allasset.Honey_strainer += int(0)
            allasset.Sandles += int(0)
            allasset.Apron += int(0)
            allasset.save()
            
        elif asset_name == "Computers":
            allasset.Tables += int(0)
            allasset.Chairs += int(0)
            allasset.Computers += int(quantity)
            allasset.Motocycles += int(0)
            allasset.Beehives += int(0)
            allasset.Packages += int(0)
            allasset.Labels += int(0)
            allasset.Buckets += int(0)
            allasset.Bee_suit += int(0)
            allasset.Gloves += int(0)
            allasset.Hire_tools += int(0)
            allasset.Bee_smoker += int(0)
            allasset.Honey_press += int(0)
            allasset.Honey_strainer += int(0)
            allasset.Sandles += int(0)
            allasset.Apron += int(0)
            allasset.save()
            
        elif asset_name == "Motocycles":
            allasset.Tables += int(0)
            allasset.Chairs += int(0)
            allasset.Computers += int(0)
            allasset.Motocycles += int(quantity)
            allasset.Beehives += int(0)
            allasset.Packages += int(0)
            allasset.Labels += int(0)
            allasset.Buckets += int(0)
            allasset.Bee_suit += int(0)
            allasset.Gloves += int(0)
            allasset.Hire_tools += int(0)
            allasset.Bee_smoker += int(0)
            allasset.Honey_press += int(0)
            allasset.Honey_strainer += int(0)
            allasset.Sandles += int(0)
            allasset.Apron += int(0)
            allasset.save()
            
        elif asset_name == "Beehives":
            allasset.Tables += int(0)
            allasset.Chairs += int(0)
            allasset.Computers += int(0)
            allasset.Motocycles += int(0)
            allasset.Beehives += int(quantity)
            allasset.Packages += int(0)
            allasset.Labels += int(0)
            allasset.Buckets += int(0)
            allasset.Bee_suit += int(0)
            allasset.Gloves += int(0)
            allasset.Hire_tools += int(0)
            allasset.Bee_smoker += int(0)
            allasset.Honey_press += int(0)
            allasset.Honey_strainer += int(0)
            allasset.Sandles += int(0)
            allasset.Apron += int(0)
            allasset.save()
            
        elif asset_name == "Packages":
            allasset.Tables += int(0)
            allasset.Chairs += int(0)
            allasset.Computers += int(0)
            allasset.Motocycles += int(0)
            allasset.Beehives += int(0)
            allasset.Packages += int(quantity)
            allasset.Labels += int(0)
            allasset.Buckets += int(0)
            allasset.Bee_suit += int(0)
            allasset.Gloves += int(0)
            allasset.Hire_tools += int(0)
            allasset.Bee_smoker += int(0)
            allasset.Honey_press += int(0)
            allasset.Honey_strainer += int(0)
            allasset.Sandles += int(0)
            allasset.Apron += int(0)
            allasset.save()
            
        elif asset_name == "Labels":
            allasset.Tables += int(0)
            allasset.Chairs += int(0)
            allasset.Computers += int(0)
            allasset.Motocycles += int(0)
            allasset.Beehives += int(0)
            allasset.Packages += int(0)
            allasset.Labels += int(quantity)
            allasset.Buckets += int(0)
            allasset.Bee_suit += int(0)
            allasset.Gloves += int(0)
            allasset.Hire_tools += int(0)
            allasset.Bee_smoker += int(0)
            allasset.Honey_press += int(0)
            allasset.Honey_strainer += int(0)
            allasset.Sandles += int(0)
            allasset.Apron += int(0)
            allasset.save()
            
        elif asset_name == "Buckets":
            allasset.Tables += int(0)
            allasset.Chairs += int(0)
            allasset.Computers += int(0)
            allasset.Motocycles += int(0)
            allasset.Beehives += int(0)
            allasset.Packages += int(0)
            allasset.Labels += int(0)
            allasset.Buckets += int(quantity)
            allasset.Bee_suit += int(0)
            allasset.Gloves += int(0)
            allasset.Hire_tools += int(0)
            allasset.Bee_smoker += int(0)
            allasset.Honey_press += int(0)
            allasset.Honey_strainer += int(0)
            allasset.Sandles += int(0)
            allasset.Apron += int(0)
            allasset.save()
            
        elif asset_name == "Bee_suit":
            allasset.Tables += int(0)
            allasset.Chairs += int(0)
            allasset.Computers += int(0)
            allasset.Motocycles += int(0)
            allasset.Beehives += int(0)
            allasset.Packages += int(0)
            allasset.Labels += int(0)
            allasset.Buckets += int(0)
            allasset.Bee_suit += int(quantity)
            allasset.Gloves += int(0)
            allasset.Hire_tools += int(0)
            allasset.Bee_smoker += int(0)
            allasset.Honey_press += int(0)
            allasset.Honey_strainer += int(0)
            allasset.Sandles += int(0)
            allasset.Apron += int(0)
            allasset.save()
            
        elif asset_name == "Gloves":
            allasset.Tables += int(0)
            allasset.Chairs += int(0)
            allasset.Computers += int(0)
            allasset.Motocycles += int(0)
            allasset.Beehives += int(0)
            allasset.Packages += int(0)
            allasset.Labels += int(0)
            allasset.Buckets += int(0)
            allasset.Bee_suit += int(0)
            allasset.Gloves += int(quantity)
            allasset.Hire_tools += int(0)
            allasset.Bee_smoker += int(0)
            allasset.Honey_press += int(0)
            allasset.Honey_strainer += int(0)
            allasset.Sandles += int(0)
            allasset.Apron += int(0)
            allasset.save()
            
        elif asset_name == "Hire_tools":
            allasset.Tables += int(0)
            allasset.Chairs += int(0)
            allasset.Computers += int(0)
            allasset.Motocycles += int(0)
            allasset.Beehives += int(0)
            allasset.Packages += int(0)
            allasset.Labels += int(0)
            allasset.Buckets += int(0)
            allasset.Bee_suit += int(0)
            allasset.Gloves += int(0)
            allasset.Hire_tools += int(quantity)
            allasset.Bee_smoker += int(0)
            allasset.Honey_press += int(0)
            allasset.Honey_strainer += int(0)
            allasset.Sandles += int(0)
            allasset.Apron += int(0)
            allasset.save()
            
        elif asset_name == "Bee_smoker":
            allasset.Tables += int(0)
            allasset.Chairs += int(0)
            allasset.Computers += int(0)
            allasset.Motocycles += int(0)
            allasset.Beehives += int(0)
            allasset.Packages += int(0)
            allasset.Labels += int(0)
            allasset.Buckets += int(0)
            allasset.Bee_suit += int(0)
            allasset.Gloves += int(0)
            allasset.Hire_tools += int(0)
            allasset.Bee_smoker += int(quantity)
            allasset.Honey_press += int(0)
            allasset.Honey_strainer += int(0)
            allasset.Sandles += int(0)
            allasset.Apron += int(0)
            allasset.save()
            
        elif asset_name == "Honey_press":
            allasset.Tables += int(0)
            allasset.Chairs += int(0)
            allasset.Computers += int(0)
            allasset.Motocycles += int(0)
            allasset.Beehives += int(0)
            allasset.Packages += int(0)
            allasset.Labels += int(0)
            allasset.Buckets += int(0)
            allasset.Bee_suit += int(0)
            allasset.Gloves += int(0)
            allasset.Hire_tools += int(0)
            allasset.Bee_smoker += int(0)
            allasset.Honey_press += int(quantity)
            allasset.Honey_strainer += int(0)
            allasset.Sandles += int(0)
            allasset.Apron += int(0)
            allasset.save()
            
        elif asset_name == "Honey_strainer":
            allasset.Tables += int(0)
            allasset.Chairs += int(0)
            allasset.Computers += int(0)
            allasset.Motocycles += int(0)
            allasset.Beehives += int(0)
            allasset.Packages += int(0)
            allasset.Labels += int(0)
            allasset.Buckets += int(0)
            allasset.Bee_suit += int(0)
            allasset.Gloves += int(0)
            allasset.Hire_tools += int(0)
            allasset.Bee_smoker += int(0)
            allasset.Honey_press += int(0)
            allasset.Honey_strainer += int(quantity)
            allasset.Sandles += int(0)
            allasset.Apron += int(0)
            allasset.save()
            
        elif asset_name == "Sandles":
            allasset.Tables += int(0)
            allasset.Chairs += int(0)
            allasset.Computers += int(0)
            allasset.Motocycles += int(0)
            allasset.Beehives += int(0)
            allasset.Packages += int(0)
            allasset.Labels += int(0)
            allasset.Buckets += int(0)
            allasset.Bee_suit += int(0)
            allasset.Gloves += int(0)
            allasset.Hire_tools += int(0)
            allasset.Bee_smoker += int(0)
            allasset.Honey_press += int(0)
            allasset.Honey_strainer += int(0)
            allasset.Sandles += int(quantity)
            allasset.Apron += int(0)
            allasset.save()
            
        elif asset_name == "Apron":
            allasset.Tables += int(0)
            allasset.Chairs += int(0)
            allasset.Computers += int(0)
            allasset.Motocycles += int(0)
            allasset.Beehives += int(0)
            allasset.Packages += int(0)
            allasset.Labels += int(0)
            allasset.Buckets += int(0)
            allasset.Bee_suit += int(0)
            allasset.Gloves += int(0)
            allasset.Hire_tools += int(0)
            allasset.Bee_smoker += int(0)
            allasset.Honey_press += int(0)
            allasset.Honey_strainer += int(0)
            allasset.Sandles += int(0)
            allasset.Apron += int(quantity)
            allasset.save()
            
        else:
            allasset.Tables += int(0)
            allasset.Chairs += int(0)
            allasset.Computers += int(0)
            allasset.Motocycles += int(0)
            allasset.Beehives += int(0)
            allasset.Packages += int(0)
            allasset.Labels += int(0)
            allasset.Buckets += int(0)
            allasset.Bee_suit += int(0)
            allasset.Gloves += int(0)
            allasset.Hire_tools += int(0)
            allasset.Bee_smoker += int(0)
            allasset.Honey_press += int(0)
            allasset.Honey_strainer += int(0)
            allasset.Sandles += int(0)
            allasset.Apron += int(0)
            allasset.save()
            
        messages.success(request, 'Added successfully.')
        return redirect('add_asset')
    
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
    }

    return render(request, 'web/add_asset.html', context)

@login_required(login_url='signin')
def add_product(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    if request.method == 'POST':
        seller_name = request.POST.get('seller_name')
        product_name = request.POST.get('product_name')
        barcode = request.POST.get('barcode')
        weight = request.POST.get('weight')
        
        ProductBuy.objects.create(
            seller_name=seller_name,
            product_name=product_name,
            barcode=barcode,
            weight=weight,
            status = "Submitted",
            user = request.user
            )

        messages.success(request, 'Added successfully.')
        return redirect('add_product')
    
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
    }

    return render(request, 'web/add_product.html', context)

@login_required(login_url='signin')
def moneyin(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    if request.method == 'POST':
        money_source = request.POST.get('money_source')
        amount = request.POST.get('amount')
        money_processor = request.POST.get('money_processor')
        
        Moneyin.objects.create(
            money_source=money_source,
            amount=amount,
            money_processor=money_processor,
            user = request.user
            )
        
        masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
        if not masteramount:
            masteramount = MasterAmount.objects.create(
            amount=Decimal(amount),
            unique_code = 'welcomemasterofus',
        )
        else:
            masteramount.amount += Decimal(amount)
            masteramount.save()
        messages.success(request, 'Added successfully.')
        return redirect('moneyin')
    
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
    }

    return render(request, 'web/moneyin.html', context)

@login_required(login_url='signin')
def moneyout(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    if request.method == 'POST':
        purpose = request.POST.get('purpose')
        amount = request.POST.get('amount')
        money_user = request.POST.get('money_user')
        
        Moneyout.objects.create(
            purpose=purpose,
            amount=amount,
            money_user=money_user,
            user = request.user
            )
        
        masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
        masteramount.amount -= Decimal(amount)
        masteramount.save()

        messages.success(request, 'Added successfully.')
        return redirect('moneyout')
    
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
    }

    return render(request, 'web/moneyout.html', context)

@login_required(login_url='signin')
def paysalary(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    if request.method == 'POST':
        payed_Name = request.POST.get('payed_Name')
        amount = request.POST.get('amount')
        paymentperiod = request.POST.get('paymentperiod')
        
        Salary.objects.create(
            payed_Name=payed_Name,
            amount=amount,
            paymentperiod=paymentperiod,
            user = request.user
            )
        
        masteramount = MasterAmount.objects.filter(unique_code='welcomemasterofus').first()
        masteramount.amount -= Decimal(amount)
        masteramount.save()

        messages.success(request, 'Added successfully.')
        return redirect('paysalary')
    
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
    }

    return render(request, 'web/paysalary.html', context)

@login_required(login_url='signin')
def addproduct(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    if request.method == 'POST':
        used_rawmaterial = request.POST.get('used_rawmaterial')
        honey = request.POST.get('honey')
        wax = request.POST.get('wax')
        comment = request.POST.get('comment')
        
        Product.objects.create(
            used_rawmaterial=used_rawmaterial,
            honey=honey,
            wax=wax,
            comment=comment,
            status = "Submitted",
            user = request.user
            )

        messages.success(request, 'Added successfully.')
        return redirect('addproduct')
    
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
    }

    return render(request, 'web/addproduct.html', context)

@login_required(login_url='signin')
def addmaterial(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    if request.method == 'POST':
        wax = request.POST.get('wax')
        comb_honey = request.POST.get('comb_honey')
        honey = request.POST.get('honey')
        comment = request.POST.get('comment')
        
        Material.objects.create(
            wax=wax,
            comb_honey=comb_honey,
            honey=honey,
            comment=comment,
            status = "Submitted",
            user = request.user
            )

        messages.success(request, 'Added successfully.')
        return redirect('addmaterial')
    
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
    }

    return render(request, 'web/addmaterial.html', context)

@login_required(login_url='signin')
def moneyrequest(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    if request.method == 'POST':
        purpose = request.POST.get('purpose')
        amount = request.POST.get('amount')
        
        MoneyRequest.objects.create(
            purpose=purpose,
            amount=amount,
            completecheck = "None",
            status = "Requested",
            user = request.user
            )

        messages.success(request, 'Added successfully.')
        return redirect('moneyrequest')
    
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
    }

    return render(request, 'web/moneyrequest.html', context)

@login_required(login_url='signin')
def productin(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    if request.method == 'POST':
        honey = request.POST.get('honey')
        wax = request.POST.get('wax')
        
        Productin.objects.create(
            honey=honey,
            wax=wax,
            user = request.user
            )
        
        masterproduct = MasterProduct.objects.filter(unique_code='masterproduct').first()
        masterproduct.honey += Decimal(honey)
        masterproduct.wax += Decimal(wax)
        masterproduct.save()

        messages.success(request, 'Added successfully.')
        return redirect('productin')
    
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
    }

    return render(request, 'web/productin.html', context)

@login_required(login_url='signin')
def productout(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    if request.method == 'POST':
        honey = request.POST.get('honey')
        wax = request.POST.get('wax')
        
        Productout.objects.create(
            honey=honey,
            wax=wax,
            user = request.user
            )
        
        masterproduct = MasterProduct.objects.filter(unique_code='masterproduct').first()
        masterproduct.honey -= Decimal(honey)
        masterproduct.wax -= Decimal(wax)
        masterproduct.save()

        messages.success(request, 'Added successfully.')
        return redirect('productout')
    
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
    }

    return render(request, 'web/productout.html', context)

@login_required(login_url='signin')
def allstaff(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    staff_members = Staff.objects.all()
    context = {
        'staff_members': staff_members,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/allstaff.html', context)

@login_required(login_url='signin')
def allvendors(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    staff_members = Staff.objects.all()
    context = {
        'staff_members': staff_members,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/allvendors.html', context)

@login_required(login_url='signin')
def allfarmers(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    allfarmers = Farmer.objects.all()
    context = {
        'allfarmers': allfarmers,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/allfarmers.html', context)

@login_required(login_url='signin')
def assethistory(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    assethistory = Asset.objects.all()
    context = {
        'assethistory': assethistory,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/assethistory.html', context)

@login_required(login_url='signin')
def allasset(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    # Check if an AllAsset with the unique_code exists
    allasset = AllAsset.objects.filter(unique_code='allasset').first()
    
    if allasset is None:
        # If the record does not exist, create it
        allasset = AllAsset.objects.create(
            Tables=0,
            Chairs=0,
            Computers=0,
            Motocycles=0,
            Beehives=0,
            Packages=0,
            Labels=0,
            Buckets=0,
            Bee_suit=0,
            Gloves=0,
            Hire_tools=0,
            Bee_smoker=0,
            Honey_press=0,
            Honey_strainer=0,
            Sandles=0,
            Apron=0,
            unique_code='allasset',
        )
    
    # Fetch all AllAsset records (if needed)
    allassetss = AllAsset.objects.all()

    context = {
        'allasset': allasset,
        'allassetss': allassetss,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
    }
    return render(request, 'web/allasset.html', context)

@login_required(login_url='signin')
def moneyinlist(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    moneyin = Moneyin.objects.all()
    context = {
        'moneyin': moneyin,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/moneyinlist.html', context)

@login_required(login_url='signin')
def moneyoutlist(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    moneyout = Moneyout.objects.all()
    context = {
        'moneyout': moneyout,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/moneyoutlist.html', context)

@login_required(login_url='signin')
def honeyproduct(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    product = ProductBuy.objects.all()
    context = {
        'product': product,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/honeyproduct.html', context)

@login_required(login_url='signin')
def payedsalary(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    salary = Salary.objects.all()
    context = {
        'salary': salary,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/payedsalary.html', context)

@login_required(login_url='signin')
def comb_honey(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    product = ProductBuy.objects.all()
    context = {
        'product': product,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/comb_honey.html', context)
@login_required(login_url='signin')
def honey(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    product = ProductBuy.objects.all()
    context = {
        'product': product,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/honey.html', context)

@login_required(login_url='signin')
def wax(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    product = ProductBuy.objects.all()
    context = {
        'product': product,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/wax.html', context)

@login_required(login_url='signin')
def requestedmoney(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    moneyrequest = MoneyRequest.objects.filter(status = "Requested")
    context = {
        'moneyrequest': moneyrequest,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/requestedmoney.html', context)

@login_required(login_url='signin')
def acceptedmoney(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    moneyrequest = MoneyRequest.objects.filter(status = "Accepted")
    context = {
        'moneyrequest': moneyrequest,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/acceptedmoney.html', context)

@login_required(login_url='signin')
def completedmoney(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    moneyrequest = MoneyRequest.objects.filter(status = "Completed")
    context = {
        'moneyrequest': moneyrequest,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/completedmoney.html', context)

@login_required(login_url='signin')
def declinedmoney(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    moneyrequest = MoneyRequest.objects.filter(status = "Declined")
    context = {
        'moneyrequest': moneyrequest,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/declinedmoney.html', context)

@login_required(login_url='signin')
def myrequest(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    moneyrequest = MoneyRequest.objects.filter(user=request.user)
    context = {
        'moneyrequest': moneyrequest,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/myrequest.html', context)

@login_required(login_url='signin')
def allproduct(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    allproduct = Product.objects.all()
    context = {
        'allproduct': allproduct,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/allproduct.html', context)

@login_required(login_url='signin')
def allmaterial(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    allmaterial = Material.objects.all()
    context = {
        'allmaterial': allmaterial,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/allmaterial.html', context)

@login_required(login_url='signin')
def stockadded(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    stockadded = Productin.objects.all()
    context = {
        'stockadded': stockadded,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/stockadded.html', context)

@login_required(login_url='signin')
def stockremoved(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    stockremoved = Productout.objects.all()
    context = {
        'stockremoved': stockremoved,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/stockremoved.html', context)

@login_required(login_url='signin')
def allstock(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    # Check if an MasterProduct with the unique_code exists
    allstock = MasterProduct.objects.filter(unique_code='masterproduct').first()
    
    if allstock is None:
        # If the record does not exist, create it
        allstock = MasterProduct.objects.create(
            honey=0,
            wax=0,
            unique_code='masterproduct',
        )
        
    allstocks = MasterProduct.objects.all()
    context = {
        'allstock': allstock,
        'allstocks': allstocks,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
    }
    return render(request, 'web/allstock.html', context)


# VIEW TO VIEW THE INFORMATIONS
@login_required(login_url='signin')
def viewfarmer(request, id):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    farmerview = Farmer.objects.get(id=id)
    
    context = {
        "farmerview":farmerview,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/viewfarmer.html', context)

@login_required(login_url='signin')
def viewstaff(request, id):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    staffview = Staff.objects.get(id=id)
    
    context = {
        "staffview":staffview,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/viewstaff.html', context)

class viewmoneyrequest(DetailView):
    model = MoneyRequest
    template_name = 'web/viewmoneyrequest.html'
    form_class = CommentMoneyRequestForm

    def post(self, request, *args, **kwargs):
        form = CommentMoneyRequestForm(request.POST)
        money_request = self.get_object()
        if form.is_valid():
            form.instance.user = request.user
            form.instance.Title = money_request
            form.save()
            messages.success(request, "Comment added successfully")
            return redirect(reverse("viewmoneyrequest", kwargs={'pk': money_request.pk}))
        else:
            messages.error(request, "There was an error adding your comment.")
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_comments = CommentMoneyRequest.objects.filter(Title=self.object)
        staff = get_object_or_404(Staff, email=self.request.user.email, username=self.request.user.username)
        context.update({
            'form': kwargs.get('form', CommentMoneyRequestForm()),
            'post_comments': post_comments,
            "designation": staff.designation,
            "first_name": staff.first_name,
            "last_name": staff.last_name,
        })
        return context
    
class viewproductbuy(DetailView):
    model = ProductBuy
    template_name = 'web/viewproductbuy.html'
    form_class = CommentProductBuyForm

    def post(self, request, *args, **kwargs):
        form = CommentProductBuyForm(request.POST)
        money_request = self.get_object()
        if form.is_valid():
            form.instance.user = request.user
            form.instance.Title = money_request
            form.save()
            messages.success(request, "Comment added successfully")
            return redirect(reverse("viewproductbuy", kwargs={'pk': money_request.pk}))
        else:
            messages.error(request, "There was an error adding your comment.")
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_comments = CommentProductBuy.objects.filter(Title=self.object)
        staff = get_object_or_404(Staff, email=self.request.user.email, username=self.request.user.username)
        context.update({
            'form': kwargs.get('form', CommentProductBuyForm()),
            'post_comments': post_comments,
            "designation": staff.designation,
            "first_name": staff.first_name,
            "last_name": staff.last_name,
        })
        return context
    
@login_required(login_url='signin')
def viewmoneyin(request, id):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    moneyinview = Moneyin.objects.get(id=id)
    
    context = {
        "moneyinview":moneyinview,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/viewmoneyin.html', context)

@login_required(login_url='signin')
def viewmoneyout(request, id):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    moneyoutview = Moneyout.objects.get(id=id)
    
    context = {
        "moneyoutview":moneyoutview,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/viewmoneyout.html', context)

# UPDATING INFORMATIONS
@login_required(login_url='signin')
def updatefarmer(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    farmer_instance = get_object_or_404(Farmer, pk=pk)  # Fetch farmer or return 404 if not found

    if request.method == "POST":
        # Extract data from request.POST and request.FILES manually
        farmer_instance.first_name = request.POST.get("first_name")
        farmer_instance.middle_name = request.POST.get("middle_name")
        farmer_instance.last_name = request.POST.get("last_name")
        farmer_instance.gender = request.POST.get("gender")
        farmer_instance.village = request.POST.get("village")
        farmer_instance.ward = request.POST.get("ward")
        farmer_instance.district = request.POST.get("district")
        farmer_instance.region = request.POST.get("region")
        farmer_instance.mobile_number = request.POST.get("mobile")
        farmer_instance.nin_number = request.POST.get("nin_number")
        farmer_instance.postal_code = request.POST.get("postal_code")
        farmer_instance.total_beehives = request.POST.get("total_beehives")
        farmer_instance.ttb_beehives = request.POST.get("ttb_beehives")
        farmer_instance.top_bar_beehives = request.POST.get("top_bar_beehives")
        farmer_instance.tch_beehives = request.POST.get("tch_beehives")
        farmer_instance.ktbh_beehives = request.POST.get("ktbh_beehives")
        farmer_instance.local_beehives = request.POST.get("local_beehives")
        farmer_instance.colonized_beehives = request.POST.get("colonized_beehives")
        farmer_instance.uncolonized_beehives = request.POST.get("uncolonized_beehives")
        farmer_instance.farmer_background = request.POST.get("farmer_background")
        
        try:
            farmer_instance.save()
            messages.success(request, "Farmer updated successfully.")
            return redirect('allfarmers')
        except Exception as e:
            messages.error(request, f"Error updating farmer: {str(e)}")
    else:
        messages.info(request, "update the farmer's information")

    context = {
        "farmer_instance": farmer_instance,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/updatefarmer.html', context)

@login_required(login_url='signin')
def updatestaff(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    staff_instance = get_object_or_404(Staff, pk=pk)  # Fetch Staff or return 404 if not found

    if request.method == "POST":
        # Extract data from request.POST and request.FILES manually
        staff_instance.first_name = request.POST.get("first_name")
        staff_instance.middle_name = request.POST.get("middle_name")
        staff_instance.last_name = request.POST.get("last_name")
        staff_instance.gender = request.POST.get("gender")
        staff_instance.village = request.POST.get("village")
        staff_instance.ward = request.POST.get("ward")
        staff_instance.district = request.POST.get("district")
        staff_instance.region = request.POST.get("region")
        staff_instance.designation = request.POST.get("designation")
        staff_instance.mobile_number = request.POST.get("mobile")
        staff_instance.nin_number = request.POST.get("nin_number")
        staff_instance.postal_code = request.POST.get("postal_code")
        staff_instance.email = request.POST.get("email")
        staff_instance.username = request.POST.get("username")
        staff_instance.profile_picture = request.FILES.get('profile_picture')
        
        myuser_instance = get_object_or_404(MyUser, email = staff_instance.email, username = staff_instance.username)
        
        try:
            staff_instance.save()
            messages.success(request, "Staff updated successfully.")
            
            myuser_instance.email = staff_instance.email
            myuser_instance.username = staff_instance.username
            myuser_instance.save
            
            return redirect('allstaff')
        except Exception as e:
            messages.error(request, f"Error updating staff: {str(e)}")
    else:
        messages.info(request, "update the staff's information")

    context = {
        "staff_instance": staff_instance,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/updatestaff.html', context)

@login_required(login_url='signin')
def updateasset(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    asset_instance = get_object_or_404(Asset, pk=pk)  # Fetch farmer or return 404 if not found

    if request.method == "POST":
        # Extract data from request.POST and request.FILES manually
        asset_instance.asset_name = request.POST.get("asset_name")
        asset_instance.quantity = request.POST.get("quantity")
        
        try:
            asset_instance.save()
            messages.success(request, "Asset updated successfully.")
            return redirect('assethistory')
        except Exception as e:
            messages.error(request, f"Error updating Asset: {str(e)}")
    else:
        messages.info(request, "update the Asset's information")

    context = {
        "asset_instance": asset_instance,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/updateasset.html', context)

@login_required(login_url='signin')
def updateallasset(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    allasset_instance = get_object_or_404(AllAsset, pk=pk)  # Fetch Staff or return 404 if not found

    if request.method == "POST":
        # Extract data from request.POST and request.FILES manually
        allasset_instance.Tables = request.POST.get("Tables")
        allasset_instance.Chairs = request.POST.get("Chairs")
        allasset_instance.Computers = request.POST.get("Computers")
        allasset_instance.Motocycles = request.POST.get("Motocycles")
        allasset_instance.Beehives = request.POST.get("Beehives")
        allasset_instance.Packages = request.POST.get("Packages")
        allasset_instance.Labels = request.POST.get("Labels")
        allasset_instance.Buckets = request.POST.get("Buckets")
        allasset_instance.Bee_suit = request.POST.get("Bee_suit")
        allasset_instance.Gloves = request.POST.get("Gloves")
        allasset_instance.Hire_tools = request.POST.get("Hire_tools")
        allasset_instance.Bee_smoker = request.POST.get("Bee_smoker")
        allasset_instance.Honey_press = request.POST.get("Honey_press")
        allasset_instance.Honey_strainer = request.POST.get("Honey_strainer")
        allasset_instance.Sandles = request.POST.get("Sandles")
        allasset_instance.Apron = request.POST.get("Apron")
        
        try:
            allasset_instance.save()
            messages.success(request, "Asset updated successfully.")
            
            return redirect('allasset')
        except Exception as e:
            messages.error(request, f"Error updating asset: {str(e)}")
    else:
        messages.info(request, "update the asset's information")

    context = {
        "allasset_instance": allasset_instance,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/updateallasset.html', context)

@login_required(login_url='signin')
def updateallstock(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    allstock_instance = get_object_or_404(MasterProduct, pk=pk)  # Fetch Staff or return 404 if not found

    if request.method == "POST":
        allstock_instance.honey = request.POST.get("honey")
        allstock_instance.wax = request.POST.get("wax")
        
        try:
            allstock_instance.save()
            messages.success(request, "Stock updated successfully.")
            
            return redirect('allstock')
        except Exception as e:
            messages.error(request, f"Error updating stock: {str(e)}")
    else:
        messages.info(request, "update the stock's information")

    context = {
        "allstock_instance": allstock_instance,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/updateallstock.html', context)

@login_required(login_url='signin')
def updatemoneyrequested(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    requestedmoney_instance = get_object_or_404(MoneyRequest, pk=pk)

    if request.method == "POST":
        requestedmoney_instance.purpose = request.POST.get("purpose")
        requestedmoney_instance.amount = request.POST.get("amount")
        
        try:
            requestedmoney_instance.save()
            messages.success(request, "Request updated successfully.")
            return redirect('requestedmoney')
        except Exception as e:
            messages.error(request, f"Error updating Request: {str(e)}")
    else:
        messages.info(request, "update the Request's information")

    context = {
        "requestedmoney_instance": requestedmoney_instance,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/updatemoneyrequested.html', context)

@login_required(login_url='signin')
def updateproductbuy(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    productbuy_instance = get_object_or_404(ProductBuy, pk=pk)

    if request.method == "POST":
        productbuy_instance.seller_name = request.POST.get("seller_name")
        productbuy_instance.product_name = request.POST.get("product_name")
        productbuy_instance.barcode = request.POST.get("barcode")
        productbuy_instance.weight = request.POST.get("weight")
        
        try:
            productbuy_instance.save()
            messages.success(request, "Product updated successfully.")
            return redirect('viewproductbuy', productbuy_instance.pk)
        except Exception as e:
            messages.error(request, f"Error updating Product: {str(e)}")
    else:
        messages.info(request, "update the Product's information")

    context = {
        "productbuy_instance": productbuy_instance,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/updateproductbuy.html', context)

@login_required(login_url='signin')
def updatepayedsalary(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    payedsalary_instance = get_object_or_404(Salary, pk=pk)

    if request.method == "POST":
        payedsalary_instance.payed_Name = request.POST.get("payed_Name")
        payedsalary_instance.paymentperiod = request.POST.get("paymentperiod")
        payedsalary_instance.amount = request.POST.get("amount")
        
        try:
            payedsalary_instance.save()
            messages.success(request, "Salary updated successfully.")
            return redirect('payedsalary')
        except Exception as e:
            messages.error(request, f"Error updating Salary: {str(e)}")
    else:
        messages.info(request, "update the Salary's information will not update the total amount, edit total amount manually.")

    context = {
        "payedsalary_instance": payedsalary_instance,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/updatepayedsalary.html', context)

@login_required(login_url='signin')
def updateallproduct(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    allproduct_instance = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        allproduct_instance.used_rawmaterial = request.POST.get("used_rawmaterial")
        allproduct_instance.honey = request.POST.get("honey")
        allproduct_instance.wax = request.POST.get("wax")
        allproduct_instance.comment = request.POST.get("comment")
        
        try:
            allproduct_instance.save()
            messages.success(request, "Product updated successfully.")
            return redirect('allproduct')
        except Exception as e:
            messages.error(request, f"Error updating Product: {str(e)}")
    else:
        messages.info(request, "update the Product's information.")

    context = {
        "allproduct_instance": allproduct_instance,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/updateallproduct.html', context)

@login_required(login_url='signin')
def updateallmaterial(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    allmaterial_instance = get_object_or_404(Material, pk=pk)

    if request.method == "POST":
        allmaterial_instance.comb_honey = request.POST.get("comb_honey")
        allmaterial_instance.honey = request.POST.get("honey")
        allmaterial_instance.wax = request.POST.get("wax")
        allmaterial_instance.comment = request.POST.get("comment")
        
        try:
            allmaterial_instance.save()
            messages.success(request, "Material updated successfully.")
            return redirect('allmaterial')
        except Exception as e:
            messages.error(request, f"Error updating Material: {str(e)}")
    else:
        messages.info(request, "update the Material's information.")

    context = {
        "allmaterial_instance": allmaterial_instance,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/updateallmaterial.html', context)

@login_required(login_url='signin')
def updatemoneyin(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    moneyin_instance = get_object_or_404(Moneyin, pk=pk)

    if request.method == "POST":
        moneyin_instance.money_processor = request.POST.get("money_processor")
        moneyin_instance.money_source = request.POST.get("money_source")
        moneyin_instance.amount = request.POST.get("amount")
        
        try:
            moneyin_instance.save()
            messages.success(request, "Money updated successfully.")
            return redirect('moneyinlist')
        except Exception as e:
            messages.error(request, f"Error updating Gained Money: {str(e)}")
    else:
        messages.info(request, "update the gained money's information will not update the total amount, edit total amount manually.")

    context = {
        "moneyin_instance": moneyin_instance,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/updatemoneyin.html', context)

@login_required(login_url='signin')
def updatemoneyout(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    moneyout_instance = get_object_or_404(Moneyout, pk=pk)

    if request.method == "POST":
        moneyout_instance.money_user = request.POST.get("money_user")
        moneyout_instance.purpose = request.POST.get("purpose")
        moneyout_instance.amount = request.POST.get("amount")
        
        try:
            moneyout_instance.save()
            messages.success(request, "Uses updated successfully.")
            return redirect('moneyoutlist')
        except Exception as e:
            messages.error(request, f"Error updating Uses: {str(e)}")
    else:
        messages.info(request, "update the Uses's information will not update the total amount, edit total amount manually.")

    context = {
        "moneyout_instance": moneyout_instance,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/updatemoneyout.html', context)

@login_required(login_url='signin')
def updateproductin(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    productin_instance = get_object_or_404(Productin, pk=pk)

    if request.method == "POST":
        productin_instance.honey = request.POST.get("honey")
        productin_instance.wax = request.POST.get("wax")
        
        try:
            productin_instance.save()
            messages.success(request, "Product updated successfully.")
            return redirect('stockadded')
        except Exception as e:
            messages.error(request, f"Error updating Product: {str(e)}")
    else:
        messages.info(request, "update the Product's information.")

    context = {
        "productin_instance": productin_instance,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/updateproductin.html', context)

@login_required(login_url='signin')
def updateproductout(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    
    productout_instance = get_object_or_404(Productout, pk=pk)

    if request.method == "POST":
        productout_instance.honey = request.POST.get("honey")
        productout_instance.wax = request.POST.get("wax")
        
        try:
            productout_instance.save()
            messages.success(request, "Product updated successfully.")
            return redirect('stockremoved')
        except Exception as e:
            messages.error(request, f"Error updating Product: {str(e)}")
    else:
        messages.info(request, "update the Product's information.")

    context = {
        "productout_instance": productout_instance,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        }
    return render(request, 'web/updateproductout.html', context)

@login_required(login_url='signin')
def deletefarmer(request, pk):
    farmerdelete = get_object_or_404(Farmer, pk=pk)
    if request.method == "POST":
        farmerdelete.delete()
        messages.success(request, "Farmer deleted successfully.")
        return redirect('allfarmers')
    return redirect('allfarmers')

@login_required(login_url='signin')
def deletestaff(request, pk):
    staffdelete = get_object_or_404(Staff, pk=pk)
    if request.method == "POST":
        staffdelete.delete()
        messages.success(request, "Staff deleted successfully.")
        return redirect('allstaff')
    return redirect('allstaff')

@login_required(login_url='signin')
def deleteasset(request, pk):
    assetdelete = get_object_or_404(Asset, pk=pk)
    if request.method == "POST":
        assetdelete.delete()
        messages.success(request, "Asset deleted successfully.")
        return redirect('assethistory')
    return redirect('assethistory')

@login_required(login_url='signin')
def deleteallasset(request, pk):
    allassetdelete = get_object_or_404(AllAsset, pk=pk)
    if request.method == "POST":
        allassetdelete.delete()
        messages.success(request, "Assets deleted successfully.")
        return redirect('allasset')
    return redirect('allasset')

@login_required(login_url='signin')
def deleteallstack(request, pk):
    allstockdelete = get_object_or_404(MasterProduct, pk=pk)
    if request.method == "POST":
        allstockdelete.delete()
        messages.success(request, "Stock deleted successfully.")
        return redirect('allstock')
    return redirect('allstock')

@login_required(login_url='signin')
def deletemoneyrequest(request, pk):
    moneyrequestdelete = get_object_or_404(MoneyRequest, pk=pk)
    if request.method == "POST":
        moneyrequestdelete.delete()
        messages.success(request, "Request deleted successfully.")
        return redirect('requestedmoney')
    return redirect('requestedmoney')

@login_required(login_url='signin')
def deleteproductbuyw(request, pk):
    productbuydelete = get_object_or_404(ProductBuy, pk=pk)
    if request.method == "POST":
        productbuydelete.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('wax')
    return redirect('wax')

@login_required(login_url='signin')
def deleteproductbuyc(request, pk):
    productbuydelete = get_object_or_404(ProductBuy, pk=pk)
    if request.method == "POST":
        productbuydelete.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('comb_honey')
    return redirect('comb_honey')

@login_required(login_url='signin')
def deleteproductbuyh(request, pk):
    productbuydelete = get_object_or_404(ProductBuy, pk=pk)
    if request.method == "POST":
        productbuydelete.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('honey')
    return redirect('honey')

@login_required(login_url='signin')
def deletepayedsalary(request, pk):
    payedsalarydelete = get_object_or_404(Salary, pk=pk)
    if request.method == "POST":
        payedsalarydelete.delete()
        messages.success(request, "Salary deleted successfully.")
        return redirect('payedsalary')
    return redirect('payedsalary')

@login_required(login_url='signin')
def deleteallproduct(request, pk):
    allproductdelete = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        allproductdelete.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('allproduct')
    return redirect('allproduct')

@login_required(login_url='signin')
def deleteallmaterial(request, pk):
    allmaterialdelete = get_object_or_404(Material, pk=pk)
    if request.method == "POST":
        allmaterialdelete.delete()
        messages.success(request, "Material deleted successfully.")
        return redirect('allmaterial')
    return redirect('allmaterial')

@login_required(login_url='signin')
def deleteproductin(request, pk):
    productindelete = get_object_or_404(Productin, pk=pk)
    if request.method == "POST":
        productindelete.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('stockadded')
    return redirect('stockadded')

@login_required(login_url='signin')
def deleteproductout(request, pk):
    productoutdelete = get_object_or_404(Productout, pk=pk)
    if request.method == "POST":
        productoutdelete.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('stockremoved')
    return redirect('stockremoved')

@login_required(login_url='signin')
def deletemoneyin(request, pk):
    moneyindelete = get_object_or_404(Moneyin, pk=pk)
    if request.method == "POST":
        moneyindelete.delete()
        messages.success(request, "Gain deleted successfully.")
        return redirect('moneyinlist')
    return redirect('moneyinlist')

@login_required(login_url='signin')
def deletemoneyout(request, pk):
    moneyoutdelete = get_object_or_404(Moneyout, pk=pk)
    if request.method == "POST":
        moneyoutdelete.delete()
        messages.success(request, "Uses deleted successfully.")
        return redirect('moneyoutlist')
    return redirect('moneyoutlist')

@login_required(login_url='signin')
def deleteqrcode(request, pk):
    qrcodedelete = get_object_or_404(QRCode, pk=pk)
    if request.method == "POST":
        qrcodedelete.delete()
        messages.success(request, "Qr code deleted successfully.")
        return redirect('view_qr_codes')
    return redirect('view_qr_codes')

#UPDATING STATUS
@login_required(login_url='signin')
def moneyrequest_status(request, id, status):
    moneyrequest = get_object_or_404(MoneyRequest, id=id)
    
    # Update the status based on the passed parameter
    if status in ['Requested', 'Accepted', 'Completed', 'Declined']:
        moneyrequest.status = status
        moneyrequest.save()
    return redirect('requestedmoney')

@login_required(login_url='signin')
def moneyrequest_statusa(request, id, status):
    moneyrequest = get_object_or_404(MoneyRequest, id=id)
    
    # Update the status based on the passed parameter
    if status in ['Requested', 'Accepted', 'Completed', 'Declined']:
        moneyrequest.status = status
        moneyrequest.save()
    return redirect('acceptedmoney')

@login_required(login_url='signin')
def moneyrequest_statusc(request, id, status):
    moneyrequest = get_object_or_404(MoneyRequest, id=id)
    
    # Update the status based on the passed parameter
    if status in ['Requested', 'Accepted', 'Completed', 'Declined']:
        moneyrequest.status = status
        moneyrequest.save()
    return redirect('completedmoney')

@login_required(login_url='signin')
def moneyrequest_statusd(request, id, status):
    moneyrequest = get_object_or_404(MoneyRequest, id=id)
    
    # Update the status based on the passed parameter
    if status in ['Requested', 'Accepted', 'Completed', 'Declined']:
        moneyrequest.status = status
        moneyrequest.save()
    return redirect('declinedmoney')

# status for product from the farmer
@login_required(login_url='signin')
def farmerproduct_statusc(request, id, status):
    farmerproduct = get_object_or_404(ProductBuy, id=id)
    
    # Update the status based on the passed parameter
    if status in ['Submitted', 'Correct', 'Incorrect']:
        farmerproduct.status = status
        farmerproduct.save()
    return redirect('comb_honey')

@login_required(login_url='signin')
def farmerproduct_statusg(request, id, status):
    farmerproduct = get_object_or_404(ProductBuy, id=id)
    
    # Update the status based on the passed parameter
    if status in ['Submitted', 'Correct', 'Incorrect']:
        farmerproduct.status = status
        farmerproduct.save()
    return redirect('viewproductbuy', farmerproduct.id)

@login_required(login_url='signin')
def farmerproduct_statush(request, id, status):
    farmerproduct = get_object_or_404(ProductBuy, id=id)
    
    # Update the status based on the passed parameter
    if status in ['Submitted', 'Correct', 'Incorrect']:
        farmerproduct.status = status
        farmerproduct.save()
    return redirect('honey')

@login_required(login_url='signin')
def farmerproduct_statusw(request, id, status):
    farmerproduct = get_object_or_404(ProductBuy, id=id)
    
    # Update the status based on the passed parameter
    if status in ['Submitted', 'Correct', 'Incorrect']:
        farmerproduct.status = status
        farmerproduct.save()
    return redirect('wax')

@login_required(login_url='signin')
def addproduct_status(request, id, status):
    addproduct = get_object_or_404(Product, id=id)

    if status in ['Submitted', 'Correct', 'Incorrect']:
        addproduct.status = status
        addproduct.save()
    return redirect('allproduct')

@login_required(login_url='signin')
def addmaterial_status(request, id, status):
    addmaterial = get_object_or_404(Material, id=id)

    if status in ['Submitted', 'Correct', 'Incorrect']:
        addmaterial.status = status
        addmaterial.save()
    return redirect('allmaterial')


def request_qr_code(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    if request.method == "POST":
        form = QRCodeForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                qr_instance = form.save(commit=False)
                qr_instance.save()
                messages.success(request, "QR Code added successfully.")
                return redirect('request_qr_code')
            except Exception as e:
                return render(request, 'web/request_qr_code.html', {
                    'form': form,
                    'error': f"An error occurred while generating the QR code: {e}"
                })
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = QRCodeForm()
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        'form': form
        }
    return render(request, 'web/request_qr_code.html', context)

def view_qr_codes(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    qr_codes = QRCode.objects.all()
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        'qr_codes': qr_codes
        }
    return render(request, 'web/view_qr_codes.html', context)