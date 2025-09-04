import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid

from django.conf import settings

import random
import string
from io import BytesIO
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PIL import Image
from django.utils.timezone import now
from django.db import models, transaction

from reportlab.lib.utils import ImageReader
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from django.utils import timezone
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from decimal import Decimal
from django.db import models
from django.db.models import Sum, F


from django.db.models import Sum, F, DecimalField
from django.db.models.functions import Coalesce

from django.core.validators import RegexValidator, MinValueValidator

# user table--------------------------------------------------------------------
class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("email is required")
        if not username:
            raise ValueError("Your user name is required")
        
        

        user=self.model(
            email=self.normalize_email(email),
            username=username,
            
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,

        )
        user.is_admin=True
        user.is_staff=True
        
        user.is_superuser=True
        user.save(using=self._db)
        return user

     

class MyUser(AbstractBaseUser):
    email=models.EmailField(verbose_name="email", max_length=100, unique=True)
    username=models.CharField(verbose_name="user name", max_length=100, unique=True)
    
    date_joined=models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    
    last_login=models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)
    


    USERNAME_FIELD="email"
    REQUIRED_FIELDS=['username']
    
    objects=MyUserManager()

    def __str__(self):
        return self.username

    


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class Staff(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)  # badala ya ForeignKey
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    village = models.CharField(max_length=100)
    ward = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    nin_number = models.CharField(max_length=20, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    profile_picture = models.FileField(upload_to="home/", blank=True, null=True, help_text="Optional")
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # Hii method inatoa initials
    def initials(self):
        return f"{self.first_name[0].upper()}{self.last_name[0].upper()}"
    
class Farmer(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # Assuming the user is from the auth.User model
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    village = models.CharField(max_length=100)
    ward = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    region = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=15)
    nin_number = models.CharField(max_length=20, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    total_beehives = models.PositiveIntegerField()
    ttb_beehives = models.PositiveIntegerField()
    tch_beehives = models.PositiveIntegerField()
    ktbh_beehives = models.PositiveIntegerField()
    local_beehives = models.PositiveIntegerField()
    colonized_beehives = models.PositiveIntegerField()
    uncolonized_beehives = models.PositiveIntegerField()
    mwanzo = models.TextField()
    malengo = models.TextField()
    muhamasishaji = models.TextField()
    kiasi_mwisho = models.TextField()
    kufanikisha_nin = models.TextField()
    kusaidia_mazingira = models.TextField()
    familia_mtazamo = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
class Asset(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Under Maintenance'),
        ('disposed', 'Disposed'),
    ]

    CONDITION_CHOICES = [
        ('new', 'New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('needs_repair', 'Needs Repair'),
        ('broken', 'Broken'),
    ]

    CATEGORY_CHOICES = [
        ('Tables', 'Tables'),
        ('Chairs', 'Chairs'),
        ('Computers', 'Computers'),
        ('Motocycles', 'Motocycles'),
        ('Beehives', 'Beehives'),
        ('Packages (kg)', 'Packages (kg)'),
        ('Labels', 'Labels'),
        ('Buckets', 'Buckets'),
        ('Bee suit', 'Bee suit'),
        ('Gloves', 'Gloves'),
        ('Hire tools', 'Hire tools'),
        ('Bee smoker', 'Bee smoker'),
        ('Honey press', 'Honey press'),
        ('Honey strainer', 'Honey strainer'),
        ('Sandles', 'Sandles'),
        ('Apron', 'Apron'),
        ('Cars', 'Cars'),
        ('Filling Machine', 'Filling Machine'),
        ('Heating Tank', 'Heating Tank'),
        ('Printers', 'Printers'),
        ('Filter Pump', 'Filter Pump'),
        ('Storage Tank', 'Storage Tank'),
        ('Honey Pressor', 'Honey Pressor'),
        ('Cartering Machine', 'Cartering Machine'),
        ('Digital Refractometor', 'Digital Refractometor'),
        ('Analogy Refractometor', 'Analogy Refractometor'),
    ]

    # Tumeondoa asset_code na badala yake tunatumia serial_number
    serial_number = models.CharField(max_length=100, unique=True, blank=True)
    asset_name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')

    assigned_to = models.CharField(max_length=200)
    location = models.CharField(max_length=255, blank=True, null=True)

    purchase_date = models.DateField(null=True, blank=True)
    purchase_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    current_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    depreciation_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                            help_text="Percentage depreciation per year")
    expected_life_years = models.PositiveIntegerField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')

    warranty_expiry = models.DateField(null=True, blank=True)
    last_service_date = models.DateField(null=True, blank=True)
    next_service_due = models.DateField(null=True, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_assets"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.serial_number:
            # Tafuta count ya assets za category husika
            category_count = Asset.objects.filter(category=self.category).count() + 1
            prefix = "PH"

            # Fupisha category kwa uppercase (kwa mfano Vehicle → VEHICLE → VEH)
            category_code = self.category.upper()

            # Format ya serial number: PH/CATEGORY-000X
            self.serial_number = f"{prefix}/{category_code}-{category_count:04d}"

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['asset_name', 'serial_number']
        verbose_name = "Asset"
        verbose_name_plural = "Assets"

    def __str__(self):
        return f"{self.asset_name} ({self.serial_number})"
    
class AllAsset(models.Model):
    unique_code = models.CharField(max_length=200)
    Tables = models.PositiveIntegerField()
    Chairs = models.PositiveIntegerField()
    Computers = models.PositiveIntegerField()
    Motocycles = models.PositiveIntegerField()
    Beehives = models.PositiveIntegerField()
    Packages = models.PositiveIntegerField()
    Labels = models.PositiveIntegerField()
    Buckets = models.PositiveIntegerField()
    Bee_suit = models.PositiveIntegerField()
    Gloves = models.PositiveIntegerField()
    Hire_tools = models.PositiveIntegerField()
    Bee_smoker = models.PositiveIntegerField()
    Honey_press = models.PositiveIntegerField()
    Honey_strainer = models.PositiveIntegerField()
    Sandles = models.PositiveIntegerField()
    Apron = models.PositiveIntegerField()


class Purchase(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='purchases')
    purchase_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("paid", "Paid"), ("cancelled", "Cancelled")],
        default="pending"
    )

    @property
    def total_amount(self):
        return self.items.aggregate(
            s=Sum(F('quantity') * F('unit_price'))
        )['s'] or 0

    def __str__(self):
        return f"Purchase {self.id} - {self.farmer} ({self.purchase_date.date()})"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    # barcode_data = models.CharField(max_length=255, blank=True, null=True)
    barcode_data = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} ({self.quantity}) ({self.barcode_data})"
    

PHONE_VALIDATOR = RegexValidator(
    regex=r'^[0-9+\-\s()]{6,20}$',
    message="Weka namba sahihi (tarakimu, +, -, mabano)."
)

class Customer(models.Model):
    PAYMENT_TERMS = [
        ("cash", "Cash"),
        ("7d", "Net 7 Days"),
        ("14d", "Net 14 Days"),
        ("30d", "Net 30 Days"),
        ("45d", "Net 45 Days"),
        ("60d", "Net 60 Days"),
    ]

    code = models.CharField(max_length=20, unique=True, editable=False, help_text="Generated e.g. CUST-0001")
    name = models.CharField(max_length=200, help_text="Jina kamili la mteja au kampuni")
    company_name = models.CharField(max_length=200, blank=True, null=True)
    contact_person = models.CharField(max_length=150, blank=True, null=True)

    phone = models.CharField(max_length=20, validators=[PHONE_VALIDATOR], blank=True, null=True)
    alt_phone = models.CharField(max_length=20, validators=[PHONE_VALIDATOR], blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    alt_email = models.EmailField(blank=True, null=True)

    address_line1 = models.CharField(max_length=250, blank=True, null=True)
    address_line2 = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=120, blank=True, null=True)
    region = models.CharField(max_length=120, blank=True, null=True)
    country = models.CharField(max_length=120, blank=True, null=True, default="Tanzania")
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    tin = models.CharField("TIN", max_length=50, blank=True, null=True)
    vat_number = models.CharField(max_length=50, blank=True, null=True)
    payment_terms = models.CharField(max_length=10, choices=PAYMENT_TERMS, default="cash")
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.name} ({self.code})" if self.code else self.name

    def save(self, *args, **kwargs):
        # Generate sequential code CUST-0001
        if not self.code:
            today = timezone.now().date()
            prefix = "CUST"
            last = Customer.objects.filter(code__startswith=f"{prefix}-").order_by("id").last()
            if last and last.code.split("-")[-1].isdigit():
                nxt = int(last.code.split("-")[-1]) + 1
            else:
                nxt = 1
            self.code = f"{prefix}-{nxt:04d}"
        super().save(*args, **kwargs)


User = get_user_model()

class Product(models.Model):
    PRODUCT_CHOICES = [
        ("Bee hives", "Bee hives"),
        ("Round bee suit", "Round bee suit"),
        ("Bee suit", "Bee suit"),
        ("Bee smoker", "Bee smoker"),
        ("Bee brush", "Bee brush"),
        ("Hive tool", "Hive tool"),
        ("Straw hat", "Straw hat"),
        ("Queen excluder", "Queen excluder"),
        ("Honey gate", "Honey gate"),
        ("Entrance gate", "Entrance gate"),
        ("Bee spacer", "Bee spacer"),
        ("1 kg stinging honey", "1 kg stinging honey"),
        ("1/2 kg stinging honey", "1/2 kg stinging honey"),
        ("100 g stinging honey", "100 g stinging honey"),
        ("7 kg stinging honey", "7 kg stinging honey"),
        ("1 litre stingless honey", "1 litre stingless honey"),
        ("500 ml stingless honey", "500 ml stingless honey"),
        ("250 ml stingless honey", "250 ml stingless honey"),
        ("1 kg wax", "1 kg wax"),
    ]

    UNIT_CHOICES = [
        ("pcs", "Pieces"),
        ("kg", "Kilogram"),
        ("g", "Gram"),
        ("ltr", "Litre"),
        ("ml", "Millilitre"),
    ]

    # Mtu ataweka product kwa kuchagua kutoka kwenye list
    name = models.CharField(max_length=200, choices=PRODUCT_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default="pcs")
    stock = models.PositiveIntegerField(default=0, help_text="Current available stock")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Price per unit")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.stock} {self.unit}"

    @property
    def total_value(self):
        """Thamani ya stock yote ya product hii"""
        return self.stock * self.unit_price


class ProductAdditionHistory(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("correct", "Correct"),
        ("incorrect", "Incorrect"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="histories")
    quantity = models.PositiveIntegerField()
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product.name} +{self.quantity} ({self.status})"

    def apply_to_stock(self):
        """Apply stock only if status == correct"""
        if self.status == "correct":
            self.product.stock += self.quantity
            self.product.save()

    def remove_from_stock(self):
        """If a correct history is deleted, remove from stock"""
        if self.status == "correct":
            self.product.stock = max(0, self.product.stock - self.quantity)
            self.product.save()

# ----------- SALES ORDER MODELS -------------
class SalesOrder(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name} - {self.status}"

    @property
    def total_amount(self):
        # Accurate on Python side; for heavy lists, consider annotate in queries.
        return sum((item.subtotal for item in self.items.all()), Decimal("0.00"))

    def mark_as_paid(self):
        """Reduce stock and add to master amount."""
        from django.db import transaction
        if self.status == "paid":
            return
        with transaction.atomic():
            for item in self.items.select_related("product"):
                product = item.product
                if product.stock < item.quantity:
                    raise ValueError(f"Not enough stock for {product.name}")
                product.stock -= item.quantity
                product.save()

            master, _ = MasterAmount.objects.get_or_create(
                unique_code="welcomemasterofus",
                defaults={"amount": Decimal("0.00")}
            )
            master.amount += Decimal(self.total_amount)
            master.save()

            self.status = "paid"
            self.save()

    def cancel_paid_order(self):
        """Return stock and remove money."""
        from django.db import transaction
        if self.status != "paid":
            return
        with transaction.atomic():
            for item in self.items.select_related("product"):
                product = item.product
                product.stock += item.quantity
                product.save()

            master = MasterAmount.objects.get(unique_code="welcomemasterofus")
            master.amount -= Decimal(self.total_amount)
            master.save()

            self.status = "cancelled"
            self.save()


class SalesOrderItem(models.Model):
    order = models.ForeignKey(SalesOrder, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
       
            
class ProductSell(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # Assuming the user is from the auth.User model
    seller_name = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    barcode = models.CharField(max_length=200)
    weight = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
class CommentProductSell(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('ProductSell', on_delete=models.CASCADE)
    content = models.TextField()


User = get_user_model()
# Your existing model (keep as is, just ensure uuid import)
class MasterAmount(models.Model):
    amount = models.DecimalField(max_digits=1000, decimal_places=2)  # as you defined
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]
        super().save(*args, **kwargs)


MASTER_CODE = "welcomemasterofus"  # the only MasterAmount that should be mutated

def _get_master_amount_for_writes():
    try:
        # Lock the row for writes inside a transaction
        return MasterAmount.objects.select_for_update().get(unique_code=MASTER_CODE)
    except MasterAmount.DoesNotExist:
        raise ValidationError(
            f'MasterAmount with unique_code="{MASTER_CODE}" not found. '
            "Create it first before recording loans/repayments."
        )
        

class Party(models.Model):
    """
    A counterparty (person/org) we can lend to or borrow from.
    net_balance > 0  => party owes us (receivable)
    net_balance < 0  => we owe party (payable)
    """
    name = models.CharField(max_length=120, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)

    net_balance = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal("0.00"))

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        sign = "owes us" if self.net_balance > 0 else "we owe" if self.net_balance < 0 else "settled"
        return f"{self.name} ({self.net_balance} — {sign})"

    # ---------- ADD THIS METHOD ----------
    def totals_for_display(self):
        """
        Returns a dict of lifetime totals useful for UIs:
          total_borrowed_from_us: sum we LENT to this party (loans type='lend')
          total_paid_to_us:      sum they PAID us (repayments type='incoming')
          total_we_borrowed:     sum we BORROWED from them (loans type='borrow')
          total_we_paid_them:    sum we PAID them (repayments type='outgoing')
          due_to_us:  max(net_balance, 0)
          we_owe:     max(-net_balance, 0)
          status:     "Settled" | "Owes us" | "We owe"
        """
        agg = lambda qs: qs.aggregate(s=Sum("amount"))["s"] or 0
        total_borrowed_from_us = agg(self.loans.filter(type="lend"))
        total_paid_to_us      = agg(self.repayments.filter(type="incoming"))
        total_we_borrowed     = agg(self.loans.filter(type="borrow"))
        total_we_paid_them    = agg(self.repayments.filter(type="outgoing"))

        due_to_us = self.net_balance if self.net_balance > 0 else 0
        we_owe    = -self.net_balance if self.net_balance < 0 else 0

        status = "Settled"
        if self.net_balance > 0:
            status = "Owes us"
        elif self.net_balance < 0:
            status = "We owe"

        return {
            "total_borrowed_from_us": total_borrowed_from_us,
            "total_paid_to_us": total_paid_to_us,
            "total_we_borrowed": total_we_borrowed,
            "total_we_paid_them": total_we_paid_them,
            "due_to_us": due_to_us,
            "we_owe": we_owe,
            "status": status,
        }
    
    


class MoneyFlowBase(models.Model):
    """
    Abstract base for flows that affect both Party.net_balance and MasterAmount.amount.
    A flow is applied exactly once (applied=True). After that:
      - amount cannot change
      - instance cannot be deleted
    """
    party = models.ForeignKey(Party, on_delete=models.PROTECT, related_name="%(class)ss")
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    note = models.TextField(blank=True, null=True)

    requested_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name="%(class)s_requests")
    created_at = models.DateTimeField(auto_now_add=True)

    applied = models.BooleanField(default=False, editable=False)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def clean(self):
        if self.amount is None or self.amount <= 0:
            raise ValidationError("Amount must be greater than 0.")


class Loan(models.Model):
    """
    A principal movement:
      type='borrow' => we borrow from the party
          - MasterAmount += amount (cash in)
          - Party.net_balance -= amount (we owe them)
      type='lend'   => we lend to the party
          - MasterAmount -= amount (cash out)
          - Party.net_balance += amount (they owe us)
    """
    TYPE_CHOICES = [
        ("borrow", "We Borrowed (cash in, we owe)"),
        ("lend", "We Lent (cash out, they owe)"),
    ]

    party = models.ForeignKey(Party, on_delete=models.PROTECT, related_name="loans")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    note = models.TextField(blank=True, null=True)

    requested_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name="loan_requests")
    created_at = models.DateTimeField(auto_now_add=True)

    applied = models.BooleanField(default=False, editable=False)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if self.amount is None or self.amount <= 0:
            raise ValidationError("Amount must be greater than 0.")
        if self.type not in dict(self.TYPE_CHOICES):
            raise ValidationError("Invalid loan type.")

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # Prevent editing amount after application
            if self.pk:
                prev = Loan.objects.select_for_update().get(pk=self.pk)
                if prev.applied and prev.amount != self.amount:
                    raise ValidationError("Cannot change amount after this loan has been applied.")
                if prev.applied and prev.type != self.type:
                    raise ValidationError("Cannot change type after this loan has been applied.")

            super().save(*args, **kwargs)  # persist to get PK

            # Apply once
            if not self.applied:
                master = _get_master_amount_for_writes()
                party = Party.objects.select_for_update().get(pk=self.party_id)

                if self.type == "borrow":
                    # cash in
                    master.amount = (master.amount or Decimal("0")) + self.amount
                    # we owe the party more (more negative)
                    party.net_balance = (party.net_balance or Decimal("0")) - self.amount
                else:
                    # lend => cash out
                    master.amount = (master.amount or Decimal("0")) - self.amount
                    # they owe us more (more positive)
                    party.net_balance = (party.net_balance or Decimal("0")) + self.amount

                master.save(update_fields=["amount"])
                party.save(update_fields=["net_balance"])
                self.applied = True
                super().save(update_fields=["applied"])

    def delete(self, *args, **kwargs):
        # Do not allow deleting applied financial records
        if self.applied:
            raise ValidationError("Cannot delete an applied loan. Create a reversing entry instead.")
        return super().delete(*args, **kwargs)


# class Repayment(models.Model):
#     """
#     A settlement movement:
#       type='incoming' => they pay us (settling when we had lent)
#           - MasterAmount += amount (cash in)
#           - Party.net_balance -= amount (reduce what they owe us)
#       type='outgoing' => we pay them (settling when we had borrowed)
#           - MasterAmount -= amount (cash out)
#           - Party.net_balance += amount (reduce what we owe them)
#     """
#     TYPE_CHOICES = [
#         ("incoming", "Incoming payment (they pay us)"),
#         ("outgoing", "Outgoing payment (we pay them)"),
#     ]

#     party = models.ForeignKey(Party, on_delete=models.PROTECT, related_name="repayments")
#     type = models.CharField(max_length=10, choices=TYPE_CHOICES)
#     amount = models.DecimalField(max_digits=18, decimal_places=2)
#     note = models.TextField(blank=True, null=True)

#     requested_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
#                                      related_name="repayment_requests")
#     created_at = models.DateTimeField(auto_now_add=True)

#     applied = models.BooleanField(default=False, editable=False)

#     class Meta:
#         ordering = ["-created_at"]

#     def clean(self):
#         if self.amount is None or self.amount <= 0:
#             raise ValidationError("Amount must be greater than 0.")
#         if self.type not in dict(self.TYPE_CHOICES):
#             raise ValidationError("Invalid repayment type.")

#     def save(self, *args, **kwargs):
#         with transaction.atomic():
#             # Prevent editing amount/type after application
#             if self.pk:
#                 prev = Repayment.objects.select_for_update().get(pk=self.pk)
#                 if prev.applied and prev.amount != self.amount:
#                     raise ValidationError("Cannot change amount after this repayment has been applied.")
#                 if prev.applied and prev.type != self.type:
#                     raise ValidationError("Cannot change type after this repayment has been applied.")

#             super().save(*args, **kwargs)

#             if not self.applied:
#                 master = _get_master_amount_for_writes()
#                 party = Party.objects.select_for_update().get(pk=self.party_id)
#                 current = party.net_balance or Decimal("0")

#                 if self.type == "incoming":
#                     # They pay us. We must have receivable (current > 0)
#                     if current <= 0:
#                         raise ValidationError(f"{party.name} does not owe us. Balance is {current}.")
#                     if self.amount > current:
#                         raise ValidationError(
#                             f"Repayment exceeds receivable. Owed: {current}, payment: {self.amount}."
#                         )
#                     # Apply
#                     master.amount = (master.amount or Decimal("0")) + self.amount
#                     party.net_balance = current - self.amount

#                 else:  # outgoing
#                     # We pay them. We must have payable (current < 0)
#                     if current >= 0:
#                         raise ValidationError(f"We do not owe {party.name}. Balance is {current}.")
#                     owed = abs(current)
#                     if self.amount > owed:
#                         raise ValidationError(
#                             f"Repayment exceeds payable. Owed: {owed}, payment: {self.amount}."
#                         )
#                     # Apply
#                     master.amount = (master.amount or Decimal("0")) - self.amount
#                     party.net_balance = current + self.amount  # since current is negative

#                 master.save(update_fields=["amount"])
#                 party.save(update_fields=["net_balance"])
#                 self.applied = True
#                 super().save(update_fields=["applied"])

#     def delete(self, *args, **kwargs):
#         if self.applied:
#             raise ValidationError("Cannot delete an applied repayment. Create a reversing entry instead.")
#         return super().delete(*args, **kwargs)

class Repayment(models.Model):
    TYPE_CHOICES = [
        ("incoming", "Incoming payment (they pay us)"),
        ("outgoing", "Outgoing payment (we pay them)"),
    ]
    party = models.ForeignKey(Party, on_delete=models.PROTECT, related_name="repayments")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    requested_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name="repayment_requests")
    created_at = models.DateTimeField(auto_now_add=True)
    applied = models.BooleanField(default=False, editable=False)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if self.amount is None or self.amount <= 0:
            raise ValidationError("Amount must be greater than 0.")
        if self.type not in dict(self.TYPE_CHOICES):
            raise ValidationError("Invalid repayment type.")

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # guard edits after apply
            if self.pk:
                prev = Repayment.objects.select_for_update().get(pk=self.pk)
                if prev.applied and (prev.amount != self.amount or prev.type != self.type):
                    raise ValidationError("Cannot edit an applied repayment. Create another entry instead.")

            super().save(*args, **kwargs)

            if not self.applied:
                master = _get_master_amount_for_writes()
                party = Party.objects.select_for_update().get(pk=self.party_id)
                current = party.net_balance or Decimal("0")

                if self.type == "incoming":
                    # They pay us; increase cash
                    master.amount = (master.amount or Decimal("0")) + self.amount
                    # Reduce receivable (if >0). If overpay, balance goes negative (we owe them).
                    party.net_balance = current - self.amount
                else:
                    # We pay them; reduce cash
                    master.amount = (master.amount or Decimal("0")) - self.amount
                    # Reduce payable (if <0). If overpay, balance goes positive (they owe us).
                    party.net_balance = current + self.amount  # current negative + amount may cross zero

                master.save(update_fields=["amount"])
                party.save(update_fields=["net_balance"])
                self.applied = True
                super().save(update_fields=["applied"])
    
    
    
        
class MasterProduct(models.Model):
    honey = models.DecimalField(max_digits=10, decimal_places=2)
    wax = models.DecimalField(max_digits=10, decimal_places=2)
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)

class Productin(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # Assuming the user is from the auth.User model
    honey = models.DecimalField(max_digits=10, decimal_places=2)
    wax = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
class Productout(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # Assuming the user is from the auth.User model
    honey = models.DecimalField(max_digits=10, decimal_places=2)
    wax = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
      
class VendorAmount(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # Assuming the user is from the auth.User model
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
class MoneyRequest(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # Assuming the user is from the auth.User model
    purpose = models.CharField(max_length=1000)
    status = models.CharField(max_length=1000)
    completecheck = models.CharField(max_length=1000)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
class CommentMoneyRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('MoneyRequest', on_delete=models.CASCADE)
    content = models.TextField()
    
class Moneyin(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # Assuming the user is from the auth.User model
    money_processor = models.CharField(max_length=1000)
    money_source = models.CharField(max_length=1000)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
class Moneyout(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # Assuming the user is from the auth.User model
    money_user = models.CharField(max_length=1000)
    purpose = models.CharField(max_length=1000)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
class Salary(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # Assuming the user is from the auth.User model
    payed_Name = models.CharField(max_length=1000)
    paymentperiod = models.CharField(max_length=1000)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
class CommentProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('Product', on_delete=models.CASCADE)
    content = models.TextField()
    
# class Material(models.Model):
#     user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # Assuming the user is from the auth.User model
#     wax = models.CharField(max_length=1000)
#     comb_honey = models.CharField(max_length=1000)
#     honey = models.CharField(max_length=1000)
#     status = models.CharField(max_length=1000)
#     comment = models.CharField(max_length=1000)
#     date_created = models.DateTimeField(auto_now_add=True, null=True)
    
class CommentMaterial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('Material', on_delete=models.CASCADE)
    content = models.TextField()
    
# Create your models here.
class Contact(models.Model):
    Full_Name = models.CharField(max_length=100, null=True)
    Email = models.EmailField(max_length=200, null=True)
    Phone = models.CharField(max_length=100, null=True)
    Message = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class QRCode(models.Model):
    qr_code_name = models.CharField(max_length=255)
    uses = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, default="inactive")
    created_at = models.DateTimeField(default=now)
    image = models.ImageField(upload_to="qr_backgrounds/", null=True, blank=True)
    pdf_file = models.FileField(upload_to="qr_pdfs/", null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            with transaction.atomic():
                super().save(*args, **kwargs)  # Save instance first to get primary key
                
                if not self.pdf_file:  # Only generate PDF if it doesn't exist
                    self.generate_qr_codes()
        except Exception as e:
            raise ValueError(f"Error during save operation: {e}")

    def generate_qr_codes(self):
        """
        Generates 12 unique QR codes and creates a PDF.
        """
        qr_codes = []
        for _ in range(12):
            random_code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            qr = qrcode.make(random_code)
            qr_image = qr.convert("RGBA")
            qr_codes.append((random_code, qr_image))

        self.save_qr_codes_as_pdf(qr_codes)

    def create_image_with_qr(self, code, qr_image):
        """
        Combines the background image with the QR code at the bottom-right.
        """
        # If background image exists, open it, otherwise use a blank white image
        if self.image and os.path.exists(self.image.path):
            background = Image.open(self.image.path).convert("RGBA")
        else:
            background = Image.new("RGBA", qr_image.size, (255, 255, 255, 255))

        # Resize the QR code to be square (equal width and height)
        qr_size = min(background.width, background.height) // 4  # 1/4th the size of the background
        qr_resized = qr_image.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

        # Position QR code at the bottom-right corner
        qr_position = (background.width - qr_resized.width - 1, background.height - qr_resized.height - 1)

        # Paste the QR code onto the background
        background.paste(qr_resized, qr_position, qr_resized)

        # Optional: Add text label below QR code (or adjust position)
        draw = ImageDraw.Draw(background)
        font = ImageFont.load_default()
        text_position = (qr_position[0], qr_position[1] + qr_resized.height + 10)
        draw.text(text_position, code, fill="black", font=font)

        return background

    def save_qr_codes_as_pdf(self, qr_codes):
        """
        Saves the generated QR codes as a multi-page PDF.
        """
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        page_width, page_height = A4

        image_height = page_height / 5
        image_width = page_width

        for i, (code, qr_image) in enumerate(qr_codes):
            combined_image = self.create_image_with_qr(code, qr_image)
            combined_image = combined_image.resize((int(image_width), int(image_height)), Image.Resampling.LANCZOS)

            img_buffer = BytesIO()
            combined_image.save(img_buffer, format="PNG")
            img_buffer.seek(0)

            y_position = page_height - (i % 5 + 1) * image_height
            pdf.drawImage(ImageReader(img_buffer), 0, y_position, width=image_width, height=image_height)

            if (i + 1) % 5 == 0:
                pdf.showPage()

        pdf.save()
        buffer.seek(0)

        # Save the PDF to the FileField
        file_name = f"qr_codes_{self.qr_code_name}.pdf"
        self.pdf_file.save(file_name, ContentFile(buffer.read()))
        buffer.close()
        
        
        
        
        
        ########### for material to use  ############
User = get_user_model()

UNIT_CHOICES = [
    ("pcs", "Pieces"),
]

class Material(models.Model):
    name = models.CharField(max_length=80, unique=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default="pcs")
    stock = models.PositiveIntegerField(default=0, help_text="Current stock in pieces")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["name"]), models.Index(fields=["is_active"])]

    def __str__(self):
        return f"{self.name} ({self.stock} {self.unit})"


class BaseFlow(models.Model):
    """
    Abstract: common fields for stock-affecting flows (receipt/requisition).
    We apply stock exactly once when status becomes 'approved'.
    If reverted from approved -> rejected, we reverse it.
    """
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name="%(class)ss")
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    note = models.TextField(blank=True, null=True)

    requested_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="%(class)s_requests")
    decided_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="%(class)s_decisions")

    # Control flags
    applied = models.BooleanField(default=False, editable=False)  # has stock mutation been applied?
    created_at = models.DateTimeField(auto_now_add=True)
    decided_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def clean(self):
        if self.quantity == 0:
            raise ValidationError("Quantity must be at least 1.")
        if self.status not in dict(self.STATUS_CHOICES):
            raise ValidationError("Invalid status.")

    def __str__(self):
        return f"{self.__class__.__name__}({self.material.name}, qty={self.quantity}, status={self.status})"


class MaterialReceipt(BaseFlow):
    """
    Increases stock when approved.
    """

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # Lock the material row to avoid race conditions
            mat = Material.objects.select_for_update().get(pk=self.material_id)  # same transaction
            # Fetch previous state (if exists)
            if self.pk:
                prev = MaterialReceipt.objects.select_for_update().get(pk=self.pk)
            else:
                prev = None

            # Validations that depend on state
            if prev and prev.applied and (prev.quantity != self.quantity):
                # To keep logic simple & safe, prevent changing quantity after approval was applied.
                raise ValidationError("Cannot change quantity after approval has been applied. Create a new receipt or revert then edit.")

            super().save(*args, **kwargs)  # save first to have a PK if new

            # Apply transitions
            if not self.applied and self.status == "approved":
                # Apply +quantity once
                mat.stock = mat.stock + self.quantity
                mat.save(update_fields=["stock"])
                self.applied = True
                super().save(update_fields=["applied"])
            elif self.applied and self.status == "rejected":
                # Reverse if it had been applied then rejected
                mat.stock = mat.stock - self.quantity if mat.stock >= self.quantity else 0
                mat.save(update_fields=["stock"])
                self.applied = False
                super().save(update_fields=["applied"])


class MaterialRequisition(BaseFlow):
    """
    Decreases stock when approved.
    """

    def save(self, *args, **kwargs):
        with transaction.atomic():
            mat = Material.objects.select_for_update().get(pk=self.material_id)
            if self.pk:
                prev = MaterialRequisition.objects.select_for_update().get(pk=self.pk)
            else:
                prev = None

            if prev and prev.applied and (prev.quantity != self.quantity):
                raise ValidationError("Cannot change quantity after approval has been applied. Create a new requisition or revert then edit.")

            # For approved requisitions (new or edited approval), ensure sufficient stock
            if (not self.applied and self.status == "approved"):
                if self.quantity > mat.stock:
                    raise ValidationError(f"Insufficient stock for {mat.name}. Available: {mat.stock}, requested: {self.quantity}")

            super().save(*args, **kwargs)

            if not self.applied and self.status == "approved":
                # Apply -quantity
                mat.stock = mat.stock - self.quantity
                mat.save(update_fields=["stock"])
                self.applied = True
                super().save(update_fields=["applied"])
            elif self.applied and self.status == "rejected":
                # Reverse if rejected after having applied
                mat.stock = mat.stock + self.quantity
                mat.save(update_fields=["stock"])
                self.applied = False
                super().save(update_fields=["applied"])