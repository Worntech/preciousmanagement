from django.contrib import admin
from .  models import *
from .models import QRCode

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class MyUserAdmin(BaseUserAdmin):
    list_display=('username', 'email', 'date_joined', 'last_login', 'is_admin', 'is_active')
    search_fields=('email', 'username')
    readonly_fields=('date_joined', 'last_login')
    filter_horizontal=()
    list_filter=('last_login',)
    fieldsets=()

    add_fieldsets=(
        (None,{
            'classes':('wide'),
            'fields':('email', 'username', 'password1', 'password2'),
        }),
    )

    ordering=('email',)

# Register your models here.
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Staff)
admin.site.register(Farmer)
admin.site.register(Asset)
admin.site.register(AllAsset)

admin.site.register(ProductBuy)
admin.site.register(CommentProductBuy)
admin.site.register(ProductSell)
admin.site.register(CommentProductSell)
admin.site.register(MasterAmount)
admin.site.register(VendorAmount)
admin.site.register(MoneyRequest)
admin.site.register(CommentMoneyRequest)
admin.site.register(Moneyin)
admin.site.register(Moneyout)
admin.site.register(Salary)
admin.site.register(Product)
admin.site.register(CommentProduct)
admin.site.register(Material)
admin.site.register(CommentMaterial)
admin.site.register(QRCode)
admin.site.register(MasterProduct)
admin.site.register(Productin)
admin.site.register(Productout)

admin.site.register(Contact)