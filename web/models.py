import os
from django.db import models
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
from django.db import models
from django.utils.timezone import now
from django.db import models, transaction

from reportlab.lib.utils import ImageReader
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

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
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # Assuming the user is from the auth.User model
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
    top_bar_beehives = models.PositiveIntegerField()
    tch_beehives = models.PositiveIntegerField()
    ktbh_beehives = models.PositiveIntegerField()
    local_beehives = models.PositiveIntegerField()
    colonized_beehives = models.PositiveIntegerField()
    uncolonized_beehives = models.PositiveIntegerField()
    farmer_background = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class Asset(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # Assuming the user is from the auth.User model
    asset_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
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
    
class ProductBuy(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # Assuming the user is from the auth.User model
    seller_name = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    barcode = models.CharField(max_length=200)
    weight = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
class CommentProductBuy(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('ProductBuy', on_delete=models.CASCADE)
    content = models.TextField()
    
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
    
class MasterAmount(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
        
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
    
class Product(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # Assuming the user is from the auth.User model
    used_rawmaterial = models.CharField(max_length=1000)
    honey = models.CharField(max_length=1000)
    wax = models.CharField(max_length=1000)
    status = models.CharField(max_length=1000)
    comment = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
class CommentProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('Product', on_delete=models.CASCADE)
    content = models.TextField()
    
class Material(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # Assuming the user is from the auth.User model
    wax = models.CharField(max_length=1000)
    comb_honey = models.CharField(max_length=1000)
    honey = models.CharField(max_length=1000)
    status = models.CharField(max_length=1000)
    comment = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
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