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
from django.utils.timezone import now

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
from django.db.models import Count
from .models import Asset

from django.shortcuts import render, get_object_or_404, redirect
from .models import SalesOrder, Customer, MasterAmount
from .forms import SalesOrderForm, SalesOrderItemForm
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from django.db.models import Sum, F, Q, IntegerField, DecimalField
from django.db.models.functions import ExtractYear
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Case, When


from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Material, MaterialReceipt, MaterialRequisition
from .forms import MaterialForm, MaterialReceiptForm, MaterialRequisitionForm

from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear
# For quarter labels (we'll compute via ExtractQuarter if available, else manual):
try:
    from django.db.models.functions import ExtractQuarter
    HAVE_EXTRACT_QUARTER = True
except Exception:
    HAVE_EXTRACT_QUARTER = False

import csv

from .models import SalesOrder, Customer

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, IntegerField, Case, When
from django.db.models.functions import (
    TruncDay, TruncWeek, TruncMonth, TruncYear,
    ExtractQuarter, ExtractYear, ExtractMonth
)

from decimal import Decimal
from django.db.models import Sum, Case, When, IntegerField, Q, Value, DecimalField
from django.db.models.functions import Coalesce, ExtractYear, ExtractQuarter, TruncDay, TruncWeek, TruncMonth, TruncYear

from django.shortcuts import render, get_object_or_404
from .models import Purchase, Farmer
import csv
from django.core.paginator import Paginator


from .forms import ProductForm, ProductAdditionForm
from .models import Product, ProductAdditionHistory

from .models import Farmer, Purchase
from .forms import FarmerSearchForm, PurchaseItemFormSet

from django.db.models.functions import TruncDay, TruncMonth, TruncWeek, TruncYear

from django.forms import inlineformset_factory
PurchaseItemFormSet = inlineformset_factory(
    Purchase, PurchaseItem,
    fields=('product_name','quantity','unit_price'),
    extra=1, can_delete=True
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Exists, OuterRef
from django.shortcuts import get_object_or_404, redirect, render
from .models import SalesOrder, SalesOrderItem, Customer, MasterAmount, Product
from .forms import SalesOrderForm, SalesOrderItemForm

from .forms import CustomerForm
from .models import Customer

from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)

# web/templatetags/dict_extras.py
from django import template
register = template.Library()

@register.filter
def dict_get(d, key):
    try:
        return d.get(key, {})
    except Exception:
        return {}

@login_required(login_url='signin')
def signup(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
    }

    return render(request, 'web/signup.html', context)

@login_required(login_url='signin')
def registervendors(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    if request.method == 'POST':
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
        "initials": initials,
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
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
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
    
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    # Pass only the designation to the template
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }

    return render(request, 'web/base.html', context)

# @login_required(login_url='signin')
# def home(request):
#     staff = Staff.objects.get(user=request.user)
#     initials = staff.initials()  # piga method ya initials
    
#     farmers = Farmer.objects.all().count()
#     staff = Staff.objects.all().count()
#     asset = Asset.objects.all().count()
#     masteramount = get_object_or_404(MasterAmount, unique_code='welcomemasterofus')
    
#     staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
#     staff = Staff.objects.get(user=request.user)
#     initials = staff.initials()  # piga method ya initials
#     allstaff = Staff.objects.all().count()
#     vendors = Staff.objects.filter(designation="Vendors").count()
    
#     Collection = Staff.objects.filter(designation="Collection Officer").count()
#     Store = Staff.objects.filter(designation="Store Keeper").count()
#     Finance = Staff.objects.filter(designation="Finance Officer").count()
#     Marketing = Staff.objects.filter(designation="Marketing Officer").count()
#     Factory = Staff.objects.filter(designation="Factory Manager").count()
#     Customer = Staff.objects.filter(designation="Customer").count()
#     CEO = Staff.objects.filter(designation="CEO").count()
#     farmers = Farmer.objects.all().count()
#     mfarmers = Farmer.objects.filter(gender="male").count()
#     ffarmers = Farmer.objects.filter(gender="female").count()
#     productp = MasterProduct.objects.all()
    
#     assetsum = AllAsset.objects.filter(unique_code='allasset').first()

#     if assetsum:  # Check to avoid potential NoneType errors
#         allasset = assetsum.Tables + assetsum.Chairs + assetsum.Computers + assetsum.Motocycles + assetsum.Beehives + assetsum.Packages + assetsum.Labels + assetsum.Buckets + assetsum.Bee_suit + assetsum.Gloves + assetsum.Hire_tools + assetsum.Bee_smoker + assetsum.Honey_press + assetsum.Honey_strainer + assetsum.Sandles + assetsum.Apron
#     else:
#         allasset = 0
    
    
#     context={
#         "farmers":farmers,
#         "staff":staff,
#         "asset":asset,
#         "masteramount":masteramount,
        
#         "allstaff":allstaff,
#         "vendors":vendors,
#         "Collection":Collection,
#         "Store":Store,
#         "Finance":Finance,
#         "Marketing":Marketing,
#         "Factory":Factory,
#         "Customer":Customer,
#         "CEO":CEO,
#         "farmers":farmers,
#         "allasset":allasset,
#         "productp":productp,
        
#         "mfarmers":mfarmers,
#         "ffarmers":ffarmers,
        
#         "designation": staff.designation,
#         "first_name": staff.first_name,
#         "last_name": staff.last_name,
#         "profile_picture": staff.profile_picture,
#         "initials": initials,
#         "gender": staff.gender,
#         "initials": initials,
#     }
#     return render(request, 'web/home.html', context)

@login_required(login_url='signin')
def home(request):
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    farmers = Farmer.objects.all().count()
    staff = Staff.objects.all().count()
    asset = Asset.objects.all().count()
    masteramount = get_object_or_404(MasterAmount, unique_code='welcomemasterofus')
    
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
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
    mfarmers = Farmer.objects.filter(gender="male").count()
    ffarmers = Farmer.objects.filter(gender="female").count()
    productp = MasterProduct.objects.all()
    
    assetsum = AllAsset.objects.filter(unique_code='allasset').first()

    if assetsum:  # Check to avoid potential NoneType errors
        allasset = assetsum.Tables + assetsum.Chairs + assetsum.Computers + assetsum.Motocycles + assetsum.Beehives + assetsum.Packages + assetsum.Labels + assetsum.Buckets + assetsum.Bee_suit + assetsum.Gloves + assetsum.Hire_tools + assetsum.Bee_smoker + assetsum.Honey_press + assetsum.Honey_strainer + assetsum.Sandles + assetsum.Apron
    else:
        allasset = 0

    # >>> new: HESABU ZA LEO (paid tu)
    today = timezone.localdate()

    # Mauzo ya leo (Orders) - tunatumia updated_at ya order wakati ina-markiwa paid
    sales_today = (
        SalesOrderItem.objects
        .filter(order__status='paid', order__updated_at__date=today)
        .aggregate(total=Sum(F('quantity') * F('unit_price')))['total']
        or Decimal('0.00')
    )

    # Manunuzi ya leo (Purchases) - tunatumia purchase_date ya purchase (imeundwa leo)
    purchases_today = (
        PurchaseItem.objects
        .filter(purchase__status='paid', purchase__purchase_date__date=today)
        .aggregate(total=Sum(F('quantity') * F('unit_price')))['total']
        or Decimal('0.00')
    )

    # Tofauti ya leo
    net_today = sales_today - purchases_today
    # <<< new

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
        
        "mfarmers":mfarmers,
        "ffarmers":ffarmers,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        "gender": staff.gender,
        "initials": initials,

        # >>> new: tupatie template values za leo
        "sales_today": sales_today,
        "purchases_today": purchases_today,
        "net_today": net_today,
        # <<< new
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

@login_required(login_url='signin')
def add_farmers(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        tch_beehives = request.POST.get('tch_beehives')
        ktbh_beehives = request.POST.get('ktbh_beehives')
        local_beehives = request.POST.get('local_beehives')
        colonized_beehives = request.POST.get('colonized_beehives')
        uncolonized_beehives = request.POST.get('uncolonized_beehives')
        mwanzo = request.POST.get('mwanzo')
        
        malengo = request.POST.get('malengo')
        muhamasishaji = request.POST.get('muhamasishaji')
        kiasi_mwisho = request.POST.get('kiasi_mwisho')
        kufanikisha_nin = request.POST.get('kufanikisha_nin')
        kusaidia_mazingira = request.POST.get('kusaidia_mazingira')
        familia_mtazamo = request.POST.get('familia_mtazamo')
        
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
            tch_beehives=tch_beehives,
            ktbh_beehives=ktbh_beehives,
            local_beehives=local_beehives,
            colonized_beehives=colonized_beehives,
            uncolonized_beehives=uncolonized_beehives,
            mwanzo=mwanzo,
            malengo=malengo,
            muhamasishaji=muhamasishaji,
            kiasi_mwisho=kiasi_mwisho,
            kufanikisha_nin=kufanikisha_nin,
            kusaidia_mazingira=kusaidia_mazingira,
            familia_mtazamo=familia_mtazamo,
            user = request.user,
            )

        messages.success(request, 'Registered successfully.')
        return redirect('add_farmers')
    
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }

    return render(request, 'web/add_farmers.html', context)

@login_required(login_url='signin')
def add_asset(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.created_by = request.user
            asset.save()
            messages.success(request, "Asset created successfully!")
            return redirect('add_asset')
    else:
        form = AssetForm()
    context = {
        "form": form,
        "title": 'Add Asset',
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, 'web/add_asset.html', context)


def allasset(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    # Group kwa category na count
    assets_summary = Asset.objects.values("category").annotate(total=Count("id")).order_by("category")

    context = {
        "assets_summary": assets_summary,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/allasset.html", context)


def assethistory(request, category):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    # List ya assets za category husika
    assets = Asset.objects.filter(category=category).order_by("-date_created")

    context = {
        "assets": assets,
        "category": category,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/assethistory.html", context)


@login_required(login_url='signin')
def remove_asset(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    if request.method == 'POST':
        allasset = AllAsset.objects.filter(unique_code='allasset').first()
        
        asset_name = request.POST.get('asset_name')
        quantity = request.POST.get('quantity')
        
        Asset.objects.create(
            asset_name=asset_name,
            quantity=quantity,
            status = 'removed',
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
            allasset.Tables -= int(quantity)
            allasset.Chairs -= int(0)
            allasset.Computers -= int(0)
            allasset.Motocycles -= int(0)
            allasset.Beehives -= int(0)
            allasset.Packages -= int(0)
            allasset.Labels -= int(0)
            allasset.Buckets -= int(0)
            allasset.Bee_suit -= int(0)
            allasset.Gloves -= int(0)
            allasset.Hire_tools -= int(0)
            allasset.Bee_smoker -= int(0)
            allasset.Honey_press -= int(0)
            allasset.Honey_strainer -= int(0)
            allasset.Sandles -= int(0)
            allasset.Apron -= int(0)
            allasset.save()
            
        elif asset_name == "Chairs":
            allasset.Tables -= int(0)
            allasset.Chairs -= int(quantity)
            allasset.Computers -= int(0)
            allasset.Motocycles -= int(0)
            allasset.Beehives -= int(0)
            allasset.Packages -= int(0)
            allasset.Labels -= int(0)
            allasset.Buckets -= int(0)
            allasset.Bee_suit -= int(0)
            allasset.Gloves -= int(0)
            allasset.Hire_tools -= int(0)
            allasset.Bee_smoker -= int(0)
            allasset.Honey_press -= int(0)
            allasset.Honey_strainer -= int(0)
            allasset.Sandles -= int(0)
            allasset.Apron -= int(0)
            allasset.save()
            
        elif asset_name == "Computers":
            allasset.Tables -= int(0)
            allasset.Chairs -= int(0)
            allasset.Computers -= int(quantity)
            allasset.Motocycles -= int(0)
            allasset.Beehives -= int(0)
            allasset.Packages -= int(0)
            allasset.Labels -= int(0)
            allasset.Buckets -= int(0)
            allasset.Bee_suit -= int(0)
            allasset.Gloves -= int(0)
            allasset.Hire_tools -= int(0)
            allasset.Bee_smoker -= int(0)
            allasset.Honey_press -= int(0)
            allasset.Honey_strainer -= int(0)
            allasset.Sandles -= int(0)
            allasset.Apron -= int(0)
            allasset.save()
            
        elif asset_name == "Motocycles":
            allasset.Tables -= int(0)
            allasset.Chairs -= int(0)
            allasset.Computers -= int(0)
            allasset.Motocycles -= int(quantity)
            allasset.Beehives -= int(0)
            allasset.Packages -= int(0)
            allasset.Labels -= int(0)
            allasset.Buckets -= int(0)
            allasset.Bee_suit -= int(0)
            allasset.Gloves -= int(0)
            allasset.Hire_tools -= int(0)
            allasset.Bee_smoker -= int(0)
            allasset.Honey_press -= int(0)
            allasset.Honey_strainer -= int(0)
            allasset.Sandles -= int(0)
            allasset.Apron -= int(0)
            allasset.save()
            
        elif asset_name == "Beehives":
            allasset.Tables -= int(0)
            allasset.Chairs -= int(0)
            allasset.Computers -= int(0)
            allasset.Motocycles -= int(0)
            allasset.Beehives -= int(quantity)
            allasset.Packages -= int(0)
            allasset.Labels -= int(0)
            allasset.Buckets -= int(0)
            allasset.Bee_suit -= int(0)
            allasset.Gloves -= int(0)
            allasset.Hire_tools -= int(0)
            allasset.Bee_smoker -= int(0)
            allasset.Honey_press -= int(0)
            allasset.Honey_strainer -= int(0)
            allasset.Sandles -= int(0)
            allasset.Apron -= int(0)
            allasset.save()
            
        elif asset_name == "Packages":
            allasset.Tables -= int(0)
            allasset.Chairs -= int(0)
            allasset.Computers -= int(0)
            allasset.Motocycles -= int(0)
            allasset.Beehives -= int(0)
            allasset.Packages -= int(quantity)
            allasset.Labels -= int(0)
            allasset.Buckets -= int(0)
            allasset.Bee_suit -= int(0)
            allasset.Gloves -= int(0)
            allasset.Hire_tools -= int(0)
            allasset.Bee_smoker -= int(0)
            allasset.Honey_press -= int(0)
            allasset.Honey_strainer -= int(0)
            allasset.Sandles -= int(0)
            allasset.Apron -= int(0)
            allasset.save()
            
        elif asset_name == "Labels":
            allasset.Tables -= int(0)
            allasset.Chairs -= int(0)
            allasset.Computers -= int(0)
            allasset.Motocycles -= int(0)
            allasset.Beehives -= int(0)
            allasset.Packages -= int(0)
            allasset.Labels -= int(quantity)
            allasset.Buckets -= int(0)
            allasset.Bee_suit -= int(0)
            allasset.Gloves -= int(0)
            allasset.Hire_tools -= int(0)
            allasset.Bee_smoker -= int(0)
            allasset.Honey_press -= int(0)
            allasset.Honey_strainer -= int(0)
            allasset.Sandles -= int(0)
            allasset.Apron -= int(0)
            allasset.save()
            
        elif asset_name == "Buckets":
            allasset.Tables -= int(0)
            allasset.Chairs -= int(0)
            allasset.Computers -= int(0)
            allasset.Motocycles -= int(0)
            allasset.Beehives -= int(0)
            allasset.Packages -= int(0)
            allasset.Labels -= int(0)
            allasset.Buckets -= int(quantity)
            allasset.Bee_suit -= int(0)
            allasset.Gloves -= int(0)
            allasset.Hire_tools -= int(0)
            allasset.Bee_smoker -= int(0)
            allasset.Honey_press -= int(0)
            allasset.Honey_strainer -= int(0)
            allasset.Sandles -= int(0)
            allasset.Apron -= int(0)
            allasset.save()
            
        elif asset_name == "Bee_suit":
            allasset.Tables -= int(0)
            allasset.Chairs -= int(0)
            allasset.Computers -= int(0)
            allasset.Motocycles -= int(0)
            allasset.Beehives -= int(0)
            allasset.Packages -= int(0)
            allasset.Labels -= int(0)
            allasset.Buckets -= int(0)
            allasset.Bee_suit -= int(quantity)
            allasset.Gloves -= int(0)
            allasset.Hire_tools -= int(0)
            allasset.Bee_smoker -= int(0)
            allasset.Honey_press -= int(0)
            allasset.Honey_strainer -= int(0)
            allasset.Sandles -= int(0)
            allasset.Apron -= int(0)
            allasset.save()
            
        elif asset_name == "Gloves":
            allasset.Tables -= int(0)
            allasset.Chairs -= int(0)
            allasset.Computers -= int(0)
            allasset.Motocycles -= int(0)
            allasset.Beehives -= int(0)
            allasset.Packages -= int(0)
            allasset.Labels -= int(0)
            allasset.Buckets -= int(0)
            allasset.Bee_suit -= int(0)
            allasset.Gloves -= int(quantity)
            allasset.Hire_tools -= int(0)
            allasset.Bee_smoker -= int(0)
            allasset.Honey_press -= int(0)
            allasset.Honey_strainer -= int(0)
            allasset.Sandles -= int(0)
            allasset.Apron -= int(0)
            allasset.save()
            
        elif asset_name == "Hire_tools":
            allasset.Tables -= int(0)
            allasset.Chairs -= int(0)
            allasset.Computers -= int(0)
            allasset.Motocycles -= int(0)
            allasset.Beehives -= int(0)
            allasset.Packages -= int(0)
            allasset.Labels -= int(0)
            allasset.Buckets -= int(0)
            allasset.Bee_suit -= int(0)
            allasset.Gloves -= int(0)
            allasset.Hire_tools -= int(quantity)
            allasset.Bee_smoker -= int(0)
            allasset.Honey_press -= int(0)
            allasset.Honey_strainer -= int(0)
            allasset.Sandles -= int(0)
            allasset.Apron -= int(0)
            allasset.save()
            
        elif asset_name == "Bee_smoker":
            allasset.Tables -= int(0)
            allasset.Chairs -= int(0)
            allasset.Computers -= int(0)
            allasset.Motocycles -= int(0)
            allasset.Beehives -= int(0)
            allasset.Packages -= int(0)
            allasset.Labels -= int(0)
            allasset.Buckets -= int(0)
            allasset.Bee_suit -= int(0)
            allasset.Gloves -= int(0)
            allasset.Hire_tools -= int(0)
            allasset.Bee_smoker -= int(quantity)
            allasset.Honey_press -= int(0)
            allasset.Honey_strainer -= int(0)
            allasset.Sandles -= int(0)
            allasset.Apron -= int(0)
            allasset.save()
            
        elif asset_name == "Honey_press":
            allasset.Tables -= int(0)
            allasset.Chairs -= int(0)
            allasset.Computers -= int(0)
            allasset.Motocycles -= int(0)
            allasset.Beehives -= int(0)
            allasset.Packages -= int(0)
            allasset.Labels -= int(0)
            allasset.Buckets -= int(0)
            allasset.Bee_suit -= int(0)
            allasset.Gloves -= int(0)
            allasset.Hire_tools -= int(0)
            allasset.Bee_smoker -= int(0)
            allasset.Honey_press -= int(quantity)
            allasset.Honey_strainer -= int(0)
            allasset.Sandles -= int(0)
            allasset.Apron -= int(0)
            allasset.save()
            
        elif asset_name == "Honey_strainer":
            allasset.Tables -= int(0)
            allasset.Chairs -= int(0)
            allasset.Computers -= int(0)
            allasset.Motocycles -= int(0)
            allasset.Beehives -= int(0)
            allasset.Packages -= int(0)
            allasset.Labels -= int(0)
            allasset.Buckets -= int(0)
            allasset.Bee_suit -= int(0)
            allasset.Gloves -= int(0)
            allasset.Hire_tools -= int(0)
            allasset.Bee_smoker -= int(0)
            allasset.Honey_press -= int(0)
            allasset.Honey_strainer -= int(quantity)
            allasset.Sandles -= int(0)
            allasset.Apron -= int(0)
            allasset.save()
            
        elif asset_name == "Sandles":
            allasset.Tables -= int(0)
            allasset.Chairs -= int(0)
            allasset.Computers -= int(0)
            allasset.Motocycles -= int(0)
            allasset.Beehives -= int(0)
            allasset.Packages -= int(0)
            allasset.Labels -= int(0)
            allasset.Buckets -= int(0)
            allasset.Bee_suit -= int(0)
            allasset.Gloves -= int(0)
            allasset.Hire_tools -= int(0)
            allasset.Bee_smoker -= int(0)
            allasset.Honey_press -= int(0)
            allasset.Honey_strainer -= int(0)
            allasset.Sandles -= int(quantity)
            allasset.Apron -= int(0)
            allasset.save()
            
        elif asset_name == "Apron":
            allasset.Tables -= int(0)
            allasset.Chairs -= int(0)
            allasset.Computers -= int(0)
            allasset.Motocycles -= int(0)
            allasset.Beehives -= int(0)
            allasset.Packages -= int(0)
            allasset.Labels -= int(0)
            allasset.Buckets -= int(0)
            allasset.Bee_suit -= int(0)
            allasset.Gloves -= int(0)
            allasset.Hire_tools -= int(0)
            allasset.Bee_smoker -= int(0)
            allasset.Honey_press -= int(0)
            allasset.Honey_strainer -= int(0)
            allasset.Sandles -= int(0)
            allasset.Apron -= int(quantity)
            allasset.save()
            
        else:
            allasset.Tables -= int(0)
            allasset.Chairs -= int(0)
            allasset.Computers -= int(0)
            allasset.Motocycles -= int(0)
            allasset.Beehives -= int(0)
            allasset.Packages -= int(0)
            allasset.Labels -= int(0)
            allasset.Buckets -= int(0)
            allasset.Bee_suit -= int(0)
            allasset.Gloves -= int(0)
            allasset.Hire_tools -= int(0)
            allasset.Bee_smoker -= int(0)
            allasset.Honey_press -= int(0)
            allasset.Honey_strainer -= int(0)
            allasset.Sandles -= int(0)
            allasset.Apron -= int(0)
            allasset.save()
            
        messages.success(request, 'Added successfully.')
        return redirect('remove_asset')
    
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }

    return render(request, 'web/remove_asset.html', context)

# @login_required(login_url='signin')
# def start_purchase(request):
#     staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
#     staff = Staff.objects.get(user=request.user)
#     initials = staff.initials()  # piga method ya initials

#     farmers = None
#     if request.method == "POST":
#         query = request.POST.get('query', '').strip()
#         if query:
#             farmers = Farmer.objects.filter(
#                 models.Q(first_name__icontains=query) |
#                 models.Q(middle_name__icontains=query) |
#                 models.Q(last_name__icontains=query)
#             ).order_by('first_name', 'last_name')[:50]

#     context = {
#         "farmers": farmers,
#         "designation": staff.designation,
#         "first_name": staff.first_name,
#         "last_name": staff.last_name,
#         "profile_picture": staff.profile_picture,
#         "initials": initials,
#     }
#     return render(request, "web/search_farmer.html", context)

@login_required(login_url='signin')
def start_purchase(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    farmers = None
    if request.method == "POST":
        query = request.POST.get('query', '').strip()
        if query:
            farmers = Farmer.objects.filter(
                models.Q(first_name__icontains=query) |
                models.Q(middle_name__icontains=query) |
                models.Q(last_name__icontains=query)
            ).order_by('first_name', 'last_name')[:50]

    # Show a default list only when not searching
    all_farmers = Farmer.objects.order_by('first_name', 'last_name')[:50] if farmers is None else None

    context = {
        "farmers": farmers,
        "all_farmers": all_farmers,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/search_farmer.html", context)



@login_required(login_url="signin")
def add_purchase(request, farmer_id):
    staff = get_object_or_404(Staff, user=request.user)
    initials = staff.initials()
    farmer = get_object_or_404(Farmer, id=farmer_id)

    purchase = (Purchase.objects
                .filter(farmer=farmer, status="pending")
                .order_by("-id")
                .first())
    if not purchase:
        purchase = Purchase.objects.create(
            farmer=farmer,
            status="pending",
            created_by=request.user,
        )

    PREFIX = "items"

    if request.method == "POST":
        formset = PurchaseItemFormSet(request.POST, instance=purchase, prefix=PREFIX)
        if formset.is_valid():
            with transaction.atomic():
                formset.save()
            messages.success(request, "Items saved.")
            return redirect("purchase_detail", purchase_id=purchase.id)
        else:
            print("FORMSET INVALID:")
            print("non_form_errors:", formset.non_form_errors())
            for i, f in enumerate(formset.forms):
                print(f"form {i} errors:", f.errors)
            messages.error(request, "Kuna makosa kwenye fomu. Tafadhali rekebisha kisha ujaribu tena.")
    else:
        formset = PurchaseItemFormSet(instance=purchase, prefix=PREFIX)

    return render(request, "web/add_purchase.html", {
        "formset": formset,
        "farmer": farmer,
        "purchase": purchase,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    })
    
@login_required(login_url='signin')
def purchase_detail(request, purchase_id):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    purchase = get_object_or_404(Purchase, id=purchase_id)

    context = {
        "purchase": purchase,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/purchase_detail.html", context)


def farmer_purchases(request, farmer_id):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    farmer = get_object_or_404(Farmer, id=farmer_id)
    purchases = farmer.purchases.select_related('farmer').prefetch_related('items').order_by('-purchase_date')

    context = {
        "farmer": farmer,
        "purchases": purchases,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/farmer_purchases.html", context)


@login_required(login_url='signin')
@transaction.atomic
def mark_purchase_paid(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)

    # Only update if not already paid
    if purchase.status != "paid":
        purchase.status = "paid"
        purchase.save()

        # Reduce from MasterAmount with unique_code = "welcomemasterofus"
        try:
            master = MasterAmount.objects.select_for_update().get(unique_code="welcomemasterofus")
            # Assuming your Purchase model has a field total_amount
            master.amount = (master.amount or Decimal("0.00")) - (purchase.total_amount or Decimal("0.00"))
            master.save()
        except MasterAmount.DoesNotExist:
            # You may choose to raise an error, log it, or create it automatically
            MasterAmount.objects.create(
                unique_code="welcomemasterofus",
                amount=Decimal("0.00") - (purchase.total_amount or Decimal("0.00"))
            )

    return redirect('purchase_detail', purchase_id=purchase.id)

@login_required(login_url='signin')
def cancel_purchase(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    purchase.status = "cancelled"
    purchase.save()
    return redirect('purchase_detail', purchase_id=purchase.id)

@login_required(login_url='signin')
def print_purchase(request, purchase_id):
    purchase = get_object_or_404(
        Purchase.objects.prefetch_related("items", "farmer"),
        id=purchase_id
    )

    company = {
        "name": "Honey ERP Company Ltd.",
        "slogan": "Pure Quality • Trusted Farmers",
        "tin": "TIN: 123-456-789",
        "vrn": "VRN: 00-0000000",
        "phone": "+255 712 000 000",
        "email": "info@yourcompany.co.tz",
        "address_line1": "P.O. Box 123, Dodoma",
        "address_line2": "Mnadani Street, Block A",
        "website": "www.yourcompany.co.tz",
        "logo_url": "img/company-logo.png",  # weka static/img/logo yako hapa
    }

    return render(
        request,
        "web/print_purchase.html",   # tumia template tuliyoandaa ya receipt
        {
            "purchase": purchase,
            "company": company,
        }
    )

# =========================
#  UTILITIES: Aggregation
# =========================

# Helper ya kujenga expression ya total (Decimal salama)
DECIMAL_FIELD = DecimalField(max_digits=20, decimal_places=2)
ZERO_DECIMAL = Value(Decimal("0.00"), output_field=DECIMAL_FIELD)

def _sum_total_decimal(field_name="items__total_price"):
    return Coalesce(
        Sum(field_name, output_field=DECIMAL_FIELD),
        ZERO_DECIMAL,
        output_field=DECIMAL_FIELD,
    )
    
def _aggregate_purchases(qs, period):
    period = (period or "month").lower()

    if period == "day":
        base = qs.annotate(period=TruncDay("purchase_date")).values("period")
        grouped = base.annotate(total=_sum_total_decimal()).order_by("-period")
        rows = [{"label": r["period"].date().isoformat(), "total": r["total"]} for r in grouped]

    elif period == "week":
        base = qs.annotate(period=TruncWeek("purchase_date")).values("period")
        grouped = base.annotate(total=_sum_total_decimal()).order_by("-period")
        rows = [{"label": f"the week of {r['period'].date().isoformat()}", "total": r["total"]} for r in grouped]

    elif period == "month":
        base = qs.annotate(period=TruncMonth("purchase_date")).values("period")
        grouped = base.annotate(total=_sum_total_decimal()).order_by("-period")
        rows = [{"label": r["period"].strftime("%B %Y"), "total": r["total"]} for r in grouped]

    elif period == "quarter":
        base = qs.annotate(
            year=ExtractYear("purchase_date"),
            quarter=ExtractQuarter("purchase_date"),
        ).values("year", "quarter")
        grouped = base.annotate(total=_sum_total_decimal()).order_by("-year", "-quarter")
        rows = [{"label": f"Q{r['quarter']} {r['year']}", "total": r["total"]} for r in grouped]

    elif period in ("half", "halfyear", "six", "sixmonths", "miezi6", "nusu"):
        base = qs.annotate(
            year=ExtractYear("purchase_date"),
            half=Case(
                When(Q(purchase_date__month__lte=6), then=1),
                When(Q(purchase_date__month__gte=7), then=2),
                output_field=IntegerField(),
            ),
        ).values("year", "half")
        grouped = base.annotate(total=_sum_total_decimal()).order_by("-year", "-half")
        rows = [{"label": f"H{r['half']} {r['year']}", "total": r["total"]} for r in grouped]

    elif period == "year":
        base = qs.annotate(period=TruncYear("purchase_date")).values("period")
        grouped = base.annotate(total=_sum_total_decimal()).order_by("-period")
        rows = [{"label": r["period"].year, "total": r["total"]} for r in grouped]

    else:
        return _aggregate_purchases(qs, "month")

    grand_total = sum((r["total"] for r in rows), Decimal("0.00"))
    return rows, grand_total


# =========================
#  REPORTS (OVERALL & FARMER)
# =========================

@login_required(login_url="signin")
def purchase_report_overall(request, period="month"):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    qs = Purchase.objects.select_related("farmer").filter(status="paid")
    rows, grand_total = _aggregate_purchases(qs, period)

    ctx = {
        "period": period,
        "rows": rows,
        "grand_total": grand_total,
        "is_farmer": False,
        "farmer": None,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/purchase_report.html", ctx)



@login_required(login_url="signin")
def purchase_report_farmer(request, farmer_id, period="month"):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    farmer = get_object_or_404(Farmer, id=farmer_id)
    qs = Purchase.objects.filter(status="paid", farmer=farmer)
    rows, grand_total = _aggregate_purchases(qs, period)

    ctx = {
        "period": period,
        "rows": rows,
        "grand_total": grand_total,
        "is_farmer": True,
        "farmer": farmer,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/purchase_report.html", ctx)



@login_required(login_url="signin")
def purchase_report_export_csv(request, scope, period, farmer_id=None):
    """
    scope: "overall" au "farmer"
    """
    if scope == "farmer":
        farmer = get_object_or_404(Farmer, id=farmer_id)
        qs = Purchase.objects.filter(status="paid", farmer=farmer)
        filename = f"purchases_{farmer.id}_{period}.csv"
    else:
        qs = Purchase.objects.filter(status="paid")
        filename = f"purchases_overall_{period}.csv"

    rows, grand_total = _aggregate_purchases(qs, period)

    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = f'attachment; filename="{filename}"'
    writer = csv.writer(resp)
    writer.writerow(["Kipindi", "Jumla (TZS)"])
    for r in rows:
        writer.writerow([r["label"], r["total"]])
    writer.writerow(["JUMLA", grand_total])
    return resp

@login_required(login_url='signin')
def purchase_report(request, period="day"):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    qs = Purchase.objects.filter(status="paid")

    if period == "day":
        qs = qs.annotate(period=TruncDay("purchase_date"))
    elif period == "week":
        qs = qs.annotate(period=TruncWeek("purchase_date"))
    elif period == "month":
        qs = qs.annotate(period=TruncMonth("purchase_date"))
    elif period == "year":
        qs = qs.annotate(period=TruncYear("purchase_date"))

    report = qs.values("period").annotate(total=Sum("items__total_price")).order_by("-period")

    context = {
        "report": report,
        "period": period,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/purchase_report.html", context)

    
@login_required
def purchase_farmer_search(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    q = (request.GET.get("q") or "").strip()
    farmers = Farmer.objects.all()

    if q:
        farmers = farmers.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(phone__icontains=q) |
            Q(national_id__icontains=q) |
            Q(card_number__icontains=q)
        )

    farmers = farmers.order_by("first_name", "last_name")
    paginator = Paginator(farmers, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    ctx = {
        "q": q,
        "page_obj": page_obj,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/purchase_farmer_search.html", ctx)


@login_required(login_url='signin')
def moneyin(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
    }

    return render(request, 'web/moneyin.html', context)

@login_required(login_url='signin')
def moneyout(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
    }

    return render(request, 'web/moneyout.html', context)

@login_required(login_url='signin')
def paysalary(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
    }

    return render(request, 'web/paysalary.html', context)

@login_required(login_url='signin')
def addproduct(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
    }

    return render(request, 'web/addproduct.html', context)

@login_required(login_url='signin')
def addmaterial(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
    }

    return render(request, 'web/addmaterial.html', context)

@login_required(login_url='signin')
def moneyrequest(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
    }

    return render(request, 'web/moneyrequest.html', context)

@login_required(login_url='signin')
def productin(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
    }

    return render(request, 'web/productin.html', context)

@login_required(login_url='signin')
def productout(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
    }

    return render(request, 'web/productout.html', context)

@login_required(login_url='signin')
def product_list(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    products = (
        Product.objects.all()
        .annotate(
            total_added=Sum("histories__quantity"),
            history_count=Count("histories"),
        )
        .order_by("name")
    )

    context = {
        "products": products,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/allproduct_list.html", context)


@login_required(login_url='signin')
def allstaff(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    staff_members = Staff.objects.all()
    context = {
        'staff_members': staff_members,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/allstaff.html', context)

@login_required(login_url='signin')
def allvendors(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    staff_members = Staff.objects.all()
    context = {
        'staff_members': staff_members,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/allvendors.html', context)

@login_required(login_url='signin')
def allfarmers(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    allfarmers = Farmer.objects.all()
    context = {
        'allfarmers': allfarmers,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/allfarmers.html', context)


@login_required(login_url='signin')
def removed_asset(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    assethistory = Asset.objects.all()
    context = {
        'assethistory': assethistory,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/removed_asset.html', context)

@login_required(login_url='signin')
def moneyinlist(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    moneyin = Moneyin.objects.all()
    context = {
        'moneyin': moneyin,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/moneyinlist.html', context)

@login_required(login_url='signin')
def moneyoutlist(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    moneyout = Moneyout.objects.all()
    context = {
        'moneyout': moneyout,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/moneyoutlist.html', context)

@login_required(login_url='signin')
def honeyproduct(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    product = ProductBuy.objects.all()
    context = {
        'product': product,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/honeyproduct.html', context)

@login_required(login_url='signin')
def payedsalary(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    salary = Salary.objects.all()
    context = {
        'salary': salary,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/payedsalary.html', context)

@login_required(login_url='signin')
def comb_honey(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    product = ProductBuy.objects.all()
    context = {
        'product': product,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/comb_honey.html', context)
@login_required(login_url='signin')
def honey(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    product = ProductBuy.objects.all()
    context = {
        'product': product,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/honey.html', context)

@login_required(login_url='signin')
def wax(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    product = ProductBuy.objects.all()
    context = {
        'product': product,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/wax.html', context)

@login_required(login_url='signin')
def requestedmoney(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    moneyrequest = MoneyRequest.objects.filter(status = "Requested")
    context = {
        'moneyrequest': moneyrequest,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/requestedmoney.html', context)

@login_required(login_url='signin')
def acceptedmoney(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    moneyrequest = MoneyRequest.objects.filter(status = "Accepted")
    context = {
        'moneyrequest': moneyrequest,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/acceptedmoney.html', context)

@login_required(login_url='signin')
def completedmoney(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    moneyrequest = MoneyRequest.objects.filter(status = "Completed")
    context = {
        'moneyrequest': moneyrequest,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/completedmoney.html', context)

@login_required(login_url='signin')
def declinedmoney(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    moneyrequest = MoneyRequest.objects.filter(status = "Declined")
    context = {
        'moneyrequest': moneyrequest,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/declinedmoney.html', context)

@login_required(login_url='signin')
def myrequest(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    moneyrequest = MoneyRequest.objects.filter(user=request.user)
    context = {
        'moneyrequest': moneyrequest,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/myrequest.html', context)

@login_required(login_url='signin')
def allproduct(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    allproduct = Product.objects.all()
    context = {
        'allproduct': allproduct,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/allproduct.html', context)

@login_required(login_url='signin')
def allmaterial(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    allmaterial = Material.objects.all()
    context = {
        'allmaterial': allmaterial,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/allmaterial.html', context)

@login_required(login_url='signin')
def stockadded(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    stockadded = Productin.objects.all()
    context = {
        'stockadded': stockadded,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/stockadded.html', context)

@login_required(login_url='signin')
def stockremoved(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    stockremoved = Productout.objects.all()
    context = {
        'stockremoved': stockremoved,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/stockremoved.html', context)

@login_required(login_url='signin')
def allstock(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
    }
    return render(request, 'web/allstock.html', context)


# VIEW TO VIEW THE INFORMATIONS
@login_required(login_url='signin')
def viewfarmer(request, id):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    farmerview = Farmer.objects.get(id=id)
    
    context = {
        "farmerview":farmerview,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/viewfarmer.html', context)

@login_required(login_url='signin')
def viewstaff(request, id):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    staffview = Staff.objects.get(id=id)
    
    context = {
        "staffview":staffview,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
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
    
@login_required(login_url='signin')
def viewmoneyin(request, id):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    moneyinview = Moneyin.objects.get(id=id)
    
    context = {
        "moneyinview":moneyinview,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/viewmoneyin.html', context)

@login_required(login_url='signin')
def viewmoneyout(request, id):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
    moneyoutview = Moneyout.objects.get(id=id)
    
    context = {
        "moneyoutview":moneyoutview,
        
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        }
    return render(request, 'web/viewmoneyout.html', context)

# UPDATING INFORMATIONS
@login_required(login_url='signin')
def updatefarmer(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        farmer_instance.tch_beehives = request.POST.get("tch_beehives")
        farmer_instance.ktbh_beehives = request.POST.get("ktbh_beehives")
        farmer_instance.local_beehives = request.POST.get("local_beehives")
        farmer_instance.colonized_beehives = request.POST.get("colonized_beehives")
        farmer_instance.uncolonized_beehives = request.POST.get("uncolonized_beehives")
        farmer_instance.mwanzo = request.POST.get("mwanzo")
        farmer_instance.malengo = request.POST.get("malengo")
        farmer_instance.muhamasishaji = request.POST.get("muhamasishaji")
        farmer_instance.kiasi_mwisho = request.POST.get("kiasi_mwisho")
        farmer_instance.kufanikisha_nin = request.POST.get("kufanikisha_nin")
        farmer_instance.kusaidia_mazingira = request.POST.get("kusaidia_mazingira")
        farmer_instance.familia_mtazamo = request.POST.get("familia_mtazamo")
        
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
        "initials": initials,
        }
    return render(request, 'web/updatefarmer.html', context)

@login_required(login_url='signin')
def updatestaff(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
        }
    return render(request, 'web/updatestaff.html', context)



@login_required(login_url='signin')
def updateasset(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    asset_instance = get_object_or_404(Asset, pk=pk)

    if request.method == "POST":
        asset_instance.asset_name = request.POST.get("asset_name", asset_instance.asset_name)

        # Only set quantity if the model has it
        if hasattr(asset_instance, "quantity"):
            raw_qty = request.POST.get("quantity", "").strip()
            if raw_qty != "":
                try:
                    asset_instance.quantity = int(raw_qty)
                except (ValueError, TypeError):
                    messages.error(request, "Quantity must be an integer.")
                    return render(request, 'web/updateasset.html', {
                        "asset_instance": asset_instance,
                        "designation": staff.designation,
                        "first_name": staff.first_name,
                        "last_name": staff.last_name,
                        "profile_picture": staff.profile_picture,
                    })

        try:
            asset_instance.save()
            messages.success(request, "Asset updated successfully.")
            return redirect('assethistory', category=asset_instance.category)
        except Exception as e:
            messages.error(request, f"Error updating Asset: {e}")
    else:
        messages.info(request, "Update the asset's information.")

    return render(request, 'web/updateasset.html', {
        "asset_instance": asset_instance,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    })

@login_required(login_url='signin')
def updateallasset(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
        }
    return render(request, 'web/updateallasset.html', context)

@login_required(login_url='signin')
def updateallstock(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
        }
    return render(request, 'web/updateallstock.html', context)

@login_required(login_url='signin')
def updatemoneyrequested(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
        }
    return render(request, 'web/updatemoneyrequested.html', context)

@login_required(login_url='signin')
def updateproductbuy(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
        }
    return render(request, 'web/updateproductbuy.html', context)

@login_required(login_url='signin')
def updatepayedsalary(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
        }
    return render(request, 'web/updatepayedsalary.html', context)

@login_required(login_url='signin')
def updateallproduct(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
        }
    return render(request, 'web/updateallproduct.html', context)

@login_required(login_url='signin')
def updateallmaterial(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
        }
    return render(request, 'web/updateallmaterial.html', context)

@login_required(login_url='signin')
def updatemoneyin(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
        }
    return render(request, 'web/updatemoneyin.html', context)

@login_required(login_url='signin')
def updatemoneyout(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
        }
    return render(request, 'web/updatemoneyout.html', context)

@login_required(login_url='signin')
def updateproductin(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
        }
    return render(request, 'web/updateproductin.html', context)

@login_required(login_url='signin')
def updateproductout(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    
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
        "initials": initials,
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
    asset = get_object_or_404(Asset, pk=pk)

    if request.method == "POST":
        category = asset.category  # capture before delete
        asset.delete()
        messages.success(request, "Asset deleted successfully.")
        return redirect('assethistory', category=category)

    # If someone hits the URL via GET, send them back to the asset's category
    return redirect('assethistory', category=asset.category)

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
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
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
        "initials": initials,
        'form': form
        }
    return render(request, 'web/request_qr_code.html', context)

def view_qr_codes(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    qr_codes = QRCode.objects.all()
    context = {
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        'qr_codes': qr_codes
        }
    return render(request, 'web/view_qr_codes.html', context)

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = "web/customer_list.html"
    context_object_name = "customers"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(company_name__icontains=q) |
                Q(contact_person__icontains=q) |
                Q(phone__icontains=q) |
                Q(email__icontains=q) |
                Q(code__icontains=q) |
                Q(city__icontains=q) |
                Q(region__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = get_object_or_404(
            Staff,
            email=self.request.user.email,
            username=self.request.user.username
        )
        # Add initials as requested
        staff = Staff.objects.get(user=self.request.user)
        initials = staff.initials()  # piga method ya initials

        context.update({
            "designation": staff.designation,
            "first_name": staff.first_name,
            "last_name": staff.last_name,
            "profile_picture": staff.profile_picture,
            "initials": initials,
        })
        return context



class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = "web/customer_detail.html"
    context_object_name = "customer"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = get_object_or_404(
            Staff,
            email=self.request.user.email,
            username=self.request.user.username
        )
        staff = Staff.objects.get(user=self.request.user)
        initials = staff.initials()  # piga method ya initials

        context.update({
            "designation": staff.designation,
            "first_name": staff.first_name,
            "last_name": staff.last_name,
            "profile_picture": staff.profile_picture,
            "initials": initials,
        })
        return context



class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "web/customer_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Customer ameundwa vizuri 🎉")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("customer_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = get_object_or_404(
            Staff,
            email=self.request.user.email,
            username=self.request.user.username
        )
        staff = Staff.objects.get(user=self.request.user)
        initials = staff.initials()  # piga method ya initials

        context.update({
            "designation": staff.designation,
            "first_name": staff.first_name,
            "last_name": staff.last_name,
            "profile_picture": staff.profile_picture,
            "initials": initials,
        })
        return context



class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "web/customer_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Customer amesahihishwa kikamilifu ✅")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("customer_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = get_object_or_404(
            Staff,
            email=self.request.user.email,
            username=self.request.user.username
        )
        staff = Staff.objects.get(user=self.request.user)
        initials = staff.initials()  # piga method ya initials

        context.update({
            "designation": staff.designation,
            "first_name": staff.first_name,
            "last_name": staff.last_name,
            "profile_picture": staff.profile_picture,
            "initials": initials,
        })
        return context



class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = "web/customer_confirm_delete.html"
    success_url = reverse_lazy("customer_list")

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, "Customer amefutwa 🗑️")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = get_object_or_404(Staff, email=self.request.user.email, username=self.request.user.username)
        staff = Staff.objects.get(user=self.request.user)  
        initials = staff.initials()  # piga method ya initials

        context.update({
            "designation": staff.designation,
            "first_name": staff.first_name,
            "last_name": staff.last_name,
            "profile_picture": staff.profile_picture,
            "initials": initials,
        })
        return context


    
@login_required
def product_list(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    products = Product.objects.all()

    context = {
        "products": products,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/product_list.html", context)



@login_required
def product_create(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product created successfully ✅")
            return redirect("product_list")
    else:
        form = ProductForm()

    context = {
        "form": form,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/product_form.html", context)



@login_required
def product_update(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully ✅")
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)

    context = {
        "form": form,
        "product": product,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/product_form.html", context)



@login_required
def product_delete(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.warning(request, "Product deleted ❌")
        return redirect("product_list")

    context = {
        "product": product,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/product_confirm_delete.html", context)



# --------- ADDITIONS ----------
@login_required
def addition_list(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    additions = ProductAdditionHistory.objects.select_related("product").all()

    context = {
        "additions": additions,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/addition_list.html", context)



@login_required
def addition_create(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    if request.method == "POST":
        form = ProductAdditionForm(request.POST)
        if form.is_valid():
            addition = form.save(commit=False)
            addition.added_by = request.user
            addition.status = "pending"
            addition.save()
            messages.info(request, "Addition pending confirmation ⚠️")
            return redirect("addition_list")
    else:
        form = ProductAdditionForm()

    context = {
        "form": form,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/addition_form.html", context)



@login_required
def addition_mark(request, pk, status):
    addition = get_object_or_404(ProductAdditionHistory, pk=pk)
    if status == "correct" and addition.status == "pending":
        addition.status = "correct"
        addition.save()
        addition.apply_to_stock()
        messages.success(request, "Addition confirmed and stock updated ✅")
    elif status == "incorrect" and addition.status == "pending":
        addition.status = "incorrect"
        addition.save()
        messages.warning(request, "Addition marked incorrect ❌")
    return redirect("addition_list")


@login_required
def addition_delete(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    addition = get_object_or_404(ProductAdditionHistory, pk=pk)
    if request.method == "POST":
        addition.remove_from_stock()
        addition.delete()
        messages.warning(request, "Addition history deleted and stock adjusted ⚠️")
        return redirect("addition_list")

    context = {
        "addition": addition,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/addition_confirm_delete.html", context)


@login_required(login_url="signin")
def order_list(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    orders = SalesOrder.objects.select_related("customer").prefetch_related("items").order_by("-created_at")

    context = {
        "orders": orders,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/order_list.html", context)


@login_required(login_url="signin")
def customer_search(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    query = request.GET.get("q", "").strip()
    customers = Customer.objects.all()
    if query:
        customers = customers.filter(Q(name__icontains=query) | Q(email__icontains=query))

    # Map: customer_id -> existing draft/confirmed order id (if any)
    existing = (
        SalesOrder.objects
        .filter(customer_id=OuterRef("pk"), status__in=["draft", "confirmed"])
        .order_by("-created_at")
    )
    customers = customers.annotate(has_open=Exists(existing))

    context = {
        "customers": customers,
        "query": query,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/customer_search.html", context)


@login_required(login_url="signin")
def customer_orders(request, customer_id):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials
    customer = get_object_or_404(Customer, pk=customer_id)
    orders = SalesOrder.objects.filter(customer=customer).order_by("-created_at")

    context = {
        "customer": customer,
        "orders": orders,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/customer_orders.html", context)


from .models import SalesOrder, SalesOrderItem, Customer, Staff
from .forms import (
    SalesOrderForm,
    SalesOrderItemForm,
    SalesOrderItemCreateFormSet,
    SalesOrderItemInlineFormSet,
)

@login_required(login_url="signin")
def order_create_for_customer(request, customer_id):
    """
    CREATE:
    - Kama customer ana DRAFT/CONFIRMED, mwaga kwenye detail ili aendelee ku-edit.
    - Vinginevyo onyesha fomu ya kuunda order mpya; items zinaongezwa client-side
      kabla ya submit (modelformset, queryset=none).
    """
    staff = get_object_or_404(Staff, user=request.user)
    initials = staff.initials()
    customer = get_object_or_404(Customer, pk=customer_id)

    existing_order = (SalesOrder.objects
                      .filter(customer=customer, status__in=["draft", "confirmed"])
                      .order_by("-created_at")
                      .first())
    if existing_order:
        return redirect("order_detail", pk=existing_order.pk)

    PREFIX = "items"

    if request.method == "POST":
        form = SalesOrderForm(request.POST, initial={"customer": customer})
        formset = SalesOrderItemCreateFormSet(
            request.POST,
            queryset=SalesOrderItem.objects.none(),
            prefix=PREFIX
        )

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.customer = customer     # hakikisha customer ni huyu
                order.status = "draft"
                order.save()

                items = formset.save(commit=False)
                # Save all non-empty forms
                for f in formset.forms:
                    if not f.cleaned_data or f.cleaned_data.get("DELETE"):
                        continue
                    item = f.save(commit=False)
                    item.order = order
                    # unaweza kuweka default ya unit_price kutoka product kama haijawekwa
                    if not item.unit_price and item.product:
                        # kama una field product.price:
                        # item.unit_price = item.product.price
                        pass
                    item.save()

                messages.success(request, "Order created successfully.")
                return redirect("order_detail", pk=order.pk)

        messages.error(request, "Kuna makosa kwenye fomu. Tafadhali kagua na ujaribu tena.")
    else:
        form = SalesOrderForm(initial={"customer": customer})
        form.fields["customer"].disabled = True  # onyesha lakini isibadilike/submit
        formset = SalesOrderItemCreateFormSet(
            queryset=SalesOrderItem.objects.none(),
            prefix=PREFIX
        )

    context = {
        "form": form,
        "formset": formset,
        "customer": customer,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        "mode": "create",
        "prefix": PREFIX,
    }
    return render(request, "web/order_form.html", context)

@login_required(login_url="signin")
def order_detail(request, pk):
    staff = get_object_or_404(Staff, user=request.user)
    initials = staff.initials()
    order = get_object_or_404(SalesOrder, pk=pk)

    PREFIX = "items"

    if request.method == "POST":
        form = SalesOrderForm(request.POST, instance=order)
        form.fields["customer"].disabled = True

        formset = SalesOrderItemInlineFormSet(
            request.POST,
            instance=order,
            prefix=PREFIX
        )

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, "Order updated.")
            return redirect("order_detail", pk=order.pk)
        messages.error(request, "Kuna makosa kwenye fomu. Tafadhali kagua na ujaribu tena.")
    else:
        form = SalesOrderForm(instance=order)
        form.fields["customer"].disabled = True
        formset = SalesOrderItemInlineFormSet(instance=order, prefix=PREFIX)

    # Flags kwa template
    can_edit = order.status in ("draft", "confirmed")
    is_read_only = order.status in ("paid", "cancelled")

    # 👉 Zima inputs zote za item ukiwa read-only (hapa, bila ku-call as_widget kwenye template)
    if is_read_only:
        for f in formset.forms:
            for name in ("product", "quantity", "unit_price"):
                if name in f.fields:
                    # njia 1 (recommended): field.disabled = True
                    f.fields[name].disabled = True
                    # njia 2 (mbadala): f.fields[name].widget.attrs["disabled"] = "disabled"

    context = {
        "order": order,
        "form": form,
        "formset": formset,
        "customer": order.customer,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
        "mode": "edit",
        "prefix": PREFIX,
        "can_edit": can_edit,
        "is_read_only": is_read_only,
    }
    return render(request, "web/order_detail.html", context)

@login_required(login_url="signin")
def order_mark_paid(request, pk):
    order = get_object_or_404(SalesOrder, pk=pk)
    if order.status != "paid":
        with transaction.atomic():
            # reduce stock
            for item in order.items.select_related("product"):
                product = item.product
                if product.stock < item.quantity:
                    messages.error(request, f"Not enough stock for {product.name}")
                    return redirect("order_detail", pk=order.pk)
                product.stock -= item.quantity
                product.save()

            # set status
            order.status = "paid"
            order.save()

            # add to master amount (welcomemasterofus)
            master, _ = MasterAmount.objects.get_or_create(
                unique_code="welcomemasterofus",
                defaults={"amount": Decimal("0.00")}
            )
            master.amount += Decimal(order.total_amount)
            master.save()

        messages.success(request, "Order marked as Paid.")
    return redirect("order_detail", pk=order.pk)

@login_required(login_url="signin")
def order_cancel_paid(request, pk):
    order = get_object_or_404(SalesOrder, pk=pk)
    if order.status == "paid":
        with transaction.atomic():
            # return stock
            for item in order.items.select_related("product"):
                product = item.product
                product.stock += item.quantity
                product.save()

            # status & money
            order.status = "cancelled"
            order.save()

            master = MasterAmount.objects.get(unique_code="welcomemasterofus")
            master.amount -= Decimal(order.total_amount)
            master.save()

        messages.warning(request, "Paid order cancelled, stock restored, and amount deducted.")
    return redirect("order_detail", pk=order.pk)


@login_required(login_url="signin")
def order_invoice(request, pk):  # Billing Invoice (HTML version to print)
    order = get_object_or_404(SalesOrder.objects.select_related("customer").prefetch_related("items__product"), pk=pk)
    return render(request, "web/invoice.html", {"order": order, "today": now()})

@login_required(login_url="signin")
def order_proforma(request, pk):
    order = get_object_or_404(SalesOrder.objects.select_related("customer").prefetch_related("items__product"), pk=pk)
    return render(request, "web/proforma.html", {"order": order, "today": now()})

@login_required(login_url="signin")
def order_purchase_order(request, pk):
    order = get_object_or_404(SalesOrder.objects.select_related("customer").prefetch_related("items__product"), pk=pk)
    return render(request, "web/purchase_order.html", {"order": order, "today": now()})

@login_required(login_url="signin")
def order_delivery_note(request, pk):
    order = get_object_or_404(SalesOrder.objects.select_related("customer").prefetch_related("items__product"), pk=pk)
    return render(request, "web/delivery_note.html", {"order": order, "today": now()})

@login_required(login_url="signin")
def order_goods_received_note(request, pk):
    order = get_object_or_404(SalesOrder.objects.select_related("customer").prefetch_related("items__product"), pk=pk)
    return render(request, "web/goods_received_note.html", {"order": order, "today": now()})

# ---------- core aggregator ----------

def _sum_amount():
    """
    Safe decimal sum of line totals: quantity * unit_price.
    """
    return Sum(F("items__quantity") * F("items__unit_price"), output_field=DecimalField(max_digits=18, decimal_places=2))


def _aggregate_sales(qs, period: str):
    """
    Group paid sales by period and return rows + grand_total.
    Latest period should be first (descending).
    """
    period = (period or "month").lower()

    if period == "day":
        base = qs.annotate(period=TruncDay("created_at")).values("period")
        grouped = base.annotate(total=_sum_amount()).order_by("-period")
        rows = [{"label": r["period"].date().isoformat(), "total": r["total"] or Decimal("0.00")} for r in grouped]

    elif period == "week":
        base = qs.annotate(period=TruncWeek("created_at")).values("period")
        grouped = base.annotate(total=_sum_amount()).order_by("-period")
        rows = [{"label": f"Week of {r['period'].date().isoformat()}", "total": r["total"] or Decimal("0.00")} for r in grouped]

    elif period == "month":
        base = qs.annotate(period=TruncMonth("created_at")).values("period")
        grouped = base.annotate(total=_sum_amount()).order_by("-period")
        rows = [{"label": r["period"].strftime("%B %Y"), "total": r["total"] or Decimal("0.00")} for r in grouped]

    elif period == "quarter":
        if HAVE_EXTRACT_QUARTER:
            base = qs.annotate(
                year=ExtractYear("created_at"),
                quarter=ExtractQuarter("created_at"),
            ).values("year", "quarter")
            grouped = base.annotate(total=_sum_amount()).order_by("-year", "-quarter")
            rows = [{"label": f"Q{r['quarter']} {r['year']}", "total": r["total"] or Decimal("0.00")} for r in grouped]
        else:
            # Fallback: approximate by month
            from django.db.models.functions import ExtractMonth
            base = qs.annotate(
                year=ExtractYear("created_at"),
                month=ExtractMonth("created_at"),
            ).annotate(
                quarter=Case(
                    When(Q(month__lte=3), then=1),
                    When(Q(month__lte=6), then=2),
                    When(Q(month__lte=9), then=3),
                    default=4,
                    output_field=IntegerField(),
                )
            ).values("year", "quarter")
            grouped = base.annotate(total=_sum_amount()).order_by("-year", "-quarter")
            rows = [{"label": f"Q{r['quarter']} {r['year']}", "total": r["total"] or Decimal("0.00")} for r in grouped]

    elif period in ("half", "halfyear", "six", "sixmonths"):
        from django.db.models.functions import ExtractMonth
        base = qs.annotate(
            year=ExtractYear("created_at"),
            month=ExtractMonth("created_at"),
        ).annotate(
            half=Case(
                When(Q(month__lte=6), then=1),
                default=2,
                output_field=IntegerField(),
            )
        ).values("year", "half")
        grouped = base.annotate(total=_sum_amount()).order_by("-year", "-half")
        rows = [{"label": f"H{r['half']} {r['year']}", "total": r["total"] or Decimal("0.00")} for r in grouped]

    elif period == "year":
        base = qs.annotate(period=TruncYear("created_at")).values("period")
        grouped = base.annotate(total=_sum_amount()).order_by("-period")
        rows = [{"label": str(r["period"].year), "total": r["total"] or Decimal("0.00")} for r in grouped]

    else:
        return _aggregate_sales(qs, "month")

    grand_total = sum((r["total"] for r in rows), Decimal("0.00"))
    return rows, grand_total


# ---------- overall & per-customer views ----------

@login_required(login_url="signin")
def sales_report_overall(request, period="month"):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    # Only paid orders count for realized sales
    qs = SalesOrder.objects.filter(status="paid")
    rows, grand_total = _aggregate_sales(qs, period)

    ctx = {
        "scope": "overall",
        "period": period,
        "rows": rows,
        "grand_total": grand_total,
        "is_customer": False,
        "customer": None,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/sales_report.html", ctx)



@login_required(login_url="signin")
def sales_report_customer(request, customer_id, period="month"):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    customer = get_object_or_404(Customer, id=customer_id)
    qs = SalesOrder.objects.filter(status="paid", customer=customer)
    rows, grand_total = _aggregate_sales(qs, period)

    ctx = {
        "scope": "customer",
        "period": period,
        "rows": rows,
        "grand_total": grand_total,
        "is_customer": True,
        "customer": customer,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/sales_report.html", ctx)



# ---------- customer search (for reports) ----------

@login_required(login_url="signin")
def sales_customer_search(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    q = request.GET.get("q", "").strip()
    customers = Customer.objects.all().order_by("name")
    if q:
        customers = customers.filter(Q(name__icontains=q) | Q(email__icontains=q))

    paginator = Paginator(customers, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "q": q,
        "page_obj": page_obj,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/sales_customer_search.html", context)



# ---------- CSV export ----------

@login_required(login_url="signin")
def sales_report_export_csv(request, scope, period, customer_id=None):
    """
    scope: "overall" or "customer"
    """
    if scope == "customer":
        customer = get_object_or_404(Customer, id=customer_id)
        qs = SalesOrder.objects.filter(status="paid", customer=customer)
        filename = f"sales_{customer.id}_{period}.csv"
    else:
        qs = SalesOrder.objects.filter(status="paid")
        filename = f"sales_overall_{period}.csv"

    rows, grand_total = _aggregate_sales(qs, period)

    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = f'attachment; filename="{filename}"'
    writer = csv.writer(resp)
    writer.writerow(["Period", "Total (TZS)"])
    for r in rows:
        writer.writerow([r["label"], r["total"]])
    writer.writerow(["GRAND TOTAL", grand_total])
    return resp









# ---------- Materials ----------
@login_required(login_url="signin")
def material_list(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    q = request.GET.get("q", "").strip()
    qs = Material.objects.all()
    if q:
        qs = qs.filter(Q(name__icontains=q))
    qs = qs.order_by("name")
    page_obj = Paginator(qs, 20).get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "q": q,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/material_list.html", context)


@login_required(login_url="signin")
def material_create(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    if request.method == "POST":
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Material created.")
            return redirect("material_list")
    else:
        form = MaterialForm()

    context = {
        "form": form,
        "title": "Add Material",
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/material_form.html", context)


@login_required(login_url="signin")
def material_update(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    obj = get_object_or_404(Material, pk=pk)
    if request.method == "POST":
        form = MaterialForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Material updated.")
            return redirect("material_list")
    else:
        form = MaterialForm(instance=obj)

    context = {
        "form": form,
        "title": f"Edit: {obj.name}",
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/material_form.html", context)


@login_required(login_url="signin")
def material_toggle(request, pk):
    obj = get_object_or_404(Material, pk=pk)
    obj.is_active = not obj.is_active
    obj.save(update_fields=["is_active"])
    messages.info(request, f'"{obj.name}" is now {"active" if obj.is_active else "inactive"}.')
    return redirect("material_list")

# Seed default materials
DEFAULT_MATERIALS = [
    "1 kg jars", "1/2 kg jars", "100 g jars", "7 kg jars", "1 litre jars",
    "1/2 litre jars", "250 mm jars", "5 litre jars", "basket", "bee spacer",
    "entrance gate", "honey gate", "queen excluder", "straw hat", "hive tool",
    "bee brush", "bee smoker", "bee suit", "round bee suit",
]

@login_required(login_url="signin")
@permission_required("web.add_material", raise_exception=True)
def material_seed_defaults(request):
    created = 0
    for n in DEFAULT_MATERIALS:
        _, was_created = Material.objects.get_or_create(name=n)
        if was_created:
            created += 1
    messages.success(request, f"Seeded {created} material(s).")
    return redirect("material_list")

# ---------- Receipts ----------
@login_required(login_url="signin")
def receipt_list(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    qs = MaterialReceipt.objects.select_related("material").all()
    status = request.GET.get("status")
    if status in {"pending", "approved", "rejected"}:
        qs = qs.filter(status=status)
    page_obj = Paginator(qs, 20).get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "status": status,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/receipt_list.html", context)


@login_required(login_url="signin")
def receipt_create(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    if request.method == "POST":
        form = MaterialReceiptForm(request.POST)
        if form.is_valid():
            obj: MaterialReceipt = form.save(commit=False)
            obj.requested_by = request.user if request.user.is_authenticated else None
            obj.save()
            messages.success(request, "Receipt recorded.")
            return redirect("receipt_list")
    else:
        form = MaterialReceiptForm()

    context = {
        "form": form,
        "title": "Add Stock (Receipt)",
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/flow_form.html", context)


@login_required(login_url="signin")
def receipt_approve(request, pk):
    obj = get_object_or_404(MaterialReceipt, pk=pk)
    obj.status = "approved"
    obj.decided_by = request.user
    obj.decided_at = timezone.now()
    obj.save()
    messages.success(request, "Receipt approved and stock increased.")
    return redirect("receipt_list")

@login_required(login_url="signin")
def receipt_reject(request, pk):
    obj = get_object_or_404(MaterialReceipt, pk=pk)
    obj.status = "rejected"
    obj.decided_by = request.user
    obj.decided_at = timezone.now()
    obj.save()
    messages.info(request, "Receipt rejected (or reversed).")
    return redirect("receipt_list")

# ---------- Requisitions ----------
@login_required(login_url="signin")
def requisition_list(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    qs = MaterialRequisition.objects.select_related("material").all()
    status = request.GET.get("status")
    if status in {"pending", "approved", "rejected"}:
        qs = qs.filter(status=status)
    page_obj = Paginator(qs, 20).get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "status": status,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/requisition_list.html", context)


@login_required(login_url="signin")
def requisition_create(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    if request.method == "POST":
        form = MaterialRequisitionForm(request.POST)
        if form.is_valid():
            obj: MaterialRequisition = form.save(commit=False)
            obj.requested_by = request.user if request.user.is_authenticated else None
            # Note: save() will validate stock if status=approved
            obj.save()
            messages.success(request, "Requisition submitted.")
            return redirect("requisition_list")
    else:
        form = MaterialRequisitionForm()

    context = {
        "form": form,
        "title": "Request Material (Requisition)",
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/flow_form.html", context)


@login_required(login_url="signin")
def requisition_approve(request, pk):
    obj = get_object_or_404(MaterialRequisition, pk=pk)
    obj.status = "approved"
    obj.decided_by = request.user
    obj.decided_at = timezone.now()
    obj.save()
    messages.success(request, "Requisition approved and stock decreased.")
    return redirect("requisition_list")

@login_required(login_url="signin")
def requisition_reject(request, pk):
    obj = get_object_or_404(MaterialRequisition, pk=pk)
    obj.status = "rejected"
    obj.decided_by = request.user
    obj.decided_at = timezone.now()
    obj.save()
    messages.info(request, "Requisition rejected (or reversed).")
    return redirect("requisition_list")










# Parties
@login_required(login_url="signin")
def party_list(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    q = request.GET.get("q", "").strip()
    qs = Party.objects.all()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(email__icontains=q) | Q(phone__icontains=q))
    qs = qs.order_by("name")
    page_obj = Paginator(qs, 20).get_page(request.GET.get("page"))

    # Build a map of totals for the parties on this page (efficiently)
    party_ids = [p.id for p in page_obj.object_list]
    loans = Loan.objects.filter(party_id__in=party_ids).values("party_id", "type").annotate(s=Sum("amount"))
    reps  = Repayment.objects.filter(party_id__in=party_ids).values("party_id", "type").annotate(s=Sum("amount"))

    totals = {pid: {"lend": 0, "borrow": 0, "incoming": 0, "outgoing": 0} for pid in party_ids}
    for row in loans:
        totals[row["party_id"]][row["type"]] = row["s"] or 0
    for row in reps:
        totals[row["party_id"]][row["type"]] = row["s"] or 0

    # Attach computed fields for display
    display = {}
    for p in page_obj.object_list:
        t = totals.get(p.id, {})
        due_to_us = p.net_balance if p.net_balance > 0 else 0
        we_owe    = -p.net_balance if p.net_balance < 0 else 0
        status = "Settled"
        if p.net_balance > 0: status = "Owes us"
        elif p.net_balance < 0: status = "We owe"
        display[p.id] = {
            "total_borrowed_from_us": t.get("lend", 0),     # we lent => they borrowed from us
            "total_paid_to_us":      t.get("incoming", 0),  # they paid us
            "due_to_us":             due_to_us,
            "we_owe":                we_owe,
            "status":                status,
        }

    context = {
        "page_obj": page_obj,
        "q": q,
        "display": display,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/party_list.html", context)


@login_required(login_url="signin")
def party_create(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    if request.method == "POST":
        form = PartyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Party created.")
            return redirect("party_list")
    else:
        form = PartyForm()

    context = {
        "form": form,
        "title": "Add Party",
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/party_form.html", context)


@login_required(login_url="signin")
def party_update(request, pk):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    obj = get_object_or_404(Party, pk=pk)
    if request.method == "POST":
        form = PartyForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Party updated.")
            return redirect("party_list")
    else:
        form = PartyForm(instance=obj)

    context = {
        "form": form,
        "title": f"Edit: {obj.name}",
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/party_form.html", context)

# Loans
@login_required(login_url="signin")
def loan_list(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    qs = Loan.objects.select_related("party").all()
    ftype = request.GET.get("type")
    if ftype in {"borrow", "lend"}:
        qs = qs.filter(type=ftype)
    page_obj = Paginator(qs, 20).get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "ftype": ftype,
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/loan_list.html", context)

@login_required(login_url="signin")
def loan_create(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    if request.method == "POST":
        form = LoanForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.requested_by = request.user if request.user.is_authenticated else None
            obj.save()  # applies & updates balances and MasterAmount
            messages.success(request, "Loan recorded and balances updated.")
            return redirect("loan_list")
    else:
        form = LoanForm()

    context = {
        "form": form,
        "title": "New Loan (Borrow/Lend)",
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/flow_form1.html", context)


# Repayments
@login_required(login_url="signin")
def repayment_list(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    qs = Repayment.objects.select_related("party").all()
    ftype = request.GET.get("type")
    if ftype in {"incoming", "outgoing"}:
        qs = qs.filter(type=ftype)
    page_obj = Paginator(qs.order_by("-created_at"), 20).get_page(request.GET.get("page"))

    # Precompute totals per party for the page
    party_ids = [r.party_id for r in page_obj.object_list]
    loans = Loan.objects.filter(party_id__in=party_ids).values("party_id", "type").annotate(s=Sum("amount"))
    reps  = Repayment.objects.filter(party_id__in=party_ids).values("party_id", "type").annotate(s=Sum("amount"))

    totals = {pid: {"lend": 0, "borrow": 0, "incoming": 0, "outgoing": 0} for pid in party_ids}
    for row in loans:
        totals[row["party_id"]][row["type"]] = row["s"] or 0
    for row in reps:
        totals[row["party_id"]][row["type"]] = row["s"] or 0

    # Build a lightweight view-model for each repayment row
    rows = []
    for r in page_obj.object_list:
        t = totals.get(r.party_id, {})
        party_balance = r.party.net_balance
        due_to_us = party_balance if party_balance > 0 else 0
        we_owe    = -party_balance if party_balance < 0 else 0

        rows.append({
            "obj": r,
            "this_payment": r.amount,
            "total_borrowed_from_us": t.get("lend", 0),     # lifetime they borrowed from us
            "total_paid_to_us":      t.get("incoming", 0),  # lifetime they paid us
            "total_we_borrowed":     t.get("borrow", 0),    # lifetime we borrowed from them
            "total_we_paid_them":    t.get("outgoing", 0),  # lifetime we paid them
            "due_to_us":             due_to_us,             # if > 0 they still owe us
            "we_owe":                we_owe,                # if > 0 we owe them
        })

    context = {
        "page_obj": page_obj,
        "ftype": ftype,
        "rows": rows,  # enriched
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/repayment_list.html", context)

@login_required(login_url="signin")
def repayment_create(request):
    staff = get_object_or_404(Staff, email=request.user.email, username=request.user.username)
    staff = Staff.objects.get(user=request.user)
    initials = staff.initials()  # piga method ya initials

    if request.method == "POST":
        form = RepaymentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.requested_by = request.user if request.user.is_authenticated else None
            obj.save()  # applies & updates balances and MasterAmount
            messages.success(request, "Repayment recorded and balances updated.")
            return redirect("repayment_list")
    else:
        form = RepaymentForm()

    context = {
        "form": form,
        "title": "New Repayment",
        "designation": staff.designation,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "profile_picture": staff.profile_picture,
        "initials": initials,
    }
    return render(request, "web/flow_form1.html", context)
