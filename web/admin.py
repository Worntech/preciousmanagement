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

admin.site.register(Purchase)
admin.site.register(PurchaseItem)
admin.site.register(ProductSell)
admin.site.register(CommentProductSell)
# admin.site.register(MasterAmount)

@admin.register(MasterAmount)
class MasterAmountAdmin(admin.ModelAdmin):
    list_display = ("unique_code", "amount")
    search_fields = ("unique_code",)

@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "net_balance", "is_active", "created_at")
    list_filter  = ("is_active",)
    search_fields = ("name", "email", "phone")

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("party", "type", "amount", "applied", "requested_by", "created_at")
    list_filter  = ("type", "applied")
    search_fields = ("party__name",)
    autocomplete_fields = ("party", "requested_by")

@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    list_display = ("party", "type", "amount", "applied", "requested_by", "created_at")
    list_filter  = ("type", "applied")
    search_fields = ("party__name",)
    autocomplete_fields = ("party", "requested_by")
    
admin.site.register(VendorAmount)
admin.site.register(MoneyRequest)
admin.site.register(CommentMoneyRequest)
admin.site.register(Moneyin)
admin.site.register(Moneyout)
admin.site.register(Salary)
admin.site.register(CommentProduct)
# admin.site.register(Material)
admin.site.register(CommentMaterial)
admin.site.register(QRCode)
admin.site.register(MasterProduct)
admin.site.register(Productin)
admin.site.register(Productout)

admin.site.register(Contact)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "phone", "email", "payment_terms", "credit_limit", "is_active", "created_at")
    list_filter = ("is_active", "payment_terms", "country", "region", "created_at")
    search_fields = ("code", "name", "company_name", "contact_person", "phone", "email", "tin", "vat_number", "city")
    readonly_fields = ("code", "created_at", "updated_at")
    fieldsets = (
        ("Identity", {"fields": ("code", "name", "company_name", "contact_person", "is_active")}),
        ("Contacts", {"fields": ("phone", "alt_phone", "email", "alt_email")}),
        ("Address", {"fields": ("address_line1", "address_line2", "city", "region", "country", "postal_code")}),
        ("Tax & Finance", {"fields": ("tin", "vat_number", "payment_terms", "credit_limit")}),
        ("Notes & Timestamps", {"fields": ("notes", "created_at", "updated_at")}),
    )
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "unit", "stock", "unit_price", "is_active", "created_at")
    list_filter = ("unit", "is_active", "created_at")
    search_fields = ("name", "description")
    ordering = ("name",)
    list_editable = ("stock", "unit_price", "is_active")  # unaweza kuedit moja kwa moja kwenye list
    readonly_fields = ("created_at",)
    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "description", "unit", "unit_price")
        }),
        ("Stock & Status", {
            "fields": ("stock", "is_active")
        }),
        ("Timestamps", {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )

@admin.register(ProductAdditionHistory)
class ProductAdditionHistoryAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "status", "added_by", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("product__name", "note")
    
class SalesOrderItemInline(admin.TabularInline):
    model = SalesOrderItem
    extra = 1

@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'total_amount', 'status', 'created_at', 'notes']
    list_filter = ['status', 'created_at']
    inlines = [SalesOrderItemInline]




######### for material #####################
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "unit", "stock", "is_active", "created_at")
    list_filter = ("is_active", "unit")
    search_fields = ("name",)

@admin.register(MaterialReceipt)
class MaterialReceiptAdmin(admin.ModelAdmin):
    list_display = ("material", "quantity", "status", "applied", "requested_by", "decided_by", "created_at")
    list_filter = ("status", "applied")
    search_fields = ("material__name",)
    autocomplete_fields = ("material", "requested_by", "decided_by")

@admin.register(MaterialRequisition)
class MaterialRequisitionAdmin(admin.ModelAdmin):
    list_display = ("material", "quantity", "status", "applied", "requested_by", "decided_by", "created_at")
    list_filter = ("status", "applied")
    search_fields = ("material__name",)
    autocomplete_fields = ("material", "requested_by", "decided_by")